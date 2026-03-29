---
name: Code Smell Catalog
description: Patterns xấu trong code cần phát hiện sớm trước khi thành bug. Auto-trigger khi review code, refactor, audit code quality. Triggers on "code smell", "code review", "refactor", "clean code", "code quality", "anti-pattern", "technical debt", "nợ kỹ thuật", "code xấu", "code bẩn".
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

<!-- SMELL_APPEND_MARKER — AI append smell mới TRƯỚC dòng này -->
