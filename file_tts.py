# file_tts.py

import os
import sys
import re
import numpy as np
from scipy.io.wavfile import write
from config import VOICE_PRESETS
from tts_utils import generate_audio_chunk
from tqdm import tqdm

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# NÂNG CẤP: Hàm tự động tìm file .txt trong thư mục 'Input'
def find_input_file():
    """
    Quét thư mục 'Input' và trả về đường dẫn của file .txt đầu tiên tìm thấy.
    """
    input_dir = "Input"
    # Kiểm tra lại để chắc chắn thư mục tồn tại
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.txt'):
            # Tìm thấy file, trả về đường dẫn đầy đủ
            return os.path.join(input_dir, filename)
    
    # Nếu vòng lặp kết thúc mà không tìm thấy file nào
    return None

def run_file_tts(model, processor, device, sampling_rate):
    """Chạy quy trình Text-to-Speech từ file."""
    try:
        clear_screen()
        print("============================================")
        print("============== TEXT-TO-SPEECH ==============")
        print("============================================")

        # NÂNG CẤP: Tự động quét thư mục 'Input'
        # print("Đang quét thư mục 'Input' để tìm file .txt...")
        input_file_path = find_input_file()

        # Kiểm tra xem có tìm thấy file không
        if not input_file_path:
            print("\nLỖI: Không tìm thấy file .txt nào trong thư mục 'Input'.")
            print("Vui lòng đặt file văn bản của bạn vào thư mục 'Input' và thử lại.")
            input("Nhấn Enter để quay lại menu chính...")
            return
        
        print(f"Đã tìm thấy file: {input_file_path}")

        # Đọc nội dung file
        with open(input_file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()

        # 2. Hỏi giọng đọc
        print("\nChọn một giọng nói để sử dụng:")
        for display_name in VOICE_PRESETS.keys():
            print(f"  {display_name}")
        print("  0. Quay lại menu chính")
        
        while True:
            choice = input("Nhập lựa chọn của bạn (0 để quay lại): ")

            if choice == '0':
                print("Đang quay lại menu chính...")
                return
            
            try:
                choice_num = int(choice)
                # Kiểm tra để đảm bảo lựa chọn nằm trong phạm vi hợp lệ
                if 1 <= choice_num <= len(VOICE_PRESETS):
                    selected_display_name = list(VOICE_PRESETS.keys())[choice_num - 1]
                    voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
                    lang_code = VOICE_PRESETS[selected_display_name]["lang"]
                    break # Lựa chọn hợp lệ, thoát khỏi vòng lặp
                else:
                    # Nếu người dùng nhập số ngoài phạm vi
                    print("Lựa chọn không hợp lệ! Vui lòng chọn một số trong danh sách.")
            except ValueError:
                # Nếu người dùng nhập chữ thay vì số
                print("Lựa chọn không hợp lệ! Vui lòng chỉ nhập số.")

        # 3. Xử lý và tạo âm thanh
        print("\nBắt đầu quá trình tạo âm thanh...")
        sentences = re.split(r'(?<=[.?!])\s+', full_text.replace('\n', ' ').strip())
        pieces = []
        
        for sentence in tqdm(sentences, desc="Tiến trình tạo file"):
            if not sentence.strip():
                continue
            audio_chunk = generate_audio_chunk(sentence, voice_preset, model, processor, device)
            pieces.append(audio_chunk)
            pause_samples = np.zeros(int(sampling_rate * 0.5), dtype=np.float32)
            pieces.append(pause_samples)

        # 4. Ghép nối và lưu file
        print("Đang xuất file audio...")
        final_audio_data = np.concatenate(pieces)
        
        output_dir = "Output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        first_three_words = "_".join(full_text.split()[:3])
        safe_filename_part = re.sub(r'[^\w\s-]', '', first_three_words).strip().replace(' ', '_')
        
        output_filename = f"{lang_code}_{safe_filename_part}.wav"
        output_filepath = os.path.join(output_dir, output_filename)
        
        write(output_filepath, sampling_rate, final_audio_data)

        print("-" * 60)
        print(f"✅ Hoàn tất! Đã tạo file audio thành công tại: {output_filepath}")
        print("-" * 60)
        input("Nhấn Enter để quay lại menu chính...")

    except KeyboardInterrupt:
        print("\nĐang quay lại menu chính...")
        return