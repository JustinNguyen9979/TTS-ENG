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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_audio_from_cache(voice_preset_name, model, processor, device, sampling_rate):
    """Kiểm tra cache. Nếu có file thì đọc, nếu không thì tạo mới."""
    filename = voice_preset_name.replace("/", "_") + ".wav"
    filepath = os.path.join(CACHE_DIR, filename)

    if os.path.exists(filepath):
        # print(f"\nĐang đọc giọng: {filepath}")
        rate, audio_data = read(filepath)
        return audio_data
    
    selected_voice_info = next(item for item in VOICE_PRESETS.values() if item["preset"] == voice_preset_name)
    lang_code = selected_voice_info["lang"]
    text_to_speak = TEXT_SAMPLES.get(lang_code, TEXT_SAMPLES["en"])
    
    with tqdm(total=1, desc=f"Đang tạo giọng '{voice_preset_name}'") as pbar:
        audio_array = generate_audio_chunk(text_to_speak, voice_preset_name, model, processor, device)
        pbar.update(1)

    write(filepath, sampling_rate, audio_array)
    print(f"\nĐã tạo và lưu file vào cache: {filepath}")
    
    return audio_array

def run_jukebox(model, processor, device, sampling_rate):
    """Chạy vòng lặp menu cho chức năng Jukebox."""
    try:
        while True:
            clear_screen()
            print(generate_centered_ascii_title("Box Voice"))
            print("Chọn một giọng nói để nghe thử:")
            
            for display_name in VOICE_PRESETS.keys():
                print(f"  {display_name}")
            
            # NÂNG CẤP: Thêm tùy chọn thoát rõ ràng
            print("  0. Quay lại menu chính")
            # print("\nNhấn (Ctrl + C) cũng sẽ quay lại menu chính.")
            
            # NÂNG CẤP: Cập nhật gợi ý input
            choice = input("\nNhập lựa chọn của bạn (0 để quay lại): ")

            # NÂNG CẤP: Ưu tiên xử lý lựa chọn thoát
            if choice == '0':
                print("Đang quay lại menu chính...")
                break # Thoát khỏi vòng lặp while và kết thúc hàm run_jukebox

            try:
                choice_num = int(choice)
                # NÂNG CẤP: Kiểm tra lựa chọn nằm trong phạm vi hợp lệ
                if 1 <= choice_num <= len(VOICE_PRESETS):
                    selected_display_name = list(VOICE_PRESETS.keys())[choice_num - 1]
                    selected_voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
                    
                    audio_to_play = get_audio_from_cache(selected_voice_preset, model, processor, device, sampling_rate)
                    
                    print(f"\nĐang phát giọng: {selected_display_name}...")
                    sd.play(audio_to_play, sampling_rate)
                    sd.wait()
                    time.sleep(1)
                else:
                    print("\nLựa chọn không hợp lệ! Vui lòng chọn một số trong danh sách.")
                    time.sleep(1.5)

            except ValueError:
                # Nếu người dùng nhập chữ
                print("\nLựa chọn không hợp lệ! Vui lòng chỉ nhập số.")
                time.sleep(1.5)

    except KeyboardInterrupt:
        print("\nĐang quay lại menu chính...")
        return