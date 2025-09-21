import os
import sys
from scipy.io.wavfile import write, read
import sounddevice as sd
import time
import re
from tqdm import tqdm
from .config import VOICE_PRESETS, TEXT_SAMPLES, LANGUAGE_NATIVE_NAMES, PROGRESS_BAR_CHAR, REMAINING_BAR_CHAR
from .tts_utils import generate_audio_chunk
from .ui import clear_screen, display_selection_menu, generate_centered_ascii_title
from rich.console import Console
from rich.text import Text

console = Console()

# Kiểm tra hệ điều hành để import thư viện tương ứng
IS_WINDOWS = sys.platform == "win32"
if IS_WINDOWS:
    import msvcrt
else:
    import select

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
    # Di chuyển việc tạo thư mục vào trong điều kiện
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        # print(f" -> Đã tạo thư mục cache lần đầu tại: {cache_dir}")

    filename = voice_preset_name.replace("/", "_").replace("\\", "_") + ".wav" # Thêm replace cho Windows
    filepath = os.path.join(cache_dir, filename)

    if os.path.exists(filepath):
        # Thông báo này có thể không cần thiết, làm rối màn hình
        # print(f"\nĐang đọc giọng '{voice_preset_name}' từ cache") 
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
    Phát audio với thanh tiến trình, hỗ trợ đa nền tảng (Windows, macOS, Linux).
    """
    try:
        duration = len(audio_data) / sampling_rate
        sd.play(audio_data, sampling_rate, blocking=False)
        
        start_time = time.time()
        
        print(f"\n▶️  Phát giọng: {voice_name} | (Nhấn phím bất kỳ để dừng...)")
        print()

        voice_display_short = voice_name.split('-', 1)[-1].strip()
        text_label = f"Playing: {voice_display_short}"

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= duration:
                break

            # --- KIỂM TRA INPUT ĐA NỀN TẢNG ---
            key_pressed = False
            if IS_WINDOWS:
                if msvcrt.kbhit(): # Kiểm tra xem có phím nào được nhấn không
                    msvcrt.getch() # Đọc và bỏ qua phím đó
                    key_pressed = True
            else:
                if select.select([sys.stdin], [], [], 0)[0]:
                    sys.stdin.readline()
                    key_pressed = True
            
            if key_pressed:
                sd.stop()
                print("\n\n⏹️  Đã dừng phát.")
                return

            # --- TÍNH TOÁN VÀ VẼ THANH TIẾN TRÌNH ---
            try:
                terminal_width = os.get_terminal_size().columns
            except OSError:
                terminal_width = 80
            
            padding = 5
            time_info_str = f"{elapsed_time:.1f}s / {duration:.1f}s"
            
            # Tính toán không gian đã chiếm bởi các yếu tố khác
            other_elements_width = padding + len(text_label) + len(" [] ") + len(time_info_str) + padding
            
            progress_bar_width = max(10, terminal_width - other_elements_width)

            progress_percent = min(1.0, elapsed_time / duration) # Đảm bảo không vượt quá 100%
            filled_len = int(progress_bar_width * progress_percent)
            bar = PROGRESS_BAR_CHAR * filled_len + REMAINING_BAR_CHAR * (progress_bar_width - filled_len)
            
            display_line = f"{' ' * padding}{text_label} [{bar}] {time_info_str}"
            
            print(f"\r{display_line.ljust(terminal_width - 1)}", end="")

            time.sleep(0.1) # Cập nhật 10 lần/giây cho mượt mà

        # Dọn dẹp sau khi phát xong
        sd.stop()
        print("\r" + " " * (terminal_width - 1) + "\r", end="") # Xóa dòng tiến trình
        # print("✅ Hoàn tất.")
    except Exception as e:
        print(f"\n❌ Lỗi khi phát âm thanh: {e}")
        sd.stop()

def run_boxvoice(model, processor, device, sampling_rate, cache_dir_path):
    """Chạy vòng lặp menu cho Box Voice với giao diện Rich."""
    try:
        while True:
            # --- MENU CHỌN NGÔN NGỮ ---
            clear_screen()

            ascii_title = generate_centered_ascii_title("Box Voice") # Giữ lại ASCII art
            console.print(Text(ascii_title, style="bold bright_cyan")) # Tô màu cho nó
            
            voices_by_lang = {}
            for key, value in VOICE_PRESETS.items():
                lang_name = re.match(r'\d+\.\s(.*?)\s-', key).group(1)
                if lang_name not in voices_by_lang:
                    voices_by_lang[lang_name] = []
                voices_by_lang[lang_name].append(key)
            
            available_langs = list(voices_by_lang.keys())
            
            # Tạo danh sách options cho menu
            lang_options = [f"{lang} ({LANGUAGE_NATIVE_NAMES.get(VOICE_PRESETS[voices_by_lang[lang][0]]['lang'], '')})" for lang in available_langs]
            
            lang_choice = display_selection_menu("Chọn một ngôn ngữ", lang_options, color="bright_cyan", back_option="Quay lại menu chính")
            
            if lang_choice == '0': break
            if lang_choice == '00': return

            try:
                lang_choice_num = int(lang_choice)
                if not (1 <= lang_choice_num <= len(available_langs)):
                    print("\nLựa chọn không hợp lệ!"); time.sleep(1); continue
                
                selected_lang = available_langs[lang_choice_num - 1]
                voices_in_lang = voices_by_lang[selected_lang]

                # --- MENU CHỌN GIỌNG NÓI ---
                while True:
                    clear_screen()
                    ascii_title = generate_centered_ascii_title("Box Voice") # Giữ lại ASCII art
                    console.print(Text(ascii_title, style="bold bright_cyan")) # Tô màu cho nó
                    native_name = LANGUAGE_NATIVE_NAMES.get(VOICE_PRESETS[voices_in_lang[0]]['lang'], '')
                    menu_title = f"Chọn giọng nói ({selected_lang} - {native_name})"
                    
                    voice_choice = display_selection_menu(menu_title, voices_in_lang, color="bright_cyan", back_option="Quay lại menu ngôn ngữ")
                    
                    if voice_choice == '0': break
                    if voice_choice == '00': return

                    try:
                        # Logic xử lý lựa chọn giọng nói không thay đổi
                        voice_choice_num = int(voice_choice)
                        # Tìm đúng lựa chọn trong danh sách gốc
                        if 1 <= voice_choice_num <= len(voices_in_lang):
                            selected_display_name = voices_in_lang[voice_choice_num - 1]
                            selected_voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
                            
                            audio_to_play = get_audio_from_cache(selected_voice_preset, model, processor, device, sampling_rate, cache_dir=cache_dir_path)
                            play_audio_with_progress(audio_to_play, sampling_rate, selected_display_name)
                        else:
                            print("\nLựa chọn không hợp lệ!"); time.sleep(1)
                    except (ValueError, IndexError):
                        print("\nLựa chọn không hợp lệ!"); time.sleep(1)

            except ValueError:
                print("\nLựa chọn không hợp lệ!"); time.sleep(1)

    except KeyboardInterrupt:
        print("\nĐang quay lại menu chính..."); return