---
name: Effective Prompt Patterns
description: Meta-optimization - những prompt patterns cho AI output tốt hơn. Auto-trigger khi prompt engineering, cải thiện output, meta-optimization. Triggers on "prompt", "better output", "improve AI", "cách hỏi AI", "prompt engineering", "kết quả tốt hơn", "AI trả lời sai", "how to prompt".
---

# 🎯 Effective Prompt Patterns

> Prompt patterns đã chứng minh cải thiện đáng kể chất lượng AI output. AI tự áp dụng các pattern này khi code.

## Format Entry

```
### PP-xxx: [Tên Pattern]

> 📅 [YYYY-MM-DD] — Context: [khi nào dùng]

**Problem**: [Vấn đề khi không dùng pattern này]
**Pattern**: [Mô tả cách làm]
**Result**: [Kết quả cải thiện]
**When to use**: [Điều kiện trigger]
```

---

## Active Patterns

### PP-001: Search-Before-Code

> 📅 2026-03-18 — Context: Khi bắt đầu dự án mới hoặc chọn tech

**Problem**: AI generate code từ đầu bằng kiến thức cũ → dùng thư viện outdated
**Pattern**: 
1. Search GitHub/npm/PyPI cho giải pháp có sẵn trước
2. So sánh stars, last commit, dependencies
3. Fork/adapt nếu phù hợp, code mới nếu không có
4. Log quyết định vào ADR
**Result**: Code production-ready nhanh hơn, dùng tech mới nhất, ít reinvent the wheel
**When to use**: Mọi lần bắt đầu feature mới hoặc chọn library

---

### PP-002: 3-Round Self-Review

> 📅 2026-03-18 — Context: Trước khi deliver code lớn

**Problem**: Code generate 1 lần → 8+ bugs ẩn (đã chứng minh qua BDR Kit)
**Pattern**:
```
Round 1: Syntax + Logic tĩnh (đọc không chạy)
Round 2: Runtime + Edge cases (chạy + test biên)
Round 3: Integration + Platform-specific (test trên target)
```
**Result**: BDR Kit — 14 issues caught in 3 rounds (8 → 4 → 2), 0 bugs tới production
**When to use**: Code >100 dòng, hoặc code liên quan trading/security

---

### PP-003: Critic-Then-Fix

> 📅 2026-03-18 — Context: Khi AI cần review/improve own output

**Problem**: Tự review không tìm ra lỗi vì "confirmation bias"
**Pattern**: Tách 2 phases:
1. **Critic phase**: "Đóng vai senior dev khó tính. Liệt kê TẤT CẢ vấn đề trong code này."
2. **Fix phase**: "Sửa từng vấn đề đã liệt kê."
**Result**: Phát hiện nhiều bug hơn ~60% so với generate rồi review cùng lúc
**When to use**: Code phức tạp, trading bots, security-sensitive code

---

### PP-004: Instrument-Aware Defaults

> 📅 2026-03-18 — Context: Khi code trading bot hoặc financial tools

**Problem**: AI dùng default values chung cho mọi instrument → EURUSD OK nhưng XAUUSD fail
**Pattern**: Trước khi set defaults, check:
- Instrument nào? → Tra bảng defaults phù hợp
- Spread range? → Set MaxSpread accordingly
- ATR range? → Set SL/TP/Trailing accordingly
**Result**: Bot hoạt động đúng trên tất cả instruments ngay lần đầu
**When to use**: Mọi trading bot/indicator development

---

### PP-005: Grep-After-Write

> 📅 2026-03-18 — Context: Sau khi viết utility function

**Problem**: Viết function xong quên gọi → code tồn tại nhưng không hoạt động
**Pattern**: Sau khi viết function mới → grep codebase xem nó được gọi ở đâu
```bash
grep -rn "functionName" --include="*.ext"
# Phải có ≥2 kết quả: definition + ≥1 call site
```
**Result**: 0 dead functions, filter/guard luôn active
**When to use**: Mỗi khi tạo function mới, đặc biệt utility/helper

---

### PP-006: Micro-Edit Protocol

> 📅 2026-03-18 — Context: Dự án lớn (>500 dòng/file)

**Problem**: AI viết lại cả file 500+ dòng → API timeout/fail, mất code, không review được
**Pattern**:
1. KHÔNG `write_to_file` overwrite file đã tồn tại
2. Dùng `replace_file_content` sửa đúng phần cần sửa (≤300 dòng/edit)
3. File mới >500 dòng → viết skeleton trước → fill từng function
4. Sửa xong 1 file → verify → sửa file tiếp
5. Khi gặp API limit → DỪNG, tách nhỏ hơn
**Result**: 0 API failures, mỗi edit reviewable, rollback dễ dàng
**When to use**: MỌI lúc — đặc biệt khi sửa >3 functions hoặc edit >300 dòng

---

## 📋 Pattern Changelog

| # | Ngày | Pattern | Impact |
|---|------|---------|--------|
| 001 | 2026-03-18 | Search-Before-Code | Tech mới nhất |
| 002 | 2026-03-18 | 3-Round Self-Review | -14 bugs |
| 003 | 2026-03-18 | Critic-Then-Fix | +60% bug detection |
| 004 | 2026-03-18 | Instrument-Aware Defaults | Bot works first try |
| 005 | 2026-03-18 | Grep-After-Write | 0 dead functions |
| 006 | 2026-03-18 | Micro-Edit Protocol | 0 API failures |

<!-- PP_APPEND_MARKER — AI append pattern mới TRƯỚC dòng này -->
