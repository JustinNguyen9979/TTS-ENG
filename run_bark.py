import torch
from transformers import AutoProcessor, BarkModel
from scipy.io.wavfile import write
import sys
import os
import shutil
import re
import numpy as np

# --- HÀM DỌN DẸP TỰ ĐỘNG (Đã tối ưu) ---
def cleanup_project_directory():
    """
    Tìm và xóa các thư mục __pycache__ và các file .wav cũ,
    sau đó báo cáo tổng dung lượng đã dọn dẹp.
    """
    project_dir = os.path.dirname(os.path.abspath(__file__))
    total_deleted_size = 0
    
    for root, dirs, files in os.walk(project_dir, topdown=False):
        for name in files:
            if name.endswith(".wav"):
                file_path = os.path.join(root, name)
                try:
                    total_deleted_size += os.path.getsize(file_path)
                    os.remove(file_path)
                except OSError: pass
        for name in dirs:
            if name == "__pycache__":
                dir_path = os.path.join(root, name)
                try:
                    dir_size = sum(os.path.getsize(os.path.join(dir_path, f)) for f in os.listdir(dir_path))
                    total_deleted_size += dir_size
                    shutil.rmtree(dir_path)
                except (OSError, FileNotFoundError): pass
    
    if total_deleted_size > 0:
        deleted_mb = total_deleted_size / (1024 * 1024)
        print(f"--- Đã giải phóng {deleted_mb:.2f} MB dung lượng. ---")

# --- PHẦN 1: HÀM CHÍNH CỦA CHƯƠNG TRÌNH ---
def main():
    # 1.1: ĐỌC FILE INPUT
    if len(sys.argv) < 2:
        print("Lỗi: Bạn chưa cung cấp file text đầu vào.")
        print("Cách dùng: python3 run_bark.py ten_file_cua_ban.txt")
        sys.exit(1)
    input_file_path = sys.argv[1]
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()
            print(f"Đã đọc thành công nội dung từ file: {input_file_path}")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file có tên '{input_file_path}'.")
        sys.exit(1)

    # 1.2: CÀI ĐẶT THIẾT BỊ
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
        torch.set_float32_matmul_precision('high')
    print(f"Sử dụng thiết bị: {device}")

    # 1.3: TẢI MODEL VÀ PROCESSOR
    print("Đang tải mô hình suno/bark...")
    processor = AutoProcessor.from_pretrained("suno/bark")
    model = BarkModel.from_pretrained("suno/bark").to(device)
    sampling_rate = model.generation_config.sample_rate

    # 1.4: CHIA VĂN BẢN THÀNH CÁC CÂU
    text_normalized = full_text.replace('\n', ' ').strip()
    sentences = re.split(r'(?<=[.?!])\s+', text_normalized)
    
    # 1.5: TẠO ÂM THANH THEO LOGIC ỔN ĐỊNH NHẤT
    print("Bắt đầu quá trình tạo âm thanh theo từng câu...")
    
    # CHỌN GIỌNG NÓI DUY NHẤT. Giọng nói này sẽ được dùng cho TẤT CẢ các câu.
    # Gợi ý: "v2/en_speaker_6" (nam trầm), "v2/en_speaker_9" (nữ trầm), "v2/en_speaker_2" (nữ cao)
    voice_preset = "v2/en_speaker_6"
    print(f"Sử dụng giọng nói cố định: {voice_preset}")
    
    pieces = [] # Danh sách để lưu các mảng âm thanh của từng câu
    
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue
            
        print(f"  Đang xử lý câu {i+1}/{len(sentences)}: '{sentence[:70]}...'")
        
        # Luôn sử dụng cùng một voice_preset để đảm bảo chất giọng nhất quán
        inputs = processor(text=sentence, voice_preset=voice_preset, return_tensors="pt").to(device)

        # Sử dụng inference_mode để tối ưu hóa, không cần các tham số phức tạp
        with torch.inference_mode():
            speech_output = model.generate(**inputs, do_sample=True)
        
        audio_array = speech_output.squeeze().cpu().numpy()
        pieces.append(audio_array)

    # 1.6: GHÉP CÁC MẢNH ÂM THANH VÀ LƯU FILE
    print("Đang ghép các file âm thanh...")
    final_audio_data = np.concatenate(pieces)
    
    base_name = os.path.splitext(os.path.basename(input_file_path))[0]
    output_file = f"{base_name}_bark_podcast_output.wav"
    
    write(output_file, rate=sampling_rate, data=final_audio_data)

    print("-" * 60)
    print(f"✅ Hoàn tất! Đã lưu file âm thanh thành công tại: {output_file}")
    print("Đã áp dụng phương pháp xử lý theo câu với giọng nói cố định để có kết quả ổn định.")
    print("-" * 60)

# --- PHẦN 2: ĐIỂM BẮT ĐẦU CỦA SCRIPT ---
if __name__ == "__main__":
    cleanup_project_directory()
    main()