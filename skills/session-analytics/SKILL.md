---
name: Session Analytics & Time Tracker
description: Đo lường hiệu quả mỗi phiên làm việc. Auto-trigger cuối mỗi session hoặc khi user hỏi về productivity. Triggers on "bao lâu", "mất bao nhiêu thời gian", "hiệu quả", "productivity", "session stats", "time tracking", "phiên làm việc", "đánh giá phiên".
---

# ⏱️ Session Analytics & Time Tracker

> Đo lường hiệu quả mỗi phiên làm việc. AI PHẢI tạo report cuối mỗi session có thay đổi code đáng kể.

## Cách Tính Thời Gian

AI tính dựa trên **timestamps giữa các user messages**:

```
User message lúc 08:36 → AI response + tools → User message lúc 08:39
→ Khoảng giữa = 3 phút
→ Phân loại:
   - Nếu AI đang chạy tools/code → "AI Work"
   - Nếu AI đã trả lời, chờ user → "User Think/Review"
   - Nếu user hỏi ngắn, AI trả lời dài → chủ yếu "AI Work"
```

### Quy Tắc Phân Loại

| Tình huống | Phân loại |
|-----------|----------|
| AI đang chạy commands, tạo files, edit code | 🤖 AI Work |
| AI đã trả lời, chờ user reply | ⏳ User Think |  
| User approve/LGTM (< 30s gap) | ⏳ User Review |
| AI trả lời câu hỏi text (không code) | 💬 Discussion |

## Format Report

```markdown
## ⏱️ Session Report — [YYYY-MM-DD]

**Dự án**: [tên]
**Thời gian**: [start] → [end] = [total] phút

### Phân Bổ Thời Gian

| Hoạt động | Thời gian | % |
|-----------|----------|---|
| 🤖 AI Work (code, tools, search) | XX phút | XX% |
| ⏳ User Think/Review | XX phút | XX% |
| 💬 Discussion | XX phút | XX% |

### Deliverables

| # | Output | Files |
|---|--------|-------|
| 1 | [Việc 1] | X files |
| 2 | [Việc 2] | Y files |

### Hiệu Quả

| Metric | Giá trị |
|--------|---------|
| Files tạo/sửa | XX |
| Lines code | XX |
| Tốc độ trung bình | XX files/phút |
| Tỷ lệ AI work | XX% |
| Rating | ⭐⭐⭐⭐⭐ |

### Đánh Giá
[1 dòng đánh giá hiệu quả phiên]
```

## Rating System

| Stars | Tiêu chí |
|-------|----------|
| ⭐⭐⭐⭐⭐ | >70% AI work, >5 deliverables, <30 phút |
| ⭐⭐⭐⭐ | >50% AI work, >3 deliverables |
| ⭐⭐⭐ | >40% AI work, >1 deliverable |
| ⭐⭐ | <40% AI work, nhiều thời gian chờ/debug loop |
| ⭐ | Session bị stuck, không deliverable |

---

## 📋 Session Changelog

> Mỗi session có thay đổi code đáng kể được log ở đây.

### Session 2026-03-18 — 7 Self-Learning Models + Disk Cleanup

**Dự án**: antigravity-self-learning
**Thời gian**: 08:36 → 09:06 = **30 phút**

#### Phân Bổ Thời Gian

| Hoạt động | Thời gian | % |
|-----------|----------|---|
| 🤖 AI Work (code, tools, search) | 23.5 phút | 79% |
| ⏳ User Think/Review | 4.0 phút | 14% |
| 💬 Discussion | 2.0 phút | 7% |

#### 8 User Prompts → 7 Deliverables

| # | Prompt (tóm tắt) | Output | AI Time |
|---|-------------------|--------|---------|
| 1 | Dọn ổ C, xoá recordings | Giải phóng 1.24 GB | 2.75 phút |
| 2 | Audit bug patterns từ history | Đọc 12+ walkthroughs, phân loại 20+ patterns | 5.0 phút |
| 3 | TIL model cho bug-fix | Tạo `bug-fix-patterns/SKILL.md` (21 patterns, 16.6KB) | 1.8 phút |
| 4 | Hỏi thêm models nào | Trả lời 7 models + so sánh | 1.0 phút |
| 5 | Plan 7 models tích hợp | Implementation plan + task.md | 2.1 phút |
| 6 | Approve → Execute | 5 skills mới + 4 workflows sửa + GEMINI.md update | 5.7 phút |
| 7 | Deploy lên GitHub | Repo `antigravity-self-learning` (10 files, 1327 lines) | 9.4 phút |
| 8 | Session analytics | Module này | — |

#### Tổng Kết

| Metric | Giá trị |
|--------|---------|
| Files tạo mới | 15 |
| Files sửa | 5 (GEMINI.md + 4 workflows) |
| Lines code tổng | 1,327+ |
| Disk freed | 1.24 GB |
| GitHub repo | ✅ Live |
| Tốc độ | **0.67 files/phút** |
| Rating | ⭐⭐⭐⭐⭐ |

**Đánh giá**: Phiên cực hiệu quả — 79% thời gian AI làm việc, 7 deliverables trong 30 phút, từ cleanup → audit → design → implement → deploy liên tục không gián đoạn đáng kể.

<!-- SESSION_APPEND_MARKER — AI append session mới TRƯỚC dòng này -->
