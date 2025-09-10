# ui.py

import os
import pyfiglet

VERSION = "v5.0 - Justin Nguyen"

def clear_screen():
    """Xóa màn hình terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

# NÂNG CẤP: Logic căn giữa đã được thêm vào
def generate_centered_ascii_title(text, font='standard'):
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80

    fig = pyfiglet.Figlet(font=font, width=terminal_width)
    banner_text = fig.renderText(text)
    
    lines = banner_text.splitlines()
    centered_lines = [line.center(terminal_width) for line in lines]
    centered_banner = "\n".join(centered_lines)

    return centered_banner

def display_main_menu():
    """
    Hàm chuyên dụng để hiển thị menu chính, bao gồm cả banner động.
    """
    clear_screen()
    
    print(generate_centered_ascii_title("TOOL TEXT TO SPEECH"))
    
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80
        
    print(f"{VERSION.center(terminal_width)}")
    print("\n" + "=" * terminal_width)
    print("1. Nghe thử các giọng nói (Box Voice)")
    print("2. Tạo âm thanh")
    print("3. Kiểm tra phần cứng (CPU/GPU)")
    print("4. Thoát chương trình")
    print("=" * terminal_width)