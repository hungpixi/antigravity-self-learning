---
name: Google Docs Terminal-First CLI (No MCP)
description: Dùng Service Account và NodeJS CLI nội bộ thay cho MCP để ghi/đọc Google Docs tiết kiệm context
type: feedback
---

**Fact/Rule:** Về việc thao tác với Google Docs bằng AI Agent, tuyệt đối **không lạm dụng MCP server** để tránh bị nhồi nhét JSON Schema khổng lồ làm tốn hàng ngàn tokens.
Giải pháp tối ưu: **Dùng Service Account** + CLI Nodejs.

**Why:**
1. **Zero-Context Overhead**: Script tự chạy ngầm và in thẳng kết quả text/markdown ra terminal.
2. Dễ điều khiển style văn bản (đặc biệt khi user muốn convert Markdown Markdown sang Docs) vì mình chủ động parse Markdown qua thư viện `marked` ra node tree, sau đó đẩy batch request updateParagraphStyle.

**How to apply:**
1. Xin/Tạo file key Service Account `.json`, và giấu nhẹm vào `.gitignore`.
2. Dùng thư viện `googleapis` và `marked` (npm install).
3. Đóng gói command shortcut trong package.json: `npm run gdoc push <DOC_ID> <file.md>`.
4. Logic bóc tách Markdown để đẩy lên GDOC:
   - Gộp tất cả text bắn vào một request `insertText` duy nhất ở `index: 1`.
   - Vòng lặp tính toán Start/End Index (Index Tracker).
   - Truyền style qua API:
     - Font size/family: `updateTextStyle` -> `{ weightedFontFamily: { fontFamily: "Calibri" } }`
     - Headings (H1-H6): `updateParagraphStyle` -> `{ namedStyleType: "HEADING_X" }`
