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
| 005 | 2026-03-18 | Startup Report Writing | Competition reports |

### RB-006: Clone & Setup Chinese Python Projects (uv-based)

> 📅 2026-03-19 — Áp dụng cho: mọi project Python từ GitHub Trung Quốc

**Khi nào dùng**: Clone Python project từ GitHub có `pyproject.toml` dùng `uv`
**Steps**:
1. `gh repo clone [user/repo]`
2. Check `pyproject.toml` → tìm `[[tool.uv.index]]` trỏ tuna/aliyun mirror → **XÓA**
3. `Remove-Item uv.lock` (xóa lock file cũ trỏ mirror)
4. `uv lock` (resolve lại deps từ PyPI mặc định)
5. `uv sync` (install tất cả)
6. `uv run playwright install chromium` (nếu project dùng Playwright)
7. `cp .env.example .env` (tạo config)
8. `uv run python main.py --help` (verify)

**Common Errors**:
- `Failed to download` → Mirror Trung Quốc block, xóa `[[tool.uv.index]]` + `uv.lock`
- `requires-python >=3.11` → `uv` tự detect, install đúng version
- `playwright install` fail → chạy riêng: `uv run playwright install --with-deps chromium`

---

### RB-007: Playwright CDP Crawler Setup

> 📅 2026-03-19 — Áp dụng cho: web scraping projects dùng Playwright

**Khi nào dùng**: Setup Playwright-based crawler với CDP mode
**Steps**:
1. Install: `uv add playwright httpx` hoặc `pip install playwright httpx`
2. Browser drivers: `playwright install chromium`
3. Config CDP mode:
   - `ENABLE_CDP_MODE = True` → dùng Chrome/Edge thật của user
   - `CDP_DEBUG_PORT = 9222` → port cho debug protocol
   - `HEADLESS = False` → nên False để QR code login thủ công
4. Anti-detection: inject `stealth.min.js` vào browser context
5. Login state: dùng `launch_persistent_context(user_data_dir=...)` để lưu cookies
6. Rate limiting: `asyncio.Semaphore(N)` + `asyncio.sleep()` giữa requests

**Architecture Pattern**:
```
Entry (main.py) → Factory → Platform Crawler → Browser/CDP → API Client → Store
                                    ↓
                              Login Handler (QR/Cookie/Phone)
```

**Common Errors**:
- Browser zombie process → register atexit + signal handler cho cleanup
- CDP port occupied → auto-increment: `find_available_port(9222)`
- Anti-bot detect → stealth.min.js + real Chrome user-data-dir

---

<!-- RUNBOOK_APPEND_MARKER — AI append runbook mới TRƯỚC dòng này -->

---

### RB-005: Competition-Quality Startup Report

> 📅 2026-03-18 — Áp dụng cho: báo cáo ý tưởng startup, cuộc thi, hackathon, pitch deck
> 📌 Template gốc: `vietfi-advisor/BAO_CAO_VONG_1_WDA2026.md` (v4.0, ~1100 dòng)

**Khi nào dùng**: Viết báo cáo ý tưởng startup cho cuộc thi hoặc pitch
**Triết lý**: YC/Sam Altman — "Ai TUYỆT VỌNG cần sản phẩm này?" + "Tốt gấp 10x"

**Steps — 5 Phase, 18 bước:**

**Phase 1 — Đặt vấn đề (RCA-driven)**
1. Bối cảnh vĩ mô: dữ liệu THỰC (verify nguồn gốc)
2. 5 Whys: ≥2 chuỗi, đào đến ROOT CAUSE, không surface-level
3. Problem Tree + Ishikawa diagram (text-based)
4. Feature → Root Cause mapping table

**Phase 2 — User-centric**
5. ≥2 User Personas: thu nhập, chi tiêu, Pain quote, VietFi demo cụ thể
6. JTBD table: Functional/Emotional/Social/Domain jobs + Trigger + Switch
7. Cơ sở lý thuyết: Behavioral Finance, trích dẫn có nguồn

**Phase 3 — Giải pháp (YC-inspired)**
8. Triết lý 1 câu + bảng mapping Steps → Features → Tần suất
9. AI Pipeline diagram + mô tả từng agent
10. ≥7 USP + giải thích tại sao không copy được
11. ≥1 Viral Feature (nghiên cứu Cleo/Duolingo trước khi thiết kế)

**Phase 4 — Kỹ thuật + Business**
12. Tech stack + FR/NFR + UML + BPMN
13. Competitive Matrix + "10x Better" table (YC framework)
14. SWOT (có Founder-Market Fit) + MOAT 4 tầng (Peter Thiel)
15. Growth: North Star Metric + "Do Things That Don't Scale" + 4+ Viral Loops + Unit Economics + Lean Validation Plan + Theory of Change

**Phase 5 — Polish**
16. Founder story + personal motivation
17. Data Verification pass: cross-check MỌI con số
18. 800-1100 dòng, mọi trích dẫn có [nguồn], diagrams text-based

**Common Errors**:
- ❌ Số liệu ảo → verify từ nguồn gốc (GSO, World Bank, S&P)
- ❌ 5 Whys dừng sớm → phải đến ROOT CAUSE
- ❌ Features không mapping vấn đề → mỗi feature = 1 root cause
- ❌ Growth plan chung chung → kế hoạch CỤ THỂ từng tuần
- ❌ Thiếu viral feature → ≥1 tính năng designed for sharing
- ❌ Thiếu "10x Better" argument → phải chứng minh tốt hơn 10x
