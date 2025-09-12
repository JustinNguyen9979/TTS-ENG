import os
import sys
import re
import numpy as np
from scipy.io.wavfile import write
from .config import VOICE_PRESETS, LANGUAGE_NATIVE_NAMES
from .tts_utils import generate_audio_chunk
from tqdm import tqdm
import time
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
                    choice_num = int(choice)
                    selected_display_name = next((key for key in voices_in_lang if key.startswith(f"{choice_num}. ")), None)
                    if selected_display_name:
                        voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
                        lang_code = VOICE_PRESETS[selected_display_name]["lang"]
                        voice_name_part = "".join(re.findall(r'\b\w', selected_display_name.split('-')[1]))
                        
                        # --- BẮT ĐẦU XỬ LÝ FILE (SAU KHI ĐÃ CHỌN GIỌNG) ---
                        files_to_process = initial_files.copy()
                        processed_files_log = []
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
                                audio_chunk = generate_audio_chunk(sentence, voice_preset, model, processor, device)
                                pieces.append(audio_chunk)
                                pause_samples = np.zeros(int(sampling_rate * 0.5), dtype=np.float32)
                                pieces.append(pause_samples)
                            if not pieces:
                                processed_files_set.add(file_path)
                                continue
                            final_audio_data = np.concatenate(pieces)

                            if not os.path.exists(output_dir): os.makedirs(output_dir)
                            base_name = os.path.splitext(os.path.basename(file_path))[0]
                            output_filename = f"{base_name}_{lang_code.upper()}_{voice_name_part}.wav"
                            output_filepath = os.path.join(output_dir, output_filename)

                            write(output_filepath, sampling_rate, final_audio_data)

                            processed_files_log.append(output_filename)
                            processed_files_set.add(file_path)
                            print(f"\n✅ Hoàn tất. Đã lưu tại: {output_filepath}")

                            current_all_files = find_and_sort_input_files(input_dir)
                            
                            for new_file in current_all_files:
                                if new_file not in files_to_process and new_file not in processed_files_set:
                                    print(f"-> Phát hiện file mới: {os.path.basename(new_file)}. Đợi xử lý.")
                                    files_to_process.append(new_file)
                        
                        # --- KẾT THÚC XỬ LÝ VÀ BÁO CÁO ---
                        try:
                            terminal_width = os.get_terminal_size().columns
                        except OSError: terminal_width = 80
                        dash_line = "-" * terminal_width
                        print(f"\n{dash_line}")
                        
                        if processed_files_log:
                            print("\n✅ XUẤT FILE AUDIO THÀNH CÔNG!".center(terminal_width))
                            print("\nCác file audio đã được tạo thành công:".center(terminal_width))
                            for log_entry in processed_files_log:
                                print(f"  - {log_entry}")
                        else:
                            print("Không có file nào được xử lý thành công.".center(terminal_width))
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