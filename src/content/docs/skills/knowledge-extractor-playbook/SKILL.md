---
title: "SKILL"
name: Nghề Đào Giếng (Knowledge Extractor Playbook)
description: Framework tự học và bóc tách domain/repo code mới theo triết lý "AI là Team" & "Cấu trúc hóa". Áp dụng nguyên lý LLM nội suy để phá vỡ barrier to entry.
---
# Triết lý "Nghề Đào Giếng" (Well-Digger) cho AI Agent

Auto-trigger khi: USER yêu cầu "đọc sâu", "nghiên cứu code", "phân tích kỹ", "self-learn", "bóc tách knowledge từ repo lạ".

## 1. Core Mindset (Luật Bất Di Bất Dịch)
- **Zero Barrier:** Mọi domain (lĩnh vực) lạ lẫm, bất kể độ phức tạp, thực chất đều chỉ là một **Tập hữu hạn gồm Cấu trúc (Rules) + Dữ liệu (Data)**. Nhiệm vụ của Antigravity là dùng năng lực nội suy để tìm ra cấu trúc đó.
- **Context Engineering (Manus Pattern - The 3 Files):** Không nhồi nhét code vào RAM (Context Window). Mọi quá trình đọc source code phức tạp phải xả ra đĩa thông qua 3 sub-files: 
  - `task_plan.md` -> Tracking các bước bóc tách
  - `findings.md` -> Chứa data, rules và insight phân tích được 
  - `progress.md` -> Lưu lại log và lỗi (Never repeat failures).
- **Quy tắc 2-Action:** Sau mỗi 2 tool calls đọc code (`view_file`, `grep_search`), bắt buộc phải xả insight vào `findings.md`.
- **Tháo tác vụ:** Hãy coi Antigravity không phải công cụ tĩnh, mà là một **Team hoàn chỉnh** đang chờ dispatch (Dev, Research, Data, Editorial).
- **Tôn trọng nhưng không giam nhốt:** Cung cấp output cực độ sắc bén, không đưa ra câu trả lời cho có. Tự phản biện chính logic của mình (hoặc giả lập đối kháng Claude vs ChatGPT).
- **Phục vụ sản phẩm cuối:** Chỉ bóc tách những gì tạo ra giá trị hành động (Actionable insights). Không quan tâm "giếng ai đào", chỉ quan tâm "nước sạch và uống được". Tức là trích xuất pattern có thể xài được ngay.

## 2. Quy Trình Vận Hành Bóc Tách Repo Code (5 Bước Tự Học)
Khi nhận một repo khổng lồ (như `DeepTutor`, `seomachine`...), Antigravity TUYỆT ĐỐI KHÔNG summarize kiểu thống kê file. Bắt buộc áp dụng 5 bước tư duy sau:

1. **Chấp Nhận Cấu Trúc (Map the Rules):** 
   - Không sa đà vào chi tiết dòng code. 
   - Đặt câu hỏi: Cấu trúc lõi của domain/repo này là gì? Tìm ra ánh xạ giữa domain này với những kiến trúc quen thuộc (VD: CRM lạ lẫm thực chất là State chuyển đổi trạng thái khách hàng).
2. **Set Role cho Team (Xác định Thẩm quyền):** 
   - Yêu cầu AI (chính bạn) nhìn repo từ nhiều góc độ khác nhau: 1 góc Data Engineer, 1 góc AI Researcher, 1 góc Product Manager. 
3. **Đối Kháng (Challenge the Blindspots):** 
   - Đừng tin mọi logic của Repo gốc. Phản biện lại các giải pháp của tác giả. Chỉ ra điểm yếu, điểm mạnh, và mù mờ. 
4. **Nội Suy Giá Trị Cốt Lõi (Extract the 'Nước Máy'):** 
   - Cô đặc 200 trang docs / 50 files code thành 5 trang / 5 patterns có giá trị ứng dụng. Bỏ qua các overhead dư thừa của hệ thống cũ.
5. **Giữ Quyền Phán Đoán Cho Cấp Trên (Agency & Skin In The Game):** 
   - Đề xuất 3 phương án để ứng dụng bộ code này. 
   - Không tự ý chốt hạ hành động rủi ro. Chỉ báo cáo: "Đây là 3 góc đánh, bạn chọn 1, mình sẽ triển khai!". Vì USER là người chịu hậu quả và trách nhiệm cuối cùng.

> **Khẩu quyết:** Bạn không cần biết tất cả. Bạn cần muốn đúng thứ, hỏi đúng cách, và dám chịu trách nhiệm. Xoa đèn thần mạnh lên!
