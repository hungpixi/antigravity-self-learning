---
name: Hướng dẫn Sử dụng Thư viện VieNeu-TTS Local (Voice Cloning)
description: Cấu trúc code nội bộ, các Parameters cốt lõi và Tính năng Zero-Shot Voice Cloning ẩn.
type: reference
---
**Fact:** Thư viện `vieneu` hoặc `vieneu-tts` local được cấp phát dưới dạng Python Package. Nó không chỉ dùng để tạo giọng đọc Text-to-Speech (TTS) thông thường qua các bộ Preset, mà còn sở hữu sức mạnh clone giọng thực tế nhờ nền tảng PyTorch / GGUF.

**Why:** Khám phá mã nguồn `standard.py` và `base.py` cho thấy các Class `VieNeuTTS` và hàm `infer()` có tham số ngầm định rất mạnh mà docs cơ bản không ghi.

**How to apply:**

1. **Khởi tạo Engine (Factory Pattern):**
```python
from vieneu import Vieneu
# mode: "standard" (Pytorch CPU/GPU GGUF), "fast" (LMDeploy GPU), "remote" (API), "xpu" (Intel).
tts = Vieneu(mode="standard")
```

2. **Các phương pháp tạo giọng (Inference Methods):**
- *Sử dụng Preset (Giọng có sẵn):* 
  Hàm lấy mã giọng: `voice = tts.get_preset_voice("Vinh")` (có các giọng như Vinh, Sơn, Bình,...). Rồi gán vào `tts.infer(text="alo", voice=voice)`.

- *Sử dụng Zero-Shot Voice Cloning (Lồng tiếng/Clone giọng cực xịn):*
  KHÔNG cần dùng `get_preset_voice`. Chỉ cần một đoạn audio `.wav` ngắn (người thật nói) và nội dung văn bản của đoạn audio đó.
  ```python
  ref_audio_path = "path/to/original_speaker_audio.wav"
  ref_text = "This is what the person is actually saying in the reference audio."
  
  # Tạo giọng tiếng Việt BẰNG vocal của người trong audio kia:
  target_text = "Xin chào tôi đã sao chép được giọng của bạn."
  audio = tts.infer(
      text=target_text,
      ref_audio=ref_audio_path,
      ref_text=ref_text
  )
  tts.save(audio, "output.wav")
  ```

Khám phá này rất quan trọng cho các cấu trúc Reup Video Tây sang Vietsub: Chỉ cắt 10s audio gốc làm `ref_audio`, sau đó feed tiếng Việt vào `text`, kết quả là tây nói tiếng Việt 100% y hệt âm độ.
