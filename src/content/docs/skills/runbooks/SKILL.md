---
title: "SKILL"
name: Operational Runbooks
description: "Quy trình vận hành lặp lại đã chuẩn hóa. Auto-trigger khi deploy, compile, setup project, push GitHub, backtest. Triggers on \"deploy\", \"compile\", \"push\", \"setup\", \"backtest\", \"quy trình\", \"cách chạy\", \"how to run\", \"how to deploy\", \"step by step\"."
---

# 🏃 Operational Runbooks

> Mỗi quy trình lặp lại >3 bước được log ở đây. AI đọc runbook thay vì hỏi lại user mỗi session.
> **Memory Sync**: Khi tạo runbook liên quan tool/service mới → tạo `memory/reference_*.md` pointer.

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
| 011 | 2026-03-22 | Supabase Hybrid Sync | Next.js App |
| 012 | 2026-04-02 | Setup & Chạy VEO_TOOL | AI Video Automation |
| 013-017 | 2026-04-02 | Workflow Advanced của VEO_TOOL | Bypass + Rotate + Graceful |

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

### RB-012: Setup & Chạy VEO_TOOL (Video Automation)

> 📅 2026-04-02 — Áp dụng cho: VEO_TOOL (Auto SORA/Grok/Veo)

**Khi nào dùng**: Setup môi trường và chạy app VEO_TOOL cho account "Ultra Google".
**Steps**:
1. Cài đặt Python (ưu tiên >=3.10) và thư viện: `pip install -r requirements.txt` (hoặc uv).
2. Khi khởi chạy lần đầu tiên, app sẽ tự tải Playwright Chromium: `python main.py`. Cần đợi tải xong mượt mà không thoát ngang (khoảng size ~172MB).
3. Thêm tài khoản Google vào file cấu hình `list_profile.json` nằm trong mục `data_general`.
4. Không bao giờ chạy `--headless=new` khi login vào Google vì sẽ dính Block "Browser uncontrolled".
5. App tự động bypass first run flag và bind vào CDP `9222`.

**Common Errors**:
- `Process Zombie`: Nếu kill UI PyQt6 mà chưa đóng Chromium, background process vẫn chạy, cần dùng Runbook xử lý kill process PID.
- UI Treo: Do gọi Async Playwright trên luồng chính thay vì dùng `threading.Thread`.

---

### RB-013 đến RB-017: Workflow Vận Hành Cao Cấp VEO_TOOL

> 📅 2026-04-02 — Áp dụng cho: VEO_TOOL

Tool VEO yêu cầu các thao tác bảo hiểm ở cấp độ Runbook để sống sót qua các thuật toán chống Bot:
* **RB-013 (Bypass Detection)**: Trước khi Extract Token của Veo/Google, bắt buộc phải simulate một thao tác Cuộn trang (`page.evaluate("window.scrollBy(0, 100)")`) hoặc hover nhẹ button, để Captcha Invisible ghi nhận Event Hành vi người dùng.
* **RB-014 (Zombie Hunting)**: Khi Force Close Tool, mở PowerShell chạy lệnh lọc rác: `Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object CommandLine -match "remote-debugging-port" | Invoke-CimMethod -MethodName Terminate`.
* **RB-015 (Profile Rotation Protocol)**: Để chạy Multi-threads, không bao giờ truy cập chung 1 `user_data_dir`. Phân tách thành `profile_1`, `profile_2` trỏ tới các thư mục vật lý khác nhau và Port CDP khác nhau (ví dụ 9222 và 9223).
* **RB-016 (UI Recovery)**: Nếu cờ `STOP=1` không thể huỷ bỏ vòng lặp Async, bấm "Stop" 3 lần liên tiếp sẽ kích hoạt Force Terminate Worker Thread bằng ngoại lệ Native của PyQt.
* **RB-017 (Failover 403)**: Khi tài khoản báo quá tải (Limit Reached - Code 403), Runbook tự động: Mở Tab Settings > Clear Website Data > Sleep 120s > Login lại Account dự phòng.

### RB-019: Publish VS Code Extension (Open VSX)

> 📅 2026-04-05 — Áp dụng cho: publish public VS Code extensions

**Khi nào dùng**: Sau khi đóng gói thành `.vsix` và cần phát hành/update lên Open VSX Registry.
**Steps**:
1. Đảm bảo file `package.json` có trường `"publisher"` chuẩn xác.
2. Kiểm tra `OVSX_PAT` đã được load trong User Environment Variable.
3. Chạy: `npx ovsx publish [folder_hoac_file.vsix] -p $env:OVSX_PAT` (hoặc pass trực tiếp token `-p token...`).
4. Kiểm tra trang https://open-vsx.org.

**Common Errors**:
- Lỗi `No metadata parsed`: Đường dẫn `.vsix` không đúng.
- Thiếu Authentication: Token hết hạn (Cần quay lại Open VSX -> Settings -> Access Tokens để sinh lại).

| 019 | 2026-04-05 | Publish VS Code Extension | VSX Registry |
| 020 | 2026-04-07 | Reverse Engineering 3D WebGL / Vue Chunks | Portfolio Clone |
<!-- RUNBOOK_APPEND_MARKER — AI append runbook mới TRƯỚC dòng này -->

### RB-020: Reverse Engineering & Patching Compiled WebGL/Astro Chunks

> 📅 2026-04-07 — Áp dụng cho: WebGL Portfolios, Astro/Vue compiled templates bị đóng gói

**Khi nào dùng**: Cần clone một trang web tương đối nâng cao (như Three.js slider) nhưng không có source code JavaScript gốc, chỉ có framework build `dist/` (các file JS đã minified / obfuscated).

**Steps**:
1. Dùng Subagent Screenshot / Puppeteer chụp ảnh các dự án thực tế muốn đưa vào 3D thay vì ảnh Placeholder. Convert sang WebP để WebGL tối ưu dung lượng Texture.
2. Tìm các biến Data Array Routing trong `public/chunks/*.js` bằng lệnh Grep. (Tham khảo cấu trúc Array mapping của template đích và phân tích Object Keys liên quan đến Title, Description).
3. Viết script Python đọc và `replace` trực tiếp JSON/Array strings trong file `.js` thành thông tin cá nhân.
4. Để scale ứng dụng (Ví dụ từ Slider 4 projects thành 8 projects): Copy đúp các mapping Component (ví dụ `Bt` -> `Bt2`, `xt` -> `xt2`) và push vào các Array Quản lý Routes 3D WebGL tương ứng.
5. Thay đổi Font chữ (Typography): KHÔNG cần Webpack recompile Geometry Map 3D. Chỉ cần tải Google Font (.woff2), đổi tên file giống font cũ (.ttf, .otf, v.v) đè thẳng lên thư mục `public/fonts/`. WebGL Text Component sẽ tự động nhận font mới với ngôn ngữ được parse mặc định.
6. Xử lý UI Localization 2 Ngôn Ngữ: Dùng lệnh Python patch biến reactive (như ngôn ngữ `yt(Xo)`) vào các Text Element tĩnh vốn dĩ bị Vue sinh flag `t[0]||(t... -1)`. Xóa sạch lớp cache hoist này bằng regexp.

**Common Errors**:
- Lỗi khoảng trắng hay ngoặc két (Unicode BOM) khi dùng lệnh thay thế `python -c "..."` trên CMD Windows ->  NÊN tạo hẳn file run `patch.py` riêng biệt cho xử lý utf-8.
- Astro template đời cũ văng lỗi Module / "Cannot read properties of undefined" -> Lỗi thời `Astro.glob`, xem Rule P93 trong Bug-Fix Skill đổi thành helper `import.meta.glob`.

### RB-018: Dọn Secret khỏi Rule/Config Local và chuyển sang User Env

> 📅 2026-04-03 — Áp dụng cho: Gemini / Codex / local AI tooling

**Khi nào dùng**: Khi phát hiện token thô nằm trong `GEMINI.md`, `settings.json`, `mcp_config.json`, `.env.example`, README local.
**Steps**:
1. Đọc file nguồn, xác định toàn bộ token đang bị hardcode.
2. Chuyển mỗi token sang User Environment Variable bằng PowerShell `[Environment]::SetEnvironmentVariable(..., 'User')`.
3. Rewrite rule/config để chỉ còn tên biến môi trường hoặc wrapper command đọc `$env:...`.
4. Tạo hoặc cập nhật `context.md` chỉ với tên biến, contact bundle, runtime defaults.
5. Verify `.gitignore` đã chặn `context.md`, credentials, `.env`, key files.
6. Restart Gemini/Codex để process mới nhận env mới.

**Common Errors**:
- Set env xong nhưng tool vẫn báo thiếu token → app đang chạy từ process cũ, phải restart.
- JSON config để literal `$env:FOO` trong field `env` → nhiều client không expand, nên để process tự inherit env hoặc dùng wrapper shell.
- Xóa token khỏi rule nhưng quên rotate token cũ đã lộ → vẫn còn rủi ro.

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
