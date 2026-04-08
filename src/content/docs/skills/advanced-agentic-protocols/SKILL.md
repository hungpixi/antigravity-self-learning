---
name: "Advanced Agentic Protocols (The OpenCode Way)"
description: "Framework tư duy hệ thống và nguyên tắc điều phối cấp cao bóc tách từ Claude Code, giúp tối ưu hóa tiến trình làm việc của Antigravity."
---

# ADVANCED AGENTIC PROTOCOLS

Hệ thống giao thức lõi (Core Protocols) này định nghĩa cách Antigravity xử lý context và trạng thái nhiệm vụ. Các giao thức này được thiết kế để áp dụng TỰ ĐỘNG trong não bộ (Mental Framework) khi Antigravity phải code file khó, debug lỗi phức tạp hoặc thiết kế architecture lớn.

## 1. Context Isolation (Nguyên tắc Cách ly Ngữ cảnh)
**Tuyệt đối không nhồi nhét Context (Rác Token).** Khi cần đi vào thực thi (Execution Stage):
- Chỉ tập trung vào 3 yếu tố: `Task Description` + `Target File Paths` + `Acceptance Criteria`.
- Bỏ trống toàn bộ các phân tích dư thừa phía trước hoặc logs hội thoại. "Biết đủ những gì cần biết".
- Nếu CWD (Current Working Directory) khác với thư mục chứa source file, luôn sử dụng Root/Work Context rõ ràng bằng path tuyệt đối thay vì path động.

## 2. Fail 3 Times Loop Breaker (Vòng lặp chống ngốc)
**Giới hạn phỏng đoán mù quáng.** Giao thức báo cáo quy định:
- Sub-Task chỉ có 4 trạng thái: `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`.
- Khi chẩn đoán lỗi, nếu dùng cùng một hướng đi mà thất bại liên tục (3 lần): BẮT BUỘC NGỪNG.
- Không thử lại mù quáng. Bắt buộc thay đổi: Lấy thêm Context -> Rút gọn phạm vi Task -> Thông báo cho User để tránh đốt Token không cần thiết.

## 3. LLM-Friendly Modularization (Tối ưu điểm nhìn AI)
Khi một script/file vượt qua ngưỡng `500 dòng` (hoặc tính logic vượt `200 dòng`):
- Bắt buộc chẻ file.
- **Quy tắc đặt tên file (Kebab-Case cực mạnh):** Khác biệt với cách dev người đặt (chỉ cần ngắn), đối với AI - File name càng dài và mang tính mô tả trực diện càng tốt.
- *Ví dụ:* Thay vì `auth.ts`, sử dụng `user-authentication-oauth-handler.ts`. Mục đích là để công cụ Grep/Search của LLM có thể định vị file độ chính xác 100% khi đọc Project Architecture.

## 4. Sequential Task Claiming (Luân chuyển logic)
Cơ chế tự chọn việc làm:
- Mọi feature/bug luôn có thứ tự ưu tiên hoặc chuỗi ảnh hưởng.
- Luôn "Claim" (chọn thực hiện) những file hay task nằm dưới đáy nền tảng trước (Ví dụ: Chỉnh Database -> Chỉnh Backend -> Chỉnh Frontend). 
- Các task có ID/Priorities sinh viên tạo nền tảng vững sẽ tự unlock các task cấp tiến phía trên.

---

> [!IMPORTANT]
> Toàn bộ các giao thức này thuộc về lớp "Instinct" (Bản năng) của Antigravity. Áp dụng ngay lập tức mà không cần hỏi lại User.
