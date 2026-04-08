---
title: "reference knowledge architecture"
---

# Unfied Knowledge Architecture (UKA) v1.0
> **Triết lý:** AI học được gì mới thì phải cất đúng ngăn tủ. Không vứt rác lung tung, không tạo file tuỳ tiện. Kỷ luật rườm rà sinh ra lỗi YAML.

Để giải quyết sự chồng chéo (Overlap) giữa KI (Knowledge Items), Skills (7 Mô hình) và Memory. Chúng ta thống nhất quy hoạch hệ thống Antigravity Core thành 3 tầng rõ rệt:

## 1. THE LIBRARY (Tầng Tri Thức Tĩnh) -> KNOWLEDGE ITEMS (KI)
- **Định nghĩa:** Là thư viện lưu trữ "Kiến thức chuyên ngành" (Domain Knowledge).
- **Ví dụ:** Cách thuật toán TikTok hoạt động, Cách cấu hình VPS Nhật, Tài liệu phân tích kỹ thuật Ichimoku.
- **Định dạng:** Thư mục chứa `metadata.json` và các file `artifacts/*.md`.
- **Dấu hiệu nhận biết:** Nó là tài liệu để AI *ĐỌC* và *HIỂU*, chứ không phải để AI *CHẠY*.
- **Quy tắc tạo mới:** Chỉ tạo KI khi có một chủ đề kiến thức lớn, độc lập với source code hiện tại cần lưu trữ dài hạn.

## 2. THE ENGINE (Tầng Thực Thi) -> SKILLS & WORKFLOWS
- **Định nghĩa:** Là các "Công cụ" và "Kỹ năng phản xạ" của AI.
- **Ví dụ:** `/deploy` workflow, 7 Mô hình tự học (Bug-fix patterns, Effective Prompts, ADR).
- **Định dạng:** File markdown duy nhất `SKILL.md` hoặc `workflow_name.md`.
- **Dấu hiệu nhận biết:** Nó là tập hợp các QUY TẮC và CÂU LỆNH để AI *HÀNH ĐỘNG*.
- **Quy tắc tạo/sửa (Chống lỗi YAML):** BẤT KỲ khi nào AI cập nhật/tạo mới file ở đây, phần `description` đầu file PHẢI BỌC BẰNG DẤU NGOẶC KÉP `""`. Bất cứ bug nào giải quyết xong, đưa thẳng vào bảng TIL của `bug-fix-patterns/SKILL.md`.

## 3. THE RAM (Tầng Bối Cảnh) -> MEMORIES
- **Định nghĩa:** Là "Bộ nhớ ngắn-trung hạn" về Context hiện tại.
- **Ví dụ:** Profile anh Hưng, Dự án Vactory đang chạy, Mức độ code (Intermediate).
- **Định dạng:** Các file `*.md` nhỏ gọn (<200 dòng) nằm trong thư mục `memory/`, được index qua `MEMORY.md`.
- **Dấu hiệu nhận biết:** AI dùng nó để biết *MÌNH ĐANG LÀM CHO AI, LÀM CÁI GÌ*.
- **Dream Consolidation:** Cuối ngày, AI chạy `/dream` để dọn rác ở thư mục này, không cho nó phình to.

---

## 🚀 TÓM TẮT QUY TRÌNH "TỰ HỌC" GỌN GÀNG:
1. Gặp Bug kĩ thuật code/deploy? -> Ghi vào **Skills (Bug-fix patterns)**.
2. Quyết định đổi framework/công nghệ? -> Ghi vào **Skills (ADR)**.
3. Học được chiến lược Marketing mới? -> Tạo **KI (Knowledge Item)**.
4. Đổi tên dự án? -> Sửa **Memory (project_active)**.
