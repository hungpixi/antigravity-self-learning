---
description: "🧠 Dream — Memory consolidation & knowledge optimization"
---

# 🧠 Dream: Memory Consolidation

> Giao thức "giấc mơ" — tổng hợp, dọn dẹp, tối ưu bộ nhớ dài hạn.
> Adapt từ Claude Code autoDream — 4 phase: Orient → Gather → Consolidate → Prune.

## Khi nào tự động trigger

Dream PHẢI chạy khi **BẤT KỲ** điều kiện nào đúng:
1. **Đầu session mới** và đã >=5 sessions kể từ lần dream cuối (check `memory/dream_log.md`)
2. **Memory dir >20 files** → cần merge/prune
3. **MEMORY.md >80 dòng** → cần tỉa index
4. **User yêu cầu** gõ `/dream` hoặc nói "dọn dẹp memory", "optimize knowledge"

## Phase 1 — Orient

// turbo
1. Đọc `MEMORY.md` index để hiểu bức tranh tổng:
```
cat ~/.gemini/antigravity/memory/MEMORY.md
```

// turbo
2. List toàn bộ memory files:
```
ls ~/.gemini/antigravity/memory/
```

3. Skim từng memory file có vẻ cũ hoặc lớn — đọc frontmatter + 10 dòng đầu.

## Phase 2 — Gather Recent Signal

Tìm thông tin mới đáng lưu từ các nguồn (ưu tiên từ trên xuống):

1. **Conversation summaries gần đây**: Check `~/.gemini/antigravity/brain/` cho các session gần nhất
2. **Memory đã drift**: So sánh memory vs code hiện tại — cái nào sai/outdated?
3. **Skills đã update**: Check `bug-fix-patterns/SKILL.md` changelog — TIL mới nào chưa có memory?
4. **User feedback chưa capture**: Grep conversation logs tìm patterns: "đừng", "không", "stop", "ok", "đúng rồi"

> ⚠ KHÔNG đọc hết conversation logs. Chỉ grep narrowly cho keywords cụ thể.

## Phase 3 — Consolidate

Với mỗi thông tin đáng nhớ:

1. **Check duplicate**: Đã có memory file tương tự chưa?
   - Có → **Update** file cũ, KHÔNG tạo file mới
   - Chưa → Tạo file mới theo format chuẩn

2. **Format chuẩn** cho mỗi memory file:
```markdown
---
name: {{tên memory}}
description: {{1 dòng mô tả — used to decide relevance}}  
type: {{user | feedback | project | reference}}
---

{{nội dung}}

Với feedback/project type:
- Rule/fact
- **Why:** lý do
- **How to apply:** cách áp dụng
```

3. **Rules khi consolidate**:
   - Merge signal mới vào file cũ thay vì tạo near-duplicate
   - Convert relative dates → absolute dates ("hôm qua" → "2026-04-03")
   - Xóa facts đã bị contradict bởi thực tế hiện tại
   - KHONG save: code patterns (derivable từ code), git history, debug solutions (fix nằm trong code rồi)

## Phase 4 — Prune & Index

1. **Update `MEMORY.md`** — giữ dưới 200 dòng:
   - Mỗi entry = 1 dòng dưới 150 chars: `- [Title](file.md) — one-line hook`
   - Xóa pointers tới memories đã stale/wrong/superseded
   - Thêm pointers tới memories mới quan trọng
   - Nếu entry >200 chars → shorten, move detail vào topic file

2. **Resolve contradictions**: 2 files nói ngược nhau → fix file sai

3. **Log dream** — append vào `memory/dream_log.md`:
```markdown
## Dream [YYYY-MM-DD]
- Files scanned: N
- Updated: [list]
- Created: [list]  
- Pruned: [list]
- Status: clean / needs-attention
```

## Phase 5 — Report

Trả lời ngắn gọn những gì đã consolidate, update, hoặc prune.
Nếu không có gì thay đổi (memories đã tight), nói vậy.

---

## Anti-patterns

- ❌ Đọc hết conversation logs → OVER CONTEXT
- ❌ Tạo memory cho mọi thứ → Noise, không phải signal
- ❌ Save code patterns/architecture → Derivable từ grep/git
- ❌ Save ephemeral task state → Thuộc về conversation, không phải memory
- ✅ Chỉ save thứ KHÔNG derivable từ codebase hiện tại
