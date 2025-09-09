# tts_utils.py

import torch
from transformers import AutoProcessor, BarkModel, logging as hf_logging

def load_models():
    """Tải model và processor của Bark, chỉ thực hiện một lần."""
    # Tắt các cảnh báo không cần thiết
    hf_logging.set_verbosity_error()

    # Cài đặt thiết bị
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    # print(f"Sử dụng thiết bị: {device}")

    print("Đang tải mô hình TTS...")
    processor = AutoProcessor.from_pretrained("suno/bark")
    model = BarkModel.from_pretrained("suno/bark").to(device)
    sampling_rate = model.generation_config.sample_rate
    
    return model, processor, device, sampling_rate

def generate_audio_chunk(text, voice_preset, model, processor, device):
    """Tạo ra một mẩu âm thanh từ văn bản và giọng nói cho trước."""
    inputs = processor(
        text=text,
        voice_preset=voice_preset,
        return_tensors="pt"
    ).to(device)

    with torch.inference_mode():
        speech_output = model.generate(**inputs, do_sample=True)
    
    return speech_output.squeeze().cpu().numpy()