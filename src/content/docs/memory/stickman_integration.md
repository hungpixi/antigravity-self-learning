---
title: "stickman integration"
name: Kiến Trúc Tự Động Hóa Stickman & Whiteboard Animation
description: Workflow phối hợp 3 nền tảng Open Source (AnimatedDrawings, HandAnim, Storyboard AI) để Gen video người que.
type: reference
---
**Fact:** Thể loại "Chill Podcast / Healing" và Kể chuyện triết lý cực kỳ hợp với nét vẽ Người Que mộc mạc.

**Why:** Việc ngồi vẽ từng Frame trên Procat/Capcut là thủ công 100%, không Scale được. Việc tích hợp Open Source giúp ta tự động hóa: Gõ Text -> Đẻ Video Người Que khớp Audio.

**How to apply (Quy tắc Phối hợp Hệ thống sau này):**

1. Ý tưởng Kịch bản (Script) sẽ luôn qua tay LLM (Gemini) để xé nhỏ thành các Scene (Cảnh số 1: Buồn bã, Cảnh số 2: Tức giận...).
2. Đẩy các đoạn Script dài cho `Storyboard-AI` hoặc `HandAnim`:
   - Dùng **Storyboard-AI** khi muốn làm nguyên một Video dài liên tục chuyển cảnh (Nó tự móc nối LLM xé script và vẽ bảng).
   - Dùng **HandAnim (Python)** nếu muốn có hiệu ứng Bàn Tay thực sự ló vào màn hình cầm cây bút lông vẽ ra nhân vật (tạo Viral tương tác thị giác đầu clip).
3. Đẩy nhân vật tự chế cho **AnimatedDrawings (Meta AI)**:
   - Khi sếp hoặc Designer vẽ được 1 con Trader người que có bản sắc riêng (Ví dụ mặc áo Vest rách nát). Mình chỉ cần xuất khung hình TĨNH của con đó dạng PNG.
   - Thả tĩnh PNG vào `AnimatedDrawings`. Engine này bằng Python sẽ tự Skeletonize (lắp xương) vào bức ảnh 2D đó.
   - Truyền motion "Walk", "Sit", "Cry", "Jump" -> Meta AI xả ra file GIF / MP4 vòng lặp con Trader đang sụp đổ.
4. **Hậu kỳ FFmpeg:** Trộn Animated PNG sinh ra từ Bước 3, quăng lên Background màu Vàng Cổ Điển đen ngòm, đẩy Audio Voice Clone (VieNeu) vào + Lofi Chillhop mờ ảo. Pipeline hoàn tất!
