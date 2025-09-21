from .ui import clear_screen, print_info_box

def show_about():
    """Hiển thị thông tin về phần mềm bằng box thông tin chung."""
    clear_screen()
    
    # Chuẩn bị dữ liệu cho các section
    author_section = [
        ("Developed By", "Justin Nguyen 🇻🇳"),
        ("Version", "1.1.0"),
        ("Date", "September 2025"),
    ]
    
    tech_section = [
        ("Core AI Model", "suno/bark, F5-TTS, OpenAI-Whisper"),
        ("AI Framework", "PyTorch"),
        ("AI Library", "Hugging Face Transformers"),
    ]

    # Tạo cấu trúc sections
    sections = {
        "Author & Version": author_section,
        "Technology": tech_section
    }

    # Gọi hàm để vẽ box
    print_info_box("Software Information", sections)

    input("\nNhấn Enter để quay lại menu chính...")