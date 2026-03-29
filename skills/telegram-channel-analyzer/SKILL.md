---
name: Telegram Channel Analyzer
description: Scrape toàn bộ messages + media từ Telegram channel/group bằng Telethon, phân loại nội dung theo mảng, phân tích timeline/engagement, tạo báo cáo tổng thể. Triggers on "telegram", "scrape channel", "phân tích channel", "telegram scraper", "download telegram messages", "telegram analysis", "lấy tin nhắn telegram", "đọc kênh telegram".
---

# 📡 Telegram Channel Analyzer

> Skill scrape + phân tích Telegram channel sử dụng Telethon (tài khoản cá nhân).
> Đã test thành công với channel Mẫn Nhi Đa Tài (4,780 messages, 754 media).

## Prerequisites

```
pip install telethon python-dotenv
```

Cần có:
- Telegram API ID + Hash (lấy từ https://my.telegram.org)
- Số điện thoại đã đăng ký Telegram
- Channel ID hoặc username

## Quy Trình

### Step 1: Tìm credentials
```bash
# Nếu đã có dự án cũ dùng Telegram API
grep -r "TELEGRAM_API_ID" D:/ --include="*.env"
```

### Step 2: Tìm Channel ID
- Mở `web.telegram.org/a/# {channel_id}` → ID trong URL
- Format Telethon: `-100{channel_id}` (thêm dấu `-100` phía trước)
- **CẢNH BÁO**: Nếu URL đã có prefix `100` thì chỉ cần thêm `-` phía trước!
  - URL: `1002150656284` → Telethon: `-1002150656284` (KHÔNG phải `-1001002150656284`)

### Step 3: Reuse session file
```bash
# Copy session từ dự án cũ để tránh nhập OTP lại
cp old_project/telegram_session.session new_project/scraper_session.session
```

### Step 4: Chạy scraper
```python
# Core pattern
from telethon import TelegramClient

client = TelegramClient("session_name", api_id, api_hash)
await client.start(phone=phone)

# Lấy thông tin channel
from telethon.tl.functions.channels import GetFullChannelRequest
entity = await client.get_entity(channel_id)
full = await client(GetFullChannelRequest(entity))

# Scrape messages
async for message in client.iter_messages(channel_id, limit=None):
    msg_data = {
        "id": message.id,
        "date": message.date.isoformat(),
        "text": message.text or "",
        "views": getattr(message, "views", None),
        "reactions": extract_reactions(message),  # Custom function
    }
    
    # Download media (skip video >50MB)
    if message.media:
        await client.download_media(message, file=str(filepath))
```

### Step 5: Phân tích
```python
# Keyword-based categorization
CATEGORIES = {
    "Chứng khoán VN": ["cổ phiếu", "vnindex", "margin", ...],
    "Kinh tế vĩ mô": ["fed", "lãi suất", "cpi", ...],
    # ... thêm categories tùy channel
}

# 1 message có thể thuộc NHIỀU categories
def categorize(text):
    return [cat for cat, keywords in CATEGORIES.items() 
            if any(kw in text.lower() for kw in keywords)]
```

## Output Structure

```
data/
├── messages.json      # Toàn bộ messages + metadata
├── media/             # Ảnh/video tải về (theo timestamp)
│   ├── 2025-01-15_103000_123.jpg
│   └── ...
└── analysis_report.md # Báo cáo phân tích tổng thể
```

## Gotchas & Lessons Learned

| # | Vấn đề | Giải pháp |
|---|--------|-----------|
| 1 | Inline `from X import Y()` trong expression | Import ở top-level, gọi trong function |
| 2 | Channel ID format sai | URL `100XXXX` → Telethon `-100XXXX` (KHÔNG thêm 100 nữa) |
| 3 | Mỗi lần chạy cần OTP | Copy `.session` file từ project cũ |
| 4 | PowerShell `{}` trong f-string | Viết script file thay vì inline command |
| 5 | Video lớn block scraper | Skip files >50MB, log lại |
| 6 | Regex `\b[A-Z]{3}\b` quá rộng | Whitelist mã CK cụ thể |
| 7 | `json.dump` fail datetime | Dùng `default=serialize_datetime` |
| 8 | Reactions format phức tạp | Check `emoticon` vs `document_id` (custom emoji) |

## Reference Files

- Scraper: `scraper.py` (Telethon-based, download text + media)
- Analyzer: `analyze.py` (keyword categorization + report gen)
- Source project: `D:\Cá nhân\Vọc vạch\Đọc telegram channel phân tích`
