import sys
import os
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

from config import CACHE_DIR
from tts_utils import load_models
from box_voice import run_boxvoice
from file_tts import run_file_tts
from hardware_check import run_hardware_check
from ui import display_main_menu
from about import show_about


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def setup_directories():
    """Tự động tạo các thư mục cần thiết nếu chúng chưa tồn tại."""
    print("Đang kiểm tra và tạo các thư mục cần thiết...")
    required_dirs = [CACHE_DIR, "Input", "Output"]
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f" -> Đã tạo thư mục: {dir_name}/")

def main_menu():
    setup_directories()
    
    model, processor, device, sampling_rate = load_models()

    try:
        while True:
            display_main_menu()
            
            choice = input("Nhập lựa chọn của bạn (0-4): ")

            if choice == '1':
                run_boxvoice(model, processor, device, sampling_rate)
            elif choice == '2':
                run_file_tts(model, processor, device, sampling_rate)
            elif choice == '3':
                run_hardware_check()
            elif choice == '4':
                show_about()
            elif choice == '0':
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