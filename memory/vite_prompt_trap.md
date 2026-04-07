---
name: Vite Prompt Trap Fix
description: Cách fix lỗi treo shell khi chạy create-vite do bị hỏi interactive prompt
type: feedback
---
**Fact:** Lệnh `npx create-vite` bản mới hoặc trên một số môi trường có thể bị kẹt (hung) ở đoạn `Install with npm and start now? ● Yes / ○ No` dẫn đến shell bị block nếu không chạy được tương tác trực tiếp.

**Why:** Mặc định của npm/npx đôi khi ưu tiên interactive shell, điều này làm gãy chuỗi CI/CD hoặc Auto-Agent.

**How to apply:** 
Luôn luôn thêm cờ `--no-interactive` khi gọi tạo project bằng Vite qua CLI tự động hóa.
VD: `npx create-vite@latest folder_name --template react-ts --no-interactive`
