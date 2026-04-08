---
name: Facebook Bot Blocking
description: Facebook chặn browser subagent/bot - không dùng browser_subagent để crawl Facebook pages
type: feedback
---

**Rule:** KHÔNG dùng browser_subagent để truy cập Facebook pages. Facebook tích cực chặn bot và sẽ hiện login modal / block access.

**Why:** User đã xác nhận nhiều lần rằng browser subagent bị Facebook chặn, gây lãng phí thời gian và tool calls.

**How to apply:**
- Khi cần nghiên cứu Facebook page: yêu cầu user cung cấp data trực tiếp (copy-paste content, screenshots)
- Hoặc dùng file contentmau.md / text files do user chuẩn bị sẵn
- Nếu cần xem page mới: hỏi user screenshot hoặc copy nội dung vào file
- KHÔNG BAO GIỜ gọi browser_subagent với URL facebook.com
