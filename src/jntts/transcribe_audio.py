import os
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
import whisper
import time
from tqdm import tqdm
from pathlib import Path
from .ui import generate_centered_ascii_title, clear_screen

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
        print(generate_centered_ascii_title("Transcribe Audio to Text"))

        input_path = Path(input_dir)
        output_path = Path(output_dir)

        # BƯỚC 1: KIỂM TRA VÀ TÌM KIẾM TẤT CẢ FILE ÂM THANH
        if not input_path.is_dir():
            print(f"❌ Lỗi: Thư mục Input '{input_dir}' không tồn tại.")
            input("\nNhấn Enter để quay lại menu chính...")
            return

        # Lấy tất cả các file .mp3 và .wav, không cần lọc
        audio_files = list(input_path.glob('*.mp3')) + list(input_path.glob('*.wav'))

        if not audio_files:
            print(f"\nℹ️ Không tìm thấy file âm thanh (.mp3 hoặc .wav) nào trong thư mục '{input_path.name}'.")
            input("\nNhấn Enter để quay lại menu chính...")
            return

        print(f"\n🔎 Tìm thấy {len(audio_files)} file âm thanh.")

        # BƯỚC 2: KHỞI TẠO MODEL WHISPER
        model_options = [
            ("large-v3", "🎯 Chính xác nhất (Yêu cầu >10GB VRAM, chậm)"),
            ("medium",   "⚖️ Cân bằng nhất (Chính xác cao, >5GB VRAM)"),
            ("small",    "⚡️ Nhanh & Tốt (Hầu hết tác vụ, >2GB VRAM)"),
            ("base",     "✅ Mặc định (Rất nhanh, >1GB VRAM)"),
            ("tiny",     "🚀 Siêu nhanh (Thử nghiệm, >1GB VRAM)"),
            ("medium.en","🗣️ Tiếng Anh - Cân bằng"),
            ("base.en",  "🗣️ Tiếng Anh - Mặc định (Rất nhanh)"),
]

        chosen_model_name = None
        while True:
            clear_screen()
            print(generate_centered_ascii_title("Transcribe Audio to Text"))
            print("\nChọn model:")
            for i, (name, desc) in enumerate(model_options):
                print(f"\n  [{i+1}] {name:<10} - {desc}")
            print("\n  [0] Quay lại menu")

            try:
                choice = int(input("\nNhập lựa chọn của bạn (0-7): "))
                if choice == 0:
                    return
                if 1 <= choice <= len(model_options):
                    chosen_model_name = model_options[choice - 1][0]
                    break # Lựa chọn hợp lệ, thoát khỏi vòng lặp
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
                    time.sleep(1.5)
            except ValueError:
                print("Vui lòng nhập một số.")
                time.sleep(1.5)

        model = None
        try:
            print(f"\n🔄 Đang tải model Whisper ({chosen_model_name})...")
            model = whisper.load_model(chosen_model_name)
            print(f"\n✅ Đang sử dụng Model {chosen_model_name}.")
        except Exception as e:
            print(f"\n❌ Lỗi khi tải model Whisper: {e}")
            input("\nNhấn Enter để quay lại menu chính...")
            return    
        # BƯỚC 3: XỬ LÝ TỪNG FILE
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
                    
                    # --- THAY ĐỔI 2: THÊM TÊN FILE VÀO DANH SÁCH LOG ---
                    processed_files_log.append(output_filename)
                    pbar.set_postfix_str(f"Thành công: {output_filename}", refresh=True)
                
                except Exception as e:
                    pbar.set_postfix_str(f"Lỗi: {audio_file_path.name}", refresh=True)
                
                pbar.update(1)
            
            pbar.set_description("Hoàn tất!")
            pbar.set_postfix_str("", refresh=True)


        print() 
        
        try:
    # Lấy chiều rộng terminal và trừ đi 1 để tránh lỗi wrapping
            terminal_width = os.get_terminal_size().columns - 2
        except OSError:
            terminal_width = 78

        core_message = "✅ Transcribe hoàn tất!"
        padded_message = f" {core_message} "

        # Tính toán số dấu gạch ngang cần thiết cho mỗi bên
        padding_len = terminal_width - len(padded_message)
        # Đảm bảo padding không bị âm nếu terminal quá hẹp
        if padding_len < 0: padding_len = 0 

        dashes_each_side = padding_len // 2

        # Tạo các chuỗi gạch ngang
        left_dashes = '-' * dashes_each_side
        right_dashes = '-' * (padding_len - dashes_each_side)

        # Kết hợp lại và in ra
        full_line_message = f"{left_dashes}{padded_message}{right_dashes}"
        print(f"\n {full_line_message}")

        if processed_files_log:
            print("\nCác file đã được transcribe thành công:")
            for filename in processed_files_log:
                print(f"  -> {filename}")
        else:
            print("⚠️ Không có file nào được xử lý thành công.")

    except KeyboardInterrupt:
        print("\n\nĐã dừng xử lý. Quay lại menu chính...")

    input("\nNhấn Enter để quay lại menu chính...")