import os
from .ui import clear_screen, generate_centered_ascii_title

BOX_CHARS = {
    'top_left': '╭',
    'top_right': '╮',
    'bottom_left': '╰',
    'bottom_right': '╯',
    'horizontal': '─',
    'vertical': '│',
}

def show_about():
    clear_screen()
    print(generate_centered_ascii_title("Software Information"))
    
    regal_border = "⚜⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯  ⚜ ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⚜"

    tool_credits_data = [
        ("Developed By:", "Justin Nguyen 🇻🇳"),
        ("Version:", "1.1.0 "),
        ("Date:", "September 2025"),
    ]
    
    tech_stack_data = [
        ("Core AI Model:", "suno/bark by Suno AI. F5-TTS"),
        ("AI Framework:", "PyTorch"),
        ("AI Library:", "Hugging Face Transformers"),
    ]
    
    all_labels = [label for label, value in tool_credits_data] + [label for label, value in tech_stack_data]
    label_width = max(len(label) for label in all_labels)
    
    content_lines = []
    
    content_lines.append("AUTHOR & VERSION")
    content_lines.append("") 
    for label, value in tool_credits_data:
        content_lines.append(f"{label.ljust(label_width)} {value}")
        
    content_lines.append("")
    content_lines.append(regal_border)
    content_lines.append("")
    
    content_lines.append("TECHNOLOGY")
    content_lines.append("")
    for label, value in tech_stack_data:
        content_lines.append(f"{label.ljust(label_width)} {value}")
        
    content_width = max(len(line) for line in content_lines)
    
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80
        
    box_width = content_width + 4
    left_padding = " " * ((terminal_width - box_width) // 2)
    
    top_border = BOX_CHARS['top_left'] + (BOX_CHARS['horizontal'] * (box_width - 2)) + BOX_CHARS['top_right']
    print("\n" + left_padding + top_border)

    for line in content_lines:
        if line.isupper() or line == regal_border:
            padded_line = f" {line.center(content_width)} "
        else:
            padded_line = f" {line.ljust(content_width)} "
        print(left_padding + BOX_CHARS['vertical'] + padded_line + BOX_CHARS['vertical'])

    bottom_border = BOX_CHARS['bottom_left'] + (BOX_CHARS['horizontal'] * (box_width - 2)) + BOX_CHARS['bottom_right']
    print(left_padding + bottom_border)

    input("\nNhấn Enter để quay lại menu chính...")