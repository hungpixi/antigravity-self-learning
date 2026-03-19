---
name: Bug-Fix Patterns & Debugging Playbook
description: Tổng hợp 20+ bug patterns thường gặp từ 14 dự án thực tế của hungpixi, kèm cách fix hiệu quả. Auto-trigger khi debug, fix bug, review code, hoặc audit. Triggers on "debug", "fix bug", "review code", "audit code", "why is this broken", "code review", "tại sao lỗi", "sửa lỗi", "kiểm tra code", "compile error", "runtime error", "logic error".
---

# 🐛 Bug-Fix Patterns & Debugging Playbook

> Skill này được tổng hợp từ audit 14 conversations thực tế (03/2026). Mỗi pattern đều có ví dụ cụ thể từ dự án đã deploy.

## Quy Trình Debug Hiệu Quả Nhất (3-Round Self-Review)

> **Đã chứng minh**: BDR Kit v1.0 — 3 rounds phát hiện 14 issues (8 → 4 → 2), tất cả fix xong trước deploy.

```
Round 1: Syntax + Logic tĩnh
  → Đọc code KHÔNG chạy, tìm lỗi syntax, type mismatch, missing returns
  → Check: hàm có gọi chính nó không? Guard conditions đủ chưa?

Round 2: Runtime + Edge cases
  → Chạy code, test các case biên: lot 0.01, spread cao, empty array
  → Check: giá trị nào là 0? Timeout nào thiếu? State nào không reset?

Round 3: Integration + Platform-specific
  → Test trên platform thật (MT5, TradingView, Browser)
  → Check: Windows paths? Pipe conflicts? Platform limits?
```

---

## CATEGORY 1: MQL5 / Trading Bot

### 🔴 P1: Đệ Quy Vô Hạn (Infinite Recursion)

**Pattern**: Hàm gọi lại chính nó thay vì return giá trị.

```mql5
// ❌ BUG — GetFillingType() gọi lại chính nó
if((fm & SYMBOL_FILLING_IOC) != 0) return GetFillingType(); // INFINITE LOOP!

// ✅ FIX
if((fm & SYMBOL_FILLING_IOC) != 0) return ORDER_FILLING_IOC;
```

**Source**: IchiDCA_CCBSN_V3.mq5 — dòng 184. EA freeze/crash ngay OnInit().

**Checklist kiểm tra**:
- [ ] Mỗi `return` trong hàm có trả giá trị cụ thể không, hay gọi lại chính hàm đó?
- [ ] Hàm recursive có base case rõ ràng?

---

### 🔴 P2: State Không Reset Khi Close All

**Pattern**: `CloseAllOrders()` đóng hết lệnh nhưng quên reset state flags → bot chết cứng.

```mql5
// ❌ BUG — CloseAllOrders() chỉ đóng lệnh, không reset CCBSN state
// Sau CloseAll: g_buyPartialDone = true mãi → bot không mở lệnh mới

// ✅ FIX — Thêm full state reset vào CloseAllOrders()
void CloseAllOrders() {
    // ... đóng lệnh ...
    g_buyPartialDone = false;
    g_sellPartialDone = false;
    g_buyTrailSL = 0;
    g_sellTrailSL = 0;
    g_buyTrailActive = false;
    g_sellTrailActive = false;
}
```

**Source**: IchiDCA_CCBSN_PropFirm.mq5 v2.1. Friday close / risk cut → state stuck.

**Rule**: **Mọi hàm "close all" PHẢI reset tất cả global state liên quan.**

---

### 🟠 P3: Hardcode Filling Type Rồi Retry

**Pattern**: `PlaceOrder()` hardcode `ORDER_FILLING_FOK`, fail rồi mới gọi `GetFillingType()`.

```mql5
// ❌ BUG
g_trade.SetTypeFilling(ORDER_FILLING_FOK);  // Hardcode!
// ... nếu fail:
g_trade.SetTypeFilling(GetFillingType());    // Retry — nhưng GetFillingType() bị bug đệ quy

// ✅ FIX — Set filling 1 lần trong OnInit()
int OnInit() {
    g_trade.SetTypeFilling(GetFillingType());  // 1 lần duy nhất
    return INIT_SUCCEEDED;
}
```

**Rule**: **Filling type, lot size, và các broker-specific configs nên set 1 lần trong OnInit(), không hardcode trong PlaceOrder().**

---

### 🟠 P4: Default Values Không Phù Hợp Instrument

**Pattern**: Default `InpMaxSpread = 3.0` pips — quá thấp cho XAUUSD (spread ~30-40 pips).

```mql5
// ❌ BUG — Spread filter block MỌI lệnh trên Gold
input double InpMaxSpread = 3.0;  // OK cho EURUSD, BLOCK cho XAUUSD

// ✅ FIX — Dùng giá trị phù hợp instrument
input double InpMaxSpread = 50.0;  // Hoặc dùng ATR-based spread filter
```

**Bảng tham chiếu quick defaults**:

| Parameter | EURUSD | XAUUSD | BTCUSD |
|-----------|--------|--------|--------|
| MaxSpread | 3 pips | 50 pips | 100 pips |
| SL Distance | 100-200 pts | 800-2000 pts | 5000+ pts |
| Trailing Start | 50 pts | 200 pts | 1000 pts |
| Trailing Step | 20 pts | 50 pts | 200 pts |

---

### 🟠 P5: Guard Condition Thiếu — Mở Lệnh Khi Đang Trailing

**Pattern**: Trailing close xong → `buyCount = 0` → bot mở lệnh mới ngay, bỏ qua cooldown.

```mql5
// ❌ BUG — ProcessFirstOrder() chỉ check buyCount == 0
if(buyCount == 0 && sellCount == 0) { /* mở lệnh */ }

// ✅ FIX — Thêm guard
if(g_buyPartialDone || g_sellPartialDone) return;  // Đang trailing, KHÔNG mở mới
if(buyCount == 0 && sellCount == 0) { /* mở lệnh */ }
```

**Rule**: **Trước khi mở lệnh, LUÔN check: (1) state machine đang ở đâu, (2) có process khác đang chạy không.**

---

### 🟠 P6: Partial Close Lot Quá Nhỏ → Vòng Lặp Vô Hạn

**Pattern**: Lot 0.01 × 50% = 0.005 → broker reject → closedCount = 0 → TP trigger lại mỗi tick mãi mãi.

```mql5
// ✅ FIX — Fallback khi partial close thất bại
if(closedCount == 0) {
    PrintFormat("⚠ Partial close failed (lot too small). Fallback to close all.");
    CloseAllByType(type);
}
```

**Rule**: **Partial close PHẢI có fallback "close all" khi lot quá nhỏ để close.**

---

### 🟠 P7: Daily Loss Limit Chỉ Dừng Trade, Không Đóng Lệnh

**Pattern**: Risk breach trả `return true` (stop trading) nhưng lệnh lỗ vẫn chạy → DD tiếp tục tăng.

```mql5
// ❌ BUG
if(dailyLoss >= InpDailyLossLimit) return true;  // Chỉ dừng trade MỚI

// ✅ FIX
if(dailyLoss >= InpDailyLossLimit) {
    CloseAllOrders();  // Đóng tất cả trước
    return true;
}
```

---

### 💡 P8: Trailing Timeout — Bot Đứng Mãi

**Pattern**: Sideway sau partial close → trailing không trigger → SL breakeven → bot đứng, tie up margin vô hạn.

```mql5
// ✅ FIX — Thêm timeout
input int InpTrailMaxBars = 50;  // 50 bars M5 = ~4 giờ

if(barsSincePartialClose >= InpTrailMaxBars) {
    CloseAllByType(type);
    PrintFormat("CCBSN TIMEOUT: %d bars since partial close", barsSincePartialClose);
}
```

---

### 💡 P9: Code Có Check Nhưng Không Gọi

**Pattern**: Session filter và spread filter đã viết nhưng `ProcessSignal()` không gọi chúng.

```mql5
// ❌ BUG — Hàm tồn tại nhưng không ai gọi
bool IsInSession() { /* logic đúng */ }
bool IsSpreadOK() { /* logic đúng */ }
void ProcessSignal() { /* KHÔNG check session/spread */ }

// ✅ FIX
void ProcessSignal() {
    if(!IsInSession()) return;
    if(!IsSpreadOK()) return;
    // ... logic signal
}
```

**Source**: ICT System EA v2.0 → v3.0. 2 hàm filter viết xong quên gọi.

**Rule**: **Sau khi viết utility function, grep lại xem nó có được gọi ở đâu không.**

---

## CATEGORY 2: PineScript / TradingView

### 🔴 P10: Label Overflow — Signal Biến Mất

**Pattern**: PineScript giới hạn ~500 labels. Indicator tạo label mỗi bar → label cũ bị xoá → entry signal biến mất.

```pinescript
// ✅ FIX — Lookback limit + compact labels
lookbackBars = input.int(2000, "Show Last N Bars", minval=100, maxval=10000)
inRange = bar_index >= last_bar_index - lookbackBars

// Chỉ tạo label khi trong range
if inRange and entrySignal
    label.new(bar_index, close, "▲", size=size.tiny, tooltip=fullDetails)
```

**Rule**: PineScript luôn cần lookback limit. Label nên `size.tiny` + tooltip chi tiết.

---

### 🟠 P11: SL Quá Sát Entry

**Pattern**: SL = entry ± vài points → quét ngay lập tức. Cần ATR-based SL.

```pinescript
// ❌ BUG — SL 1-5 points, vô nghĩa trên Gold
sl = close - 3  // 3 points = 0.03 pips

// ✅ FIX — ATR-based
atr = ta.atr(14)
sl = close - atr * 1.5  // 800-2000 points, hợp lý
```

---

## CATEGORY 3: Web / Frontend

### 🟠 P12: Tag HTML Thừa Gây Vỡ Layout

**Pattern**: Copy-paste hoặc AI generate ra HTML có tag thừa → layout vỡ tùy browser.

```html
<!-- ❌ BUG — div thừa, không matching -->
<div class="hero">
    <div>
        <h1>Title</h1>
    </div>
</div>
</div>  <!-- TAG THỪA! -->

<!-- ✅ FIX — Dùng HTML validator / grep đếm open vs close tags -->
```

**Rule**: Sau mỗi lần edit HTML, chạy validator hoặc đếm `<div>` vs `</div>`.

---

### 🟠 P13: API Update Partial → Icon/Type Corrupt

**Pattern**: `PUT /api/v1/providers/{name}` chỉ update `url` và `api_key`, bỏ qua `icon`, `label`, `provider_type` → data corrupt.

```rust
// ❌ BUG — PUT chỉ update 2 field
pub async fn update_provider(name, body) {
    update url, api_key only  // icon bị override thành NULL
}

// ✅ FIX — Mở rộng PUT hoặc dùng PATCH
pub async fn update_provider(name, body) {
    // Update ALL fields: url, api_key, icon, label, provider_type
}
```

**Rule**: **REST API update phải update TẤT CẢ fields, hoặc dùng PATCH cho partial update.**

---

### 🟠 P14: CSS Typography Không Nhất Quán

**Pattern**: `h1` = `7xl`, `h2` = `5xl` → quá to, không hierarchy rõ ràng.

```css
/* ✅ FIX — Harmonized scale */
h1 { font-size: 3rem; }     /* 5xl, không phải 7xl */
h2 { font-size: 2.25rem; }  /* 4xl */
h3 { font-size: 1.5rem; }   /* 2xl */
body { font-size: 1rem; }
```

---

## CATEGORY 4: Python / Backend

### 🟠 P15: Windows Path Issues

**Pattern**: Python script dùng `/` path → fail trên Windows. Hoặc hardcode Unix path.

```python
# ❌ BUG
data_path = "/home/user/data/ohlcv.csv"

# ✅ FIX
from pathlib import Path
data_path = Path.home() / "data" / "ohlcv.csv"
```

---

### 🟠 P16: Library Binary Không Cài Được (TA-Lib)

**Pattern**: `TA-Lib` cần C binary, Windows install cực khó → chặn cả pipeline.

```python
# ❌ BUG — Cần compile C library
import talib  # → DLL not found trên Windows

# ✅ FIX — Dùng pure Python alternative
import pandas_ta as ta  # Drop-in replacement, không cần binary
```

**Rule**: **Ưu tiên pure Python libraries cho cross-platform. Nếu cần native binary, document rõ cách install.**

---

### 🟠 P17: API Fallback Khi Provider Fail

**Pattern**: DeepSeek API fail → toàn bộ pipeline chết.

```python
# ✅ FIX — Multi-provider fallback
def call_llm(prompt):
    try:
        return deepseek_api(prompt)
    except Exception:
        print("⚠ DeepSeek failed, switching to Gemini")
        return gemini_api(prompt)
```

**Rule**: **Mọi external API call cần try/except + fallback provider.**

---

## CATEGORY 5: Scripting / DevOps

### 🟠 P18: Bash Arrays Cần `bash` Không Phải `sh`

```bash
# ❌ BUG — sh không hỗ trợ arrays
#!/bin/sh
arr=("a" "b" "c")  # SYNTAX ERROR in sh

# ✅ FIX
#!/bin/bash
arr=("a" "b" "c")  # OK in bash
```

---

### 🟠 P19: `curl | bash` Conflict Với `read` Stdin

**Pattern**: Install script dùng `curl | bash` → stdin bị pipe chiếm → `read` không nhận input từ user.

```bash
# ❌ BUG
curl -sL url | bash
# Script bên trong dùng: read -p "Enter name: " name  → SKIP!

# ✅ FIX — Dùng process substitution hoặc download trước
curl -sL url -o install.sh && bash install.sh
```

---

### 🟠 P20: PowerShell `Push-Location` Stack Overflow

**Pattern**: `Push-Location` trong loop/error không có `Pop-Location` → stack tràn.

```powershell
# ✅ FIX — Dùng try/finally
Push-Location $targetDir
try {
    # ... logic
} finally {
    Pop-Location  # LUÔN pop, kể cả khi error
}
```

---

### 🟠 P22: PyPI Mirror (tuna/Trung Quốc) Gây Download Fail

> 📅 TIL 2026-03-19 — Dự án: MediaCrawler setup

**Pattern**: Project Trung Quốc dùng `[[tool.uv.index]]` trỏ về tuna.tsinghua.edu.cn → fail download khi chạy từ VN/nước khác.

```toml
# ❌ BUG — pyproject.toml
[[tool.uv.index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true

# ✅ FIX — Xóa block trên + xóa uv.lock + chạy lại
# rm uv.lock && uv lock && uv sync
```

**Rule**: **Khi clone project Trung Quốc, CHECK `pyproject.toml` và `uv.lock` cho tuna/aliyun mirror → xóa trước khi `uv sync`.**

---

### 🟠 P23: Windows stdout Encoding Gây Crash Khi Print Unicode

> 📅 TIL 2026-03-19 — Dự án: MediaCrawler

**Pattern**: Terminal Windows dùng encoding khác UTF-8 → crash khi print tiếng Trung/Việt.

```python
# ✅ FIX — Đặt ở TOP file, TRƯỚC mọi import khác
import sys, io
if sys.stdout and hasattr(sys.stdout, 'buffer'):
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

**Rule**: **Mọi Python CLI app xử lý Unicode nên force UTF-8 stdout đầu file.**

---

### 🟠 P24: Playwright CDP Browser Process Leak

> 📅 TIL 2026-03-19 — Dự án: MediaCrawler

**Pattern**: CDP mode launch browser subprocess → nếu app crash/Ctrl+C, browser process zombie.

```python
# ✅ FIX — Register cleanup ở 3 nơi:
import atexit, signal

# 1. atexit
atexit.register(lambda: launcher.cleanup())

# 2. signal handlers (SIGINT, SIGTERM)  
signal.signal(signal.SIGINT, lambda s, f: launcher.cleanup())

# 3. try/finally trong main flow
try:
    await app_main()
finally:
    await asyncio.wait_for(cleanup(), timeout=15.0)  # BOUNDED cleanup
```

**Rule**: **Subprocess nào launch → PHẢI cleanup ở atexit + signal + finally. Cleanup phải có TIMEOUT.**

---

## CATEGORY 6: PostgreSQL / Database

### 🟠 P21: Remote PostgreSQL Timeout (~10-12s)

**Pattern**: Mỗi request tạo TCP connection mới tới VPS Nhật → latency 10-12 giây.

```python
# ❌ BUG — New connection mỗi request
conn = psycopg2.connect(DATABASE_URL)

# ✅ FIX — Connection pool
from psycopg2.pool import SimpleConnectionPool
pool = SimpleConnectionPool(1, 10, DATABASE_URL)  # Min 1, Max 10
conn = pool.getconn()
try:
    # ... query
finally:
    pool.putconn(conn)
```

**Source**: KI `pg-connection-pool-fix`. Giảm từ 10-12s → <100ms.

---

## Quick Reference: Debug Checklist

Khi gặp bug, chạy qua checklist này:

```
□ 1. Hàm có gọi lại chính nó không? (P1)
□ 2. Close/Reset có reset TẤT CẢ state flags? (P2)
□ 3. Hardcode giá trị nào mà nên dynamic? (P3, P4)
□ 4. Guard conditions đủ chưa? (P5, P9)
□ 5. Edge case: value = 0, lot quá nhỏ, array empty? (P6)
□ 6. Risk/Loss limit có THỰC SỰ đóng lệnh? (P7)
□ 7. Process nào chạy mãi không timeout? (P8)
□ 8. Utility function viết xong có gọi chưa? (P9)
□ 9. Platform limits? Labels, memory, connections? (P10, P21)
□ 10. Default values phù hợp instrument/environment? (P4, P11)
□ 11. API update có đủ fields? (P13)
□ 12. Cross-platform: paths, binaries, shell syntax? (P15-P20)
```

## Khi Tạo Code Mới — Anti-Pattern Rules

1. **Mọi hàm recursive PHẢI có base case** trước recursive call
2. **Mọi "close all" PHẢI reset toàn bộ global state**
3. **KHÔNG hardcode broker-specific values** (filling type, lot step) — query từ broker
4. **Mọi external API PHẢI có try/except + fallback**
5. **Mọi process PHẢI có timeout** — không có gì chạy vô hạn
6. **Sau khi viết function, grep xem nó có được gọi không**
7. **Partial operations PHẢI có fallback** khi partial amount quá nhỏ
8. **Input defaults PHẢI document instrument nào phù hợp**
9. **REST API PUT phải update ALL fields** hoặc dùng PATCH
10. **Cross-platform script: test cả bash, sh, PowerShell**

---

## 🧠 TIL Auto-Update Protocol

> **Mô hình TIL (Today I Learned)**: Mỗi khi fix bug hiệu quả xong, AI PHẢI tự động cập nhật skill này.

### Khi Nào Trigger TIL

TIL update được trigger khi **TẤT CẢ** điều kiện sau đúng:
1. Đã fix bug thành công (code compile, test pass, hoặc user confirm OK)
2. Bug pattern **CHƯA** có trong file này (grep trước khi append)
3. Bug đủ "general" để áp dụng lại cho dự án khác (không phải typo đơn thuần)

### Cách Thực Hiện TIL Update

Sau khi fix bug xong, AI thực hiện các bước sau:

```
Step 1: EVALUATE — Bug này có đáng lưu không?
  → Nó có lặp lại được không? (typo thì KHÔNG, logic error thì CÓ)
  → Nó có áp dụng cho dự án khác không?
  → Nó có khiến mình mất >5 phút debug không?

Step 2: CHECK DUPLICATE — Pattern này đã có chưa?
  → Grep SKILL.md tìm keyword liên quan
  → Nếu đã có → BỎ QUA hoặc BỔ SUNG thêm ví dụ vào pattern cũ

Step 3: CLASSIFY — Thuộc category nào?
  → Cat 1: MQL5/Trading Bot
  → Cat 2: PineScript/TradingView  
  → Cat 3: Web/Frontend
  → Cat 4: Python/Backend
  → Cat 5: Scripting/DevOps
  → Cat 6: Database
  → Cat 7+: Tạo category mới nếu cần

Step 4: APPEND — Thêm entry mới theo format chuẩn
  → Dùng Pxx tiếp theo (P22, P23, ...)
  → Format giống các pattern trên
  → PHẢI có: Pattern description, ❌ BUG code, ✅ FIX code, Source, Rule

Step 5: UPDATE METADATA
  → Cập nhật description trong YAML frontmatter (số pattern mới)
  → Thêm vào Debug Checklist nếu quan trọng
  → Thêm vào Anti-Pattern Rules nếu là rule mới
```

### Format Mẫu Cho TIL Entry

```markdown
### 🟠 Pxx: [Tên Bug Pattern Ngắn Gọn]

> 📅 TIL [YYYY-MM-DD] — Dự án: [tên dự án/file]

**Pattern**: [Mô tả ngắn gọn bug pattern, khi nào xảy ra]

\`\`\`[language]
// ❌ BUG — [mô tả]
[code gây bug]

// ✅ FIX — [mô tả]
[code đã fix]
\`\`\`

**Source**: [File/Dự án]. [Mô tả impact].

**Rule**: **[Rule 1 dòng để nhớ]**
```

### Severity Guide

| Icon | Level | Tiêu chí |
|------|-------|----------|
| 🔴 | CRITICAL | Crash, data loss, infinite loop, security hole |
| 🟠 | HIGH | Logic sai, tính năng không hoạt động, performance chết |
| 🟡 | MEDIUM | UI vỡ, UX xấu, code smell |
| 💡 | IMPROVE | Optimization, best practice, nice-to-have |

### Ví Dụ TIL Trigger

```
✅ ĐÁNG LƯU:
- "Fix: async function quên await → race condition" → P22
- "Fix: React useEffect missing dependency → infinite re-render" → P23
- "Fix: MQL5 OrderSend timeout chưa retry" → Append vào P3

❌ KHÔNG ĐÁNG LƯU:
- Fix typo trong variable name
- Thiếu semicolon
- Import sai tên module (1 lần duy nhất)
```

---

## 📋 TIL Changelog

> Mỗi TIL entry mới được log ở đây để track sự phát triển của playbook.

| # | Ngày | Pattern | Dự án | Severity |
|---|------|---------|-------|----------|
| — | 2026-03-18 | P1-P21 (Initial audit) | 14 conversations | Mixed |
| P22 | 2026-03-19 | PyPI Mirror Download Fail | MediaCrawler | 🟠 |
| P23 | 2026-03-19 | Windows stdout UTF-8 | MediaCrawler | 🟠 |
| P24 | 2026-03-19 | Playwright CDP Cleanup Leak | MediaCrawler | 🟠 |

<!-- TIL_APPEND_MARKER — AI append dòng mới vào bảng trên, TRƯỚC dòng này -->
