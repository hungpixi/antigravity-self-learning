---
title: "SKILL"
name: Code Smell Catalog
description: "Patterns xấu trong code cần phát hiện sớm trước khi thành bug. Auto-trigger khi review code, refactor, audit code quality. Triggers on \"code smell\", \"code review\", \"refactor\", \"clean code\", \"code quality\", \"anti-pattern\", \"technical debt\", \"nợ kỹ thuật\", \"code xấu\", \"code bẩn\"."
---

# 🔍 Code Smell Catalog

> Phát hiện sớm pattern xấu = ngăn bug trước khi xảy ra. AI check catalog này khi `/review` hoặc `/refactor`.

## Format Entry

```
### SMELL-xxx: [Tên Code Smell]

> 📅 [YYYY-MM-DD] — Phát hiện tại: [dự án]

**Signal**: [Dấu hiệu nhận biết]
**Risk**: [Hậu quả nếu không fix]
**Refactor**: [Cách sửa]
**Example**: [Code ví dụ trước/sau]
```

---

## Active Smells

### SMELL-001: Global Flag Orchestra

> 📅 2026-03-16 — Phát hiện tại: IchiDCA_CCBSN

**Signal**: >5 global boolean flags (`g_buyDone`, `g_sellDone`, `g_trailActive`, `g_partialDone`...)
**Risk**: 2^N combinations = impossible to track. State bugs **sẽ** xảy ra (đã xảy ra 3 lần ở CCBSN).
**Refactor**: Thay bằng `enum TradeState { SCANNING, IN_TRADE, PARTIAL_CLOSED, TRAILING, COOLDOWN }` — 1 variable thay N flags.
```
// ❌ SMELL
bool g_buyPartialDone, g_sellPartialDone, g_buyTrailActive, g_sellTrailActive;

// ✅ CLEAN
enum TradeState { SCANNING, IN_TRADE, PARTIAL, TRAILING, COOLDOWN };
TradeState g_buyState = SCANNING;
```

---

### SMELL-002: Hardcode Config Values

> 📅 2026-03-16 — Phát hiện tại: IchiDCA_CCBSN_V3

**Signal**: Magic numbers trong code (`3.0`, `ORDER_FILLING_FOK`, `50` bars)
**Risk**: Khi đổi instrument/broker → phải sửa code thay vì settings
**Refactor**: Extract thành `input` parameters với default hợp lý
```
// ❌ SMELL
if(spread > 3.0) return;  // WHY 3.0?

// ✅ CLEAN
input double InpMaxSpread = 50.0;  // Document: default cho XAUUSD
if(spread > InpMaxSpread) return;
```

---

### SMELL-003: Dead Function — Viết Nhưng Không Gọi

> 📅 2026-03-17 — Phát hiện tại: ICT_SystemEA_v2

**Signal**: Utility function tồn tại nhưng không ai gọi (grep không ra caller)
**Risk**: Logic bypass — filter có nhưng không hoạt động, trade khi không nên trade
**Refactor**: Grep ngay sau khi viết function. Nếu không gọi → hoặc gọi hoặc xóa.
```bash
# Quick check
grep -rn "IsInSession" --include="*.mq5"  # Phải có ≥2 kết quả (define + call)
```

---

### SMELL-004: Close All Nhưng Quên Reset

> 📅 2026-03-16 — Phát hiện tại: IchiDCA_CCBSN

**Signal**: Hàm close/cleanup mà không reset tất cả state liên quan
**Risk**: State stuck → bot chết cứng sau emergency close
**Refactor**: Mọi cleanup function phải có checklist: "Còn global nào cần reset?"

---

### SMELL-005: Partial Operation Không Có Fallback

> 📅 2026-03-16 — Phát hiện tại: IchiDCA_CCBSN

**Signal**: `close 50%` hoặc `process batch` mà không handle case "partial amount quá nhỏ"
**Risk**: Infinite loop — trigger lại mỗi tick vì partial fail nhưng condition vẫn true
**Refactor**: Luôn có fallback `if(partialFailed) closeAll()`

---

## 📋 Smell Changelog

| # | Ngày | Smell | Phát hiện tại |
|---|------|-------|---------------|
| 001 | 2026-03-16 | Global Flag Orchestra | IchiDCA_CCBSN |
| 002 | 2026-03-16 | Hardcode Config | IchiDCA_CCBSN_V3 |
| 003 | 2026-03-17 | Dead Function | ICT_SystemEA_v2 |
| 004 | 2026-03-16 | Close Without Reset | IchiDCA_CCBSN |
| 005 | 2026-03-16 | Partial No Fallback | IchiDCA_CCBSN |
| 006 | 2026-04-02 | Unmanaged CDP Browser Cache | VEO_TOOL |
| 007 | 2026-04-02 | Swallowed Exception (`pass`) | VEO_TOOL |
| 008 | 2026-04-02 | Hardcoded External Locators | VEO_TOOL |
| 009 | 2026-04-02 | Busy-Wait Loop thiếu Timeout | VEO_TOOL |
| 010 | 2026-04-02 | God Object Workflow Thread | VEO_TOOL |
| 011 | 2026-04-02 | JSON IO Blocks Async Loop | VEO_TOOL |
| 012 | 2026-04-02 | Mix `os.path` và `pathlib` | VEO_TOOL |
| 013 | 2026-04-02 | Shadowing Variables | VEO_TOOL |
| 014 | 2026-04-02 | `DEBUG=True` Hardcode | VEO_TOOL |
| 015 | 2026-04-02 | Manual Regex Extract thay vì JSON DOM | VEO_TOOL |

### SMELL-006: Để Mặc Chromium Tự Quản Lý Cache/Session Trong Tool Auto

> 📅 2026-04-02 — Phát hiện tại: VEO_TOOL

**Signal**: Chạy Automation với profile dài hạn nhưng không cấu trúc cleanup logic (sử dụng Playwright `user_data_dir` nguyên bản). Tắt browser bằng cách Force Kill thẳng thừng.
**Risk**: Rác Session tăng dần theo thời gian. Force Kill khiến file Preferences và Profile corrupt, gây lỗi mất sạch token và state login web.
**Refactor**: Luôn áp dụng "Graceful Shutdown" với Timeout Fallback. Xây dựng logic clean thủ công thư mục `Cache` nhưng chừa lại phân vùng `Login Data`.

```python
# ❌ SMELL: Xóa bạo lực hoặc Mặc hệ thống
shutil.rmtree(profile_dir) # Xoá sạch → Mất token login

# ✅ CLEAN: Graceful Close → Target Specific Dirs
try:
    os.system(f"taskkill /PID {pid} /T") # Ask to close politely
except: ...
# Loop check cache folder để dọn rác, CHỪA lại Login Data
```

### SMELL-007 tới SMELL-015 — VEO_TOOL Code Smells
> 📅 2026-04-02 — Phát hiện tại: VEO_TOOL

Do kiến trúc phức tạp, tool xuất hiện nhiều đoạn nợ kỹ thuật (Technical Debt) như sau:
* **SMELL-007 (Swallowed Exception)**: Dùng `except Exception: pass` vô tội vạ khi parse data. Gây hiệu ứng "Silent Fail" — Lỗi xảy ra nhưng app vẫn im lìm trót lọt, rất khó trace ngược. Refactor: Ít nhất phải có `logging.warning()`.
* **SMELL-008 (Hardcode Locators)**: Selector Playwright cứng mã `textarea[placeholder*='Bạn muốn']`. Nền tảng chỉ cần đổi ngôn ngữ là Bot mù hẵn. Refactor: Dùng XPath liên kết ngữ nghĩa hoặc Extract Constants.
* **SMELL-009 (Busy Wait)**: Vòng lặp `while True: asyncio.sleep(0.1)` không có `if time.time() > deadline: break`. Nếu state bị kẹt, vòng lặp chạy vĩnh viễn tốn CPU.
* **SMELL-010 (God Object)**: `TextToVideoWorkflow` chứa tới 30 properties, ôm đồm từ quản lý tiến trình thread, gọi API, thao tác biến môi trường, đến ghi file JSON. Vi phạm Single Responsibility.
* **SMELL-011 (Blocking IO)**: Trong hàm `async` lại gọi thư viện đồng bộ `json.dump()` và `open()`. Ở network chậm hoặc disk bận, nguyên loop async sẽ nghẽn. Refactor: Dùng `aiofiles`.
* **SMELL-012 (Path API Mix)**: Trong một file, lúc thì dùng `os.path.join()`, lúc dùng `Path(dir) / file`. Refactor: Chuẩn hoá 100% bằng `.resolve()` của Python `pathlib`.
* **SMELL-013 (Var Shadowing)**: Đặt tên biến `loop = asyncio.new_event_loop()` ở tầm Threading, sau đó trong logic lại gọi `for loop in range(3)` gây đè scope.
* **SMELL-014 (Debug Flag)**: `DEBUG = True` được comment out ngay line 40 trong source code thay vì dùng Environment/`dotenv`. Rất dễ rò rỉ log trên máy user nếu build sót.
* **SMELL-015 (Regex DOM)**: Phân tích kết quả DOM rớt ra từ Google trả về bằng Regex thay vì bóc tách chuẩn cấu trúc AST/JSON. Khả năng gãy cao khi Google tối ưu code minification.

<!-- SMELL_APPEND_MARKER — AI append smell mới TRƯỚC dòng này -->
