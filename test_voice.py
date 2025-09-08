import torch
from transformers import AutoProcessor, BarkModel
import sounddevice as sd # Thư viện để phát âm thanh trực tiếp
import numpy as np

# ==============================================================================
# --- KHU VỰC TÙY CHỈNH ---
# Bạn chỉ cần thay đổi nội dung trong khu vực này để thử nghiệm

# 1. ĐOẠN VĂN BẢN BẠN MUỐN NGHE THỬ
# Hãy giữ nó ngắn (1-2 câu) để quá trình tạo âm thanh nhanh hơn.
text_to_speak = "Hello, my name is Bark. I can generate realistic speech, music, and sound effects. How do you like my voice?"

# 2. DANH SÁCH CÁC GIỌNG NÓI BẠN MUỐN THỬ
# Thêm hoặc xóa các giọng nói trong danh sách này.
# Bạn có thể tìm thêm tên các giọng nói khác trên trang Hugging Face của suno/bark.
voices_to_test = [
    "v2/en_speaker_6", # Nam, giọng trầm (phổ biến)
    "v2/en_speaker_9", # Nữ, giọng trầm
    "v2/en_speaker_2", # Nữ, giọng cao hơn
    "v2/en_speaker_1", # Nam, giọng trung
    "v2/fr_speaker_5", # Thử giọng Pháp nói tiếng Anh
    "v2/ja_speaker_3", # Thử giọng Nhật nói tiếng Anh
]
# ==============================================================================


def main():
    """
    Hàm chính để tải model và lặp qua các giọng nói để nghe thử.
    """
    # Cài đặt thiết bị
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
        torch.set_float32_matmul_precision('high')
    print(f"Sử dụng thiết bị: {device}")

    # Tải model và processor (chỉ một lần)
    print("Đang tải mô hình suno/bark (lần đầu có thể mất vài phút)...")
    processor = AutoProcessor.from_pretrained("suno/bark")
    model = BarkModel.from_pretrained("suno/bark").to(device)
    sampling_rate = model.generation_config.sample_rate
    
    print("\n--- Bắt đầu quá trình nghe thử ---")
    print(f"Văn bản mẫu: '{text_to_speak}'")

    # Lặp qua từng giọng nói trong danh sách để thử
    for voice_preset in voices_to_test:
        print("-" * 40)
        print(f"Đang tạo âm thanh cho giọng: {voice_preset}...")

        # Xử lý văn bản với giọng nói đã chọn
        inputs = processor(text=text_to_speak, voice_preset=voice_preset, return_tensors="pt").to(device)

        # Tạo âm thanh
        with torch.inference_mode():
            speech_output = model.generate(**inputs, do_sample=True)
        
        audio_array = speech_output.squeeze().cpu().numpy()
        
        # Phát âm thanh trực tiếp qua loa
        print(" -> Đang phát âm thanh...")
        sd.play(audio_array, sampling_rate)
        
        # Chờ cho đến khi âm thanh phát xong
        sd.wait()

    print("-" * 40)
    print("✅ Đã nghe thử xong tất cả các giọng nói!")


# Điểm bắt đầu của script
if __name__ == "__main__":
    main()