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

Quy tắc: Grep skill file trước → nếu chưa có → append. KHÔNG lưu typo hoặc lỗi 1 lần.
```
