---
title: "ai voice humanization"
name: Khử Tính Máy Móc của Giọng AI (Humanize TTS)
description: Kinh nghiệm đánh lừa cảm giác người nghe, biến giọng AI thành giọng KOL người thật.
type: feedback
---
**Fact:** Dù dùng mô hình AI xịn tới đâu (VieNeu, Vbee), nếu kịch bản viết khô khan theo kiểu "báo chí", người nghe sẽ phát hiện ra AI ngay lập tức do giọng điệu thiếu cảm xúc, thiếu tiếng lóng.

**Why:** Khán giả TikTok rất tinh vi với slop AI. Kịch bản tóm tắt bình thường AI sẽ đọc với tone "Google Translate" vì thiếu dấu phẩy ép nhịp và thiếu từ đệm.

**How to apply:**
1. **Dùng Tiếng Lóng (Slang):** Nhồi nhét các từ ngữ kiểu "thề luôn", "này nha", "vãi chưởng", "chúa ghét", "mấy ba", "ngáo ngáo".
2. **Ngắt Nghỉ Lố (Over-Punctuate):** Spam thật nhiều dấu ba chấm `...` và dấu chấm than `!` để ép AI phải dừng lại thở hắt ra, tạo độ gằn.
3. **Studio Audio Filter:** Khi dùng FFmpeg render, quất thêm bộ filter `-af "bass=g=5:treble=g=-3"` để hạ tông the thé của máy đi, tăng bass trầm ấm nghe như xài mic cắm phòng thu (Podcast vibe).
