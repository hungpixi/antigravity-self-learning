# Workflow Self-Learning Hooks

Thêm các đoạn sau vào workflows tương ứng của Antigravity.

## /code — Thêm vào cuối Giai đoạn Handover

```markdown
### Self-Learning Check (Auto)
Sau khi code xong, TỰ ĐỘNG check:
□ Có chọn tech/lib mới? → Log vào adr-decisions/SKILL.md
□ Có fix bug? → Check bug-fix-patterns/SKILL.md (TIL)
□ Bug lặp lại lần 2+? → Viết 5 Whys RCA
□ Có optimize? → Log vào performance-playbook/SKILL.md
□ Task sẽ lặp lại? → Log vào runbooks/SKILL.md
```

## /debug — Thêm vào cuối Giai đoạn Handover

```markdown
### TIL/RCA Auto-Update (Auto)
Sau khi fix bug xong:
1. Đọc bug-fix-patterns/SKILL.md
2. Grep xem pattern đã có chưa
3. Nếu CHƯA và đủ general → Append TIL entry
4. Nếu lặp lại lần 2+ → Viết 5 Whys RCA
5. Nếu phát hiện code smell → Append vào code-smell-catalog
```

## /refactor — Thêm vào cuối Giai đoạn Handover

```markdown
### Code Smell Catalog Update (Auto)
□ Smell phát hiện mới? → Append vào code-smell-catalog/SKILL.md
□ Refactor pattern hiệu quả? → Log vào prompt-patterns/SKILL.md
□ Performance cải thiện? → Log vào performance-playbook/SKILL.md
```

## /review — Thêm TRƯỚC khi quét code

```markdown
### Đọc Code Smell Catalog (Trước khi review!)
→ Đọc code-smell-catalog/SKILL.md
→ Dùng danh sách smells làm checklist
→ Phát hiện smell mới → Append vào catalog
```
