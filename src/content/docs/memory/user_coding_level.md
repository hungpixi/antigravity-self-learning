---
name: user_coding_level
description: "Trình độ code của user để AI biết cách giao tiếp không bị basic quá"
type: user
---
User có khả năng code (biết code căn bản / intermediate), đọc hiểu cấu trúc hệ thống và deploy tốt.

**Why:** User nhắc nhở "chỉnh lại preferences.json đi... chứ tao cũng biết code sơ rồi mà" khi quy trình `/deploy` xưng hô và giải thích các thuật ngữ như SSL, DNS, CDN quá cơ bản như giảng cho newbie.

**How to apply:** 
- Đã Hardcode `technical_level: "intermediate"` trong `preferences.json`.
- TỪ NAY VỀ SAU: Giao tiếp rành mạch, đi thẳng vào thuật ngữ IT. Lên thẳng giải pháp. Không được phép dùng văn mẫu "Progressive disclosure" hỏi từng bước rườm rà. Bỏ qua mọi định nghĩa khái niệm IT 101.
