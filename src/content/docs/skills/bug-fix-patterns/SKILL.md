---
title: "SKILL"
name: Bug-Fix Patterns & Debugging Playbook
description: "Tổng hợp 52+ bug patterns từ 15+ dự án thực tế của hungpixi, kèm cách fix hiệu quả. Auto-trigger khi debug, fix bug, review code, hoặc audit. Triggers on \"debug\", \"fix bug\", \"review code\", \"audit code\", \"why is this broken\", \"code review\", \"tại sao lỗi\", \"sửa lỗi\", \"kiểm tra code\", \"compile error\", \"runtime error\", \"logic error\"."
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

## CATEGORY 7: UI/UX & Design Workflow

### 🟠 P25: CSS Edit Silent Fail → Visual Regression

> 📅 TIL 2026-03-19 — Dự án: VietFi Landing Page

**Pattern**: `replace_file_content` cho CSS không match target (content đã thay đổi hoặc format khác) → edit fail silently → image hiển thị full size thay vì 56px.

```css
/* ❌ BUG — CSS edit fail, images hiển thị raw ở kích thước gốc */
/* Không có .vet-level__img rule → ảnh 200x200 full size trên trang */

/* ✅ FIX — Sau mỗi CSS edit, KIỂM TRA bằng 1 trong 3 cách */
/* 1. view_file lại CSS để confirm rule đã xuất hiện */
/* 2. Browser screenshot kiểm tra visual */
/* 3. grep rule name trong CSS file */
```

**Rule**: **Sau mỗi CSS edit, PHẢI verify rule đã tồn tại trong file. Không được assume edit thành công.**

---

### 🔴 P26: Section Reorder Loses Content — Large Replace Anti-Pattern

> 📅 TIL 2026-03-19 — Dự án: VietFi Landing Page

**Pattern**: Khi reorder các HTML section (A→B→C thành B→A→C), dùng 1 replace lớn bao cả 3 section → quên include section C (FAQ) → mất hoàn toàn.

```html
<!-- ❌ BUG — Replace cả block Dành cho ai? + FAQ + Vẹt Vàng -->
<!-- Chỉ viết lại Vẹt Vàng + Dành cho ai?, QUÊN FAQ -->
<!-- FAQ biến mất hoàn toàn khỏi trang -->

<!-- ✅ FIX — Khi reorder sections: -->
<!-- 1. Đếm sections TRƯỚC replace: 6 sections -->
<!-- 2. Đếm sections SAU replace: phải vẫn là 6 -->
<!-- 3. Hoặc dùng nhiều edit nhỏ: cut section A + paste ở vị trí mới -->
```

**Rule**: **Khi di chuyển sections, ĐẾM sections trước/sau. Dùng cut+paste (2 edits nhỏ) thay vì 1 replace lớn thay thế cả block.**

---

### 💡 P27: AI Image Generation Style Inconsistency

> 📅 TIL 2026-03-19 — Dự án: VietFi Landing Page Mascot

**Pattern**: Gen 5 mascot images riêng lẻ → mỗi ảnh style khác nhau (realistic vs cartoon vs chibi). Dù cùng prompt cũng không consistent.

```
❌ Approach 1: Gen từng ảnh riêng → 5 styles khác nhau, không match
❌ Approach 2: Gen với ImagePaths reference → gần hơn nhưng vẫn không identical
❌ Approach 3: Gen "simple icon style" → vẫn mỗi con 1 kiểu

✅ Giải pháp đúng cho character consistency:
1. Dùng 1 base character (mascot sly) → overlay accessories bằng CSS/SVG
2. Thuê illustrator vẽ 1 bộ từ 1 art style
3. Dùng vector tool (Figma/Illustrator) tự vẽ variations từ 1 base
4. Chấp nhận emoji-only cho prototype, ảnh thật khi production
```

**Rule**: **AI image gen KHÔNG đảm bảo style consistency giữa các ảnh. Với character sets, dùng 1 base + CSS overlay, hoặc thuê illustrator.**

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
□ 13. CSS edit đã thực sự apply chưa? (P25)
□ 14. Section reorder có mất content không? (P26)
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
11. **Recharts Tooltip/Label formatter dùng `unknown` + cast**, không trust TS types
12. **Tailwind utilities (`ring-*`, `shadow-*`) KHÔNG dùng trong inline `style={{}}`** — dùng `border`/`outline`
13. **Lucide-react icons dùng `color` prop**, KHÔNG dùng `style={{ color }}`. Khai báo type `{ className?: string; color?: string }`

---

## 🧠 TIL Auto-Update Protocol

> **Mô hình TIL (Today I Learned)**: Mỗi khi fix bug hiệu quả xong, AI PHẢI tự động cập nhật skill này.
> **Tích hợp Memory Protocol**: Pattern nào đủ general → tạo thêm feedback memory trong `~/.gemini/antigravity/memory/`

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

Step 6: MEMORY SYNC (nếu đủ general)
  → Nếu pattern áp dụng được ngoài phạm vi bug-fix (vd: architectural preference, workflow)
  → Tạo/update feedback memory: `memory/feedback_*.md`
  → Update `memory/MEMORY.md` index
  → Dùng format: rule → **Why:** → **How to apply:**
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
| P25 | 2026-03-19 | CSS Edit Silent Fail → Visual Regression | VietFi Landing Page | 🟠 |
| P26 | 2026-03-19 | Section Reorder Loses Content | VietFi Landing Page | 🔴 |
| P27 | 2026-03-19 | AI Image Gen Style Inconsistency | VietFi Landing Page | 💡 |
| P28 | 2026-03-19 | VieNeu-TTS venv dependency conflict (numpy/tokenizers) | vietfi-advisor TTS | 🟠 |
| P29 | 2026-03-19 | VieNeu-TTS GGUF context window overflow khi voice cloning | vietfi-advisor TTS | 🔴 |
| P30 | 2026-03-19 | Python f-string dict literal SyntaxError | vietfi-advisor TTS | 🟠 |
| P31 | 2026-03-19 | Demucs 4.0+ cần torchcodec không tương thích Windows | vietfi-advisor TTS | 🟠 |
| P32 | 2026-03-19 | Recharts Tooltip formatter type mismatch | VietFi Dashboard | 🟠 |
| P33 | 2026-03-19 | CSS `ringColor` không phải valid CSS property | VietFi Dashboard | 🟠 |
| P34 | 2026-03-19 | Lucide-react icons không accept `style` prop | VietFi Dashboard | 🟠 |
| P35 | 2026-03-20 | Vercel AI SDK v6 Data Stream Protocol format sai → useChat không render | VietFi Chatbot | 🔴 |
| P36 | 2026-03-20 | useChat setMessages callback với parts format → message không hiện | VietFi Chatbot | 🔴 |
| P37 | 2026-03-20 | Web Speech API không có giọng vi-VN → fallback giọng EN đọc tiếng Việt | VietFi TTS | 🟠 |
| P38 | 2026-03-20 | edge-tts-universal API mismatch: docs vs actual (constructor args, Blob output) | VietFi TTS | 🟠 |
| P39 | 2026-03-20 | replace_file_content xóa state declarations khi replace block code lớn | VietFi Chat Component | 🔴 |
| P40 | 2026-03-20 | Framer Motion character animation từ PNG tĩnh — không khả thi | VietFi Mascot | 💡 |
| P41 | 2026-03-20 | Local-first chat: tách logic client-side thay vì format server response | VietFi Chat Architecture | 💡 |
| P42 | 2026-03-20 | PowerShell curl syntax khác Bash — cần Invoke-WebRequest | DevOps Testing | 🟡 |
| P43 | 2026-03-20 | Playwright browser_press_key không hỗ trợ Unicode Vietnamese (ă, ở, ệ) | Browser Testing | 🟠 |
| P44 | 2026-03-20 | Node.js edge runtime không compatible với edge-tts-universal | VietFi API Route | 🟠 |
| P45 | 2026-03-20 | JSON.stringify escape cho data stream protocol thay vì manual escape | VietFi Chat | 🟠 |
| P46 | 2026-03-20 | Python inline `from X import Y()` trong expression → SyntaxError | Telegram Scraper | 🟠 |
| P47 | 2026-03-20 | Telegram channel ID format: URL đã bao gồm prefix 100 | Telegram Scraper | 🟠 |
| P48 | 2026-03-20 | Reuse Telethon session file thay vì re-auth OTP mỗi lần | Telegram Scraper | 💡 |
| P49 | 2026-03-20 | PowerShell f-string quoting fail với `{}` brackets → dùng script file | Telegram Scraper | 🟠 |
| P50 | 2026-03-20 | Skip large media (>50MB) khi scrape để tránh block pipeline | Telegram Scraper | 💡 |
| P51 | 2026-03-20 | Keyword-based NLP: 1 message thuộc nhiều categories → dùng list thay vì single | Telegram Analyzer | 💡 |
| P52 | 2026-03-20 | Regex `\b[A-Z]{3}\b` match quá rộng → cần whitelist stock codes | Telegram Analyzer | 🟠 |
| P53 | 2026-03-20 | `datetime.fromisoformat()` xử lý timezone offset tự động từ Python 3.7+ | Telegram Analyzer | 💡 |
| P54 | 2026-03-20 | JSON default serializer cho datetime: `json.dump(default=serialize_datetime)` | Telegram Scraper | 💡 |
| P55 | 2026-03-20 | Telethon `get_entity()` cần channel ID dạng `-100XXXXXXXXXX` (signed int64) | Telegram Scraper | 🟠 |
| P56 | 2026-03-20 | `client.start(phone=PHONE)` auto-handles OTP nếu đã có session file | Telegram Scraper | 💡 |

| P57 | 2026-03-21 | Bịa Data (Data Hallucination) khi viết Báo Cáo | Report Generation | 🔴 |
| P58 | 2026-03-21 | Scraper mù HTML5 Canvas (TradingView) | tv-vision-ocr | 🔴 |
| P59 | 2026-03-21 | vnstock API Rate Limit (TCBS 404) | Data Fetching | 🟠 |
| P60 | 2026-03-22 | WSL Update `Class not registered` | OpenClaw Setup | 🔴 |
| P61 | 2026-03-22 | Docker named volume EACCES (root owner vs node user) | OpenClaw Setup | 🔴 |
| P62 | 2026-03-22 | OpenClaw `auth-profiles.json` format v2026.2.19+ | OpenClaw Setup | 🟠 |
| P63 | 2026-03-22 | `docker cp` tạo file thuộc root → container user không đọc được | Docker General | 🔴 |
| P64 | 2026-03-22 | Supabase hybrid sync: localStorage (instant) + Supabase (background) | VietFi Advisor | 💡 |
| P65 | 2026-03-22 | Supabase client without generated types → `any` cast needed | VietFi Advisor | 🟠 |
| P66 | 2026-03-22 | AttributeError: FetchedTranscriptSnippet object has no attribute 'get' | YouTube Analyzer | 🔴 |
| P67 | 2026-03-26 | API Crawling Webgia/DOM quá bấp bênh → Graceful Degradation Bằng Nội Suy | VietFi Advisor | 💡 |
| P68 | 2026-03-28 | Windows `npx` vs `npx.cmd` Process Spawn Fail (MCP) | Antigravity IDE Setup | 🔴 |
| P69 | 2026-03-29 | MetaEditor Backtest Button Disabled (Out of Data Folder) | MQL5 Trading Bot | 🟡 |
| P70 | 2026-03-29 | React Hooks Conditional Execution (Early Return) | ERP Project (Next.js) | 🔴 |
| P71 | 2026-03-30 | Windows batch file CMD popup khi relaunch IDE | MPA Extension Fork | 🟠 |
| P72 | 2026-03-30 | VSCode extension poll interval quá chậm (2s) | MPA Extension Fork | 🟠 |
| P73 | 2026-03-30 | Step input required không auto-expand → accept bị block | MPA Extension Fork | 🟠 |
| P74 | 2026-04-02 | Chạy asyncio blocks Event Loop của PyQt6 GUI → App đứng hình | VEO_TOOL | 🔴 |
| P75 | 2026-04-02 | `asyncio.wait_for` không catch TimeoutError làm chết worker loop | VEO_TOOL | 🔴 |
| P76 | 2026-04-02 | Chrome Zombie Processes rò rỉ RAM khi dùng CDP | VEO_TOOL | 🟠 |
| P77 | 2026-04-02 | Socket Open != CDP Ready (Race condition trên port 9222) | VEO_TOOL | 🟠 |
| P78 | 2026-04-02 | Lỗi `shutil.rmtree` permission denied do tiến trình Chrome tắt chậm | VEO_TOOL | 🟠 |
| P79 | 2026-04-02 | 403 Block Rate Limit Loop Vô Tận | VEO_TOOL | 🔴 |
| P80 | 2026-04-02 | PyQt6 Crash khi update UI widget từ Background Thread | VEO_TOOL | 🔴 |
| P81 | 2026-04-02 | Playwright Context Invalidation do điều hướng trang trước khi DOM stable | VEO_TOOL | 🟠 |
| P82 | 2026-04-02 | Mất Token vì xoá toàn bộ Profile thay vì chỉ xoá Cache/Cookies | VEO_TOOL | 🔴 |
| P83 | 2026-04-02 | Ẩn Cửa Sổ Chrome (`hide_window`) bằng PowerShell thay vì Playwright Headless | VEO_TOOL | 💡 |
| P84 | 2026-04-04 | Dấu hai chấm (:) không escape trong YAML Frontmatter phá hỏng Parser | System Workflows | 🔴 |
| P85 | 2026-04-04 | Lệnh Vercel `login` thành công nhưng CLI/MCP vẫn báo lỗi Token Invalid do dính Global Env Vars cũ | Vercel Deployment | 🔴 |
| P86 | 2026-04-06 | Auto-Clicker Bot Scope Creep Khớp Sai Element (Chat Send Button) | Antigravity Auto Accept | 🔴 |
| P87 | 2026-04-06 | Lỗi 500 Vercel Serverless khi fetch Youtube do dải IP Web bị chặn (Bot Check) | YT SlideX | 🔴 |
| P88 | 2026-04-06 | Lỗi 404 Alias Vercel: project name != vercel.json name tạo alias hỏng | Vercel Deployment | 🟠 |
| P89 | 2026-04-07 | MQL5 nested ternary `a ? b : c ? d : e` compile error | Phoenix DCA Pro | 🟠 |
| P90 | 2026-04-07 | MQL5 unary negation trước cast/MathMin: `-(int)X` và `-MathMin()` | Phoenix DCA Pro | 🟠 |
| P91 | 2026-04-07 | Cloudflare HTTP 403 Block trên Headless Crawl4AI | Kháng Bot Crawler | 🔴 |
| P92 | 2026-04-07 | Vue AST Static Hoisting chặn Reactivity trong Minified Chunks | WebGL Portfolio Clone | 🟠 |
| P93 | 2026-04-07 | Lỗi Astro.glob bị deprecate trong Astro 5.0+ gây build crash | WebGL Portfolio Clone | 🔴 |
<!-- TIL_APPEND_MARKER — AI append dòng mới vào bảng trên, TRƯỚC dòng này -->

---

### P91 - Cloudflare HTTP 403 Block trên Headless Crawl4AI

**Dự án:** Knowledge Agent Crawler  
**Ngày:** 2026-04-07  
**Severity:** 🔴 CRITICAL

**Triệu chứng:**
Khi sử dụng thư viện `crawl4ai` (ngay cả khi bật `magic=True` hoặc `headless=False`), hệ thống bot protection của Cloudflare hoặc WordPress WAF vẫn detect request là bot automation và trả về lỗi HTTP 403. Website không nhả DOM cho chromium.

**Root Cause:**
Hệ thống security tiên tiến nhận diện signature của Playwright/Puppeteer ở tầng Network hoặc Browser Fingerprint, từ chối serve HTML content.

**Fix:**
Sử dụng kiến trúc Fallback: Nếu browser crawl thất bại (403), bắt Exception/Success==False, lập tức dùng `aiohttp.ClientSession` hoặc thư viện HTTP chuẩn (requests/httpx) để get mã nguồn RAW HTML tĩnh với User-Agent người dùng thật. Sau đó passthrough chuỗi RAW HTML này thẳng vào method `crawler.arun(url=f"raw:{html_text}")` của Crawl4AI để tiếp tục tận dụng pipeline bóc tách Markdown BM25 mà không bị WAF chặn IP thêm.

```python
# ❌ BUG — Crawler fail không có phương án 2
result = await crawler.arun(url=url, config=run_config, magic=True)
if not result.success: raise Exception("Blocked by 403")

# ✅ FIX — Thêm aiohttp Fallback
if not result.success:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={'User-Agent': 'Mozilla/5.0...'}) as resp:
            html = await resp.text()
            raw_result = await crawler.arun(url=f"raw:{html}", config=run_config)
            return raw_result.markdown.fit_markdown
```

---

### P87 — Serverless IP Block: Vercel / Next.js API không thể vượt bot check của Youtube

**Dự án:** YT SlideX (Next.js)  
**Ngày:** 2026-04-06  
**Severity:** 🔴 CRITICAL

**Triệu chứng:** Khi chạy `play-dl` hoặc `ytdl-core` hoặc custom API Server nội bộ của Next.js (chạy trên hạ tầng Vercel Serverless/Edge) để fetch luồng MP4 từ URL Youtube, hệ thống luôn báo lỗi 500: `While getting info from youtube: "Sign in to confirm you’re not a bot"`. Trong khi đó, chạy cùng source code đó ở Localhost (IP gia đình) thì thành công.

**Root Cause:**
Youtube cấm và thắt chặt các hệ thống tự động cào dữ liệu từ các ASN nổi tiếng (ví dụ AWS/Vercel Data Centers). Do các API Route `/api/youtube` chạy bằng HTTP trên Node, Google dễ dàng chặn requests từ IP của Vercel (bắt sign-in/captcha). Dù dùng thư viện nào, miễn là IP bị chặn gốc, toàn bộ kết nối bị treo 500.

**Fix:**
* **Chiến thuật thay đổi kiến trúc (Pivot):** Tránh Server-Side fetching khi hạ tầng IP bị thắt chặt. Chuyển sang **100% Client-side xử lý File Upload** thay vì yêu cầu User dán link. UI `<input type="file" />` -> Client fetch file tĩnh vào RAM -> ffmpeg.wasm chạy hoàn toàn độc lập tại máy Local người dùng, triệt tiêu sự phụ thuộc CORS và Server Blocks.  
* **Hoặc (Dùng External APIs):** Giao Fetching cho các hệ sinh thái xử lý tải như API public của `cobalt.tools` hoặc `Invidious`, thay vì bắt Vercel serverless functions tự làm.

---

### P88 - Vercel CLI Deprecated Project `name` tạo Alias 404 ảo

**Dự án:** Vercel Deployment  
**Ngày:** 2026-04-06  
**Severity:** 🟠 HIGH

**Triệu chứng:** Deploy bằng lệnh terminal `vercel --prod` xuất ra CLI log `✅ Production: https://yt-slidex-xxx.vercel.app` và `🔗 Aliased: https://yt-slide.vercel.app`. Nhưng khi user click vào link rút gọn `yt-slide.vercel.app` bị dính cửa sổ báo 404 `DEPLOYMENT_NOT_FOUND`.

**Root Cause:**
Tại config `vercel.json` chứa thuộc tính `name` (deprecated) bị định danh sai lệch với project slug (yt-slidex). Điều này dẫn tới Vercel tự động gán ngẫu hứng 1 Alias Domain nhưng lại không resolve thành công tới Production Release đã push.

**Fix:**
Dựa vào Production URL chưa alias (`<projectname>-<hash>-<user/org>.vercel.app`) để xác nhận API/Page đã triển khai ổn định chưa. Sau đó loại bỏ trường `name` ra khỏi `vercel.json` và setup lại domain thông qua lệnh `npx vercel domains`. Mọi phán đoán 404 nên check kĩ nguồn gốc domain hay app crash.

---

### P75-P83 — VEO_TOOL Architectural Bug Fixes

**Dự án:** VEO_TOOL (Video Automation)  
**Ngày:** 2026-04-02  

* Mở rộng thêm 9 mẫu Bug/Fix từ kiến trúc VEO_TOOL:
* **P75 (TimeoutError Uncaught)**: Khi gọi `await asyncio.wait_for(...)`, nếu thiếu `except asyncio.TimeoutError:`, worker loop sẽ sụp đổ hoàn toàn. Cần bao bọc kĩ toàn bộ Async Calls tương tác với Network.
* **P76 (Zombie Process)**: Việc kill App PyQt6 không tự động kill Chrome subprocess. Giải pháp: dùng `atexit` hoặc gọi WMI (`Get-CimInstance Win32_Process`) để dò PID Chrome command line `--remote-debugging-port` và taskkill.
* **P77 (CDP Race Condition)**: Socket check `port 9222` mở chưa là không đủ. Port có thể mở nhưng endpoint `/json/version` của CDP chưa khởi động xong. Fix: Poll HTTP endpoint thay vì chỉ dùng `socket.connect_ex`.
* **P78 (Permission Denied `shutil.rmtree`)**: Xoá folder Chrome profile gặp lỗi vì file `LOCK` hoặc SQLite DB chưa nhả handle. Fix: Bọc `try-except` từng file, dùng `time.sleep(1)` fallback loop.
* **P79 (Ban/403 Loop)**: Gặp lỗi 403 Google/Cloudflare (Rate Limit), bot retry điên cuồng 0s delay → IP Ban. Fix: Exponential backoff + clear cookie sau 2 lần failed liên tiếp.
* **P80 (PyQt Cross-Thread Exception)**: Background worker call `self.ui.label.setText()`. Fix: Bắt buộc dùng `@pyqtSignal` để truyền string lên Main UI Thread.
* **P81 (Context Invalidation)**: Gọi `locator.click()` khi page đang redirect → exception `target closed`. Fix: `wait_for_selector` trước hành động.
* **P82 (Nuke Token)**: Xoá thư mục `User Data` để clean rác Automation → đi tong Login Session (`Login Data`). Fix: Phân vùng xoá, chỉ xoá `Cache`, giữ nguyên `Cookies` và `Login Data`.
* **P83 (Fake Headless bypass Bot Detection)**: Chạy Playwright với flag `headless=new` dễ bị vạch trần. Fix: Chạy `headless=false` nhưng kéo toạ độ cửa sổ ra ngoài màn hình (X: -9999) bằng flag PowerShell/Win32.

---

### P74 — Chạy asyncio blocks Event Loop của PyQt6 GUI → App đứng hình

**Dự án:** VEO_TOOL (Video Automation)  
**Ngày:** 2026-04-02  
**Severity:** 🔴 CRITICAL

**Triệu chứng:**
Khi ấn nút chạy `asyncio.run()` (hoặc `loop.run_until_complete`) từ một callback/signal của PyQt6 UI để kết nối Playwright CDP `browser = await p.chromium.connect_over_cdp(...)`, toàn bộ cửa sổ GUI bị treo (Not Responding) cho tới khi operation chạy xong.

**Root Cause:**
`asyncio` loop chạy đồng bộ trên thread chính của ứng dụng PyQt6. Thread chính này có nhiệm vụ vẽ UI (Event Loop Qt). Việc chiếm quyền xử lý bằng một loop `async` sẽ khoá hoàn toàn các mouse clicks và repaint của cửa sổ.

**Fix:**
Chạy mã `asyncio` cô lập trong một sub-thread thông qua `threading.Thread`.
```python
# ❌ BUG: Chạy trực tiếp trên UI thread
def on_btn_click(self):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(connect_cdp()) # TREO UI
    
# ✅ FIX: Bọc vào Threading
def on_btn_click(self):
    def _runner():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(connect_cdp())
        finally:
            loop.close()
            
    worker = threading.Thread(target=_runner, daemon=True)
    worker.start()
```

**Lesson:** **Tách biệt GUI Loop và Asyncio Loop.** Không bao giờ start event loop của `asyncio` trên Main Thread đang chạy Qt Application. Bạn buộc phải Spawn Threading riêng biệt để giữ giao diện trơn tru.

---

### P70 — React Hooks Conditional Execution (Early Return)

**Dự án:** ERP Project (Next.js)  
**Ngày:** 2026-03-29  
**Severity:** 🔴 CRITICAL

**Triệu chứng:**
Next.js lint (hoặc ESLint) báo lỗi `react-hooks/rules-of-hooks` và dự án không thể build được. Lỗi thông báo cụ thể: `Error: React Hook "useState" is called conditionally. React Hooks must be called in the exact same order in every component render.`

**Root Cause:**
Component có chứa lệnh `if (condition) return ...;` (hoặc early return) nằm ĐẰNG TRƯỚC các câu lệnh gọi hook `useState`, `useEffect`. Do React dựa vào thứ tự index để nhớ state, việc chạy nhánh `return` sớm khiến các móc nối state/effects bị đứt gãy, gây crash render tree.

**Fix:**
```tsx
// ❌ BUG: Early return phía trên Hooks
const pathname = usePathname();

if (exclusionArray.includes(pathname)) {
  return null; // THOÁT SỚM
}

const [isFullscreen, setIsFullscreen] = useState(false); // LỖI (hook không được chạy ổn định)
useEffect(() => { ... }, []);

// ✅ FIX: Di dời TẤT CẢ Hooks lên trước lệnh rẽ nhánh
const pathname = usePathname();
const [isFullscreen, setIsFullscreen] = useState(false);
useEffect(() => { ... }, []);

// Đã định nghĩa xong state/effects -> được phép rẽ nhánh
if (exclusionArray.includes(pathname)) {
  return null; 
}
```

**Lesson:** **Sự sống còn của React Hooks là thứ tự dòng chảy (Flow order).** TUYỆT ĐỐI không đặt bất kỳ lệnh `return` nào nằm phía trước các block khai báo `useState`, `useEffect`, `useRef` hay custom hooks trong functional component.

---

### P69 — MetaEditor Backtest Button Disabled (Out of Data Folder)

**Dự án:** MQL5 Trading Bot (CCBSN)  
**Ngày:** 2026-03-29  
**Severity:** 🟡 MEDIUM

**Triệu chứng:**
Khi mở file source code MQL5 (`.mq5`) trực tiếp từ ổ cứng (ví dụ: `D:\Projects\...`), nút bấm "Start Debugging" hoặc "Compile" có thể chạy, nhưng nút "Start Strategy Tester/Backtest" (icon Play màu xanh lá) trên thanh công cụ của MetaEditor bị mờ đi hoàn toàn. User thắc mắc "tại sao không hiện nút lên để backtest?".

**Root Cause:**
MetaEditor chỉ cho phép liên kết trực tiếp (Seamless Debugging/Backtesting) giữa file `.mq5` và ứng dụng MetaTrader 5 nếu file mã nguồn đó đang nằm **bên trong thư mục gốc của Terminal (`MQL5\Experts\` hoặc `MQL5\Indicators\`)**. Nếu mở file từ một thư mục bên ngoài độc lập (external path), MetaEditor sẽ coi đây giống như file text thông thường, nó vẫn compile được ra `.ex5` ngay tại ổ D:, nhưng MT5 không tự động load file đó lên Tester.

**Fix:**
```cmd
// ❌ Cách sai: Copy thủ công file từ D:\ sang C:\...\MQL5\Experts\ mỗi lần sửa code
// Rất mất thời gian và dễ nhầm phiên bản.

// ✅ Cách đúng: Dùng thư mục nối (Directory Junction) mklink /J
// Windows DOS Command (Không cần quyền Admin như Symlink):
mklink /J "C:\Users\...\Terminal\...\MQL5\Experts\Ten_Project" "D:\Cá nhân\Trading\Ten_Project"
```
Khi setup Junction xong: Mở MetaEditor của MT5 -> Mở Navigator -> MQL5 -> Experts -> Ten_Project -> Mở file. Lúc này mọi thao tác sửa code ở D: sẽ đồng bộ 100% thời gian thực nhưng lại được MT5 ghi nhận là nằm trong lõi phần mềm. Nhấn `F7` để dịch và `F5` để Backtest mượt mà.

**Lesson:** Khi lập trình bot MT5 bằng VS Code hoặc lưu source code ngoài ổ đĩa khác để dùng Git, **bắt buộc phải setup Directory Junction (`mklink /J`)** nối thư mục code vào bên trong `MQL5\Experts\` của cấu trúc Terminal. Tuyệt đối không copy thủ công để tránh rủi ro version mismatch.

---

### P68 — Windows `npx` vs `npx.cmd` Process Spawn Fail (MCP)

**Dự án:** Antigravity IDE Setup (MCP Configuration)  
**Ngày:** 2026-03-28  
**Severity:** 🔴 CRITICAL

**Triệu chứng:**
Lỗi `fetch failed` hoặc `calling "tools/list"` fails silently khi khởi tạo MCP Server (như `github-mcp-server` hoặc `supabase-mcp-server`) trên môi trường Windows. IDE không thể giao tiếp với tool.

**Root Cause:**
Node.js `spawn` hoặc `exec` trên Windows gặp khó khăn khi thực thi file không có đuôi mở rộng rõ ràng (như `npx` thay vì `npx.cmd`). Mặc dù trên Git Bash hoặc một số terminal có thể tự resolve, nhưng khi hệ thống tự động spawn process thô, nó sẽ fail vì không tìm thấy executable `npx`. Đối với MCP server (nền tảng giao tiếp qua stdout/stdin pipe), process crash ngầm sẽ làm API fetch bị fail.

**Fix:**
```json
// ❌ BUG: Cấu hình MCP dùng lệnh npx chung chung (fail trên Windows)
"command": "npx",
"args": ["-y", "@modelcontextprotocol/server-github"]

// ✅ FIX: Luôn cấu hình npx.cmd dứt khoát trên môi trường Windows
"command": "npx.cmd",
"args": ["-y", "@modelcontextprotocol/server-github"]
```

**Lesson:** Khi config bất kỳ tool CLI nào chạy ngầm (MCP, background agents, auto scripts) trên Windows thông qua process spawn/exec, **luôn ưu tiên dùng đuôi `.cmd` hoặc `.bat` (ví dụ `npx.cmd`)** để bảo đảm OS có thể thực thi chính xác file wrapper thay vì gặp lỗi `ENOENT`.

---

### P66 — AttributeError trên youtube_transcript_api do thay đổi cấu trúc Object

**Dự án:** YouTube Stock Analyzer  
**Ngày:** 2026-03-22  
**Severity:** 🔴 CRITICAL

**Triệu chứng:**
Lỗi `AttributeError: 'FetchedTranscriptSnippet' object has no attribute 'get'` khi dùng `.fetch()` từ thư viện `youtube_transcript_api`. Kịch bản bị crash hoàn toàn, dừng workflow.

**Root Cause:**
Tại các bản cũ, `.fetch()` trả về một list các dictionary `{'text': '...', 'start': 0.0}` nên code dùng `item.get('text')` hợp lệ. Ở bản mới nhất, cấu trúc trả về một list các class objects (`FetchedTranscriptSnippet`). Object này không có định nghĩa hàm `.get()`.

**Fix:**
```python
# ❌ BUG: Cố lookup dictionary key trên class Object (chỉ map được với dict)
text = item.get('text', '')
start = item.get('start', 0.0)

# ✅ FIX: Kiểm tra type linh hoạt bằng hasattr để fallback giữa Object và Dict
text = item.text if hasattr(item, 'text') else item.get('text', '')
start = item.start if hasattr(item, 'start') else item.get('start', 0.0)
```

**Lesson:** Khi xử lý JSON-like output từ thư viện API nội bộ (đặc biệt là wrapper chưa specify API model cứng), cấu trúc trả về có thể thay đổi ngầm từ `dict` sang `Object` bất kỳ lúc nào. Luôn kiểm tra cấu trúc động (Type Ducking) thông qua `hasattr` trước khi gọi `.get()` hoặc key indexing để hệ thống an toàn ở đa phiên bản.

---

### P29 — VieNeu-TTS GGUF Context Window Overflow khi Voice Cloning

**Dự án:** vietfi-advisor TTS  
**Ngày:** 2026-03-19  
**Severity:** 🔴 HIGH

**Triệu chứng:**
- `tts.infer(ref_audio=..., ref_text=...)` trả về file WAV chỉ ~1964 bytes (gần empty)
- Terminal hiển thị: `llama_context: n_ctx_per_seq (2048) <`
- Sau đó: `ValueError: Requested tokens (2072) exceed context window of 2048`

**Root Cause:**
VieNeu-TTS GGUF model (Q4, 0.3B) có context window cứng 2048 tokens. Khi voice cloning, ref_audio encoding đã chiếm ~1500-1700 tokens, phần còn lại không đủ cho text. Bất kể text ngắn đến đâu vẫn overflow.

**Fix:**
```python
# ❌ Fail: ref_audio + text > 2048 tokens dù text cực ngắn
audio = tts.infer(text="Xin chào", ref_audio="clip.wav", ref_text="transcript")

# ✅ Fix Option 1: Dùng preset voices (không cần ref_audio)
voices = tts.list_preset_voices()
voice_data = tts.get_preset_voice("Ly")
audio = tts.infer(text="Xin chào", voice=voice_data)

# ✅ Fix Option 2: Dùng PyTorch (non-GGUF) backbone — context window lớn hơn
tts = Vieneu(backbone_repo="pnnbao-ump/VieNeu-TTS-0.5B", backbone_device="cpu")

# ✅ Workaround: Pitch shift preset voice để ra giọng mong muốn
# Dùng ffmpeg: asetrate*rate_mult + atempo=1/rate_mult
```

---

### P67 — API Web Scraper DOM Quá Bấp Bênh → Áp Dụng Graceful Degradation Bằng Tự Suy

**Dự án:** VietFi Advisor (Lõi Định Giá Vàng Webgia/DOJI)  
**Ngày:** 2026-03-26  
**Severity:** 💡 IMPROVE

**Triệu chứng:**
Khi cào thẻ HTML (scraping DOM) từ các trang Việt Nam như webgia.com, giavang.vn. Chẳng may các trang này đổi thẻ `<table>` hoặc Class Name. Lần Crawler tiếp theo QuerySelector sẽ fail, Parse Integer ra `NaN`, dẫn đến toàn bộ App user báo lỗi hoặc hiển thị số `$N/A`, phá huỷ Flow trải nghiệm Cố Vấn Đầu Tư của khách.

**Root Cause:**
Code tin tưởng ngây thơ vào 1 Single Point of Failure (chỉ phụ thuộc nguồn DOM ngoài).

**Fix (Graceful Fallback - Nội Suy PnL):**
```tsx
// ❌ Yếu kém: Tin tưởng 100% Cào HTML
const goldData = await getBTMCRing(); 
return goldData.buyPrice; // Tạch là xong phim!

// ✅ Tối ưu: Xây động cơ Toán học Nội suy (Tầng 2) Fallback vô hình
let price = marketData.goldBrands['BTMC_NHAN']?.buy;

if (!price || price === 0 || price < 10000000) {
    // 💡 Tự suy từ giá Global cực nến (XAUUSD * Tỷ Giá VCB + Chênh lệch VN)
    // 1 Lượng = 1.20565 Ounce. Chênh VN = ~3 triệu
    const autoPrice = (marketData.goldUsd * XchangeRate * 1.20565) + 3000000;
    price = autoPrice; 
}
return price / 10; // User nhận Data chuẩn mượt hệt như không có gì xảy ra
```

**Lesson:** Không bao giờ để cấu trúc Core tính toán sinh lợi phụ thuộc vào 1 Website Local Cùi Mía. Phải luôn viết một hàm **Động Cơ Toán Học Tự Phái Sinh (Global Derived Engine)** để làm Tầng Bảo Hiểm cho Data Feeds. 


**Lesson:** GGUF models trade context window for speed. Với voice cloning cần context dài → phải dùng full PyTorch model hoặc preset voices + pitch shift.

---

### P30 — Python f-string Dict Literal SyntaxError

**Dự án:** vietfi-advisor TTS  
**Ngày:** 2026-03-19  
**Severity:** 🟠 MEDIUM

**Triệu chứng:**
```
SyntaxError: f-string: single '}' is not allowed
```

**Root Cause:**
Trong Python f-string, `{}` là delimiter cho expression. Dict literal `{"key": "val"}` bên trong f-string khiến parser nhầm `}` đầu tiên của dict là kết thúc expression.

**Fix:**
```python
# ❌ Sai — parser confuse dấu } của dict
print(f"Result: {{'A': 'nhẹ', 'B': 'vừa'}.get(x)}")

# ✅ Đúng — tách ra variable trước
desc = {"A": "nhẹ", "B": "vừa"}.get(x)
print(f"Result: {desc}")
```

**Lesson:** KHÔNG dùng dict literal trực tiếp trong f-string expression. Luôn tách ra variable.

---

### P31 — Demucs 4.0+ Cần torchcodec Không Tương Thích Windows

**Dự án:** vietfi-advisor TTS  
**Ngày:** 2026-03-19  
**Severity:** 🟠 MEDIUM

**Triệu chứng:**
- `pip install demucs` thành công (v4.0.1)
- Chạy `python -m demucs --two-stems=vocals -n htdemucs` fail với: `ImportError: TorchCodec is required`
- `pip install torchcodec` fail: `torchcodec_core4.dll` không load được

**Root Cause:**
Demucs v4.0+ đã migrate sang torchcodec (thay torchaudio) cho audio I/O, nhưng torchcodec chưa support Windows stable.

**Fix/Workaround:**
```bash
# ✅ Option 1: FFmpeg L-R subtraction (karaoke trick) — không cần Demucs
ffmpeg -i input.wav \
  -af "pan=mono|c0=0.5*c0-0.5*c1,highpass=f=200,lowpass=f=6000,dynaudnorm" \
  -ar 22050 vocal_only.wav

# ✅ Option 2: Downgrade Demucs xuống v3.x (trước khi migrate torchcodec)
pip install demucs==3.0.6

# ✅ Option 3: Dùng Spleeter (Deezer) thay thế
pip install spleeter
python -m spleeter separate -p spleeter:2stems input.wav -o output/
```

**Lesson:** Khi vocal separation cần trên Windows, check torchcodec compatibility trước. FFmpeg karaoke trick (L-R subtraction) là fallback nhanh nhất dù chất lượng thấp hơn AI models.

---

## CATEGORY 8: Next.js / React Dashboard

### 🟠 P32: Recharts Tooltip Formatter Type Mismatch

> 📅 TIL 2026-03-19 — Dự án: VietFi Dashboard

**Pattern**: Recharts `<Tooltip formatter=.../>` TypeScript yêu cầu type `(value: number) => string` nhưng runtime truyền `unknown`. Build fail với `no overload matches this call`.

```tsx
// ❌ BUG — TypeScript strict mode reject
<Tooltip formatter={(value: number) => formatVND(value)} />
// Error: Type '(value: number) => string' is not assignable...

// ✅ FIX — Suppress + cast
{/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
<Tooltip
  formatter={(value: unknown) => formatVND(value as number)}
/>
```

**Rule**: **Recharts v2 TypeScript types không khớp runtime. Dùng `unknown` + cast cho Tooltip formatter, Label, etc.**

---

### 🟠 P33: CSS `ringColor` Không Phải Valid CSS Property

> 📅 TIL 2026-03-19 — Dự án: VietFi Dashboard Budget Page

**Pattern**: Dùng `ringColor` trong `style={{}}` JSX — đây là Tailwind utility class, KHÔNG phải CSS property. TypeScript reject: `'ringColor' does not exist in type Properties`.

```tsx
// ❌ BUG — ringColor là Tailwind concept, không phải CSS
<button
  className={`${selected ? "ring-2 ring-offset-2" : ""}`}
  style={{ backgroundColor: c, ringColor: c }}  // ← TypeScript ERROR
/>

// ✅ FIX — Dùng border thay ring, hoặc dùng pure Tailwind
<button
  className={`border-2 ${selected ? "scale-110 border-white/60" : "border-transparent"}`}
  style={{ backgroundColor: c }}
/>
```

**Rule**: **`ring-*` là Tailwind utility, KHÔNG có CSS equivalent. Trong inline `style={{}}`, dùng `border` hoặc `outline` thay thế. Hoặc dùng pure Tailwind classes.**

---

### 🟠 P34: Lucide-react Icons Không Accept `style` Prop

> 📅 TIL 2026-03-19 — Dự án: VietFi Dashboard Budget Page

**Pattern**: Lucide-react icon components chỉ accept `{ className?: string }` — KHÔNG có `style` prop. Khi cần dynamic color, phải dùng `color` prop thay vì `style={{ color: x }}`.

```tsx
// ❌ BUG — TypeScript error: 'style' does not exist
const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = { Coffee, Home, ... };
const Icon = ICON_MAP[key];
<Icon className="w-4 h-4" style={{ color: pot.color }} />  // ← ERROR

// ✅ FIX — Khai báo type có `color` prop + dùng color thay style
const ICON_MAP: Record<string, React.ComponentType<{ className?: string; color?: string }>> = { Coffee, Home, ... };
<Icon className="w-4 h-4" color={pot.color} />  // ← OK
```

**Rule**: **Lucide-react icons dùng `color` prop (native SVG fill), KHÔNG dùng `style={{ color }}`. Khi tạo dynamic icon maps, khai báo type có `color?: string`.**

---

### Pattern 22: Next.js SSR Hydration Mismatch — localStorage Read
- **Dự án**: VietFi Advisor (03/2026)
- **Triệu chứng**: "Hydration failed because the server rendered text didn't match the client" — server shows default text, client shows localStorage data
- **Nguyên nhân**: Component gọi `getGamification()` (đọc localStorage) trực tiếp trong render → SSR returns defaults, client returns real data → mismatch
- **Fix**:
```tsx
// ❌ BAD: Direct localStorage read during render
export function BadgeGrid() {
  const gam = getGamification(); // FAILS on SSR
  const earned = BADGES.filter(b => b.condition(gam));
  // ... renders "ĐÃ MỞ KHOÁ (1/7)" on client but "CHƯA MỞ KHOÁ" on server
}

// ✅ GOOD: Lazy init with useEffect
export function BadgeGrid() {
  const [mounted, setMounted] = useState(false);
  const [earned, setEarned] = useState<Badge[]>([]);
  useEffect(() => {
    const gam = getGamification();
    setEarned(BADGES.filter(b => b.condition(gam)));
    setMounted(true);
  }, []);
  if (!mounted) return null; // Render nothing until client hydrates
  // ... now safe to render localStorage-dependent content
}
```
- **Rule**: **EVERY "use client" component reading localStorage/sessionStorage MUST: (1) Init with safe defaults, (2) Read storage in useEffect, (3) Return null or skeleton before mount.**
- **Đã áp dụng**: GamificationBar, BadgeGrid, BadgeMiniRow, VetVangFloat, WeeklyReportModal

### Pattern 23: React Infinite Re-render Loop — State Objects in useEffect Deps
- **Dự án**: VietFi Advisor (03/2026)
- **Triệu chứng**: "Maximum update depth exceeded" — component re-renders infinitely
- **Nguyên nhân**: `useEffect(() => {...}, [prevDone, quests])` — `quests` is recreated every render → deps always "change" → infinite loop
- **Fix**:
```tsx
// ❌ BAD: Object/array state in deps
const [prevDone, setPrevDone] = useState(0);
useEffect(() => { ... }, [prevDone, quests]); // quests recreated → infinite

// ✅ GOOD: useRef for mutable tracking
const prevDoneRef = useRef(0);
const questsRef = useRef(quests);
useEffect(() => {
  questsRef.current = quests;
  // compare with prevDoneRef.current
}, [quests.length]); // primitive dep only
```
- **Rule**: **useEffect deps phải là primitive (number, string, boolean) hoặc stable references. KHÔNG bao giờ put object/array trực tiếp — dùng useRef hoặc extract primitive.**

---

## CATEGORY 9: Vercel AI SDK / Chat Integration

### 🔴 P35: Vercel AI SDK v6 Data Stream — useChat Không Render Response

> 📅 TIL 2026-03-20 — Dự án: VietFi Advisor Chatbot

**Pattern**: Tự build data stream response cho `useChat()` hook — format trông đúng nhưng useChat không render message.

```typescript
// ❌ BUG — Tự format data stream, thiếu finish step event
const stream = new ReadableStream({
  start(controller) {
    controller.enqueue(encoder.encode(`0:"${text}"\n`));
    controller.enqueue(encoder.encode(`d:{"finishReason":"stop"}\n`));
    controller.close();
  }
});
// useChat() nhận data nhưng KHÔNG tạo message vào state

// ✅ FIX — Dùng JSON.stringify + thêm finish step event `e:`
const escaped = JSON.stringify(text); // Proper JSON escape
controller.enqueue(encoder.encode(`0:${escaped}\n`));
controller.enqueue(encoder.encode(`e:{"finishReason":"stop","usage":{"promptTokens":0,"completionTokens":0},"isContinued":false}\n`));
controller.enqueue(encoder.encode(`d:{"finishReason":"stop","usage":{"promptTokens":0,"completionTokens":0}}\n`));

// ✅✅ BEST FIX — Bypass hoàn toàn: xử lý phía client, thêm message trực tiếp vào state
```

**Rule**: **ĐỪNG tự build Vercel AI SDK data stream. Hoặc dùng `streamText()` built-in, hoặc xử lý phía client với `setMessages()`. Tự format stream = nguồn bug vô tận.**

---

### 🔴 P36: Client-Side Local-First Thay Vì Server-Side Format

> 📅 TIL 2026-03-20 — Dự án: VietFi Advisor Chatbot

**Pattern**: Scripted response (không cần AI) được xử lý ở server API route → phải format data stream protocol → useChat không render. Chuyển sang xử lý phía client giải quyết triệt để.

```tsx
// ❌ BUG — Server-side scripted response, tự format data stream
// api/chat/route.ts
if (intent !== 'unknown') {
  return createTextResponse(response); // Tự build stream → useChat reject
}

// ✅ FIX — Client-side: check trước khi gọi API
// VetVangChat.tsx
const localReply = tryLocalResponse(text);
if (localReply) {
  setMessages((prev) => [...prev,
    { id: `user-${Date.now()}`, role: "user", parts: [{ type: "text", text }] },
    { id: `bot-${Date.now()+1}`, role: "assistant", parts: [{ type: "text", text: localReply }] },
  ]);
  return; // 0 API calls, render ngay lập tức
}
sendMessage({ text }); // Chỉ gọi AI khi cần
```

**Rule**: **Khi response không cần AI → xử lý phía CLIENT (thêm message trực tiếp vào state). Không cần đi qua API route rồi format stream phức tạp.**

---

### 🟠 P37: Web Speech API Không Có Giọng Việt → Fallback Giọng EN

> 📅 TIL 2026-03-20 — Dự án: VietFi Advisor TTS

**Pattern**: `window.speechSynthesis.getVoices()` không có giọng ti-VN trên nhiều trình duyệt/OS → utterance dùng giọng mặc định (EN) đọc text tiếng Việt → nghe như nói tiếng Anh.

```typescript
// ❌ BUG — Nếu không có giọng Việt, vẫn nói bằng giọng EN
const viVoice = voices.find(v => v.lang.startsWith("vi"));
if (viVoice) utterance.voice = viVoice;
// Không có viVoice → dùng default EN voice → đọc tiếng Việt bằng giọng Anh

// ✅ FIX — Skip nếu không có giọng Việt
if (!viVoice) return; // Im lặng thay vì đọc sai ngôn ngữ

// ✅✅ BEST FIX — Dùng Edge TTS API server-side
const res = await fetch("/api/tts", {
  method: "POST", body: JSON.stringify({ text }),
});
const audio = new Audio(URL.createObjectURL(await res.blob()));
await audio.play();
```

**Rule**: **Web Speech API KHÔNG tin cậy cho tiếng Việt. Dùng Edge TTS (Microsoft, miễn phí) qua server API route để đảm bảo 100% có giọng Việt.**

---

### 🟠 P38: npm Package API Mismatch — Docs vs Actual Runtime

> 📅 TIL 2026-03-20 — Package: edge-tts-universal

**Pattern**: NPM package docs/README nói A, nhưng runtime API khác:
- Docs: `EdgeTTS()` no args → thực tế: `EdgeTTS(text, voice?)` cần args
- Docs: `tts.toBuffer()` → thực tế: không có method này
- Thực tế: `synthesize()` trả `{ audio: Blob, subtitle }` → cần `.arrayBuffer()`

```typescript
// ❌ BUG — Theo docs/guess
const tts = new EdgeTTS();      // Error: text must be a string
tts.synthesize(text, voice);     // Wrong signature
const buf = tts.toBuffer();      // Not a function

// ✅ FIX — Probe actual API trước khi dùng
const tts = new EdgeTTS(text, "vi-VN-HoaiMyNeural");
const result = await tts.synthesize();
const audioBlob = result.audio;  // Blob, not Buffer
const buffer = Buffer.from(await audioBlob.arrayBuffer());
```

**Debug approach khi npm package API không rõ**:
```javascript
// 1. Check constructor
console.log(Object.getOwnPropertyNames(Object.getPrototypeOf(obj)));
// 2. Check instance properties sau khi gọi method
console.log(Object.keys(result));
// 3. Check return type
console.log(result?.constructor?.name); // "Blob", "Buffer", etc.
```

**Rule**: **KHÔNG tin docs của npm packages nhỏ. Probe API bằng `Object.keys()`, `constructor.name`, `typeof` TRƯỚC khi viết production code.**

---

### 🔴 P39: replace_file_content Xóa Mất Declarations Khi Replace Block Lớn

> 📅 TIL 2026-03-20 — Dự án: VietFi Advisor VetVangChat.tsx

**Pattern**: Dùng `replace_file_content` thay thế block code 40 dòng (TTS logic). Block mới không chứa `useState/useRef` declarations vì chúng nằm TRƯỚC block cũ nhưng BÊN TRONG block target → mất `isSpeaking`, `messagesEndRef`, `inputRef`, `lastSpokenIdRef`.

```
❌ Quá trình xảy ra:
1. Target: dòng 85-125 (gồm state declarations + TTS logic)
2. Replacement: chỉ chứa TTS logic mới (KHÔNG có state declarations)
3. Kết quả: 12 lint errors "Cannot find name 'setIsSpeaking'", etc.

✅ Phòng tránh:
1. TRƯỚC khi replace: list TẤT CẢ declarations/imports trong target range
2. Đảm bảo replacement chứa ĐỦ declarations
3. Hoặc: tách replace thành 2 phần — keep declarations, chỉ thay logic
```

**Rule**: **Khi replace_file_content block lớn (>20 dòng), ĐẾM declarations/imports trước và sau. Nếu target chứa state/ref declarations → giữ chúng trong replacement hoặc tách edit nhỏ hơn.**

---

### 💡 P40: Framer Motion Character Animation Từ PNG Tĩnh

> 📅 TIL 2026-03-20 — Dự án: VietFi Advisor Mascot

**Pattern**: Muốn animate character mascot (vẹt) từ 1 ảnh PNG tĩnh. Thử nhiều approach đều fail:
- Framer Motion transform (rotate, scale) → unnatural
- Canvas sprite sheet → cần vẽ nhiều frames
- Lottie → cần file .json animation riêng
- Split PNG thành layers → quá phức tạp cho 1 ảnh flat

**Kết luận**: Animation character từ 1 PNG tĩnh là **dead end** cho prototype. Các giải pháp khả thi:
1. **Simple CSS**: bounce, pulse, hover effects trên ảnh nguyên
2. **Rive/Spine**: Tool chuyên animate character (cần assets riêng)
3. **Lottie**: Pre-made animation file
4. **Emoji/SVG**: Dùng emoji + CSS animation cho prototype

**Rule**: **Character animation cần assets chuyên dụng (sprite sheets, rigged models, Lottie files). KHÔNG cố animate 1 ảnh PNG tĩnh thành character animation — chỉ có thể làm simple transforms (bounce, scale, rotate).**

---

### 🟡 P42: PowerShell curl Syntax Khác Bash

> 📅 TIL 2026-03-20 — Dự án: VietFi Advisor API Testing

**Pattern**: `curl -X POST -H "Content-Type: application/json" -d '...'` fail trên PowerShell vì:
- `curl` là alias cho `Invoke-WebRequest`, không phải GNU curl
- `-H` maps sang `-Headers` (cần IDictionary, không phải string)
- Single quotes `'...'` xử lý khác

```powershell
# ❌ BUG — Bash curl syntax trên PowerShell
curl -s -X POST http://localhost:3000/api/chat -H "Content-Type: application/json" -d '{"messages":[]}'
# Error: Cannot convert string to IDictionary

# ✅ FIX — PowerShell native
$body = '{"messages":[{"role":"user","content":"hello"}]}'
Invoke-WebRequest -Uri "http://localhost:3000/api/tts" -Method POST -ContentType "application/json" -Body $body -UseBasicParsing
```

**Rule**: **Trên Windows PowerShell: dùng `Invoke-WebRequest` + `-UseBasicParsing`, KHÔNG dùng `curl` shortcuts.**

---

### 🟠 P43: Playwright Không Hỗ Trợ Unicode Vietnamese Keys

> 📅 TIL 2026-03-20 — Browser Testing

**Pattern**: `browser_press_key` với text tiếng Việt ("phở 30k", "ăn cơm") fail: `Unknown key: "ở"`, `Unknown key: "ă"`. Playwright `page.keyboard.type()` chỉ hỗ trợ ASCII keys.

```
❌ Fail: browser_press_key text="phở 30k"  → Unknown key: "ở"
❌ Fail: browser_press_key text="ăn cơm"  → Unknown key: "ă"

✅ Fix: Dùng JavaScript injection thay vì keyboard
const input = document.querySelector('input');
const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
setter.call(input, 'phở 30k');
input.dispatchEvent(new Event('input', { bubbles: true }));
```

**Rule**: **Khi test web app tiếng Việt qua Playwright/browser automation: dùng JavaScript `value.set` + `dispatchEvent` thay vì `keyboard.type()` cho text Unicode.**

---

### 🟠 P44: Edge Runtime Không Compatible Với Một Số NPM Packages

> 📅 TIL 2026-03-20 — Dự án: VietFi API Routes

**Pattern**: `edge-tts-universal` cần Node.js APIs (WebSocket, Buffer) → không chạy trên Edge Runtime.

```typescript
// ❌ BUG — Edge runtime
export const runtime = 'edge';
// edge-tts-universal dùng WebSocket → fail trên Edge

// ✅ FIX — Node.js runtime
export const runtime = 'nodejs';
// Hoạt động bình thường, nhưng bị giới hạn 10s trên Vercel Hobby
```

**Rule**: **Khi tích hợp npm package vào Next.js API route, check xem package cần Node.js hay Edge compatible. TTS/audio packages thường cần `runtime = 'nodejs'`.**

---

### 🟠 P45: JSON.stringify Thay Vì Manual String Escape

> 📅 TIL 2026-03-20 — Dự án: VietFi Chat API

**Pattern**: Tự escape JSON string bằng regex thay vì dùng `JSON.stringify()` → thiếu edge cases (newlines, unicode, backslashes).

```typescript
// ❌ BUG — Manual escape thiếu cases
const escaped = `"${text.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"`;
// Thiếu: \r, \t, \\, unicode escapes, etc.

// ✅ FIX — JSON.stringify handles ALL cases
const escaped = JSON.stringify(text);
// Tự động escape: ", \, /, \n, \r, \t, \b, \f, unicode
```

**Rule**: **LUÔN dùng `JSON.stringify()` khi cần escape string cho JSON/protocol. KHÔNG BAO GIỜ tự regex escape — sẽ luôn thiếu edge cases.**

---

## CATEGORY 7: Vercel / Deployment

### 🔴 P46: Vercel JSON Schema — "additional property" Error

> 📅 TIL 2026-03-20 — Dự án: VietFi Advisor

**Pattern**: `vercel.json` có field `"comment"` trong crons config → Vercel schema validation reject, build fail.

```json
// ❌ BUG — "comment" không nằm trong Vercel schema
{
  "crons": [{
    "path": "/api/cron/market-data",
    "schedule": "30 8 * * 1-5",
    "comment": "15:30 ICT = 08:30 UTC"  // ← REJECT!
  }]
}

// ✅ FIX — Xóa comment, chỉ giữ valid fields
{
  "crons": [{
    "path": "/api/cron/market-data",
    "schedule": "30 8 * * 1-5"
  }]
}
```

**Rule**: **Vercel JSON schema STRICT — chỉ accept documented fields. KHÔNG thêm `"comment"`, `"description"`, hay bất kỳ custom field nào.**

---

### 🔴 P47: edge-tts-universal API Mismatch

> 📅 TIL 2026-03-20 — Dự án: VietFi TTS Bank

**Pattern**: Gọi `new EdgeTTS()` rồi `tts.synthesize(text, voice)` → "text must be a string". API thật là text trong constructor.

```typescript
// ❌ BUG — text phải là constructor arg
const tts = new EdgeTTS();
await tts.synthesize(text, voice, { rate: '+5%' });

// ✅ FIX — text + voice trong constructor, rate/pitch là properties
const tts = new EdgeTTS(text, 'vi-VN-HoaiMyNeural');
tts.rate = '+5%';
tts.pitch = '+2Hz';
const result = await tts.synthesize();
const audioBlob: Blob = result.audio;
```

**Rule**: **Khi dùng thư viện lạ, LUÔN check source code đang dùng trong project (ví dụ route.ts) trước khi viết script mới. Copy API call pattern từ code đang chạy, đừng đoán.**

---

## CATEGORY 8: React / useEffect / TTS

### 🟡 P48: Double TTS — useEffect + Explicit Call

> 📅 TIL 2026-03-20 — Dự án: VietFi Chat

**Pattern**: `submitForm` gọi `speak()` explicit + `useEffect` auto-speak cũng trigger → audio phát 2 lần.

```typescript
// ❌ BUG — 2 nơi cùng gọi speak cho 1 message
// submitForm:
speak(localReply.ttsText);
addLocalMessage(text, localReply.text); // → triggers useEffect below

// useEffect:
if (lastMsg.role === "assistant" && lastMsg.id !== lastSpokenIdRef.current) {
  speak(text); // ← DOUBLE SPEAK!
}

// ✅ FIX — useEffect skip local messages (bot-*) + set ref trước
const botId = `bot-${Date.now() + 1}`;
lastSpokenIdRef.current = botId; // block useEffect
addLocalMessage(text, localReply.text);
speak(localReply.ttsText); // only explicit call fires

// useEffect: skip bot-* IDs
if (!lastMsg.id.startsWith("bot-") && lastMsg.id !== "greet-1") {
  speak(text); // only fires for AI streaming responses
}
```

**Rule**: **Khi có cả explicit call + useEffect auto-trigger cùng 1 action → PHẢI có mechanism chống duplicate. Dùng ref ID hoặc ID prefix convention (`bot-*` = local).**

---

### 🟡 P49: Auto-Speak on Mount — useEffect + Initial Message

> 📅 TIL 2026-03-20 — Dự án: VietFi Chat

**Pattern**: Chat component mount với greeting message → useEffect detect "new assistant message" → auto-speak ngay cả khi user chưa mở chat.

```typescript
// ❌ BUG — useEffect fires on mount
useEffect(() => {
  if (lastMsg?.role === "assistant") speak(text); // fires for greeting too!
}, [messages]);

// ✅ FIX — Skip greeting + check isOpen
if (
  lastMsg.id !== "greet-1" &&    // skip initial greeting
  !lastMsg.id.startsWith("bot-") && // skip local responses
  isOpen                         // only when chat is visible
) {
  speak(text);
}
```

**Rule**: **useEffect auto-actions (speak, animate, fetch) PHẢI check: (1) component visible? (2) user đã tương tác? (3) có phải initial state?**

---

### 🔴 P50: Missing .env.local → API Fail Âm Thầm

> 📅 TIL 2026-03-20 — Dự án: VietFi Advisor

**Pattern**: Code access `process.env.GEMINI_API_KEY` → `.env.local` không tồn tại → key = `''` → API call fail → catch block trả 500 → client `useChat` swallow error → user thấy **im lặng hoàn toàn**.

```
Chain: No .env.local → empty key → Gemini 401 → route catch → 500 response
      → useChat error state → NO UI feedback → user confused
```

**Fix**:
1. Tạo `.env.local` ngay sau khi clone/setup project
2. Thêm error fallback useEffect → hiện scripted response khi AI fail
3. Set env vars trên Vercel: `npx vercel env add GEMINI_API_KEY production`

**Rule**: **Khi deploy → LUÔN kiểm tra: (1) .env.local có đủ keys? (2) Vercel env vars set chưa? (3) Error handling có hiện UI feedback?**

---

### 🟡 P51: Quick Action Key Mismatch Sau Refactor

> 📅 TIL 2026-03-20 — Dự án: VietFi Chat

**Pattern**: Refactor QUICK_ACTIONS keys (`spending` → `ask_spending`) nhưng quên update `handleQuickAction` labels map → click button gửi raw key "ask_spending" → intent detection fail.

```typescript
// ❌ BUG — keys đổi nhưng labels map vẫn cũ
const QUICK_ACTIONS = [{ key: "ask_spending", ... }]; // CHANGED
const labels = { spending: "text..." }; // NOT UPDATED
// labels["ask_spending"] = undefined → text = "ask_spending" → no match

// ✅ FIX — labels phải match new keys
const labels = {
  ask_spending: "phân tích chi tiêu",  // contains intent keyword
  ask_debt: "tình hình nợ",
};
```

**Rule**: **Khi refactor enum/key values → grep TOÀN BỘ codebase cho old values. Dùng `grep_search` cho old key name trước khi commit.**

---

## CATEGORY 9: Architecture Patterns

### 🟢 P52: Pre-Generated Audio Bank — TTS Performance Pattern

> 📅 TIL 2026-03-20 — Dự án: VietFi TTS

**Pattern (tốt)**: Thay vì gọi TTS API real-time cho mỗi response → pre-generate audio files cho scripted responses, serve static.

```
Architecture:
1. scripted-responses.ts: mỗi item có { text, ttsText, id, isDynamic? }
2. generate-tts-bank.ts: sinh MP3 cho static responses → /public/audio/tts/
3. Client: static → play /audio/tts/{id}.mp3 (instant)
           dynamic → call /api/tts (real-time)
           AI → call /api/tts (real-time)

Benefits:
- 83 static responses → 3MB MP3 → instant playback (0ms vs 1-2s)
- 0 API calls cho 90%+ use cases
- Vercel static files = miễn phí, không timeout
```

**Khi nào dùng**: App có bộ responses cố định + TTS. Pre-generate static, fallback real-time cho dynamic.


---

### P57 — Data Hallucination (Bịa Data Vĩ Mô/Tài Chính)

**Dự án:** 100-page Investment Report  
**Ngày:** 2026-03-21  
**Severity:** 🔴 CRITICAL

**Triệu chứng:**
- Khi yêu cầu phân tích theo ngữ cảnh thời gian (vd: T3/2026), AI tự nội suy và bịa ra các số liệu ảo (Oil 120$, VNI 1600) thay vì fetch API thực tế.

**Root Cause:**
- LLM luôn mang khuynh hướng dự đoán từ tiếp theo thay vì verification. Không có cơ chế hard-code buộc kiểm tra Base Data trước khi render Text.

**Fix:**
```python
# ❌ BUG — Dựa vào 'feeling' để phân tích
"Dầu thô đang đứng ở 120$ vì tin đồn..."

# ✅ FIX — Data Verification Protocol
1. Chạy script (yfinance, ccxt) fetch data thực tế.
2. Dump ra một file `00_Data_Verification.md` (Ground Truth).
3. Ép AI đọc file Ground Truth này trước toàn bộ các prompt phân tích.
```
**Lesson:** TRONG TÀI CHÍNH KHÔNG CÓ CHỮ ĐOÁN. AI bắt buộc phải đi chạy code bóc API lấy tham số thực trước khi nhả chữ.

---

### P58 — Web Scraper Bó Tay Trước HTML5 Canvas

**Dự án:** tv-vision-ocr  
**Ngày:** 2026-03-21  
**Severity:** 🔴 HIGH

**Triệu chứng:**
- DOM Scraping (Selenium/BeautifulSoup) không móc được các chỉ số vẽ trên TradingView chart.

**Root Cause:**
- WebGL / HTML5 Canvas vẽ nguyên khối pixel ảnh, không lưu Text trong thẻ HTML.

**Fix:**
```python
# ✅ FIX — Computer Vision (OCR)
import easyocr, re
reader = easyocr.Reader(['en'])
txt = ' '.join(reader.readtext('chart.png', detail=0))
peak = max(float(x) for x in re.findall(r'[Hh]\s*([0-9.,]+)', txt))
```
**Lesson:** Thấy `<canvas>` là vứt Selenium. Chuyển sang chụp màn hình và gọi OCR (Computer Vision).

---

### P60 — WSL Update Corrupted (Class not registered) trên Win 11 Build 26200

**Dự án:** OpenClaw Setup / Docker Desktop  
**Ngày:** 2026-03-22  
**Severity:** 🔴 HIGH

**Triệu chứng:**
- Mở Docker Desktop báo "WSL needs updating".
- Chạy `wsl --update` hoặc `wsl --install` trên CMD/PowerShell báo lỗi: `wsl: WSL installation appears to be corrupted (Error code: Wsl/CallMsi/Install/REGDB_E_CLASSNOTREG). Class not registered.`

**Root Cause:**
- Đây là một bug đã được biết đến trên **Windows 11 Insider Preview (Build 26200)**. Trình cài đặt MSI nội bộ của WSL bị hỏng, nên các lệnh native của WSL không thể cài hoặc update.

**Fix/Workaround:**
```bash
# ❌ Lệnh gặp lỗi (do gọi MSI nội bộ bị hỏng)
wsl --update

# ✅ Cách fix: Bypass MSI nội bộ, tải và cài đặt qua Winget (Microsoft Store)
winget install --id Microsoft.WSL
```
*Sau khi chạy winget xong, khởi động lại Docker Desktop hoặc Reboot máy là WSL sẽ chạy bình thường.*

**Lesson:** Khi gặp lỗi `REGDB_E_CLASSNOTREG` của hệ thống con WSL trên các bản Windows Insider, đừng cố repair hay reset. Chỉ cần bypass bằng `winget install --id Microsoft.WSL` là nhanh nhất.

---

### P61 — Docker Named Volume EACCES (root owner vs container user)

**Dự án:** OpenClaw Agency Docker  
**Ngày:** 2026-03-22  
**Severity:** 🔴 HIGH

**Triệu chứng:**
- Container crash loop với `EACCES: permission denied` khi ghi vào `/home/node/.openclaw`.
- Docker logs lặp lại `Gateway failed to start: Error: EACCES`.

**Root Cause:**
- Named volume mount (`openclaw_data:/home/node/.openclaw`) tạo directory thuộc `root:root`. Container chạy dưới user `node` (uid 1000) không có quyền ghi.
- Bind mount file cụ thể (`./auth-profiles.json:/home/node/.openclaw/...`) **conflict** với named volume mount trên cùng parent path.

**Fix:**
```yaml
# ❌ SAI — named volume + bind mount conflict trên cùng path
volumes:
  - ./auth-profiles.json:/home/node/.openclaw/agents/main/agent/auth-profiles.json
  - openclaw_data:/home/node/.openclaw  # conflict!

# ✅ ĐÚNG — KHÔNG mount volume lên /.openclaw, để container tự quản lý
volumes:
  - ./config:/app/config
  - ./context.md:/app/context.md:ro
```

**Lesson:** Đừng mount named volume lên thư mục mà container cần write với non-root user. Nếu cần persist data, dùng `docker cp` sau khi container start + `docker exec -u root chown`.

---

### P62 — OpenClaw `auth-profiles.json` Format v2026.2.19+

**Dự án:** OpenClaw Agency  
**Ngày:** 2026-03-22  
**Severity:** 🟠 MEDIUM

**Triệu chứng:**
- Lỗi `No API key found for provider "anthropic"` dù đã tạo auth-profiles.json.
- Agent cố gọi provider `anthropic` thay vì `openrouter`.

**Root Cause:**
- Format auth-profiles.json SAI (dùng key-value đơn giản thay vì cấu trúc chuẩn).
- File này **KHÔNG hỗ trợ env variable substitution** (khác với `openclaw.json`).
- OpenClaw mặc định agent dùng Anthropic nếu chưa ai chọn model lần nào.

**Fix:**
```json
// ❌ SAI — format tự bịa, không đúng schema
{ "openrouter": "sk-or-v1-xxx", "anthropic": "sk-or-v1-xxx" }

// ✅ ĐÚNG — format chính thức v2026.2.19+
{
  "version": 1,
  "profiles": {
    "openrouter": {
      "provider": "openrouter",
      "mode": "api_key",
      "key": "sk-or-v1-xxx"  // field "key" (không phải "token")
    },
    "anthropic": {
      "provider": "anthropic",
      "mode": "api_key",
      "key": "sk-or-v1-xxx"  // route qua OpenRouter
    }
  }
}
```

**Lesson:** Luôn search docs chính thức trước khi đoán format. `auth-profiles.json` dùng JSON5, cần `version` + `profiles` wrapper. Dùng `key` thay vì `token` từ v2026.2.19+.

---

### P63 — `docker cp` Tạo File Thuộc Root → Container User Không Đọc Được

**Dự án:** OpenClaw Agency Docker  
**Ngày:** 2026-03-22  
**Severity:** 🔴 HIGH

**Triệu chứng:**
- Sau `docker cp file container:/path`, container báo `EACCES: permission denied, open '/path/file'`.
- File đã tồn tại đúng chỗ nhưng app không đọc được.

**Root Cause:**
- `docker cp` luôn copy file với owner = `root:root` bất kể container chạy user nào.
- Container chạy dưới user `node` (hoặc non-root) không có quyền đọc file thuộc root.

**Fix:**
```bash
# Step 1: Copy file vào container (file sẽ thuộc root)
docker cp ./file.json container_name:/path/file.json

# Step 2: LUÔN chown sau docker cp
docker exec -u root container_name chown node:node /path/file.json

# Hoặc chown recursive
docker exec -u root container_name chown -R node:node /path/
```

**Lesson:** Sau MỌI lệnh `docker cp`, PHẢI chạy `docker exec -u root ... chown` để đổi owner. Không bao giờ quên bước này.

---

### P84 — Dấu hai chấm (:) không bọc trong chuỗi YAML Frontmatter Description làm sập Parser

**Dự án:** Antigravity Workflows / Custom Skills  
**Ngày:** 2026-04-04  
**Severity:** 🔴 CRITICAL

**Triệu chứng:**
Toàn bộ danh sách Custom Workflow hay rules (.md files) tự nhiên biến mất hoàn toàn khỏi UI của extension (ví dụ: mất `/deploy`).

**Root Cause:**
Khi khai báo trường `description` ở Frontmatter có chứa dấu `:` (Ví dụ: `description: The Release Manager (Dual Mode: Public Open Source & Private SaaS)`). Vì không bọc trong dấu ngoặc kép `""`, YAML Parser nghĩ dấu `:` thứ hai là một syntax báo Key-Value mới nằm trên cùng dòng → Syntax error → Extension parser fail âm thầm và loại bỏ luôn file đó khỏi hệ thống.

**Fix:**
```yaml
# ❌ BUG — Lỗi hở dấu hai chấm
---
description: The Release Manager (Dual Mode: Public Open Source & Private SaaS)
---

# ✅ FIX — Bọc String bằng ngoặc kép (Double Quotes)
---
description: "The Release Manager (Dual Mode: Public Open Source & Private SaaS)"
---
```

**Lesson:** **Nguyên tắc sống còn của Frontmatter:** Bất cứ khi nào viết `description` (hoặc title) có chứa các ký tự lạ hoặc dấu câu `:`, `-`, hãy **BỌC TẤT CẢ VÀO TRONG NGOẶC KÉP** `""`. Lỗi này không báo bug log, chỉ làm biến mất UI một cách âm thầm, cực kỳ khó truy vết nếu không chú ý. Đã chạy script auto-escape sửa hàng loạt 32 file toàn hệ thống.

---

### 🔴 P85: Lệnh Vercel `login` báo thành công nhưng CLI/MCP lỗi Token Invalid do dính Global Env Vars cũ

> 📅 TIL 2026-04-04 — Dự án: Vactory Landing Page Deployment

**Pattern**: Thực thi `npx vercel login` qua trình duyệt báo *Authorization successful*, nhưng mọi command (CLI hoặc qua lệnh gọi MCP Server) đều văng lỗi: `Error: The token provided via VERCEL_TOKEN environment variable is not valid.`

``powershell
# ❌ BUG — Token cũ bị kẹt trong System/User Variables của Windows
# Lệnh 'login' tạo auth .json trong thư mục AppData, nhưng biến môi trường VERCEL_TOKEN có độ ưu tiên RÀNG BUỘC CAO HƠN.
# Do token trong Environment Variable đã bị khoá/hết hạn nên Node CLI cứ chạy là crash trước khi kịp đụng vào session.
# Sai lầm: Lệnh Remove-Item Env:\VERCEL_TOKEN chỉ xoá ở cache của cửa sổ Powershell đó, tắt bật lại vẫn sẽ dính lỗi!

# ✅ FIX — Setup 1 lần dùng mãi mãi (Dập vĩnh viễn qua .NET Powershell)
# 1. Tạo 1 Token "No Expiration" trên Web.
# 2. Add vĩnh viễn bằng lệnh Powershell .NET thay vì thao tác tay ở Control Panel:
[Environment]::SetEnvironmentVariable('VERCEL_TOKEN', 'vcp_Dán_Token_Vào_Đây', 'User')

# 3. Ép cập nhật context hiện tại để dùng ngay lập tức không cần Restart IDE:
$env:VERCEL_TOKEN='vcp_Dán_Token_Vào_Đây'
``

**Source**: Vactory Production Deployment. Quá trình pipeline Vercel bị khựng do auth auth-session.

**Rule**: **Khi CLI ưu tiên Token Env Vars, phải đảm bảo ghi đè/xóa biến tận cấp độ hệ điều hành Windows ([Environment]::SetEnvironmentVariable()) chứ không cấu hình tạm thời bằng $env:. Tốt nhất là setup No-Expiration API Token.**

---

### 🔴 P86: Auto-Clicker Bot Scope Creep Khớp Sai Element (Chat Send Button)

> 📅 TIL 2026-04-06 — Dự án: Antigravity Auto Accept Extension

**Pattern**: Bot cào DOM tự động (DOM Observer) bằng `querySelectorAll` bắt trúng nhầm nút "Send Chat" của IDE thay vì chỉ bắt nút "Run", do việc gán selector quá lỏng lẻo (`.action-label`, `.codicon`) nhằm tìm cách "bắt chước UI IDE". 

```javascript
// ❌ BUG — Selector lưới cào MỌI CHI TIẾT trên UI
await performClick(['[role="button"]', 'a.action-label', 'a.action-item', '[class*="codicon"]']);
// Extension vô tình vơ vét cả DOM Tree gốc của màn hình ChatGPT/Windsurf và cướp session click enter.

// ✅ FIX — Return to First Principles: Thu hẹp tối đa Attack Surface
await performClick(['button', '[class*="button"]', '[class*="anysphere"]']);
// CHỈ nhắm vào core framework components mang tính nút thật (Real buttons).
```

**Source**: Antigravity Auto Accept Extension v2.0.x. Hành vi vi phạm nguyên tắc "Giảm thiểu bề mặt tiếp xúc" sinh ra False Positives tràn ngập hệ thống.

---

### 🟠 P89: MQL5 Nested Ternary Operator Compile Error

> 📅 TIL 2026-04-07 — Dự án: Phoenix DCA Pro EA

**Pattern**: MQL5 compiler không hỗ trợ nested ternary `a ? b : c ? d : e`. Lỗi báo "some operator expected" mà không chỉ rõ dòng.

```mql5
// ❌ BUG — Nested ternary fail compile
int signal = (score > 0) ? 1 : (score < 0) ? -1 : 0;

// ✅ FIX — Dùng if-else tường minh
int signal = 0;
if(score > 0) signal = 1;
else if(score < 0) signal = -1;
```

**Rule**: **MQL5 KHÔNG dùng nested ternary. Luôn dùng if-else. Ternary đơn giản `a ? b : c` OK nhưng KHÔNG lồng.**

---

### 🟠 P90: MQL5 Unary Negation Trước Cast/MathMin

> 📅 TIL 2026-04-07 — Dự án: Phoenix DCA Pro EA

**Pattern**: `-(int)MathMin(...)` và `-MathMin(...)` gây "some operator expected" vì MQL5 parser hiểu nhầm `-` là binary operator thiếu operand trái.

```mql5
// ❌ BUG — Unary minus trước cast
return -(int)MathMin(100, val);
return -MathMin(100, score);

// ✅ FIX — Bọc ngoặc rõ ràng
return -((int)MathMin(100, val));
return -((int)MathMin(100, score));
```

**Rule**: **MQL5 return negative value: LUÔN bọc `-(expression)` trong ngoặc kép `-((type)func())`. Không để `-` đứng trước cast hay function call trực tiếp.**

---

**Rule**: **Khi lập trình DOM/UI Observer Agent chạy ngầm liên tục, TUYỆT ĐỐI không dùng các Selectors CSS phổ quát (role=button, icon classes). Phải tuân thủ Principle of Least Privilege: Chỉ quét thẻ HTML mang bản chất nút hoặc Framework-isolated class (Minimal Attack Surface).**

---

### 🔴 P87: Extension Lifecycle Auto-Relaunch Tự Động Quit IDE Khi System Lag

> 📅 TIL 2026-04-07 — Dự án: Antigravity Auto Accept Extension

**Pattern**: Extension chứa cơ chế "Auto-Fix" chạy ngầm (do Scheduler gọi) để check `localhost:9004`. Nếu HTTP request bị timeout 800ms do IDE đang ăn nhiều CPU, extension kết luận là mất mạng CDP và tự động gọi `vscode.commands.executeCommand('workbench.action.quit')` nhằm "khởi động lại để cập nhật Flag". Kết quả: Người dùng bị ngắt ngang "đang làm mà cứ sập", IDE tắt liên tục không báo trước.

```javascript
// ❌ BUG — Fatal background auto-relaunch
async function autoFixCDP() {
    if (relauncher && !relaunchAttemptedThisSession) {
        log('CDP not found. Attempting automatic relaunch...');
        relaunchAttemptedThisSession = true;
        // Fatal: Gọi lệnh kill toàn bộ cửa sổ IDE trong background
        const result = await relauncher.ensureCDPAndRelaunch(); 
        return Boolean(result && result.relaunched);
    }
}

// ✅ FIX — Prompt user + Tăng Timeout HTTP
async function autoFixCDP() {
    if (relauncher && !relaunchAttemptedThisSession) {
        log('CDP not found. Suppressing automatic IDE quit to prevent crashes.');
        relaunchAttemptedThisSession = true;
        // Bật popup cảnh báo thay vì kill ngầm
        vscode.window.showWarningMessage('Antigravity CDP Port dropped...', 'Restart Now');
        return false;
    }
}
// Đi kèm với tăng cấu hình Timeout của request JSON: HTTP Timeout `_fetchJson` từ 800ms -> 2000ms.
```

**Rule**: **TUYỆT ĐỐI KHÔNG gọi `workbench.action.quit` hoặc `window.close()` ngầm từ background task chạy định kỳ. Bất kỳ tiến trình nào có khả năng shutdown/restart app gốc PHẢI được bọc bằng Popup Window (cảnh báo) và đòi hỏi EXPLICT USER CONSENT (Người dùng bấm đồng ý mới chạy).**
