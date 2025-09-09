# hardware_check.py

import torch
import os
from ui import clear_screen, generate_centered_ascii_title

def clear_screen():
    """Xóa màn hình terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def run_hardware_check():
    """
    Kiểm tra và hiển thị thông tin về CPU/GPU mà PyTorch đang sử dụng.
    Đây là hàm duy nhất được export từ module này.
    """
    clear_screen()
    print(generate_centered_ascii_title("HARDWARE CHECK"))
    print(f"Phiên bản PyTorch: {torch.__version__}")
    
    # Kiểm tra cho GPU NVIDIA (CUDA)
    is_cuda_available = torch.cuda.is_available()
    print(f"\n[NVIDIA GPU]")
    print(f"Hỗ trợ CUDA: {is_cuda_available}")
    if is_cuda_available:
        gpu_count = torch.cuda.device_count()
        print(f"Số lượng GPU tìm thấy: {gpu_count}")
        for i in range(gpu_count):
            print(f"  - GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print(" -> Không tìm thấy GPU NVIDIA hoặc PyTorch chưa được cài đặt với hỗ trợ CUDA.")

    # Kiểm tra cho GPU Apple (MPS)
    is_mps_available = torch.backends.mps.is_available()
    print(f"\n[APPLE GPU]")
    print(f"Hỗ trợ MPS (Apple Silicon): {is_mps_available}")
    if not is_mps_available:
        print(" -> Đây không phải là máy Mac với chip Apple Silicon hoặc PyTorch chưa hỗ trợ.")

    # Xác định thiết bị sẽ được sử dụng bởi các module khác
    device = "cpu"
    if is_cuda_available:
        device = "cuda"
    elif is_mps_available:
        device = "mps"
    
    result_text = f">>> THIẾT BỊ SẼ ĐƯỢC ƯU TIÊN SỬ DỤNG: {device.upper()} <<<"
    
    line_length = len(result_text)
    dash_line = "-" * line_length

    print(f"\n{dash_line}")
    print(result_text)
    print(dash_line)

    input("\nNhấn Enter để quay lại menu chính...")