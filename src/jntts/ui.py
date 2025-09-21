import os
import pyfiglet
import textwrap
import wcwidth
import random
import re

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()

# --- HẰNG SỐ CHO VIỆC VẼ BOX ---
BOX_CHARS_SINGLE = {
    'top_left': '╭', 'top_right': '╮', 'bottom_left': '╰', 'bottom_right': '╯',
    'horizontal': '─', 'vertical': '│',
}
BOX_CHARS_DOUBLE = {
    'top_left': '╔', 'top_right': '╗', 'bottom_left': '╚', 'bottom_right': '╝',
    'horizontal': '═', 'vertical': '║',
}

# --- HẰNG SỐ MÀU SẮC ---
COLOR_SUCCESS = '\033[92m'
COLOR_WARNING = '\033[93m'
COLOR_RESET = '\033[0m'

VERSION = "v1.1.0 - Developed By Justin Nguyen 🇻🇳"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def _render_and_center_block(block_str):
    """Nhận một chuỗi đa dòng, tính toán và in nó ra giữa terminal."""
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80
    
    # Tìm dòng dài nhất trong khối để xác định chiều rộng của khối
    block_width = 0
    if block_str:
        block_width = max(wcwidth.wcswidth(line) for line in block_str.split('\n'))

    # Tính toán lề trái
    left_padding_str = " " * ((terminal_width - block_width) // 2)

    # Sử dụng textwrap.indent để thêm lề vào mỗi dòng của khối
    centered_block = textwrap.indent(block_str, left_padding_str)
    print(centered_block)

# --- HÀM MASTER ĐỂ VẼ BOX (PRIVATE) ---
def _draw_box_wrapper(content_lines, box_chars, color_code=COLOR_RESET, inner_padding=2):
    """Hàm lõi, chịu trách nhiệm tính toán và vẽ mọi loại box."""
    
    # Helper để tính chiều rộng hiển thị thực tế của chuỗi (hỗ trợ emoji)
    def display_width(s):
        return wcwidth.wcswidth(s)

    if not content_lines:
        return

    content_width = max(display_width(line) for line in content_lines)
    box_width = content_width + (inner_padding * 2) + 2 # +2 cho viền dọc

    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80
        
    left_padding_str = " " * ((terminal_width - box_width) // 2)

    # Vẽ viền trên
    top_border = box_chars['top_left'] + (box_chars['horizontal'] * (box_width - 2)) + box_chars['top_right']
    print(color_code + left_padding_str + top_border + COLOR_RESET)

    # Vẽ nội dung
    for line in content_lines:
        line_padding_right = " " * (content_width - display_width(line))
        padded_line = f"{' ' * inner_padding}{line}{line_padding_right}{' ' * inner_padding}"
        print(color_code + left_padding_str + box_chars['vertical'] + padded_line + box_chars['vertical'] + COLOR_RESET)

    # Vẽ viền dưới
    bottom_border = box_chars['bottom_left'] + (box_chars['horizontal'] * (box_width - 2)) + box_chars['bottom_right']
    print(color_code + left_padding_str + bottom_border + COLOR_RESET)


def print_info_box(title, sections):
    """
    Vẽ một info box đẹp mắt bằng Rich, đã sửa lỗi ImportError cho Group.
    """
    clear_screen()
    
    # In tiêu đề ASCII Art có màu
    ascii_art_string = generate_centered_ascii_title(title)
    console.print(Text(ascii_art_string, style="bold bright_cyan"))

    # --- TẠO MỘT DANH SÁCH CÁC THÀNH PHẦN CÓ THỂ RENDER ---
    renderables = []

    all_labels = [label for section in sections.values() for label, value in section]
    if not all_labels: return
    label_width = max(len(label) for label in all_labels)

    first_section = True
    for section_title, data in sections.items():
        if not first_section:
            renderables.append(Text("\n"))
        first_section = False

        section_header = Text(f"--- {section_title.upper()} ---", style="bold magenta")
        renderables.append(Align.center(section_header))
        renderables.append(Text("\n"))
        
        section_content = Text()
        for label, value in data:
            section_content.append(f"{label.ljust(label_width)} : ", style="cyan")
            section_content.append(f"{value}\n")
        
        renderables.append(section_content)

    # --- TẠO VÀ IN PANEL TỪ DANH SÁCH CÁC THÀNH PHẦN ---
    # SỬA LỖI IMPORT Ở ĐÂY:
    from rich.console import Group # Group nằm trong rich.console

    content_group = Group(*renderables)

    info_panel = Panel(
        content_group,
        border_style="green",
        padding=(1, 2)
    )

    console.print(Align.center(info_panel))


# --- HÀM PUBLIC CHO HIGHLIGHT BOX (PHIÊN BẢN RICH) ---
def print_highlight_box(lines, status='success'):
    """Vẽ một highlight box nổi bật bằng Rich, đã sửa lỗi TypeError."""
    
    color_map = {'success': 'green', 'warning': 'yellow'}
    icon_map = {'success': '✅', 'warning': '⚠️'}
    
    color = color_map.get(status, 'white')
    icon = icon_map.get(status, '➡️')

    # Xây dựng nội dung bằng cách kết hợp các đối tượng Text
    content = Text()
    
    # Dòng 1 với icon, căn lề trái (mặc định)
    content.append(f"{icon} {lines[0]}\n\n", style="bold")
    
    # Dòng 2 được tạo riêng và căn giữa
    # Chúng ta thêm một đối tượng Text mới được căn giữa vào content
    content.append(Text(lines[1], justify="center", style="bold"))

    # Tạo Panel với viền đôi và màu sắc
    highlight_panel = Panel(
        content, # Không cần Align.center ở đây nữa vì đã justify bên trong Text
        border_style=f"bold {color}",
        box=box.DOUBLE,
        padding=(1, 5),
        title_align="center"
    )
    
    # In Panel ra giữa màn hình
    console.print(Align.center(highlight_panel))

from rich import box

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
    """Hiển thị menu chính với màu sắc ngẫu nhiên."""
    clear_screen()
    
    # --- LOGIC CHỌN MÀU NGẪU NHIÊN ---
    # Danh sách các màu sắc tươi sáng, đẹp mắt từ thư viện Rich
    bright_colors = [
        "bright_cyan",
        "bright_magenta",
        "bright_yellow",
        "bright_green",
        "bright_blue",
        "bright_red",
    ]
    # Chọn một màu ngẫu nhiên từ danh sách trên
    random_color = random.choice(bright_colors)

    # In tiêu đề ASCII Art với màu ngẫu nhiên
    ascii_title = generate_centered_ascii_title("TOOL TEXT TO SPEECH")
    console.print(Text(ascii_title, style=f"bold {random_color}"))
    
    # In phiên bản
    console.print(Align.center(Text(VERSION, style="italic dim")))

    # --- XÂY DỰNG NỘI DUNG MENU BẰNG RICH ---
    menu_items = [
        "Nghe thử giọng nói (Box Voice)",
        "Tạo giọng nói (Text To Speech)",
        "Nhân bản giọng nói (Clone Voice)",
        "Chuyển giọng nói thành văn bản (Transcribe Audio)",
        "Kiểm tra phần cứng (Check CPU/GPU)",
        "Thông tin & Giới thiệu (About)"
    ]

    menu_content = Text()
    for i, item in enumerate(menu_items):
        # Định dạng số và mục menu với các màu khác nhau
        menu_content.append(f"  [", style="default")
        menu_content.append(str(i + 1), style=f"bold {random_color}")
        menu_content.append(f"]. {item}\n\n", style="default")

    # Thêm lựa chọn thoát
    menu_content.append(f"  [", style="default")
    menu_content.append("0", style=f"bold {random_color}")
    menu_content.append(f"]. Thoát chương trình (Exit)\n", style="default")

    # Tạo một Panel (hộp) để chứa menu
    menu_panel = Panel(
        menu_content,
        border_style=random_color, # Viền của hộp cũng có màu ngẫu nhiên
        title="[bold]CHỌN CHỨC NĂNG[/bold]",
        title_align="center",
        padding=(1, 2)
    )

    # In menu ra giữa màn hình
    console.print(Align.center(menu_panel))

def display_selection_menu(title, options, color="cyan", back_option="Quay lại menu trước"):
    """
    Hiển thị một menu lựa chọn chung với phong cách của Rich.
    
    Args:
        title (str): Tiêu đề của menu (ví dụ: "Chọn một ngôn ngữ").
        options (list): Danh sách các chuỗi lựa chọn.
        color (str): Màu sắc chủ đạo cho menu.
        back_option (str): Văn bản cho lựa chọn quay lại (số 0).
    
    Returns:
        str: Lựa chọn của người dùng.
    """
    menu_content = Text()
    for i, item in enumerate(options):
        # Loại bỏ số thứ tự cũ nếu có (ví dụ: "1. English - Male 1")
        item_text = re.sub(r'^\d+\.\s*', '', item)
        menu_content.append(f"  [", style="default")
        menu_content.append(str(i + 1), style=f"bold {color}")
        menu_content.append(f"]. {item_text}\n\n", style="default")

    menu_content.append(f"  [", style="default")
    menu_content.append("0", style=f"bold {color}")
    menu_content.append(f"]. {back_option}\n", style="default")

    menu_panel = Panel(
        menu_content,
        title=f"[bold]{title}[/bold]",
        title_align="center",
        border_style=color,
        padding=(1, 2)
    )
    
    console.print(Align.center(menu_panel))
    
    choice = input(f"\nNhập lựa chọn của bạn (0 để quay lại): ")
    return choice