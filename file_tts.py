# file_tts.py

import os
import sys
import re
import numpy as np
from scipy.io.wavfile import write
from config import VOICE_PRESETS
from tts_utils import generate_audio_chunk
from tqdm import tqdm
import time
from ui import clear_screen, generate_centered_ascii_title
from jukebox import display_voice_menu_grid

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# NÂNG CẤP: Hàm tự động tìm file .txt trong thư mục 'Input'
def find_and_sort_input_files():
    """
    Tìm file TXT trong Folder Input.
    """
    input_dir = "Input"
    # Kiểm tra lại để chắc chắn thư mục tồn tại
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    txt_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.txt')]
        
    # Hàm key để sắp xếp: trích xuất số ở đầu tên file
    def get_sort_key(filename):
        match = re.match(r'(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    txt_files.sort(key=get_sort_key)
    return [os.path.join(input_dir, f) for f in txt_files]

def run_file_tts(model, processor, device, sampling_rate):
    """Chạy quy trình Text-to-Speech từ file."""
    try:
        clear_screen()
        print(generate_centered_ascii_title("Text To Speech"))
        
        initial_files = find_and_sort_input_files()

        if not initial_files:
            print("\nLỖI: Không tìm thấy file .txt nào trong thư mục 'Input'.")
            print("Vui lòng đặt các file văn bản (ví dụ: 1_Chapter1.txt) vào thư mục 'Input'.")
            input("Nhấn Enter để quay lại menu chính...")
            return
        
        # 2. HỎI GIỌNG ĐỌC MỘT LẦN
        print(f"\nĐã tìm thấy {len(initial_files)} file.")
        # print("\nChọn một giọng nói:")
        # for display_name in VOICE_PRESETS.keys():
        #     print(f"  {display_name}")
        # print("  0. Quay lại menu chính")
        
        # voice_preset, lang_code, voice_name_part = None, None, None
        # while True:
        #     choice = input("\nNhập lựa chọn của bạn (0 để quay lại): ")
        #     if choice == '0': return

        #     try:
        #         choice_num = int(choice)
        #         if 1 <= choice_num <= len(VOICE_PRESETS):
        #             selected_display_name = list(VOICE_PRESETS.keys())[choice_num - 1]
        #             voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
        #             lang_code = VOICE_PRESETS[selected_display_name]["lang"]
        #             voice_name_part = "".join(re.findall(r'\b\w', selected_display_name.split('-')[1]))
        #             break
        #         else: print("Lựa chọn không hợp lệ!")
        #     except (ValueError, IndexError):
        #         print("Lựa chọn không hợp lệ!")
        # THAY BẰNG KHỐI CODE NÀY
        print("\nChọn giọng nói:")
        
        display_voice_menu_grid(VOICE_PRESETS)
        print("\n  0. Quay lại menu chính")

        voice_preset, lang_code, voice_name_part = None, None, None
        while True:
            choice = input("\nNhập lựa chọn của bạn (0 để quay lại): ")
            if choice == '0': return

            try:
                choice_num = int(choice)
                selected_display_name = next((key for key in VOICE_PRESETS.keys() if key.startswith(f"{choice_num}. ")), None)
                
                if selected_display_name:
                    voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
                    lang_code = VOICE_PRESETS[selected_display_name]["lang"]
                    voice_name_part = "".join(re.findall(r'\b\w', selected_display_name.split('-')[1]))
                    break
                else:
                    print("Lựa chọn không hợp lệ!")
            except (ValueError, IndexError):
                print("Lựa chọn không hợp lệ!")

        files_to_process = initial_files.copy() # Tạo một bản sao để làm hàng đợi
        processed_files_log = [] # Lưu lại log các file đã xử lý thành công
        processed_files_set = set() # Dùng để kiểm tra file đã xử lý chưa một cách nhanh chóng

        while files_to_process: # Vòng lặp sẽ tiếp tục chừng nào hàng đợi còn file
            # Lấy file đầu tiên trong hàng đợi để xử lý
            file_path = files_to_process.pop(0)

            # Bỏ qua nếu file này đã được xử lý trong một lần quét trước đó
            if file_path in processed_files_set:
                continue

            try:
                terminal_width = os.get_terminal_size().columns
            except OSError:
                terminal_width = 80 # Giá trị mặc định

            header_text = f" Bắt đầu xử lý file: {os.path.basename(file_path)} "
            full_header_line = header_text.center(terminal_width, '-')
            print(f"\n{full_header_line}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    full_text = f.read().strip()

                if not full_text:
                    print(f"⚠️ Cảnh báo: File '{os.path.basename(file_path)}' không có nội dung. Bỏ qua file này.")
                    processed_files_set.add(file_path) # Đánh dấu đã xử lý để không lặp lại
                    # Kiểm tra file mới trước khi tiếp tục
                    current_all_files = find_and_sort_input_files()
                    for new_file in current_all_files:
                        if new_file not in files_to_process and new_file not in processed_files_set:
                            files_to_process.append(new_file)
                    continue # Chuyển sang file tiếp theo trong hàng đợi

            except Exception as e:
                print(f"Lỗi khi đọc file {file_path}: {e}. Bỏ qua file này.")
                processed_files_set.add(file_path) # Đánh dấu đã xử lý (dù lỗi)
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
                print(f"⚠️ Cảnh báo: File '{os.path.basename(file_path)}' rỗng. Bỏ qua.")
                processed_files_set.add(file_path)
                continue

            final_audio_data = np.concatenate(pieces)
            
            output_dir = "Output"
            if not os.path.exists(output_dir): os.makedirs(output_dir)

            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_filename = f"{base_name}_{lang_code.upper()}_{voice_name_part}.wav"
            output_filepath = os.path.join(output_dir, output_filename)
            
            write(output_filepath, sampling_rate, final_audio_data)
            
            processed_files_log.append(output_filename)
            processed_files_set.add(file_path)

            print(f"\n✅ Hoàn tất. Đã lưu tại: {output_filepath}")

            # Sau mỗi file, quét lại thư mục Input để tìm file mới
            current_all_files = find_and_sort_input_files()
            for new_file in current_all_files:
                # Nếu tìm thấy một file chưa có trong hàng đợi và cũng chưa được xử lý
                if new_file not in files_to_process and new_file not in processed_files_set:
                    print(f"\n-> Phát hiện file mới: {os.path.basename(new_file)}.")
                    files_to_process.append(new_file) # Thêm vào cuối hàng đợi

        try:
            terminal_width = os.get_terminal_size().columns
        except OSError:
            terminal_width = 80 # Giá trị mặc định
            
        dash_line = "-" * terminal_width

        print(f"\n{dash_line}")
        print("✅ XUẤT FILE AUDIO THÀNH CÔNG!".center(terminal_width))
        if processed_files_log:
            print("\nCác file audio đã được tạo thành công:".center(terminal_width))
            for log_entry in processed_files_log:
                print(f"  - {log_entry}")
        else:
            print("Không có file audio nào được xử lý thành công.".center(terminal_width))
        print(dash_line)
        
    except KeyboardInterrupt:
        print("\n\nĐã dừng xử lý. Đang quay lại menu chính...")
        time.sleep(2)
        return
        
    input("\nNhấn Enter để quay lại menu chính...")
