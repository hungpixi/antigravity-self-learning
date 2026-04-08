---
name: Effective Prompt Patterns
description: "Meta-optimization - những prompt patterns cho AI output tốt hơn. Auto-trigger khi prompt engineering, cải thiện output, meta-optimization. Triggers on \"prompt\", \"better output\", \"improve AI\", \"cách hỏi AI\", \"prompt engineering\", \"kết quả tốt hơn\", \"AI trả lời sai\", \"how to prompt\"."
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

| 007 | 2026-04-02 | Veo 3 Consistent Character Prompt | Giữ ổn định khuôn mặt + Voice |
| 008 | 2026-04-04 | Intermediate Developer Automation Persona | Tăng tốc thực thi Workflow CI/CD |

### PP-008: Tự động hóa triệt để CI/CD (Bỏ Progressive Disclosure cho Dev Giỏi)

> 📅 2026-04-04 — Context: Kích hoạt các Workflow hệ thống thay làm việc (như `/deploy`, `/audit`)

**Problem**: Thiết kế AI Workflow mô phỏng "Bác sĩ" hoặc "Newbie Guide" hỏi quá nhiều (dùng progressive disclosure, hỏi từng câu một) làm chậm tốc độ làm việc thực sự của Dev đã có nền tảng. User phát bực vì AI giải thích SSL hay DNS là gì thay vì đục thẳng CLI để deploy.
**Pattern**: 
1. Loại bỏ các form câu hỏi tu từ dài dòng. Không xài tư duy "hướng dẫn lý thuyết".
2. Chuyển đổi công cụ (Skill/Workflow) thành một dạng script thực thi (Automation Executor).
3. Sử dụng các kỹ năng command-line (Vercel CLI, Netlify CLI), dò file `.env.production` hay `package.json` và trực tiếp auto-run.
4. Giao tiếp cực ngắn (Terse/No filler), đưa ra đúng báo cáo Handover có Link URL.
**Result**: Deploy hoàn tất trong vòng 1 tool call mà không cần user confirm giải thích khái niệm.
**When to use**: Dành riêng cho User có `technical_level: "intermediate"` hoặc "advanced". Đối xử với User như một đồng nghiệp DevOps trưởng thành.

<!-- PP_APPEND_MARKER — AI append pattern mới TRƯỚC dòng này -->
> 📅 2026-04-02 — Context: Viết prompt video Text-to-Video trên Veo 3 Google Labs

**Problem**: Nhân vật bị biến dạng, đổi quần áo, mất giọng hoặc sai bối cảnh sau mỗi đợt generate.
**Pattern**: Bắt buộc chia cấu trúc 3 phần trong một Prompt:
1. **Phần Character**: Ngoại hình (quần áo, tóc tai phải cố định/chi tiết). Đặc điểm tương tác (direct eye contact).
2. **Phần Bối Cảnh**: Không gian tả chi tiết lighting (warm, bright), màu sắc, thời điểm. Nếu có transition cũng phải tả.
3. **Phần Giọng Nói (Voice)**: Yêu cầu VEO3 lồng ghép giọng cụ thể ví dụ `(Southern/Saigon Accent), Clear, mid-range baritone, fast-paced and energetic`. Có kịch bản lời thoại nằm ngay trong Prompt.
Sử dụng tham số `charID_...`, `settingID_...` để ghim bộ nhớ đệm cho Veo 3 các video sau.
**Result**: Video sinh ra giữ nguyên nhân vật 100%, giọng đọc xuyên suốt liền mạch, bối cảnh ăn khớp không bị sượng phim.
**When to use**: Sinh video kịch bản dài / chuỗi video 8 giây nối nhau.

<!-- PP_APPEND_MARKER — AI append pattern mới TRƯỚC dòng này -->


## Pattern: The Empirical Truth Wall (Bức Tường Phủ Quyết Data)

**Vấn đề:** Khi bắt AI phân tích báo cáo lớn, càng viết dài nó càng có xu hướng bịa số (Hallucinate) hoặc nội suy kịch bản không có thật.  
**Dấu hiệu:** AI tự thay đổi mốc VNINDEX, tự nghĩ ra giá Vàng, Dầu để lập luận cho khớp.

**Công thức Prompt / Quy trình:**
1. **Force Code Execution:** Bắt buộc AI viết một đoạn script Python gõ API (yfinance/binance) lấy số liệu chốt phiên hiện tại.
2. **Anchor File:** Buộc AI lưu file `00_Data_Truth.json` hoặc `.md`.
3. **The Wall Prompt:** Thêm câu prompt: *"Mọi lập luận trong báo cáo KHÔNG được phép chệch 1 Dấu Phẩy nào so với bộ Data Truth ở file X. Cấm đoán ý. Bất cứ con số nào đưa vào cũng phải có cơ sở."*

**Hiệu ứng:** AI hóa thân thành nhà phân tích Quant chân chính, bớt văn vở và chỉ tập trung vào Logic nhân quả từ số liệu thực tế.
