import os
import pyfiglet

VERSION = "v1.1.0 - Developed By Justin Nguyen 🇻🇳"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    clear_screen()
    
    print(generate_centered_ascii_title("TOOL TEXT TO SPEECH"))
    
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 79
    
    menu_items = [
        "Nghe thử giọng nói (Box Voice)",
        "Tạo giọng nói (Text To Speech)",
        "Nhân bản giọng nói (Clone Voice)",
        "Chuyển giọng nói thành văn bản (Transcribe Audio)",
        "Kiểm tra phần cứng (Check CPU/GPU)",
        "Thông tin & Giới thiệu (About)"
    ]
        
    print(f"{VERSION.center(terminal_width)}")
    print("\n" + "=" * terminal_width)
    for i, item in enumerate(menu_items):
        print(f"\n  [{i+1}]. {item}")
    print("\n  [0]. Thoát chương trình (Exit)")
    print("\n" + "=" * terminal_width)