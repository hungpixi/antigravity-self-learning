---
name: "Comarai Agency Sincere Agent (Zalo & Telegram Outreach)"
description: "AI Agent xây dựng phễu thu hút B2B bằng 'Kho Khóa Học Miễn Phí'. Tự động Spam mồi vào các Group (Tele/FB/Zalo), hứng khách vào Channel, sau đó dùng Zalo 1:1 tiếp cận cá nhân hóa (browser_subagent) để Upsell dịch vụ AIO/SEO và Tặng AI tích hợp."
---

# 📚 Cẩm Nang Vận Hành: Zalo & Telegram B2B Sincere Agent

Kỹ năng này giúp Antigravity vận hành quy trình kéo Lead tàn bạo nhưng lại chốt sale chân thành. Vũ khí chính: **Tặng Kho Khóa Học / Script AI** -> Kéo vào Tele -> Quét SĐT -> Liên hệ Zalo 1:1.

## 🗂️ Môi Trường Làm Việc
- File điều khiển: `D:\Cá nhân\Vọc vạch\Sales Agent\Comarai-B2B-Agent\comarai_cli.py`
- CRM States: `D:\Cá nhân\Vọc vạch\Sales Agent\Comarai-B2B-Agent\crm_telegram_zalo.json`

## 🕹️ Thao Tác (Giao Việc Cho Antigravity Browser Subagent)

### Lệnh 1: Đi Rải Link Khóa Học (Mass Seeding Groups)
Khi Host yêu cầu: "Đi spam kho khóa học vào các Group MMO đi".
-> **Bạn thực hiện:**
1. Chạy CLI lấy kịch bản: `python "D:\Cá nhân\Vọc vạch\Sales Agent\Comarai-B2B-Agent\comarai_cli.py" --run spam_groups --topic "MMO/Marketing" --tele_link "t.me/KhoHocComarai"`
2. Đọc kịch bản Output từ Console.
3. Kích hoạt `browser_subagent`: 
   - Đăng nhập Facebook Web / Telegram Web.
   - Tìm kiếm các Group theo từ khóa được giao.
   - Dán 100% nguyên văn lời nhắn "Tặng code/khóa học miễn phí..." vào khung chat.
   - Rút lui sau 10-15 nhóm để tránh tình trạng Spammed IP.

### Lệnh 2: Quét Khách Hàng Chất Lượng Chuyển Qua Zalo
Khi Host yêu cầu: "Nạp ông Nguyễn Văn B sđt 09xxx vào luồng Zalo nhé".
-> **Bạn thực hiện:**
```bash
python "D:\Cá nhân\Vọc vạch\Sales Agent\Comarai-B2B-Agent\comarai_cli.py" --run add_zalo_lead --phone "09xxx" --name "Văn B" --industry "E-commerce"
```

### Lệnh 3: Trợ Lý Zalo 1:1 Chăm Sóc Vàng (Sincere Pitch)
Khi Host yêu cầu: "Chạy lịch trình Zalo hỏi thăm tặng quà hôm nay đi".
-> **Bạn thực hiện:**
1. Chạy lệnh: `python "D:\Cá nhân\Vọc vạch\Sales Agent\Comarai-B2B-Agent\comarai_cli.py" --run zalo_outreach`
2. Kích hoạt `browser_subagent`:
   - Truy cập thẳng `https://chat.zalo.me/`.
   - Gõ từng SĐT Zalo vào thanh Tìm Kiếm trên góc trái.
   - Mở ô Add Friend (Kết bạn) hoặc tin nhắn trực tiếp.
   - Dán chính xác kịch bản cá nhân hóa sinh ra từ Terminal: *"Dạ chào anh Văn B... Em bên nhóm share khóa học..."* rủ rê anh ta dùng thêm Tool SEO Premium / Gợi ý làm Website chuẩn AIO.

## 🛡️ Cam Kết Hành Động Của Agent
* Nấp bóng phía sau Zalo Web và Tele Web, đóng kịch bản hệt người thật (gõ từng chữ, delay chờ load mạng).
* Nếu `browser_subagent` bị kẹt ở CAPTCHA, phải thông báo ngay lập tức cho anh Hưng thông qua Tool `notify_user` để giải quyết. Không được bối rối.
