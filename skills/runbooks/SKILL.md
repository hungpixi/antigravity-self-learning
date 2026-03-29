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
1. Mở n8n## 📋 Runbook Changelog

| # | Ngày | Runbook | Áp dụng |
|---|------|---------|---------| 
| 001 | 2026-03-16 | MQL5 Compile & Backtest | Trading bots |
| 002 | 2026-03-16 | GitHub Push Portfolio | Public repos |
| 003 | 2026-03-17 | Netlify Deploy | Static sites |
| 004 | 2026-03-10 | n8n Workflow Setup | Automation |
| 005 | 2026-03-18 | Startup Report Writing | Competition reports |
| 010 | 2026-03-22 | OpenClaw Docker Setup | AI Agency |

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

### RB-008: Multi-Page UX Audit Report

> 📅 2026-03-19 — Áp dụng cho: audit UI/UX web app, dashboard, mobile app

**Khi nào dùng**: Phân tích UX nhiều trang (>3 pages)
**Quy tắc VÀNG**: **KHÔNG xem hết → viết hết. Phải: xem 1 trang → viết phân tích → xem trang tiếp.**

**Steps**:
1. Tạo report skeleton (headings cho từng trang + summary + recommendations)
2. **Với MỖI trang** (loop):
   a. Browser navigate → screenshot
   b. Phân tích 6 tiêu chí: hierarchy, density, CTA, nav, empty state, responsive
   c. VIẾT NGAY phần phân tích cho trang đó vào report
   d. Mới chuyển sang trang tiếp
3. Sau khi xong tất cả trang → viết Summary + Prioritized Recommendations
4. Review lại toàn bộ report → polish

**6 Tiêu Chí Audit Mỗi Trang**:
```
1. Visual Hierarchy — Thông tin quan trọng nhất có nổi bật không?
2. Information Density — Quá nhiều? Quá ít? Tỷ lệ content vs whitespace?
3. CTA Clarity — User biết phải làm gì tiếp theo không?
4. Navigation — Dễ quay lại? Biết mình đang ở đâu?
5. Empty/Default State — Khi chưa có data thì hiển thị gì?
6. Mobile Responsiveness — Có vỡ layout trên mobile không?
```

**Anti-Patterns**:
- ❌ Xem hết 10 pages → bắt đầu viết = **OVER CONTEXT, forget details**
- ❌ Screenshot tất cả rồi mới phân tích = **Mất observation freshness**
- ✅ Loop: view → analyze → write → next page

**Common Errors**:
- Browser subagent over context khi navigate quá nhiều pages trong 1 session
- Quên so sánh với reference design (nếu có prototype/mockup)
- Chỉ nói "đẹp/xấu" mà không nêu lý do UX + đề xuất cụ thể

---

### RB-009: Vercel Auto-Deploy Bypass Hobby Limit (GitHub Actions)

> 📅 2026-03-20 — Áp dụng cho: Vercel projects trên gói Free (Hobby) có external PRs

**Khi nào dùng**: Khi có team member / external dev push code hoặc tạo Pull Request, Vercel Free sẽ block Deploy Preview vì lỗi "Hobby teams do not support collaboration".
**Steps**:
1. Lấy Vercel Token cá nhân (từ Dashboard Account Settings).
2. Lấy Org ID và Project ID của Vercel project.
3. Import Secrets vào GitHub repository: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`.
4. Tạo file `.github/workflows/vercel-deploy.yml`:
   - Job Install Vercel CLI: `npm install --global vercel@latest`
   - Job Deploy Preview (on pull_request): `vercel deploy --token=${{ secrets.VERCEL_TOKEN }} --yes`
   - Job Deploy Prod (on push main/master): `vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }} --yes`
5. Chạy lệnh: `gh auth refresh -s workflow` (nếu terminal báo lỗi lack of workflow scope).
6. Commit & Push file YAML.

**Bypass Mechanism**:
GitHub Actions chạy tự động trên server GitHub, đóng giả làm chính user owner qua Token. Vercel cho rằng owner đang tự deploy thủ công bằng CLI nên cho phép pass qua mọi luật Block rườm rà.

**Common Errors**:
- `refusing to allow an OAuth App to create or update workflow`: Terminal chưa cấp quyền workflow. Dùng `gh auth refresh -s workflow`.

---

### RB-010: OpenClaw Docker Setup (AI Agency)

> 📅 2026-03-22 — Áp dụng cho: OpenClaw AI agency trên Docker

**Khi nào dùng**: Setup mới hoặc tái cấu hình OpenClaw Docker
**Steps**:
1. **Pull image**: `docker pull ghcr.io/openclaw/openclaw:latest`
2. **docker-compose.yml** — chỉ mount config, KHÔNG mount volume lên `/.openclaw`:
   ```yaml
   volumes:
     - ./config:/app/config
     - ./context.md:/app/context.md:ro
   environment:
     - OPENROUTER_API_KEY=sk-or-v1-xxx
     - TELEGRAM_BOT_TOKEN=xxx
   ```
3. **Start**: `docker compose up -d`
4. **Approve Telegram pairing**:
   - Nhắn tin vào bot → lấy mã pairing
   - `docker exec openclaw_agency openclaw pairing approve telegram <CODE>`
5. **Inject auth-profiles.json** (format v2026.2.19+):
   ```bash
   docker cp ./auth-profiles.json openclaw_agency:/home/node/.openclaw/agents/main/agent/auth-profiles.json
   docker exec -u root openclaw_agency chown node:node /home/node/.openclaw/agents/main/agent/auth-profiles.json
   ```
6. **Set model**: Telegram `/model` → chọn model OpenRouter
7. **Install skills**: 
   ```bash
   docker exec openclaw_agency npx clawhub install <slug> --force
   ```
   *Lưu ý rate limit 20 req/min — cài từng cái với `sleep 5` giữa mỗi cái*
8. **Restart**: `docker exec openclaw_agency kill 1` (container auto-restart)

**auth-profiles.json Format**:
```json
{
  "version": 1,
  "profiles": {
    "openrouter": { "provider": "openrouter", "mode": "api_key", "key": "sk-or-v1-xxx" },
    "anthropic": { "provider": "anthropic", "mode": "api_key", "key": "sk-or-v1-xxx" }
  }
}
```

**Common Errors**:
- EACCES permission → LUÔN `docker exec -u root ... chown node:node` sau `docker cp`
- `No API key for provider "anthropic"` → auth-profiles.json sai format hoặc sai owner
- Container crash loop → check `docker logs`, thường do volume mount conflict
- ClawHub rate limit → `sleep 5` giữa các lần install
- Model mặc định Anthropic → phải gõ `/model` trên Telegram chọn OpenRouter model

### RB-011: Supabase Migration (localStorage → Hybrid Sync)

> 📅 2026-03-22 — Áp dụng cho: Next.js apps dùng localStorage cần sync cloud

**Khi nào dùng**: App đang dùng localStorage, cần thêm Supabase sync mà KHÔNG break guest mode
**Steps**:
1. **List tất cả localStorage keys**: `grep -r "localStorage\." --include="*.ts" --include="*.tsx"`
2. **Tạo Supabase tables**: 1 table per data domain, RLS policies cho mỗi table
3. **Tạo auto-create trigger**: `ON INSERT auth.users → INSERT profiles + gamification`
4. **Viết abstraction layer** (`user-data.ts`):
   - `getAuthUserId()` → async, cache result
   - `getCachedUserId()` → sync, dùng cached value
   - Mỗi CRUD function: check auth → Supabase nếu logged in, return default nếu guest
5. **Viết migration helper** (`migrate-local.ts`):
   - Đọc tất cả `localStorage` keys → upsert Supabase
   - Set flag `migrated=true` → không chạy lại
6. **Update existing code**: Thêm `if (getCachedUserId()) { syncToSupabase().catch(() => {}) }` sau mỗi `localStorage.setItem`
7. **Trigger migration**: Trong layout/root component, `getAuthUserId().then(id => migration(id))`
8. **Fix search_path**: `SET search_path = public` cho tất cả SECURITY DEFINER functions
9. **Verify**: `npm run build` + `npx vitest run` + Supabase security advisor

**Common Errors**:
- Supabase client chưa có generated types → `row: any` cast (P65)
- `function_search_path_mutable` warning → thêm `SET search_path = public`
- RLS block insert → check `WITH CHECK` clause, không chỉ `USING`
- Migration loop → check `vietfi_migrated` flag trước khi chạy

---

<!-- RUNBOOK_APPEND_MARKER — AI append runbook mới TRƯỚC dòng này -->ush main/master): `vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }} --yes`
5. Chạy lệnh: `gh auth refresh -s workflow` (nếu terminal báo lỗi lack of workflow scope).
6. Commit & Push file YAML.

**Bypass Mechanism**:
GitHub Actions chạy tự động trên server GitHub, đóng giả làm chính user owner qua Token. Vercel cho rằng owner đang tự deploy thủ công bằng CLI nên cho phép pass qua mọi luật Block rườm rà.

**Common Errors**:
- `refusing to allow an OAuth App to create or update workflow`: Terminal chưa cấp quyền workflow. Dùng `gh auth refresh -s workflow`.

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
