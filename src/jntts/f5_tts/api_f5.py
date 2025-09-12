import random
import sys
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

import soundfile as sf
from tqdm import tqdm
from cached_path import cached_path
from omegaconf import OmegaConf

from .infer.utils_infer import (
    load_model,
    load_vocoder,
    transcribe,
    preprocess_ref_audio_text,
    infer_process,
    remove_silence_for_generated_wav,
    save_spectrogram,
)
from .model import DiT, UNetT
from .model.utils import seed_everything


class F5TTS:
    def __init__(
        self,
        model="F5TTS_v1_Base",
        ckpt_file="",
        ode_method="euler",
        use_ema=True,
        vocoder_local_path=None,
        device=None,
        hf_cache_dir=None,
    ):
        # --- BƯỚC 1: TÌM ĐƯỜNG DẪN ĐẾN CÁC FILE CẤU HÌNH BÊN TRONG GÓI ---

        package_root = files("jntts.f5_tts")
        
        # Đường dẫn đến file config .yaml
        config_path = str(package_root.joinpath(f"configs/{model}.yaml"))
        # Đường dẫn đến file vocab .txt (đã Việt hóa)
        vocab_path = str(package_root.joinpath("assets/vocab.txt"))

        # --- BƯỚC 2: TẢI CẤU HÌNH VÀ XÂY DỰNG KIẾN TRÚC MODEL ---
        # print(f"Đang tải cấu hình từ: {config_path}")
        model_cfg = OmegaConf.load(config_path)
        model_cls = globals()[model_cfg.model.backbone]
        model_arc = model_cfg.model.arch

        self.mel_spec_type = model_cfg.model.mel_spec.mel_spec_type
        self.target_sample_rate = model_cfg.model.mel_spec.target_sample_rate
        self.ode_method = ode_method
        self.use_ema = use_ema

        # --- BƯỚC 3: CÀI ĐẶT THIẾT BỊ VÀ TẢI VOCODER (bộ giải mã âm thanh) ---
        if device is not None:
            self.device = device
        else:
            import torch
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            if torch.backends.mps.is_available(): self.device = "mps"
        
        self.vocoder = load_vocoder(
            self.mel_spec_type, vocoder_local_path is not None, vocoder_local_path, self.device, hf_cache_dir
        )

        # --- BƯỚC 4: TÌM ĐƯỜNG DẪN ĐẾN CHECKPOINT (trọng số đã huấn luyện) ---
        repo_name, ckpt_step, ckpt_type = "SWivid/F5-TTS", 1250000, "safetensors"

        # Tự động tải checkpoint từ Hugging Face Hub nếu chưa được cung cấp
        if not ckpt_file:
            ckpt_file = str(
                cached_path(f"hf://{repo_name}/{model}/model_{ckpt_step}.{ckpt_type}", cache_dir=hf_cache_dir)
            )

        # --- BƯỚC 5: TẢI MODEL CHÍNH VỚI VOCAB ĐÃ VIỆT HÓA ---
        # print(f"Sử dụng từ điển (vocab) tại: {vocab_path}")
        self.ema_model = load_model(
            model_cls, 
            model_arc, 
            ckpt_file, 
            self.mel_spec_type, 
            vocab_path, 
            self.ode_method, 
            self.use_ema, 
            self.device
        )

    def transcribe(self, ref_audio, language=None):
        return transcribe(ref_audio, language)

    def export_wav(self, wav, file_wave, remove_silence=False):
        sf.write(file_wave, wav, self.target_sample_rate)
        if remove_silence:
            remove_silence_for_generated_wav(file_wave)

    def export_spectrogram(self, spec, file_spec):
        save_spectrogram(spec, file_spec)

    def infer(
        self,
        ref_file,
        ref_text,
        gen_text,
        show_info=print,
        progress=tqdm,
        target_rms=0.1,
        cross_fade_duration=0.15,
        sway_sampling_coef=-1,
        cfg_strength=2,
        nfe_step=32,
        speed=1.0,
        fix_duration=None,
        remove_silence=False,
        file_wave=None,
        file_spec=None,
        seed=None,
    ):
        if seed is None:
            self.seed = random.randint(0, sys.maxsize)
        seed_everything(self.seed)

        if progress is None:
            from tqdm import tqdm as progress_bar_class
            progress = progress_bar_class

        ref_file, ref_text = preprocess_ref_audio_text(ref_file, ref_text, device=self.device)
        wav, sr, spec = infer_process(
            ref_file, ref_text, gen_text, self.ema_model, self.vocoder, self.mel_spec_type, show_info=show_info,
            progress=progress, target_rms=target_rms, cross_fade_duration=cross_fade_duration, nfe_step=nfe_step,
            cfg_strength=cfg_strength, sway_sampling_coef=sway_sampling_coef, speed=speed, fix_duration=fix_duration,
            device=self.device,
        )
        if file_wave is not None:
            self.export_wav(wav, file_wave, remove_silence)

        if file_spec is not None:
            self.export_spectrogram(spec, file_spec)

        return wav, sr, spec