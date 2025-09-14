import sys
import os
import warnings

from pathlib import Path
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

warnings.filterwarnings("ignore", category=FutureWarning)

# from .config import CACHE_DIR
from .tts_utils import load_models
from .box_voice import run_boxvoice
from .file_tts import run_file_tts
from .hardware_check import run_hardware_check
from .ui import display_main_menu
from .about import show_about
from .voice_cloning import run_voice_cloning
from .transcribe_audio import run_transcription

package_path = files('jntts')
CACHE_DIR_APP = str(package_path / 'audio_cache')

HOME_PATH = Path.home()
DOWNLOADS_PATH = HOME_PATH / "Downloads" # Nối đường dẫn đến thư mục Downloads

INPUT_DIR = DOWNLOADS_PATH / "jntts" / "Input"
OUTPUT_DIR = DOWNLOADS_PATH / "jntts" / "Output"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def setup_directories():
    print("Đang kiểm tra và tạo các thư mục cần thiết...")
    print(f"Dữ liệu Input/Output sẽ được lưu tại: {os.path.join(DOWNLOADS_PATH, 'jntts')}")
    
    required_dirs = [INPUT_DIR, OUTPUT_DIR, CACHE_DIR_APP, "Voice"]
    for dir_name in required_dirs:
        # Xây dựng đường dẫn đầy đủ cho thư mục Voice
        if dir_name == "Voice":
            path_to_create = os.path.join(DOWNLOADS_PATH, "jntts", dir_name)
        else:
            path_to_create = dir_name

        if not os.path.exists(path_to_create):
            try:
                os.makedirs(path_to_create)
                print(f" -> Đã tạo thư mục: {path_to_create}")
            except OSError as e:
                print(f"LỖI: Không thể tạo thư mục {path_to_create}. Lỗi: {e}")
                sys.exit(1)


def main():
    setup_directories()
    
    model, processor, device, sampling_rate = load_models()

    try:
        while True:
            display_main_menu()
            
            choice = input("Nhập lựa chọn của bạn (0-6): ")

            if choice == '1':
                run_boxvoice(model, processor, device, sampling_rate, CACHE_DIR_APP)
            elif choice == '2':
                run_file_tts(model, processor, device, sampling_rate, INPUT_DIR, OUTPUT_DIR)
            elif choice == '3':
                run_voice_cloning(INPUT_DIR, OUTPUT_DIR, DOWNLOADS_PATH)
            elif choice == '4':
                run_transcription(INPUT_DIR, OUTPUT_DIR, DOWNLOADS_PATH)
            elif choice == '5':
                run_hardware_check()
            elif choice == '6':
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
    main()