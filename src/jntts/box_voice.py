import os
import sys
from scipy.io.wavfile import write, read
import sounddevice as sd
import select
from .config import VOICE_PRESETS, TEXT_SAMPLES, LANGUAGE_NATIVE_NAMES, PROGRESS_BAR_WIDTH, PROGRESS_BAR_CHAR, REMAINING_BAR_CHAR
from .tts_utils import generate_audio_chunk
from tqdm import tqdm
import time
from .ui import clear_screen, generate_centered_ascii_title
import re

def display_voice_menu_grid(presets):
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80

    voices_by_lang = {}
    for key, value in presets.items():
        lang_name = re.match(r'\d+\.\s(.*?)\s-', key).group(1)
        if lang_name not in voices_by_lang:
            voices_by_lang[lang_name] = []
        voices_by_lang[lang_name].append(key)

    for lang, voices in voices_by_lang.items():
        if not voices: continue

        start_num = re.match(r'(\d+)', voices[0]).group(1)
        end_num = re.match(r'(\d+)', voices[-1]).group(1)
        range_str = f"({start_num}-{end_num})"

        first_voice_key = voices[0]
        lang_code = presets[first_voice_key]['lang']
        native_name = LANGUAGE_NATIVE_NAMES.get(lang_code, '') 
        native_str = f"({native_name})" if native_name else ""

        header_text = f" {lang} {range_str} {native_str} "
        full_header_line = header_text.center(terminal_width, '*')
        print(f"\n{full_header_line}")
        
        max_len = max(len(v) for v in voices) + 4
        num_columns = max(1, terminal_width // max_len)
        
        for i in range(0, len(voices), num_columns):
            row_items = voices[i:i + num_columns]
            print("".join(item.ljust(max_len) for item in row_items))

def get_audio_from_cache(voice_preset_name, model, processor, device, sampling_rate, cache_dir):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        print(f" -> Đã tạo thư mục cache lần đầu tại: {cache_dir}")

    filename = voice_preset_name.replace("/", "_") + ".wav"
    filepath = os.path.join(cache_dir, filename)

    if os.path.exists(filepath):
        print(f"\nĐang đọc giọng '{voice_preset_name}'")
        rate, audio_data = read(filepath)
        return audio_data

    selected_voice_info = next(item for item in VOICE_PRESETS.values() if item["preset"] == voice_preset_name)
    lang_code = selected_voice_info["lang"]
    text_to_speak = TEXT_SAMPLES.get(lang_code, TEXT_SAMPLES["en"])
    with tqdm(total=1, desc=f"Đang tạo giọng '{voice_preset_name}'") as pbar:
        audio_array = generate_audio_chunk(text_to_speak, voice_preset_name, model, processor, device)
        pbar.update(1)
    write(filepath, sampling_rate, audio_array)
    print(f"\nĐã tạo và lưu audio vào: {filepath}")
    return audio_array

def play_audio_with_progress(audio_data, sampling_rate, voice_name):
    """
    Phát một đoạn audio, hiển thị nhãn văn bản, thanh tiến trình và thời gian.
    Giao diện sẽ tự động co giãn theo kích thước terminal.
    Cho phép người dùng nhấn Enter để dừng phát.
    """
    try:
        duration = len(audio_data) / sampling_rate
        sd.play(audio_data, sampling_rate)
        
        start_time = time.time()
        
        # In thông báo ban đầu
        print(f"\n▶️  Đang chuẩn bị phát: {voice_name}")
        print("\n(Nhấn Enter để dừng bất kỳ lúc nào)")
        print()

        # Trích xuất tên giọng đọc ngắn gọn để hiển thị trên thanh tiến trình
        voice_display_short = voice_name.split('-', 1)[-1].strip()
        text_label = f"Playing: {voice_display_short}"

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > duration:
                break # Âm thanh đã phát xong

            # Kiểm tra xem người dùng có nhấn phím nào không
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                sys.stdin.readline()
                print("\n\n⏹️  Đã dừng phát.")
                sd.stop()
                return

            # --- TÍNH TOÁN ĐỘ RỘNG THANH TIẾN TRÌNH MỘT CÁCH LINH HOẠT ---
            try:
                terminal_width = os.get_terminal_size().columns
            except OSError:
                terminal_width = 80
            
            # Tính toán không gian cho các phần tử khác (lề, nhãn, thời gian)
            padding = 5 # Giữ lề 5 ký tự ở đầu
            time_info_str = f"{elapsed_time:.1f}s / {duration:.1f}s"
            
            # Tổng không gian đã chiếm bởi các yếu tố không phải thanh tiến trình
            # Gồm: lề trái + nhãn text + khoảng cách + cặp ngoặc [] + khoảng cách + chuỗi thời gian
            other_elements_width = padding + len(text_label) + len(" [] ") + len(time_info_str)
            
            # Độ rộng cuối cùng của thanh tiến trình
            progress_bar_width = max(10, terminal_width - other_elements_width - padding) # Trừ đi lề phải 10

            # --- VẼ THANH TIẾN TRÌNH ---
            progress_percent = elapsed_time / duration
            filled_len = int(progress_bar_width * progress_percent)
            bar = PROGRESS_BAR_CHAR * filled_len + REMAINING_BAR_CHAR * (progress_bar_width - filled_len)
            
            # Tạo chuỗi hiển thị hoàn chỉnh
            display_line = f"{' ' * padding}{text_label} [{bar}] {time_info_str}"
            
            # In ra màn hình, .ljust để đảm bảo ghi đè toàn bộ dòng cũ
            print(f"\r{display_line.ljust(terminal_width - 1)}", end="")

            time.sleep(1)

        # Xóa dòng tiến trình sau khi hoàn tất
        print("\r" + " " * (terminal_width - 1) + "\r", end="")
        print("\n✅ Hoàn tất.")
        sd.stop()

    except Exception as e:
        print(f"\nLỗi khi phát âm thanh: {e}")
        sd.stop()

def run_boxvoice(model, processor, device, sampling_rate, cache_dir_path):
    """Chạy vòng lặp menu cho chức năng Jukebox với menu phân cấp."""
    try:
        while True:
            # --- MENU CHỌN NGÔN NGỮ ---
            clear_screen()
            print(generate_centered_ascii_title("Box Voice"))
            
            # 1. Nhóm các giọng nói theo ngôn ngữ để tạo menu
            voices_by_lang = {}
            for key, value in VOICE_PRESETS.items():
                lang_name = re.match(r'\d+\.\s(.*?)\s-', key).group(1)
                if lang_name not in voices_by_lang:
                    voices_by_lang[lang_name] = []
                voices_by_lang[lang_name].append(key)
            
            # Tạo danh sách các ngôn ngữ có sẵn
            available_langs = list(voices_by_lang.keys())
            
            print("\nChọn một ngôn ngữ:")
            
            for i, lang in enumerate(available_langs):
                lang_code = VOICE_PRESETS[voices_by_lang[lang][0]]['lang']
                native_name = LANGUAGE_NATIVE_NAMES.get(lang_code, '')
                print(f"\n  {i+1}. {lang} ({native_name})")
            
            print("\n  0. Quay lại menu chính")
            
            lang_choice = input("\nNhập lựa chọn của bạn (0 để quay lại): ")
            if lang_choice == '0': break

            try:
                lang_choice_num = int(lang_choice)
                if not (1 <= lang_choice_num <= len(available_langs)):
                    print("\nLựa chọn không hợp lệ!")
                    time.sleep(1)
                    continue # Quay lại menu chọn ngôn ngữ
                
                selected_lang = available_langs[lang_choice_num - 1]
                voices_in_lang = voices_by_lang[selected_lang]

                first_voice_key = voices_in_lang[0]
                lang_code = VOICE_PRESETS[first_voice_key]['lang']
                native_name_with_flag = LANGUAGE_NATIVE_NAMES.get(lang_code, '')

                # --- MENU CHỌN GIỌNG NÓI TRONG NGÔN NGỮ ĐÃ CHỌN ---
                while True:
                    clear_screen()
                    print(generate_centered_ascii_title("Box Voice"))
                    print(f"\n--- Chọn giọng nói: ({selected_lang} - {native_name_with_flag}) ---")
                    
                    for voice_key in voices_in_lang:
                        print(f"\n  {voice_key}")

                    print("\n  0. Quay lại menu ngôn ngữ")
                    voice_choice = input("\nChọn một giọng nói để nghe thử (0 để quay lại): ")
                    if voice_choice == '0': break

                    try:
                        voice_choice_num = int(voice_choice)
                        selected_display_name = next((key for key in voices_in_lang if key.startswith(f"{voice_choice_num}. ")), None)
                        
                        if selected_display_name:
                            selected_voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
                            audio_to_play = get_audio_from_cache(selected_voice_preset, model, processor, device, sampling_rate, cache_dir=cache_dir_path)
                            
                            # Gọi hàm phát audio mới thay cho logic cũ
                            play_audio_with_progress(audio_to_play, sampling_rate, selected_display_name)
                        else:
                            print("\nLựa chọn không hợp lệ!")
                            time.sleep(1)
                    except ValueError:
                        print("\nLựa chọn không hợp lệ! Vui lòng chỉ nhập số.")
                        time.sleep(1)

            except ValueError:
                print("\nLựa chọn không hợp lệ! Vui lòng chỉ nhập số.")
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nĐang quay lại menu chính...")
        return