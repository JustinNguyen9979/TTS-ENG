import torch
import numpy as np
from transformers import AutoProcessor, BarkModel, logging as hf_logging

def load_models():
    """Tải model và processor của Bark, chỉ thực hiện một lần."""
    # Tắt các cảnh báo không cần thiết
    hf_logging.set_verbosity_error()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    # print(f"Sử dụng thiết bị: {device}")

    print("Đang tải mô hình TTS...")
    processor = AutoProcessor.from_pretrained("suno/bark")
    model = BarkModel.from_pretrained("suno/bark").to(device)
    sampling_rate = model.generation_config.sample_rate
    
    return model, processor, device, sampling_rate

def generate_audio_chunk(text, voice_preset, model, processor, device, speed=1.0, cfg_strength=2.0):
    """
    Tạo ra một mẩu âm thanh từ văn bản và giọng nói cho trước.
    Phiên bản này được nâng cấp để hỗ trợ tùy chỉnh Tốc độ (Speed).
    """
    inputs = processor(
        text=text,
        voice_preset=voice_preset,
        return_tensors="pt"
    ).to(device)

    # Thêm tham số điều khiển tốc độ vào lệnh generate
    # Tham số `length_penalty` là cách phổ biến để kiểm soát tốc độ trong các model của Hugging Face
    # speed > 1.0 -> nhanh hơn -> length_penalty < 1.0
    # speed < 1.0 -> chậm hơn -> length_penalty > 1.0
    with torch.inference_mode():
        speech_output = model.generate(
            **inputs, 
            do_sample=True,
            length_penalty=1.0 / speed if speed > 0 else 1.0 # <-- DÒNG MỚI ĐƯỢC THÊM
        )
    
    return speech_output.squeeze().cpu().numpy()