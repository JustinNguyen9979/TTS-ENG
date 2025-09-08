# app.py

import sys
import os
from config import CACHE_DIR
from tts_utils import load_models
from jukebox import run_jukebox
from file_tts import run_file_tts

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def setup_directories():
    """Tự động tạo các thư mục cần thiết nếu chúng chưa tồn tại."""
    print("Đang kiểm tra và thiết lập các thư mục cần thiết...")
    # NÂNG CẤP: Thêm 'Input' và 'Output' vào danh sách
    required_dirs = [CACHE_DIR, "Input", "Output"]
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f" -> Đã tạo thư mục: {dir_name}/")

def main_menu():
    """Hiển thị và xử lý menu chính."""
    # Thiết lập thư mục ngay khi bắt đầu
    setup_directories()
    
    # Tải model một lần duy nhất khi chương trình khởi động
    model, processor, device, sampling_rate = load_models()

    try:
        while True:
            clear_screen()
            print("======= CÔNG CỤ TẠO GIỌNG NÓI SUNO/BARK (v2) =======")
            print("1. Nghe thử các giọng nói (Jukebox)")
            print("2. Tạo âm thanh từ file trong thư mục 'Input'")
            print("3. Thoát chương trình")
            print("===================================================")
            
            choice = input("Nhập lựa chọn của bạn (1-3): ")

            if choice == '1':
                run_jukebox(model, processor, device, sampling_rate)
            elif choice == '2':
                run_file_tts(model, processor, device, sampling_rate)
            elif choice == '3':
                print("Tạm biệt!")
                sys.exit(0)
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
                input("Nhấn Enter để tiếp tục...")

    except KeyboardInterrupt:
        print("\n\nĐã thoát chương trình. Tạm biệt!")
        sys.exit(0)

if __name__ == "__main__":
    main_menu()