import os
import sys
import re
import numpy as np
import time
from scipy.io.wavfile import write, read
from .config import VOICE_PRESETS, LANGUAGE_NATIVE_NAMES, prompt_for_audio_settings, Timer
from .tts_utils import generate_audio_chunk
from tqdm import tqdm
from scipy.signal import butter, filtfilt
from .ui import clear_screen, generate_centered_ascii_title, display_selection_menu
from rich.console import Console
from rich.text import Text

console = Console()

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

# XÓA HÀM run_file_tts CŨ VÀ DÁN HÀM HOÀN CHỈNH NÀY VÀO

def run_file_tts(model, processor, device, sampling_rate, input_dir, output_dir):
    try:
        while True:
            clear_screen()
            ascii_title = generate_centered_ascii_title("Text To Speech") # Giữ lại ASCII art
            console.print(Text(ascii_title, style="bold bright_yellow")) # Tô màu cho nó
            
            initial_files = find_and_sort_input_files(input_dir)
            if not initial_files:
                print(f"\n❌ LỖI: Không tìm thấy file .txt nào trong thư mục '{input_dir}'.")
                print("\n   Vui lòng sao chép các file văn bản của bạn vào đó.")
                input("\nNhấn Enter để quay lại menu chính...")
                return
            
            # print(f"\nĐã tìm thấy {len(initial_files)} file.")
            
            # --- MENU CHỌN NGÔN NGỮ ---
            voices_by_lang = {}
            for key, value in VOICE_PRESETS.items():
                lang_name = re.match(r'\d+\.\s(.*?)\s-', key).group(1)
                if lang_name not in voices_by_lang:
                    voices_by_lang[lang_name] = []
                voices_by_lang[lang_name].append(key)
            available_langs = list(voices_by_lang.keys())
            lang_options = [f"{lang} ({LANGUAGE_NATIVE_NAMES.get(VOICE_PRESETS[voices_by_lang[lang][0]]['lang'], '')})" for lang in available_langs]

            lang_choice = display_selection_menu("Chọn ngôn ngữ cho giọng đọc", lang_options, color="bright_yellow", back_option="Quay lại menu chính")
            if lang_choice == '0': return
            if lang_choice == '00': return

            try:
                lang_choice_num = int(lang_choice)
                if not (1 <= lang_choice_num <= len(available_langs)):
                    print("Lựa chọn không hợp lệ!"); time.sleep(1); continue
                
                selected_lang = available_langs[lang_choice_num - 1]
                voices_in_lang = voices_by_lang[selected_lang]

                # --- MENU CHỌN GIỌNG NÓI ---
                while True:
                    clear_screen()
                    ascii_title = generate_centered_ascii_title("Text To Speech") # Giữ lại ASCII art
                    console.print(Text(ascii_title, style="bold bright_yellow")) # Tô màu cho nó
                    native_name = LANGUAGE_NATIVE_NAMES.get(VOICE_PRESETS[voices_in_lang[0]]['lang'], '')
                    menu_title = f"Chọn giọng nói cụ thể ({selected_lang} - {native_name})"
                    
                    choice = display_selection_menu(menu_title, voices_in_lang, color="bright_yellow", back_option="Quay lại menu chọn ngôn ngữ")
                    if choice == '0': break
                    if choice == '00': return

                    try:
                        choice_num = int(choice)
                        if not (1 <= choice_num <= len(voices_in_lang)):
                            print("Lựa chọn không hợp lệ!"); time.sleep(1); continue

                        selected_display_name = voices_in_lang[choice_num - 1]
                        
                        # --- BẮT ĐẦU PHẦN LOGIC XỬ LÝ CHÍNH ---
                        clear_screen()
                        ascii_title = generate_centered_ascii_title("Text To Speech") # Giữ lại ASCII art
                        console.print(Text(ascii_title, style="bold bright_yellow")) # Tô màu cho nó
                        
                        voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
                        lang_code = VOICE_PRESETS[selected_display_name]["lang"]
                        voice_name_part = "".join(re.findall(r'\b\w', selected_display_name.split('-')[1]))
                        voice_display_short = selected_display_name.split('-', 1)[-1].strip()

                        audio_settings = prompt_for_audio_settings(
                            ask_for_speed=True, 
                            ask_for_stability=True, 
                            ask_for_bass_boost=True
                        )

                        if audio_settings is None:
                            break

                        user_speed = audio_settings['speed']
                        user_cfg_strength = audio_settings['stability']
                        bass_boost_db = audio_settings['bass_boost']

                        speed_info = f"Tốc độ = {user_speed}" if user_speed is not None else "Tốc độ = Mặc định"
                        stability_info = f"Độ ổn định = {user_cfg_strength}" if user_cfg_strength is not None else "Độ ổn định = Mặc định"
                        bass_info = f"Âm trầm = {bass_boost_db}" if bass_boost_db > 0 else "Âm trầm = Không"
                        voice_info = f"Giọng = '{voice_display_short}'"

                        print(f"\n   -> Cấu hình: {speed_info}, {stability_info}, {bass_info}, {voice_info}")
                        
                        tts_timer = Timer()
                        tts_timer.start()

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
                            header_text = f" Đang xử lý file: {os.path.basename(file_path)} "
                            print(f"\n{header_text.center(terminal_width, '-')}\n")

                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    full_text = f.read().strip()
                                if not full_text:
                                    print(f"⚠️  Cảnh báo: File {os.path.basename(file_path)} rỗng. Bỏ qua.")
                                    processed_files_set.add(file_path)
                                    continue
                            except Exception as e:
                                print(f"❌ Lỗi khi đọc file: {e}. Bỏ qua.")
                                processed_files_set.add(file_path)
                                continue
                            sentences = [s for s in re.split(r'(?<=[.?!])\s+', full_text.replace('\n', ' ').strip()) if s]
                            pieces = []

                            for sentence in tqdm(sentences, desc=f"Tiến trình"):
                                audio_chunk = generate_audio_chunk(
                                    sentence, voice_preset, model, processor, device,
                                    speed=user_speed, cfg_strength=user_cfg_strength
                                )
                                pieces.append(audio_chunk)
                                pause_samples = np.zeros(int(sampling_rate * 0.5), dtype=np.float32)
                                pieces.append(pause_samples)

                            if not pieces:
                                processed_files_set.add(file_path)
                                continue
                            
                            final_audio_data = np.concatenate(pieces)
                            final_audio_data = np.clip(final_audio_data, -1.0, 1.0)
                            final_audio_data = (final_audio_data * 32767).astype(np.int16)

                            if not os.path.exists(output_dir): os.makedirs(output_dir)
                            base_name = os.path.splitext(os.path.basename(file_path))[0]
                            
                            speed_suffix = f"_S{user_speed}" if user_speed is not None else ""
                            cfg_suffix = f"_C{user_cfg_strength}" if user_cfg_strength is not None else ""
                            
                            output_filename = f"{base_name}_{lang_code.upper()}_{voice_name_part}{speed_suffix}{cfg_suffix}.wav"
                            output_filepath = os.path.join(output_dir, output_filename)

                            write(output_filepath, sampling_rate, final_audio_data)

                            generated_files_info.append({
                                'path': output_filepath,
                                'original_name': output_filename
                            })
                            processed_files_log.append(output_filename)
                            processed_files_set.add(file_path)

                            current_all_files = find_and_sort_input_files(input_dir)
                            for new_file in current_all_files:
                                if new_file not in files_to_process and new_file not in processed_files_set:
                                    tqdm.write(f"-> Phát hiện file mới: {os.path.basename(new_file)}. Đã thêm vào hàng đợi.")
                                    files_to_process.append(new_file)
                        
                        # --- HẬU KỲ VÀ BÁO CÁO ---
                        if bass_boost_db > 0:
                            for file_info in generated_files_info:
                                file_path = file_info['path']
                                try:
                                    rate, audio_data = read(file_path)
                                    boosted_audio = apply_bass_boost(audio_data, rate, boost_db=bass_boost_db)
                                    boosted_audio = np.clip(boosted_audio, -1.0, 1.0)
                                    boosted_audio = (boosted_audio * 32767).astype(np.int16)
                                    
                                    base, ext = os.path.splitext(file_path)
                                    new_filepath = f"{base}_B{bass_boost_db}{ext}"
                                    
                                    write(new_filepath, rate, boosted_audio)
                                    os.remove(file_path)
                                except Exception as e:
                                    print(f"\n⚠️  Lỗi khi tăng âm trầm cho file '{os.path.basename(file_path)}': {e}")

                        tts_timer.stop()
                        
                        try:
                            terminal_width = os.get_terminal_size().columns
                        except OSError: terminal_width = 80
                        dash_line = "-" * terminal_width
                        print(f"\n{dash_line}")

                        final_log = []
                        for file_info in generated_files_info:
                            original_filename_base, ext = os.path.splitext(file_info['original_name'])
                            bass_suffix = f"_B{bass_boost_db}" if bass_boost_db > 0 else ""
                            final_filename = f"{original_filename_base}{bass_suffix}{ext}"
                            final_log.append(final_filename)

                        if not final_log:
                            print("Không có file audio nào được xử lý thành công.".center(terminal_width))
                        else:
                            header_msg = "✅ XỬ LÝ HOÀN TẤT!"
                            time_msg = f"Tổng thời gian xử lý: {tts_timer.elapsed_formatted()}"
                            files_header_msg = "Các file sau đã được tạo thành công:"
                            print("\n" + header_msg.center(terminal_width))
                            print("\n" + time_msg.center(terminal_width))
                            print("\n" + files_header_msg.center(terminal_width))
                            for log_entry in final_log:
                                print(f"  - {log_entry}")
                        
                        print(dash_line)
                        input("\nNhấn Enter để quay lại menu chính...")
                        return

                    except (ValueError, IndexError):
                        print("Lựa chọn không hợp lệ!"); time.sleep(1)

            except ValueError:
                print("Lựa chọn không hợp lệ! Vui lòng chỉ nhập số."); time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nĐã dừng xử lý. Đang quay lại menu chính...")
        time.sleep(2)
        return