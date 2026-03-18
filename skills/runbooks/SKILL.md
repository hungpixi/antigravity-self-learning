---
name: Operational Runbooks
description: Quy trình vận hành lặp lại đã chuẩn hóa. Auto-trigger khi deploy, compile, setup project, push GitHub, backtest. Triggers on "deploy", "compile", "push", "setup", "backtest", "quy trình", "cách chạy", "how to run", "how to deploy", "step by step".
---

# 🏃 Operational Runbooks

> Mỗi quy trình lặp lại >3 bước được log ở đây. AI đọc runbook thay vì hỏi lại user mỗi session.

## Format Runbook Entry

```
### RB-xxx: [Tên Quy Trình]

> 📅 [YYYY-MM-DD] — Áp dụng cho: [dự án/công cụ]

**Khi nào dùng**: [Trigger condition]
**Steps**:
1. [Step 1]
2. [Step 2]
...
**Common Errors**: [Lỗi hay gặp + cách fix]
**Notes**: [Ghi chú thêm]
```

---

## Active Runbooks

### RB-001: Compile & Backtest MQL5 EA

> 📅 2026-03-16 — Áp dụng cho: tất cả MQL5 trading bots

**Khi nào dùng**: Sau khi sửa xong file .mq5, cần test
**Steps**:
1. Copy file `.mq5` → `C:\Users\ppnh1\AppData\Roaming\MetaQuotes\Terminal\[ID]\MQL5\Experts\`
2. Mở MetaEditor → mở file → nhấn **F7** compile
3. Check: **0 errors, 0 warnings** (warnings OK nếu không critical)
4. Mở MT5 → Strategy Tester → chọn EA
5. Settings: Symbol `XAUUSDm`, Period `M5`, Dates `2026.01.01-2026.03.15`, Deposit `$5000`, Leverage `1:500`, Model `Every tick`
6. Load `.set` file nếu có → Start
7. Check kết quả: PF >1.5, DD <10%, WR >50%

**Common Errors**:
- `'CTrade' undeclared identifier` → Thêm `#include <Trade\Trade.mqh>` ở đầu file
- `Cannot open file` → Check path, file phải trong đúng thư mục MQL5/Experts/
- `OrderSend error 10030` → Invalid fill type. Dùng `GetFillingType()` thay vì hardcode

---

### RB-002: Push GitHub Portfolio

> 📅 2026-03-16 — Áp dụng cho: mọi public repo

**Khi nào dùng**: Push dự án lên GitHub dạng portfolio
**Steps**:
1. Check `.gitignore` có: `.env`, `context.md`, `*.key`, `*.secret`, `node_modules/`
2. Check **KHÔNG** có API key trong code: `grep -r "sk-" --include="*.py" --include="*.js" --include="*.ts"`
3. README.md phải có: Comarai branding, "Bạn muốn X tương tự?" footer, 3 nút CTA
4. `git add . && git commit -m "feat: [mô tả]"`
5. `gh repo create hungpixi/[name] --public --source=. --push` (hoặc `git push`)
6. Double-check: mở repo trên GitHub, verify không có sensitive data

**Common Errors**:
- Quên gitignore → `git rm --cached .env && git commit --amend`
- API key leak → Revoke key ngay, rotate key mới, `git filter-branch` xóa history

---

### RB-003: Netlify Deploy Static Site

> 📅 2026-03-17 — Áp dụng cho: landing pages (comarai.com, ict-ea)

**Khi nào dùng**: Deploy HTML/CSS/JS static site
**Steps**:
1. Đảm bảo file nằm trong folder `docs/` hoặc root
2. `npx netlify-cli deploy --dir=docs --prod` (hoặc manual upload trên netlify.com)
3. Check live URL hoạt động
4. Verify: OG tags, sitemap.xml, robots.txt, favicon

---

### RB-004: n8n Workflow Setup

> 📅 2026-03-10 — Áp dụng cho: automation workflows

**Khi nào dùng**: Tạo hoặc import n8n workflow
**Steps**:
1. Mở n8n: `http://localhost:5678`
2. Import workflow JSON nếu có: Settings → Import → Paste JSON
3. Cấu hình credentials: mỗi node cần auth → add credentials
4. Test từng node: Execute Node → check output
5. Activate workflow khi test xong

---

## 📋 Runbook Changelog

| # | Ngày | Runbook | Áp dụng |
|---|------|---------|---------|
| 001 | 2026-03-16 | MQL5 Compile & Backtest | Trading bots |
| 002 | 2026-03-16 | GitHub Push Portfolio | Public repos |
| 003 | 2026-03-17 | Netlify Deploy | Static sites |
| 004 | 2026-03-10 | n8n Workflow Setup | Automation |

<!-- RUNBOOK_APPEND_MARKER — AI append runbook mới TRƯỚC dòng này -->
