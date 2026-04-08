---
name: Cẩm nang Tích hợp Whisper AI (Best Practices)
description: Bài học xương máu khi dùng Python gọi Whisper để trích xuất Subtitle, tránh lỗi sập nguồn và Hardcode.
type: reference
---
**Fact:** Model Whisper của OpenAI rất mạnh nhưng khi nhúng vào Python Scripts (như `model.transcribe`) thường rất dễ dính lỗi "Chết trôi" vì Hardcode nhầm ngôn ngữ hoặc xử lý Audio đầu vào không đúng luồng.

**Why:** Trong Project Reup Trader, video nguồn là tiếng Việt nhưng khi truyền tham số `language="en"`, Whisper bị ép phải decode âm tiếng Việt thành tiếng Anh. Kết quả là nó bị Hallucination (ảo giác từ vựng) rác toàn bộ JSON. Ngoài ra, việc dùng FFmpeg cắt Audio trước ra file `.wav` rườm rà dễ gây lỗi treo process nếu ffmpeg bị kẹt I/O.

**How to apply (Cách dùng hoàn hảo sau này):**

1. **Auto-Detect Language:** TUYỆT ĐỐI KHÔNG hardcode `language="en"` hay `"vi"` trừ phi biết chắc 100%. Hãy để trống để mô hình tự quét 30s đầu:
```python
# Sai lầm cũ:
# result = model.transcribe(audio, task="transcribe", language="en") 

# Bắt buộc chuẩn:
result = model.transcribe(audio_path, task="transcribe")
# Whisper sẽ tự lấy ra result["language"] và trả về result["segments"] đúng chuẩn.
```

2. **Dừng tự mài mò code FFmpeg lấy Audio:**
Whisper hỗ trợ truyền TỰ DO định dạng `.mp4`, `.mp3` trực tiếp vào hàm `transcribe`. Nó tự gọi FFmpeg ngầm bên dưới bộ nhớ. Không cần phải code script dài 30 dòng tự trích xuất `.wav` rườm rà gây lỗi "File not found" hay "Access denied".
```python
# Nhanh - Gọn - Lẹ:
model = whisper.load_model("base")
result = model.transcribe("video_goc.mp4") # Đút thẳng MP4 vào. Nhanh hơn 50%.
```

3. **Cấu trúc lưu Subtitles chuẩn chỉnh:**
Luôn output ra 2 định dạng: `.json` (để downstream xử lý Data cho LLM khác đọc) và `.srt` (để Hardsub FFmpeg nếu cần hiển thị chữ lên video). Mọi Project reup sau này đều bưng đúng khung code này mà phang, không viết lại từ đầu.

4. **Các Tham số KHỦNG (Advanced Kwargs) đào được từ Source Code:**
Khi chui vào đọc hàm `whisper.transcribe`, ta thấy có những lá bùa chống lỗi sau mà Docs ít nói:
- `fp16=False`: Giải quyết dứt điểm cái Warning đỏ lòm `FP16 is not supported on CPU` làm bẩn Terminal.
- `condition_on_previous_text=False`: Chìa khóa vàng **Chống Ảo Giác (Anti-Hallucination)**. Khi video có những khoảng lặng dài (như Podcast), Whisper hay bị ảo giác tự bịa ra câu "Cảm ơn các bạn đã theo dõi". Set bằng `False` cắt đứt hoàn toàn vòng lặp lỗi này.
- `initial_prompt="Trading, Forex, Stoploss, Buy, Sell, Cắt lỗ"`: Tính năng cực mạnh để **dạy từ vựng chuyên ngành**. Nhét cái này vào hàm `transcribe`, AI sẽ không bao giờ nghe nhầm chữ "Forex" thành "For ex" hay "Stoploss" thành tiếng Việt vớ vẩn.
- `word_timestamps=True`: Mặc định Whisper lòi ra Subtitle cho cả Câu. Bật cờ này lên, nó sẽ bóc tách Timestamp cho **Từng Từ Một**. Đây là nguyên liệu Cốt Lõi để làm CapCut Style Text Animation (Chữ nhảy theo giọng nói).

**Template Code Cuối Cùng:**
```python
result = model.transcribe(
    "video_chill_podcast.mp4",
    task="transcribe",
    fp16=False,
    condition_on_previous_text=False,
    word_timestamps=True,
    initial_prompt="Trading, Forex, Nến Nhật, Cắt lỗ, Gồng lời, Kỷ luật"
)
```
