import torch
from transformers import AutoProcessor, BarkModel, logging as hf_logging # NÂNG CẤP: Import module logging
from scipy.io.wavfile import write, read
import sounddevice as sd
import numpy as np
import sys
import os
import shutil
from tqdm import tqdm

# ==============================================================================
# --- KHU VỰC TÙY CHỈNH ---

# 1. CÁC ĐOẠN VĂN BẢN MẪU THEO TỪNG NGÔN NGỮ
# Điều này đảm bảo chúng ta nghe được chất giọng chuẩn nhất.
TEXT_SAMPLES = {
    "en": "A very warm welcome to you! It is a genuine pleasure to have you with us today. I sincerely hope you've been having a wonderful day so far and that the rest of your time here is enjoyable and productive.",
    "fr": "Bonjour et bienvenue ! Je suis absolument ravi(e) de vous accueillir parmi nous. J'espère sincèrement que votre journée se déroule bien jusqu'à présent et je vous souhaite de passer un excellent moment en notre compagnie. Comment allez-vous ?",
    "ja": "はじめまして。本日はようこそお越しくださいました。皆様にお会いできて大変光栄に存じます。これから素晴らしい時間を共に過ごせることを心より楽しみにしております。どうぞ、よろしくお願いいたします。",
    "zh": "大家好！非常欢迎各位的光临，我们在此怀着无比激动的心情迎接您的到来。希望您旅途顺利，并能在这里度过一段愉快而难忘的时光。我们期待与您共创美好回忆。",
    # Thêm các ngôn ngữ khác nếu muốn
}

# 2. DANH SÁCH CÁC GIỌNG NÓI ĐỂ HIỂN THỊ TRONG MENU
# Mỗi giọng nói bây giờ sẽ có thêm mã ngôn ngữ ('lang')
VOICE_PRESETS = {
    "1. English - Male, Deep (Phổ biến)": {"preset": "v2/en_speaker_6", "lang": "en"},
    "2. English - Female, Deep": {"preset": "v2/en_speaker_9", "lang": "en"},
    "3. English - Male, Higher": {"preset": "v2/en_speaker_2", "lang": "en"},
    "4. French - Female": {"preset": "v2/fr_speaker_5", "lang": "en"}, # Giọng Pháp nói tiếng Anh
    "5. Japanese - Female": {"preset": "v2/ja_speaker_3", "lang": "ja"}, # Giọng Nhật nói tiếng Nhật
    "6. Chinese - Male": {"preset": "v2/zh_speaker_5", "lang": "zh"}, # Giọng TQ nói tiếng TQ
    "7. Chinese - Female": {"preset": "v2/zh_speaker_2", "lang": "zh"},
}

# 3. TÊN THƯ MỤC CACHE
CACHE_DIR = "audio_cache"
# ==============================================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_audio_from_cache(voice_preset_name, model, processor, device, sampling_rate):
    """
    Kiểm tra cache. Nếu có file thì đọc, nếu không thì tạo mới với thanh trạng thái.
    """
    filename = voice_preset_name.replace("/", "_") + ".wav"
    filepath = os.path.join(CACHE_DIR, filename)

    if os.path.exists(filepath):
        print(f"\nĐã tìm thấy file trong cache. Đang đọc: {filepath}")
        rate, audio_data = read(filepath)
        return audio_data
    
    selected_voice_info = next(item for item in VOICE_PRESETS.values() if item["preset"] == voice_preset_name)
    lang_code = selected_voice_info["lang"]
    text_to_speak = TEXT_SAMPLES.get(lang_code, TEXT_SAMPLES["en"])
    
    # Sử dụng tqdm để tạo thanh trạng thái cho cả quá trình
    with tqdm(total=1, desc=f"Đang tạo giọng '{voice_preset_name}'") as pbar:
        inputs = processor(
            text=text_to_speak,
            voice_preset=voice_preset_name,
            return_tensors="pt"
        ).to(device)

        # Tạo âm thanh trong chế độ inference để tối ưu hóa
        with torch.inference_mode():
            speech_output = model.generate(**inputs, do_sample=True)
        
        audio_array = speech_output.squeeze().cpu().numpy()
        pbar.update(1) # Cập nhật thanh trạng thái là đã hoàn thành 100%

    write(filepath, sampling_rate, audio_array)
    print(f"\nĐã tạo và lưu file vào cache: {filepath}")
    
    return audio_array

def main():
    # NÂNG CẤP: "Ra lệnh" cho thư viện transformers im lặng ngay từ đầu
    hf_logging.set_verbosity_error()

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    print(f"Sử dụng thiết bị: {device}")

    print("Đang tải mô hình suno/bark (chỉ một lần)...")
    processor = AutoProcessor.from_pretrained("suno/bark")
    model = BarkModel.from_pretrained("suno/bark").to(device)
    sampling_rate = model.generation_config.sample_rate

    try:
        while True:
            clear_screen()
            print("======= JUKEBOX GIỌNG NÓI THÔNG MINH (v5 - Hoàn Thiện) =======")
            print("Chọn một giọng nói để nghe thử:")
            for display_name in VOICE_PRESETS.keys():
                print(f"  {display_name}")
            print("\nNhấn (Ctrl + C) để thoát chương trình.")
            
            choice = input("Nhập lựa chọn của bạn: ")
            
            try:
                choice_num = int(choice)
                selected_display_name = list(VOICE_PRESETS.keys())[choice_num - 1]
                selected_voice_preset = VOICE_PRESETS[selected_display_name]["preset"]
                
                audio_to_play = get_audio_from_cache(selected_voice_preset, model, processor, device, sampling_rate)
                
                print(f"\nĐang phát giọng: {selected_display_name}...")
                sd.play(audio_to_play, sampling_rate)
                sd.wait()
            except (ValueError, IndexError):
                print("\nLựa chọn không hợp lệ!")
            
            input("\nNhấn Enter để quay lại menu...")

    except KeyboardInterrupt:
        print("\n\nCảm ơn đã sử dụng. Tạm biệt!")
        sys.exit(0)

# Điểm bắt đầu của script
if __name__ == "__main__":
    # Hàm dọn dẹp không cần thiết cho script này, bạn có thể thêm lại nếu muốn
    # cleanup_project_directory()
    main()