import torch
from transformers import AutoProcessor, VitsModel
import sys
import os
import re
from pydub import AudioSegment
import numpy as np
import shutil

# --- HÀM DỌN DẸP TỰ ĐỘNG ---
def cleanup_project_directory():
    """Tìm và xóa các thư mục __pycache__ và các file .wav cũ."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    print("--- BẮT ĐẦU QUÁ TRÌNH DỌN DẸP TỰ ĐỘNG ---")
    for root, dirs, files in os.walk(project_dir, topdown=False):
        for name in files:
            if name.endswith(".wav"):
                try: os.remove(os.path.join(root, name))
                except OSError: pass
        for name in dirs:
            if name == "__pycache__":
                try: shutil.rmtree(os.path.join(root, name))
                except OSError: pass
    print("--- KẾT THÚC DỌN DẸP ---")

# --- HÀM TẠO ÂM THANH ---
def generate_audio_segment(text, model, processor, sampling_rate):
    """Tạo âm thanh cho một khối văn bản và trả về dưới dạng AudioSegment."""
    if not text or not text.strip():
        return AudioSegment.empty()
    inputs = processor(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    audio_data_float32 = output[0].cpu().numpy()
    audio_data_int16 = (audio_data_float32 * np.iinfo(np.int16).max).astype(np.int16)
    return AudioSegment(
        audio_data_int16.tobytes(),
        frame_rate=sampling_rate,
        sample_width=audio_data_int16.dtype.itemsize,
        channels=1
    )

# --- PHẦN CHÍNH CỦA CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    # 0. DỌN DẸP
    cleanup_project_directory()

    # 1. ĐỌC FILE INPUT
    if len(sys.argv) < 2:
        print("Cách dùng: python3 tts.py ten_file_cua_ban.txt")
        sys.exit(1)
    input_file_path = sys.argv[1]
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{input_file_path}'.")
        sys.exit(1)

    # 2. TẢI MODEL
    print("Đang tải mô hình facebook/mms-tts-vie...")
    model_id = "facebook/mms-tts-vie"
    processor = AutoProcessor.from_pretrained(model_id)
    model = VitsModel.from_pretrained(model_id)
    sampling_rate = model.config.sampling_rate

    # 3. CHIA VĂN BẢN THEO CÂU HOÀN CHỈNH - CHIẾN LƯỢC TỐI ƯU
    print("Đang xử lý văn bản theo từng câu để tối ưu hóa sự nhất quán...")
    # Chuẩn hóa văn bản: thay thế xuống dòng bằng dấu cách
    text_normalized = full_text.replace('\n', ' ').strip()
    # Tách văn bản thành các câu dựa vào dấu chấm, hỏi, than
    sentences = re.split(r'(?<=[.?!])\s+', text_normalized)
    
    # Định nghĩa khoảng nghỉ duy nhất và quan trọng nhất: giữa các câu
    pause_between_sentences = AudioSegment.silent(duration=700) # Bạn có thể tùy chỉnh
    final_audio = AudioSegment.empty()

    # 4. TẠO ÂM THANH CHO TỪNG CÂU HOÀN CHỈNH
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue
            
        print(f"Đang xử lý câu {i+1}/{len(sentences)}: '{sentence[:70]}...'")
        
        # Tạo âm thanh cho CẢ CÂU. Mô hình sẽ tự xử lý dấu phẩy bên trong.
        sentence_audio = generate_audio_segment(sentence, model, processor, sampling_rate)
        final_audio += sentence_audio
        
        # Thêm khoảng nghỉ tùy chỉnh sau mỗi câu
        # Kiểm tra để không thêm khoảng nghỉ sau câu cuối cùng
        if i < len(sentences) - 1:
            final_audio += pause_between_sentences

    # 5. LƯU FILE ÂM THANH CUỐI CÙNG
    base_name = os.path.splitext(os.path.basename(input_file_path))[0]
    output_file = f"{base_name}_final_output.wav"
    
    print(f"Đang xuất file âm thanh hoàn chỉnh...")
    final_audio.export(output_file, format="wav")
    print("-" * 30)
    print(f"✅ Hoàn tất! Đã lưu file âm thanh tại: {output_file}")
    print("Đã áp dụng phương pháp xử lý theo câu để cân bằng giữa sự nhất quán và ngắt nghỉ.")
    print("-" * 30)