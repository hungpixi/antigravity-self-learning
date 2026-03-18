# Thêm vào ~/.gemini/GEMINI.md

## Tech Radar — Chống Dùng Công Nghệ Cũ

```
Trước khi chọn bất kỳ thư viện/framework nào cho dự án:
1. Search trước: `gh search repos` hoặc npm/PyPI cho alternatives mới nhất
2. So sánh: stars, last commit date, bundle size, số dependencies
3. Ưu tiên: hiệu quả nhất + đơn giản nhất + active maintained + phù hợp scope dự án
4. KHÔNG dùng thư viện >2 năm không commit trừ khi là standard (lodash, express, numpy)
5. Khi 2 options tương đương → chọn cái ít dependencies hơn, nhẹ hơn
6. Khi đã có ADR cho quyết định tương tự → follow ADR, không flip-flop
7. Log quyết định vào skills/adr-decisions/SKILL.md
```

## Micro-Edit Protocol — Dự Án Lớn

```
Hầu hết dự án đều ở mức quy mô lớn. LUÔN LUÔN áp dụng:

1. KHÔNG viết lại cả file — Chỉ edit đúng phần cần sửa
2. Tách nhỏ mọi thay đổi — Mỗi edit ≤100 dòng
3. File mới >300 dòng → viết skeleton trước → fill từng function
4. 1 task = 1 file — Sửa xong file A → verify → sửa file B
5. Verify sau mỗi edit — chạy compile/build/test
6. Khi gặp API limit → DỪNG, tách task nhỏ hơn

Anti-patterns TUYỆT ĐỐI TRÁNH:
- ❌ write_to_file overwrite file 500+ dòng
- ❌ Edit 10 functions cùng 1 lần
- ✅ Edit 1-2 functions → verify → edit tiếp
- ✅ Viết skeleton → fill function A → verify → fill function B
```

## Self-Learning Protocol (7 Models)

```
Sau mỗi session code/debug/refactor/review, AI check và cập nhật skill tương ứng:

| # | Model | Trigger | Skill File |
|---|-------|---------|------------|
| 1 | TIL | Fix bug thành công | bug-fix-patterns/SKILL.md |
| 2 | ADR | Chọn tech/architecture | adr-decisions/SKILL.md |
| 3 | Runbook | Task lặp lại >3 bước | runbooks/SKILL.md |
| 4 | RCA | Bug tái phát lần 2+ | bug-fix-patterns/SKILL.md (5 Whys) |
| 5 | Performance | Optimize có metrics | performance-playbook/SKILL.md |
| 6 | Code Smell | Pattern xấu khi review | code-smell-catalog/SKILL.md |
| 7 | Prompt Patterns | Prompt hiệu quả | prompt-patterns/SKILL.md |

Quy tắc: Grep skill file trước → nếu chưa có pattern → append theo format TIL. KHÔNG lưu typo hoặc lỗi 1 lần.
```

## Session Analytics (Auto-trigger cuối session)

```
Cuối mỗi session có thay đổi code đáng kể (≥3 files), TỰ ĐỘNG tạo report:
1. Đọc session-analytics/SKILL.md để lấy format
2. Tính thời gian: AI Work vs User Think (dựa trên timestamps giữa prompts)
3. Đếm deliverables, files tạo/sửa
4. Đánh giá rating ⭐ (1-5)
5. Append vào session-analytics/SKILL.md trước MARKER
```
