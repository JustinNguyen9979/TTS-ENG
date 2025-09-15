import os
import sys
# Chặn log MallocStackLogging trên macOS
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
import re
import time
import numpy as np
from scipy.io.wavfile import write
from tqdm import tqdm # Giữ nguyên import
from .file_tts import find_and_sort_input_files
from .ui import clear_screen, generate_centered_ascii_title
from contextlib import redirect_stdout, redirect_stderr

try:
    import whisper
    from .f5_tts.api_f5 import F5TTS
    F5TTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ CẢNH BÁO: Không thể import các thư viện cần thiết cho Voice Cloning...")
    F5TTS = None
    F5TTS_AVAILABLE = False

def find_voice_file(voice_dir):
    if not os.path.exists(voice_dir): os.makedirs(voice_dir)
    for filename in os.listdir(voice_dir):
        if filename.lower().endswith(('.wav', '.mp3', '.m4a')):
            return os.path.join(voice_dir, filename)
    return None

def count_sentences_in_file(file_path):
    """Hàm phụ để đọc file và đếm số câu."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            full_text = f.read().strip()
        if not full_text:
            return 0
        return len([s for s in re.split(r'(?<=[.?!])\s+', full_text.replace('\n', ' ').strip()) if s])
    except Exception:
        return 0

def run_voice_cloning(input_dir, output_dir, downloads_path):
    """
    Chạy quy trình nhân bản giọng nói hàng loạt với logic hàng đợi động chuẩn.
    """
    if not F5TTS_AVAILABLE:
        input("\n❌ LỖI: Chức năng không khả dụng. Nhấn Enter...")
        return
        
    try:
        clear_screen()
        print(generate_centered_ascii_title("Voice Cloning"))

        voice_dir = os.path.join(downloads_path, "jntts", "Voice")
        print(f"\nBước 1: Đang quét thư mục '{os.path.basename(voice_dir)}'...")
        ref_file = find_voice_file(voice_dir)
        if not ref_file:
            print(f"\nLỖI: Không tìm thấy file âm thanh mẫu trong thư mục 'Voice'.")
            input("Nhấn Enter...")
            return
        
        print("\nBước 2: Đang nhận dạng giọng nói mẫu...")
        ref_text = ""
        try:
            whisper_model = whisper.load_model("base")
            audio = whisper.load_audio(ref_file)
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)
            _, probs = whisper_model.detect_language(mel)
            detected_lang = max(probs, key=probs.get)
            print(f" -> Ngôn ngữ audio: {detected_lang.upper()}")

            if detected_lang == "vi":
                expected_txt_file = os.path.splitext(ref_file)[0] + ".txt"
                if os.path.exists(expected_txt_file):
                    with open(expected_txt_file, 'r', encoding='utf-8') as f:
                        ref_text = f.read().strip()
                else:
                    print(f"\n❌ LỖI: Ngôn ngữ là Tiếng Việt, nhưng không tìm thấy file .txt tương ứng.")
                    input("Nhấn Enter...")
                    return
            else:
                result = whisper_model.transcribe(ref_file, fp16=False)
                ref_text = result['text'].strip()
            if not ref_text: raise ValueError("Không thể lấy được nội dung.")
        except Exception as e:
            print(f"\n❌ LỖI: Đã xảy ra sự cố ở Bước 2. Lỗi: {e}")
            input("Nhấn Enter...")
            return

        initial_files = find_and_sort_input_files(input_dir)
        if not initial_files:
            print(f"\n❌ LỖI: Không tìm thấy file .txt nào trong thư mục 'Input'.")
            input("Nhấn Enter...")
            return
        
        print(f"\nBước 3: Tìm thấy {len(initial_files)} file. Đang tính toán tổng số câu...")
        
        # --- 1: TÍNH TỔNG SỐ CÂU TRƯỚC KHI BẮT ĐẦU ---
        total_sentences = 0
        for file_path in initial_files:
            total_sentences += count_sentences_in_file(file_path)

        if total_sentences == 0:
            print("⚠️ Cảnh báo: Tất cả các file đầu vào đều rỗng. Không có gì để xử lý.")
            input("\nNhấn Enter để quay lại menu chính...")
            return
            
        print("\nBước 4: Đang khởi tạo mô hình F5-TTS...")
        f5tts = F5TTS()

        files_to_process = initial_files.copy()
        processed_files_log = []
        processed_files_set = set()
        
        # --- 2: KHỞI TẠO THANH TIẾN TRÌNH DUY NHẤT ---
        with tqdm(total=total_sentences, desc="Chuẩn bị...", unit="câu") as pbar:
            while files_to_process:
                file_path = files_to_process.pop(0)
                if file_path in processed_files_set:
                    continue

                pbar.set_description(f"File: {os.path.basename(file_path)}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        full_text = f.read().strip()
                    if not full_text:
                        tqdm.write(f"⚠️ Bỏ qua file rỗng: '{os.path.basename(file_path)}'")
                        processed_files_set.add(file_path)
                        continue
                except Exception as e:
                    tqdm.write(f"Lỗi khi đọc file: {e}. Bỏ qua.")
                    processed_files_set.add(file_path)
                    continue

                sentences = [s for s in re.split(r'(?<=[.?!])\s+', full_text.replace('\n', ' ').strip()) if s]
                pieces = []
                
                for sentence in sentences:
                    try:
                        with open(os.devnull, 'w') as devnull:
                            with redirect_stdout(devnull), redirect_stderr(devnull):
                                wav, _, _ = f5tts.infer(ref_file=ref_file, ref_text=ref_text, gen_text=sentence)
                        pieces.append(wav)
                        pause_samples = np.zeros(int(f5tts.target_sample_rate * 0.5), dtype=np.float32)
                        pieces.append(pause_samples)
                    except Exception as e:
                        tqdm.write(f"\nLỗi khi tạo âm thanh cho câu: \"{sentence[:30]}...\". Lỗi: {e}")
                    
                    # --- 3: CẬP NHẬT THANH TIẾN TRÌNH SAU MỖI CÂU ---
                    pbar.update(1)

                if not pieces:
                    processed_files_set.add(file_path)
                    continue

                final_audio_data = np.concatenate(pieces)
                
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                voice_name_part = os.path.splitext(os.path.basename(ref_file))[0]
                safe_voice_name = re.sub(r'[^\w-]', '', voice_name_part)
                output_filename = f"{base_name}_CLONE_{safe_voice_name}.wav"
                output_filepath = os.path.join(output_dir, output_filename)
                
                f5tts.export_wav(final_audio_data, output_filepath)
                processed_files_log.append(output_filename)
                processed_files_set.add(file_path)

                # Quét tìm file mới
                current_all_files = find_and_sort_input_files(input_dir)
                new_files_found = []
                for new_file in current_all_files:
                    if new_file not in files_to_process and new_file not in processed_files_set:
                        files_to_process.append(new_file)
                        new_files_found.append(new_file)
                
                if new_files_found:
                    new_sentence_count = 0
                    for new_file in new_files_found:
                        new_sentence_count += count_sentences_in_file(new_file)
                    pbar.total += new_sentence_count
                    pbar.refresh()
                    tqdm.write(f"-> Phát hiện {len(new_files_found)} file mới. Đã thêm {new_sentence_count} câu vào hàng đợi.")
            
            pbar.set_description("Hoàn tất!")

        try:
            terminal_width = os.get_terminal_size().columns
            dash_line = "-" * terminal_width
            print(f"\n{dash_line}")
            print("✅ XUẤT FILE AUDIO THÀNH CÔNG!".center(terminal_width))
            if processed_files_log:
                print("\nCác file sau đã được tạo thành công:".center(terminal_width))
                for log_entry in processed_files_log:
                    print(f"  - {log_entry}".center(terminal_width))
            else:
                print("Không có file nào được xử lý thành công.".center(terminal_width))
            print(dash_line)
        except OSError: pass

    except KeyboardInterrupt:
        print("\n\nĐã dừng xử lý. Quay lại menu chính...")
        time.sleep(2)
        return
        
    input("\nNhấn Enter để quay lại menu chính...")