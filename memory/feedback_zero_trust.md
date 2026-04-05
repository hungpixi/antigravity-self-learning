---
name: Zero Trust Secret Hygiene
description: "Absolute rule — no secrets in source code, rules, commits, or PR"
type: feedback
---

Tuyet doi khong de secret tho trong rule files, README, source code, commit, PR

**Why:** Da xay ra incident secret leak. User cuc ky nghiem khac ve van de nay.
**How to apply:**
- Secret luu trong User Environment Variable hoac `context.md` (gitignored)
- Rule files chi luu policy, KHONG luu token/key
- Truoc commit: grep secret patterns
- Neu leak: dung push → xoa → rotate key ngay
