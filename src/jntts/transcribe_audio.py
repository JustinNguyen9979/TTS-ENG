import os
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
import whisper
import time
from tqdm import tqdm
from pathlib import Path
from .ui import display_selection_menu, clear_screen, generate_centered_ascii_title
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()

def run_transcription(input_dir: str, output_dir: str, downloads_path: str):
    """
    Quét thư mục Input để tìm file .mp3 và .wav,
    chuyển đổi chúng thành văn bản bằng Whisper,
    và lưu/ghi đè kết quả vào thư mục Output.

    Args:
        input_dir (str): Đường dẫn đến thư mục chứa file âm thanh.
        output_dir (str): Đường dẫn đến thư mục để lưu file văn bản kết quả.
        downloads_path (str): Tham số này không được sử dụng nhưng cần có để tương thích.
    """
    try:
        clear_screen()
        ascii_title = generate_centered_ascii_title("Transcribe Audio") # Giữ lại ASCII art
        console.print(Text(ascii_title, style="bold bright_magenta")) # Tô màu cho nó

        input_path = Path(input_dir)
        output_path = Path(output_dir)

        # BƯỚC 1: KIỂM TRA VÀ TÌM KIẾM TẤT CẢ FILE ÂM THANH
        if not input_path.is_dir():
            console.print(Align.center(f"[bold red]❌ Lỗi: Thư mục Input '{input_dir}' không tồn tại.[/bold red]"))
            input("\nNhấn Enter để quay lại menu chính...")
            return

        # Lấy tất cả các file .mp3 và .wav, không cần lọc
        audio_files = list(input_path.glob('*.mp3')) + list(input_path.glob('*.wav'))

        if not audio_files:
            console.print(Align.center(f"[yellow]ℹ️ Không tìm thấy file âm thanh (.mp3 hoặc .wav) nào trong thư mục '{input_path.name}'.[/yellow]"))
            input("\nNhấn Enter để quay lại menu chính...")
            return

        print(f"\n🔎 Tìm thấy {len(audio_files)} file âm thanh.")

        # BƯỚC 2: KHỞI TẠO MODEL WHISPER
        model_options_data = [
            ("large-v3", "Chính xác nhất (Yêu cầu >10GB VRAM, chậm)"),
            ("medium",   "Cân bằng nhất (Chính xác cao, >5GB VRAM)"),
            ("small",    "Nhanh & Tốt (Hầu hết tác vụ, >2GB VRAM)"),
            ("base",     "Mặc định (Rất nhanh, >1GB VRAM)"),
            ("tiny",     "Siêu nhanh (Thử nghiệm, >1GB VRAM)"),
            ("medium.en","Tiếng Anh - Cân bằng"),
            ("base.en",  "Tiếng Anh - Mặc định (Rất nhanh)"),
        ]

        model_display_options = [f"{name:<12} - {desc}" for name, desc in model_options_data]

        chosen_model_name = None
        while True:
            clear_screen()
            ascii_title = generate_centered_ascii_title("Transcribe Audio to Text")
            console.print(Align.center(Text(ascii_title, style="bold bright_magenta")))
            
            choice_str = display_selection_menu("Chọn model Whisper", model_display_options, color="bright_cyan", back_option="Quay lại menu chính")

            try:
                if choice_str == '0': return
                if choice_str == '00': return
                   
                choice = int(choice_str)
                if 1 <= choice <= len(model_options_data):
                    chosen_model_name = model_options_data[choice - 1][0]
                    break
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng thử lại."); time.sleep(1.5)
            except ValueError:
                print("Vui lòng nhập một số."); time.sleep(1.5)

        # --- TẢI MODEL VÀ XỬ LÝ (GIỮ NGUYÊN) ---
        model = None
        try:
            print(f"\n🔄 Đang tải model Whisper ({chosen_model_name})...")
            model = whisper.load_model(chosen_model_name)
            print(f"\n✅ Đang sử dụng Model {chosen_model_name}.")
        except Exception as e:
            console.print(Align.center(f"[bold red]❌ Lỗi khi tải model Whisper: {e}[/bold red]"))
            input("\nNhấn Enter để quay lại menu chính..."); return
        
        print()
        processed_files_log = []
        
        with tqdm(total=len(audio_files), desc="Tiến trình", unit="file", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]") as pbar:
            for audio_file_path in audio_files:
                pbar.set_postfix_str(f"Đang xử lý: {audio_file_path.name}", refresh=True)
                output_filename = f"transcribe_{audio_file_path.stem}.txt"
                output_txt_path = output_path / output_filename
                try:
                    result = model.transcribe(str(audio_file_path), fp16=False)
                    transcribed_text = result['text'].strip()
                    with open(output_txt_path, 'w', encoding='utf-8') as f:
                        f.write(transcribed_text)
                    processed_files_log.append(output_filename)
                    pbar.set_postfix_str(f"Thành công: {output_filename}", refresh=True)
                except Exception as e:
                    pbar.set_postfix_str(f"Lỗi: {audio_file_path.name}", refresh=True)
                pbar.update(1)
            pbar.set_description("Hoàn tất!"); pbar.set_postfix_str("", refresh=True)

        # --- BÁO CÁO KẾT QUẢ (PHIÊN BẢN RICH) ---
        report_content = Text()
        if processed_files_log:
            report_content.append("Các file đã được transcribe thành công:\n\n", style="bold")
            for filename in processed_files_log:
                report_content.append(f"  - {filename}\n", style="green")
        else:
            report_content.append("⚠️ Không có file nào được xử lý thành công.", style="yellow")

        report_panel = Panel(
            report_content,
            title="[bold]✅ Transcribe Hoàn Tất![/bold]",
            title_align="center",
            border_style="green",
            padding=(1, 2)
        )
        console.print()
        console.print(Align.center(report_panel))

    except KeyboardInterrupt:
        print("\n\nĐã dừng xử lý. Quay lại menu chính...")

    input("\nNhấn Enter để quay lại menu chính...")