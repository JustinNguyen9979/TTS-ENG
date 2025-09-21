import os
import pyfiglet
import textwrap
import wcwidth
import random
import re

from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.console import Console
from rich.style import Style
from rich.color import Color

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
    
    bright_colors = [
        # --- Các màu sáng cơ bản (tương phản cao) ---
        "bright_cyan",
        "bright_magenta",
        "bright_yellow",
        "bright_green",
        "bright_blue",
        "bright_red",
        
        # --- Các màu tông Lục và Lam (Greens & Blues) ---
        "spring_green1",
        "spring_green2",
        "sea_green1",
        "turquoise2",
        "deep_sky_blue1",
        "dodger_blue1",
        "steel_blue1",
        
        # --- Các màu tông Vàng và Cam (Yellows & Oranges) ---
        "gold1",
        "dark_orange",
        "orange1",
        "light_goldenrod1",
        
        # --- Các màu tông Đỏ và Hồng (Reds & Pinks) ---
        "light_coral",
        "indian_red1",
        "hot_pink",
        "deep_pink1",
        
        # --- Các màu tông Tím (Purples) ---
        "medium_purple",
        "orchid",
        "blue_violet"
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
    Hiển thị một menu lựa chọn chung với phong cách đơn giản và đáng tin cậy,
    giống hệt như menu chính để đảm bảo tính ổn định tuyệt đối.
    """
    # Xây dựng nội dung menu bằng Text object.
    menu_content = Text()
    
    for i, item in enumerate(options):
        # Chuyển đổi item thành chuỗi để xử lý nhất quán
        if isinstance(item, tuple):
            # Nếu là tuple ('key', 'value'), ghép chúng lại thành một chuỗi
            item_text = f"{item[0]:<12} - {item[1]}"
        else:
            # Nếu là chuỗi, xóa số thứ tự cũ (nếu có)
            item_text = re.sub(r'^\d+\.\s*', '', str(item))
        
        # Thêm từng dòng lựa chọn vào menu
        menu_content.append(f"  [", style="default")
        menu_content.append(str(i + 1), style=f"bold {color}")
        menu_content.append(f"]. {item_text}\n\n", style="default")

    # Thêm lựa chọn quay lại
    menu_content.append(f"  [", style="default")
    menu_content.append("0", style=f"bold {color}")
    menu_content.append(f"]. {back_option}\n", style="default")

    # Đặt nội dung vào trong một Panel
    menu_panel = Panel(
        menu_content,
        title=f"[bold]{title}[/bold]",
        title_align="center",
        border_style=color,
        padding=(1, 2)
    )
    
    # In Panel ra giữa màn hình
    console.print(Align.center(menu_panel))
    
    # Lấy lựa chọn của người dùng
    choice = input(f"\nNhập lựa chọn của bạn (00 để về menu chính): ")
    return choice