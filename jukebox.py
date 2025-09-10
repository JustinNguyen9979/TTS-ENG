# jukebox.py

import os
import sys
from scipy.io.wavfile import write, read
import sounddevice as sd
from config import VOICE_PRESETS, TEXT_SAMPLES, CACHE_DIR
from tts_utils import generate_audio_chunk
from tqdm import tqdm
import time
from ui import clear_screen, generate_centered_ascii_title
import re

# NÂNG CẤP: HÀM VẼ MENU DẠNG CỘT ĐÃ ĐƯỢC CẢI TIẾN
def display_voice_menu_grid(presets):
    """
    Hiển thị danh sách giọng nói dưới dạng lưới (grid) co giãn theo chiều rộng terminal,
    với các tiêu đề ngôn ngữ được định dạng đẹp mắt.
    """
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
        # NÂNG CẤP: Logic tạo tiêu đề động
        # 1. Tạo văn bản tiêu đề với khoảng trắng đệm hai bên
        header_text = f" {lang.upper()} "
        # 2. Sử dụng .center() để căn giữa và lấp đầy bằng dấu '-'
        full_header_line = header_text.center(terminal_width, '-')
        print(f"\n{full_header_line}")
        
        if not voices: continue
        max_len = max(len(v) for v in voices) + 4

        num_columns = max(1, terminal_width // max_len)
        
        for i in range(0, len(voices), num_columns):
            row_items = voices[i:i + num_columns]
            print("".join(item.ljust(max_len) for item in row_items))

def get_audio_from_cache(voice_preset_name, model, processor, device, sampling_rate):
    # ... (Hàm này giữ nguyên, không cần thay đổi) ...
    filename = voice_preset_name.replace("/", "_") + ".wav"
    filepath = os.path.join(CACHE_DIR, filename)
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
    print(f"\nĐã tạo audio: {filepath}")
    return audio_array

def run_jukebox(model, processor, device, sampling_rate):
    """Chạy vòng lặp menu cho chức năng Jukebox."""
    try:
        while True:
            clear_screen()
            print(generate_centered_ascii_title("Jukebox", font='small'))
            
            display_voice_menu_grid(VOICE_PRESETS)
            
            print("\n  0. Quay lại menu chính")
            print("\nNhấn (Ctrl + C) cũng sẽ quay lại menu chính.")
            
            choice = input("\nNhập lựa chọn của bạn (0 để quay lại): ")

            if choice == '0': break

            try:
                choice_num = int(choice)
                selected_display_name = next((key for key in VOICE_PRESETS.keys() if key.startswith(f"{choice_num}. ")), None)

                if selected_display_name:
                    selected_voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
                    audio_to_play = get_audio_from_cache(selected_voice_preset, model, processor, device, sampling_rate)
                    print(f"\nĐang phát giọng: {selected_display_name}")
                    sd.play(audio_to_play, sampling_rate)
                    sd.wait()
                    # print("...Phát xong.")
                    # time.sleep(1)
                else:
                    print("\nLựa chọn không hợp lệ!")
                    time.sleep(1.5)
            except ValueError:
                print("\nLựa chọn không hợp lệ! Vui lòng chỉ nhập số.")
                time.sleep(1.5)

    except KeyboardInterrupt:
        print("\nĐang quay lại menu chính...")
        return