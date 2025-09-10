import torch
import os
import psutil
from cpuinfo import get_cpu_info
from config import MIN_RAM_GB, MIN_VRAM_GB
from ui import generate_centered_ascii_title, clear_screen

try:
    import pynvml
    NVML_AVAILABLE = True
except ImportError:
    NVML_AVAILABLE = False

def get_system_specs():
    specs = {}
    cpu_info = get_cpu_info()
    specs['cpu_model'] = cpu_info.get('brand_raw', 'Không xác định')
    specs['cpu_cores'] = psutil.cpu_count(logical=True)
    mem = psutil.virtual_memory()
    specs['ram_total_gb'] = round(mem.total / (1024**3), 2)
    specs['ram_available_gb'] = round(mem.available / (1024**3), 2)
    specs['gpu_model'] = "Không có"
    specs['gpu_vram_total_gb'] = 0
    specs['compute_platform'] = "CPU"
    specs['active_device'] = "cpu"
    if torch.cuda.is_available():
        specs['active_device'] = "cuda"
        specs['compute_platform'] = f"NVIDIA CUDA v{torch.version.cuda}"
        if NVML_AVAILABLE:
            try:
                pynvml.nvmlInit()
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                specs['gpu_model'] = pynvml.nvmlDeviceGetName(handle)
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                specs['gpu_vram_total_gb'] = round(mem_info.total / (1024**3), 2)
                pynvml.nvmlShutdown()
            except Exception:
                specs['gpu_model'] = torch.cuda.get_device_name(0)
                specs['gpu_vram_total_gb'] = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
        else:
            specs['gpu_model'] = torch.cuda.get_device_name(0)
            specs['gpu_vram_total_gb'] = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
    elif torch.backends.mps.is_available():
        specs['active_device'] = "mps"
        specs['compute_platform'] = "Apple Metal (MPS)"
        specs['gpu_model'] = "Apple Silicon (Unified Memory)"
        specs['gpu_vram_total_gb'] = specs['ram_total_gb']
    return specs

def evaluate_specs(specs):
    failure_reasons = []
    if specs['ram_total_gb'] < MIN_RAM_GB:
        failure_reasons.append(f"- RAM hệ thống ({specs['ram_total_gb']}GB) thấp hơn yêu cầu ({MIN_RAM_GB}GB).")
    if specs['compute_platform'].startswith("NVIDIA CUDA"):
        if specs['gpu_vram_total_gb'] < MIN_VRAM_GB:
            failure_reasons.append(f"- VRAM của GPU ({specs['gpu_vram_total_gb']}GB) thấp hơn yêu cầu ({MIN_VRAM_GB}GB).")
    return not failure_reasons, failure_reasons

def run_hardware_check():
    """Hàm chính để chạy toàn bộ quy trình kiểm tra và hiển thị."""
    clear_screen()
    print(generate_centered_ascii_title("Hardware Check", font='small'))
    
    specs = get_system_specs()
    is_sufficient, reasons = evaluate_specs(specs)
    
    info_data = [
        ('CPU', f"{specs['cpu_model']} ({specs['cpu_cores']} cores)"),
        ('RAM', f"{specs['ram_total_gb']} GB (Khả dụng: {specs['ram_available_gb']} GB)"),
        ('GPU', f"{specs['gpu_model']}")
    ]
    if specs['compute_platform'] != "CPU":
        info_data.append(('VRAM', f"{specs['gpu_vram_total_gb']} GB"))
        info_data.append(('Nền tảng', f"{specs['compute_platform']}"))

    label_width = max(len(label) for label, value in info_data)

    formatted_lines = [f"{label.ljust(label_width)} : {value}" for label, value in info_data]
    
    max_line_length = max(len(line) for line in formatted_lines)
    title = "--- THÔNG TIN HỆ THỐNG ---"
    box_width = max(max_line_length, len(title))
    
    dash_line = "-" * (box_width + 4) 

    print(f"\n{dash_line}")
    print(title.center(len(dash_line)))
    for line in formatted_lines:
        # In mỗi dòng với 2 khoảng trắng đệm ở bên trái
        print(f"\n  {line}")
    print(dash_line)
    
    print(f"\n➡️ Chương trình ưu tiên sử dụng: {specs['active_device'].upper()}")

    if is_sufficient:
        result_text = ">>> MÁY TÍNH ĐỦ ĐIỀU KIỆN <<<"
    else:
        result_text = ">>> MÁY TÍNH KHÔNG ĐỦ ĐIỀU KIỆN <<<"
        
    result_line_length = len(result_text)
    result_dash_line = "-" * result_line_length
    
    print(f"\n{result_dash_line}")
    print(result_text)
    print(result_dash_line)
    
    if not is_sufficient:
        print("\nLý do:")
        for reason in reasons:
            print(reason)
        print("\n*Lưu ý: Chương trình vẫn có thể chạy nhưng sẽ rất chậm hoặc gặp lỗi bộ nhớ.")

    input("\nNhấn Enter để quay lại menu chính...")