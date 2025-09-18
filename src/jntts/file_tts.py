import os
import sys
import re
import numpy as np
import time
from scipy.io.wavfile import write, read
from .config import VOICE_PRESETS, LANGUAGE_NATIVE_NAMES, prompt_for_audio_settings
from .tts_utils import generate_audio_chunk
from tqdm import tqdm
from scipy.signal import butter, filtfilt
from .ui import clear_screen, generate_centered_ascii_title
from .box_voice import display_voice_menu_grid

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def find_and_sort_input_files(input_dir):
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    
    txt_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.txt')]
        
    def get_sort_key(filename):
        match = re.match(r'(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    txt_files.sort(key=get_sort_key)
    return [os.path.join(input_dir, f) for f in txt_files]

def apply_bass_boost(audio_data, sampling_rate, boost_db=0, cutoff_freq=400):
    """
    Áp dụng hiệu ứng tăng âm trầm dựa trên giá trị boost_db (0-10).
    """
    if boost_db <= 0:
        return audio_data

    # Chuyển đổi giá trị boost (1-10) thành một hệ số nhân hợp lý (ví dụ: 0.1-1.0)
    boost_factor = boost_db / 10.0
    
    # Chuyển đổi audio sang float nếu nó là integer
    if np.issubdtype(audio_data.dtype, np.integer):
        max_val = np.iinfo(audio_data.dtype).max
        audio_data = audio_data.astype(np.float32) / max_val

    try:
        nyquist = 0.5 * sampling_rate
        normal_cutoff = cutoff_freq / nyquist
        b, a = butter(4, normal_cutoff, btype='low', analog=False)
        low_freqs = filtfilt(b, a, audio_data)
        
        boosted_audio = audio_data + low_freqs * boost_factor

        max_abs_val = np.max(np.abs(boosted_audio))
        if max_abs_val > 1.0:
            boosted_audio /= max_abs_val

        return boosted_audio
    except Exception as e:
        print(f"\n⚠️ Lỗi khi áp dụng hiệu ứng âm trầm: {e}. Giữ nguyên âm thanh gốc.")
        return audio_data

def run_file_tts(model, processor, device, sampling_rate, input_dir, output_dir):
    try:
        while True:
            clear_screen()
            print(generate_centered_ascii_title("Text To Speech"))
            
            initial_files = find_and_sort_input_files(input_dir)
            if not initial_files:
                print(f"\n❌ LỖI: Không tìm thấy file .txt nào trong thư mục '{input_dir}'.")
                print("\n   Vui lòng sao chép các file văn bản của bạn vào đó.")
                input("\nNhấn Enter để quay lại menu chính...")
                return
            
            print(f"\nĐã tìm thấy {len(initial_files)} file.")
            
            # --- MENU CHỌN NGÔN NGỮ ---
            voices_by_lang = {}
            for key, value in VOICE_PRESETS.items():
                lang_name = re.match(r'\d+\.\s(.*?)\s-', key).group(1)
                if lang_name not in voices_by_lang:
                    voices_by_lang[lang_name] = []
                voices_by_lang[lang_name].append(key)
            
            available_langs = list(voices_by_lang.keys())
            
            print("\nChọn ngôn ngữ cho giọng đọc:")
            for i, lang in enumerate(available_langs):
                lang_code_lookup = VOICE_PRESETS[voices_by_lang[lang][0]]['lang']
                native_name = LANGUAGE_NATIVE_NAMES.get(lang_code_lookup, '')
                print(f"\n  {i+1}. {lang} ({native_name})")
            
            print("\n  0. Quay lại menu chính")
            
            selected_lang = None
            while True:
                lang_choice = input("\nNhập lựa chọn của bạn (0 để quay lại): ")
                if lang_choice == '0':
                    return 
                try:
                    lang_choice_num = int(lang_choice)
                    if 1 <= lang_choice_num <= len(available_langs):
                        selected_lang = available_langs[lang_choice_num - 1]
                        break
                    else: print("Lựa chọn không hợp lệ!")
                except ValueError: print("Lựa chọn không hợp lệ! Vui lòng chỉ nhập số.")
                    
            # --- MENU CHỌN GIỌNG NÓI ---
            voices_in_lang = voices_by_lang[selected_lang]
            first_voice_key = voices_in_lang[0]
            lang_code_for_header = VOICE_PRESETS[first_voice_key]['lang']
            native_name_with_flag = LANGUAGE_NATIVE_NAMES.get(lang_code_for_header, '')

            while True:
                clear_screen() 
                print(generate_centered_ascii_title("Text To Speech"))
                print(f"\nChọn một giọng nói cụ thể ({selected_lang} - {native_name_with_flag}):")
                for voice_key in voices_in_lang:
                    print(f"\n  {voice_key}")
                print("\n  0. Quay lại menu chọn ngôn ngữ")
                
                choice = input("\nNhập lựa chọn của bạn (0 để quay lại): ")
                if choice == '0':
                    break 

                try:
                    clear_screen() 
                    print(generate_centered_ascii_title("Text To Speech"))
                    choice_num = int(choice)
                    selected_display_name = next((key for key in voices_in_lang if key.startswith(f"{choice_num}. ")), None)
                    if selected_display_name:
                        voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
                        lang_code = VOICE_PRESETS[selected_display_name]["lang"]
                        voice_name_part = "".join(re.findall(r'\b\w', selected_display_name.split('-')[1]))
                        voice_display_short = selected_display_name.split('-', 1)[-1].strip()

                        # Gọi hàm cấu hình đa năng, yêu cầu tất cả các thông số
                        audio_settings = prompt_for_audio_settings(
                            ask_for_speed=False, 
                            ask_for_stability=False, 
                            ask_for_bass_boost=True
                        )

                        # Gán các giá trị vào biến để sử dụng
                        user_speed = audio_settings['speed']
                        user_cfg_strength = audio_settings['stability']
                        bass_boost_db = audio_settings['bass_boost']

                        speed_info = f"Tốc độ={user_speed}" if user_speed is not None else "Tốc độ = Mặc định"
                        stability_info = f"Độ ổn định = {user_cfg_strength}" if user_cfg_strength is not None else "Độ ổn định = Mặc định"
                        bass_info = f"Âm trầm = {bass_boost_db}" if bass_boost_db > 0 else "Âm trầm = Không"
                        voice_info = f"Giọng = '{voice_display_short}'"

                        print(f"\n   -> Cấu hình: {speed_info}, {stability_info}, {bass_info}, {voice_info}")
                        
                        # --- BẮT ĐẦU XỬ LÝ FILE (SAU KHI ĐÃ CHỌN GIỌNG) ---
                        files_to_process = initial_files.copy()
                        processed_files_log = []
                        generated_files_info = []
                        processed_files_set = set()
                        while files_to_process:
                            file_path = files_to_process.pop(0)
                            if file_path in processed_files_set: continue
                            try:
                                terminal_width = os.get_terminal_size().columns
                            except OSError: terminal_width = 80
                            header_text = f" Bắt đầu xử lý file: {os.path.basename(file_path)} "
                            full_header_line = header_text.center(terminal_width, '-')
                            print(f"\n{full_header_line}")
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    full_text = f.read().strip()
                                if not full_text:
                                    print(f"⚠️ Cảnh báo: File {os.path.basename(file_path)} rỗng. Bỏ qua.")
                                    processed_files_set.add(file_path)
                                    continue
                            except Exception as e:
                                print(f"Lỗi khi đọc file: {e}. Bỏ qua.")
                                processed_files_set.add(file_path)
                                continue
                            sentences = re.split(r'(?<=[.?!])\s+', full_text.replace('\n', ' ').strip())
                            pieces = []
                            for sentence in tqdm(sentences, desc=f"Tiến trình"):
                                if not sentence.strip(): continue
                                audio_chunk = generate_audio_chunk(
                                    sentence, 
                                    voice_preset, 
                                    model, 
                                    processor, 
                                    device,
                                    speed=user_speed,
                                    cfg_strength=user_cfg_strength
                                    )
                                pieces.append(audio_chunk)
                                pause_samples = np.zeros(int(sampling_rate * 0.5), dtype=np.float32)
                                pieces.append(pause_samples)
                            if not pieces:
                                processed_files_set.add(file_path)
                                continue
                            final_audio_data = np.concatenate(pieces)

                            # Chỉ chuyển đổi và chuẩn bị ghi file GỐC
                            final_audio_data = np.clip(final_audio_data, -1.0, 1.0)
                            final_audio_data = (final_audio_data * 32767).astype(np.int16)

                            if not os.path.exists(output_dir): os.makedirs(output_dir)
                            base_name = os.path.splitext(os.path.basename(file_path))[0]
                            
                            # Tạo tên file GỐC (chưa có hậu tố âm trầm)
                            speed_suffix = f"_S{user_speed}" if user_speed is not None else ""
                            cfg_suffix = f"_C{user_cfg_strength}" if user_cfg_strength is not None else ""
                            
                            output_filename = f"{base_name}_{lang_code.upper()}_{voice_name_part}{speed_suffix}{cfg_suffix}.wav"
                            output_filepath = os.path.join(output_dir, output_filename)

                            # Ghi file audio GỐC ra đĩa
                            write(output_filepath, sampling_rate, final_audio_data)

                            # Lưu lại thông tin cần thiết cho bước hậu kỳ
                            generated_files_info.append({
                                'path': output_filepath,
                                'original_name': output_filename
                            })
                            processed_files_log.append(output_filename)
                            processed_files_set.add(file_path)
                            # print(f"\n✅ Đã tạo file gốc: {output_filename}")

                            # Phần quét file mới bắt đầu ngay sau đây...
                            current_all_files = find_and_sort_input_files(input_dir)

                            current_all_files = find_and_sort_input_files(input_dir)
                            
                            for new_file in current_all_files:
                                if new_file not in files_to_process and new_file not in processed_files_set:
                                    print(f"-> Phát hiện file mới: {os.path.basename(new_file)}. Đợi xử lý.")
                                    files_to_process.append(new_file)
                        
                        # --- GIAI ĐOẠN HẬU KỲ VÀ BÁO CÁO CUỐI CÙNG ---
                        final_log = processed_files_log

                        # --- BƯỚC HẬU KỲ ÂM TRẦM (NẾU CẦN) ---
                        if bass_boost_db > 0:
                            # print("\nÁp dụng hiệu ứng âm trầm một cách thầm lặng...") # Dòng này có thể bật để debug
                            boosted_file_map = {} # Dùng để ánh xạ tên file cũ sang tên file mới
                            
                            # Thay thế tqdm bằng vòng lặp thường để không hiển thị progress bar
                            for file_info in generated_files_info:
                                file_path = file_info['path']
                                try:
                                    rate, audio_data = read(file_path)
                                    boosted_audio = apply_bass_boost(audio_data, rate, boost_db=bass_boost_db)
                                    boosted_audio = np.clip(boosted_audio, -1.0, 1.0)
                                    boosted_audio = (boosted_audio * 32767).astype(np.int16)
                                    
                                    # Tạo tên file mới
                                    base, ext = os.path.splitext(file_path)
                                    new_filepath = f"{base}_B{bass_boost_db}{ext}"
                                    
                                    # Ghi file mới đã được làm ấm
                                    write(new_filepath, rate, boosted_audio)
                                    
                                    # XÓA FILE GỐC
                                    os.remove(file_path)
                                    
                                    # Lưu lại sự thay đổi tên file
                                    original_filename = file_info['original_name']
                                    new_filename = os.path.basename(new_filepath)
                                    boosted_file_map[original_filename] = new_filename
                                    
                                except Exception as e:
                                    # In lỗi ra nếu có sự cố, nhưng không hiển thị progress bar
                                    print(f"\n⚠️ Lỗi khi xử lý hậu kỳ file '{os.path.basename(file_path)}': {e}")
                            
                            # Cập nhật lại danh sách log cuối cùng với các tên file mới
                            final_log = [boosted_file_map.get(log, log) for log in processed_files_log]

                        # --- BÁO CÁO TỔNG KẾT ---
                        try:
                            terminal_width = os.get_terminal_size().columns
                        except OSError: terminal_width = 80
                        dash_line = "-" * terminal_width
                        print(f"\n{dash_line}")

                        if not final_log:
                            print("Không có file nào được xử lý thành công.".center(terminal_width))
                        else:
                            print("\n✅ XỬ LÝ HOÀN TẤT!".center(terminal_width))
                            print("\nCác file sau đã được tạo thành công:".center(terminal_width))
                            for log_entry in final_log:
                                print(f"  - {log_entry}")
                        
                        print(dash_line)
                        input("\nNhấn Enter để quay lại menu chính...")
                        return
                    else:
                        print("Lựa chọn không hợp lệ!")
                except (ValueError, IndexError):
                    print("Lựa chọn không hợp lệ!")

    except KeyboardInterrupt:
        print("\n\nĐã dừng xử lý. Đang quay lại menu chính...")
        time.sleep(2)
        return