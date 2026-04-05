---
name: user_tools_env
description: "Ghi nhớ máy tính user ĐÃ LOGIN SẴN Vercel CLI và Github CLI (gh)"
type: user
---
User đã cài đặt và cấu hình đăng nhập sẵn hai công cụ triển khai đám mây cực kỳ quan trọng là `vercel` và `gh` (Github CLI) trên hệ thống.
**Why:** Powershell Terminal bên trong IDE có thể trả về lỗi "The term 'vercel' is not recognized" do Alias hoặc đường dẫn ENV Path bị thiếu ở session hiện tại, làm AI lầm tưởng User chưa cài đặt.
**How to apply:** 
- Tuyệt đối không bắt bẻ "Máy tính anh chưa cài Vercel/Github".
- Hãy tự tìm workaround (ví dụ dùng `npx vercel` thay cho `vercel`) hoặc tự động dùng `gh repo create` thay vì bắt User thao tác tay.
- Luôn nhớ User đã Auth (có Session gốc), chỉ việc dùng lệnh Auto.
