import torch
import psutil

from cpuinfo import get_cpu_info
from .config import MIN_RAM_GB, MIN_VRAM_GB
from .ui import clear_screen, print_info_box, print_highlight_box
from rich.console import Console 
from rich.text import Text
from rich.align import Align

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
    """Chạy quy trình kiểm tra và hiển thị bằng box thông tin chung."""
    clear_screen()
    
    specs = get_system_specs()
    is_sufficient, reasons = evaluate_specs(specs)
    
    # Chuẩn bị dữ liệu cho box
    system_data = [
        ('CPU', f"{specs['cpu_model']} ({specs['cpu_cores']} cores)"),
        ('RAM', f"{specs['ram_total_gb']} GB (Khả dụng: {specs['ram_available_gb']} GB)"),
        ('GPU', f"{specs['gpu_model']}")
    ]
    if specs['compute_platform'] != "CPU":
        system_data.append(('VRAM', f"{specs['gpu_vram_total_gb']} GB"))
        system_data.append(('Nền tảng', f"{specs['compute_platform']}"))

    # Tạo cấu trúc sections
    sections = {
        "Thông tin hệ thống": system_data
    }
    
    # Gọi hàm để vẽ box
    print_info_box("Hardware Check", sections)
    
    # In kết quả kiểm tra
    device_line = f"Ưu tiên sử dụng: {specs['active_device'].upper()}"
    
    if is_sufficient:
        status_line = "HỆ THỐNG ĐỦ ĐIỀU KIỆN"
        print_highlight_box([device_line, status_line], status='success')
    else:
        status_line = "HỆ THỐNG CÓ THỂ KHÔNG ĐỦ ĐIỀU KIỆN"
        print_highlight_box([device_line, status_line], status='warning')
        
        # In các lý do bên ngoài hộp (có thể tạo một Panel khác cho nó nếu muốn)
        reasons_text = Text("\nLý do:\n", style="bold red")
        for reason in reasons:
            reasons_text.append(f" {reason}\n")
        reasons_text.append("\n*Lưu ý: Chương trình vẫn có thể chạy nhưng sẽ rất chậm hoặc gặp lỗi bộ nhớ.")
        Console.print(Align.center(reasons_text))

    input("\nNhấn Enter để quay lại menu chính...")