---
title: "SKILL"
name: video-storytelling-pipeline
description: Pipeline tự động chuyển ảnh minh họa + kịch bản thành video storytelling có lồng tiếng AI (VieNeu-TTS + FFmpeg Ken Burns). Triggers on "tạo video", "storytelling", "video từ ảnh", "lồng tiếng", "VieNeu", "Ken Burns", "animation từ ảnh".
---

# Video Storytelling Pipeline

## Tổng Quan
Tự động chuyển ảnh minh họa + kịch bản text → video storytelling có lồng tiếng AI đa nhân vật.

**Stack**: VieNeu-TTS (voice) + FFmpeg (animation + compose) + Python (orchestration)

## Cài Đặt

```bash
pip install vieneu pyyaml
# FFmpeg phải có trong PATH
```

## Cấu Trúc Dự Án

```
project/
├── config/
│   ├── settings.yaml      # Cấu hình video, animation, TTS
│   └── characters.yaml    # Nhân vật + voice mapping
├── input/
│   ├── images/            # Ảnh minh họa (1.png, 2.png, ...)
│   └── script.json        # Kịch bản phân vai
├── audio/
│   ├── refs/              # Audio tham chiếu (cho voice cloning)
│   └── voices/            # Audio narration đã generate
└── output/
    ├── scenes/            # Scenes trung gian
    └── final/             # Video hoàn chỉnh
```

## VieNeu-TTS — Gotchas Quan Trọng

### ⚠️ Preset Names PHẢI là ASCII KHÔNG DẤU

```python
# ❌ SAI — sẽ tạo ra file silence
tts.get_preset_voice("Bình")   # KeyError
tts.get_preset_voice("Ngọc")   # KeyError

# ✅ ĐÚNG — preset names không dấu
tts.get_preset_voice("Binh")   # OK
tts.get_preset_voice("Ngoc")   # OK
```

### Danh sách 10 preset voices

| Preset Name | Giới tính | Vùng miền |
|-------------|-----------|-----------|
| `Binh`      | Nam       | Bắc       |
| `Tuyen`     | Nam       | Bắc       |
| `Nguyen`    | Nam       | Nam       |
| `Son`       | Nam       | Nam       |
| `Vinh`      | Nam       | Nam       |
| `Huong`     | Nữ        | Bắc       |
| `Ly`        | Nữ        | Bắc       |
| `Ngoc`      | Nữ        | Bắc       |
| `Doan`      | Nữ        | Nam       |
| `Dung`      | Nữ        | Nam       |

### API Usage Pattern

```python
from vieneu import Vieneu
import numpy as np

tts = Vieneu()  # Factory → VieNeuTTS (CPU/GGUF)

# 1. Dùng preset voice
voice = tts.get_preset_voice("Binh")  # → dict {'codes': tensor, 'text': str}
audio = tts.infer(text="Xin chào!", voice=voice)  # → np.ndarray
tts.save(audio, "output.wav")  # Dùng soundfile, sample_rate=24000

# 2. Clone voice từ reference audio (3-5 giây WAV)
ref_codes = tts.encode_reference("reference.wav")
audio = tts.infer(text="Xin chào!", ref_codes=ref_codes, ref_text="ref text")

# 3. Batch processing
audios = tts.infer_batch(["Text 1", "Text 2"], voice=voice)
```

### Lưu ý hiệu năng
- **Lần chạy đầu**: Tải model GGUF ~1.6GB từ HuggingFace (chỉ 1 lần)
- **CPU mode (i7 12 cores)**: ~3-5 giây/câu ngắn, 8-15 giây/câu dài
- **GPU mode**: Cần NVIDIA CUDA >= 12.8, nhanh hơn 3-5x

## FFmpeg Ken Burns Animation

### Hiệu ứng từ ảnh tĩnh (FREE)

```python
import subprocess

def kenburns(image, output, duration, effect="zoom_in", w=1080, h=1920, fps=30):
    tf = int(duration * fps)
    zs = 0.3 / tf
    
    filters = {
        "zoom_in":  f"zoompan=z='min(1.0+{zs}*in,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={tf}:s={w}x{h}:fps={fps}",
        "zoom_out": f"zoompan=z='max(1.3-{zs}*in,1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={tf}:s={w}x{h}:fps={fps}",
        "pan_left": f"zoompan=z='1.1':x='iw*0.3-iw*0.3*in/{tf}':y='ih/2-(ih/zoom/2)':d={tf}:s={w}x{h}:fps={fps}",
        "pan_right":f"zoompan=z='1.1':x='iw*0.3*in/{tf}':y='ih/2-(ih/zoom/2)':d={tf}:s={w}x{h}:fps={fps}",
    }
    
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", image,
        "-vf", f"{filters[effect]},format=yuv420p",
        "-t", str(duration), "-r", str(fps),
        "-c:v", "libx264", "-b:v", "8M", "-pix_fmt", "yuv420p", "-an", output
    ], capture_output=True, timeout=120)
```

### Ghép video + audio

```bash
# Merge 1 clip + 1 audio
ffmpeg -y -i clip.mp4 -i voice.wav -c:v copy -c:a aac -b:a 256k -shortest output.mp4

# Concat nhiều scenes
ffmpeg -y -f concat -safe 0 -i list.txt -c copy final.mp4
```

## Script JSON Format

```json
[{
  "chapter": 1,
  "title": "Tiêu đề",
  "image": "1.png",
  "lines": [{
    "voice": "narrator_m",
    "text": "Nội dung narration",
    "animation": "zoom_in",
    "focus_point": "center"
  }]
}]
```

## Chi Phí Sản Xuất

| Mode | Chi phí | Chất lượng | Speed |
|------|---------|------------|-------|
| Ken Burns (FFmpeg) | **FREE** | ⭐⭐⭐ | ~15s/clip CPU |
| Veo 3.1 Lite API | $0.05/s | ⭐⭐⭐⭐⭐ | ~30s/clip cloud |
| Hybrid | ~$2.5/video | ⭐⭐⭐⭐ | Mixed |

## Chạy Pipeline

```bash
# Render tất cả (VieNeu + Ken Burns + Compose)
python render_now.py

# Ước tính chi phí
python pipeline.py --project ./project --estimate --mode kenburns
```

## Troubleshooting

| Lỗi | Nguyên nhân | Fix |
|-----|-------------|-----|
| Audio silence (-91 dB) | Preset name sai dấu | Dùng ASCII: `Binh` không phải `Bình` |
| `object is not callable` | VieNeu model chưa load xong | Chờ download model ~1.6GB lần đầu |
| FFmpeg timeout | Ảnh gốc quá lớn | Resize ảnh xuống ~2000px width |
