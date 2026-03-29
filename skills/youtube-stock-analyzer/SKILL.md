---
name: YouTube Stock Analyzer
description: Kỹ năng phân tích, tóm tắt transcript video YouTube thành báo cáo gắn timeline và đối chiếu thực tế (Fact-Check) dành riêng cho nội dung tài chính/chứng khoán.
---

# YouTube Stock Analyzer Skill
SKILL này giúp biến AI thành một chuyên gia phân tích video trên YouTube, chủ yếu dành cho các livestream phân tích tài chính/cổ phiếu từ các Kols. Nó không chỉ đơn thuần là tóm tắt văn bản, mà còn theo dõi theo dòng thời gian và đóng vai trò phản biện độc lập (Fact-check) để cung cấp góc nhìn trung lập.

## Trigger Keywords
Skill này tự động kích hoạt khi User nhắc đến:
- "Phân tích video youtube này"
- "Tóm tắt kênh chứng khoán..."
- "Lấy ý chính video youtube có timeline"
- "Phân tích mã từ video..."
- "youtube analyzer"

## Quy Trình Xử Lý (Runbook)

### Bước 1: Kéo dữ liệu bằng `fetch_transcript.py`
Sử dụng script có sẵn `fetch_transcript.py` nằm trong dự án (do user chỉ định hoặc script mẫu).
Script này bắt buộc phải sử dụng thư viện `yt-dlp` và `youtube-transcript-api` (version >=1.2.4) để cào transcript.
Yêu cầu Output từ script: File txt có chèn Timestamp dưới định dạng `[MM:SS] Nội dung.`.

### Bước 2: AI đọc Text và lọc từ khóa (Timeline parsing)
AI sẽ đọc text qua công cụ `view_file` (chia chặng nếu text vượt 800-1000 dòng).
Tìm kiếm các nhóm nội dung:
1. Keyword vĩ mô: "lãi suất", "lạm phát", "fed", "giá dầu", "tỷ giá".
2. Keyword cổ phiếu: Các mã chứng khoán (như DGC, PVS, VNI, ...).
Ghi chú lại **Chính xác Timetamp** (Ví dụ `[44:45]`) tại vị trí đoạn hội thoại liên quan.

### Bước 3: Phản biện & Đối chiếu (Fact-Checking)
- **Fact-Check Vĩ mô:** So sánh nhận định trong video với dữ liệu kinh tế hiện thời AI biết. Nêu rõ nó "Hợp lý", "Phóng đại", hay "Chậm so với tin tức hiện tại".
- **Fact-Check Cổ phiếu:** Phân tích lại luận điểm cơ bản của mã đó (Khấu hao, P/E, Giá nguyên liệu đầu vào). Cảnh báo nếu lời khuyên mua không phù hợp với xu hướng chung.

### Bước 4: Tạo Artifact Báo Cáo Markdown
Output ra file Markdown lưu vào dự án với cấu trúc:
- Header (Người phân tích: Tên AI, Thời gian log phân tích).
- Phân đoạn `DÒNG THỜI GIAN VĨ MÔ & RỦI RO HỆ THỐNG`.
- Phân đoạn `DÒNG THỜI GIAN CỔ PHIẾU GẮN KÈM FACT-CHECK`.
Trong mỗi phân đoạn lại áp dụng Format:
- `[MM:SS]` Tiêu đề:
    - **Nội dung Kênh:** [Tóm tắt lời nói chuyên gia]
    - **🔎 Thực tế Thị Trường/Fact-Check:** [Phản biện của AI]

## Quy tắc Tối Cổ (Cấm Kỵ)
- Không trả về file toàn chữ dày đặc thiếu cấu trúc list/bullet.
- Bắt buộc phải có ngày giờ phân tích ghi rành rành trên report.
- Phải tách bạch rõ ràng giữa "Ông ấy (Kênh youtube) nói gì" và "Thực tế nó như thế nào (AI Fact check)". Ngăn chặn thiên kiến người xem bị Kols lùa gà.
