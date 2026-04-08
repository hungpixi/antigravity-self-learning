---
name: Paperclip AI Setup And Deploy Lessons
description: "Tóm tắt cách setup, mode triển khai, adapter prerequisites, và bài học áp dụng Paperclip AI làm control plane cho hệ agent."
type: reference
---

## Paperclip AI là gì

- Paperclip là control plane để điều phối nhiều AI agents theo mô hình company: companies, org chart, goals, issues, budgets, approvals, heartbeats.
- Nó không thay thế agent runtime. Nó đứng trên Codex, Claude, Cursor, OpenClaw, shell process, HTTP webhook.
- Phù hợp khi cần quản lý nhiều agent dài hạn. Không đáng dùng nếu chỉ chạy một crawler/script đơn lẻ.

## Local setup nhanh nhất

```bash
cd D:\code\crawl-ai-agent\paperclip-ai
pnpm install
pnpm dev
```

- Yêu cầu chính: Node.js 20+, `pnpm` 9+.
- API và UI cùng chạy ở `http://localhost:3100`.
- Nếu không set `DATABASE_URL`, Paperclip tự dùng embedded PostgreSQL.
- Lệnh bootstrap tiện nhất là `pnpm paperclipai run` hoặc `npx paperclipai onboard --yes`.

## Những path quan trọng

- Config: `~/.paperclip/instances/default/config.json`
- Database: `~/.paperclip/instances/default/db`
- Storage: `~/.paperclip/instances/default/data/storage`
- Secrets key: `~/.paperclip/instances/default/secrets/master.key`
- Logs: `~/.paperclip/instances/default/logs`
- Workspace fallback cho agent local: `~/.paperclip/instances/default/workspaces/<agent-id>`

## Adapter lessons

- `codex_local` cần CLI `codex` + `OPENAI_API_KEY`.
- `claude_local` cần CLI `claude` + `ANTHROPIC_API_KEY`.
- Cả hai đều cần `cwd` là absolute path và writable.
- Session persistence phụ thuộc workspace/cwd. Đổi `cwd` là dễ mất continuity.
- Paperclip inject env runtime cho agent như `PAPERCLIP_API_URL`, `PAPERCLIP_API_KEY`, `PAPERCLIP_AGENT_ID`, `PAPERCLIP_RUN_ID`.

## Chọn deployment mode đúng

- `local_trusted`: local máy cá nhân, nhanh nhất, không login.
- `authenticated + private`: dùng qua Tailscale/VPN/LAN, có login, hợp cho private ops.
- `authenticated + public`: internet-facing, bắt buộc có canonical public URL và security check chặt hơn.

## Bài học triển khai quan trọng

1. Quickstart local nên giữ `local_trusted`, vì đây là mode ít ma sát nhất để test luồng.
2. Nếu deploy để truy cập từ máy khác hoặc qua private network, chuyển sang `authenticated + private`, không nên cố expose `local_trusted`.
3. Khi dùng Docker/public auth flow, phải set ít nhất:
   - `BETTER_AUTH_SECRET`
   - `PAPERCLIP_PUBLIC_URL`
   - `PAPERCLIP_DEPLOYMENT_MODE=authenticated`
   - `PAPERCLIP_DEPLOYMENT_EXPOSURE=private|public`
4. Toàn bộ state quan trọng nằm dưới `PAPERCLIP_HOME`, nên volume mount thư mục này là bắt buộc nếu không muốn mất DB, assets, secrets, và workspace.
5. Embedded PostgreSQL rất hợp local hoặc single-node Docker. Nếu muốn scale/multi-node, nên tách:
   - DB sang external Postgres/Supabase
   - file storage sang S3-compatible storage
6. Docker image của repo đã preinstall `codex`, `claude`, `opencode-ai`, nhưng không tự có API keys. Thiếu key thì app vẫn boot, chỉ adapter check fail.
7. Secrets không nên để inline trong agent config khi triển khai thật. Dùng secret refs và cân nhắc bật `PAPERCLIP_SECRETS_STRICT_MODE=true`.

## Use case phù hợp hơn: digital marketing agency

- Paperclip hợp hơn với mô hình agency đa phòng ban so với một repo crawl đơn lẻ.
- Use case đúng là: thay việc brainstorm, planning, phân công và follow-up thủ công trên ChatGPT bằng một control plane có hierarchy, backlog, approvals và recurring heartbeats.
- Mapping nên theo structure agency:
  - CEO / Agency Director: giữ goal doanh thu, positioning, budget, duyệt chiến lược
  - Strategy Planner: research thị trường, chân dung khách hàng, campaign plan, funnel map
  - Content Lead: lập content pillars, calendar, brief, tiêu chuẩn brand voice
  - SEO Lead: keyword clusters, content gap, internal linking, technical audit backlog
  - Content Writer agents: viết bài, outline, ad copy, landing page copy
  - SEO Specialist agents: on-page audit, SERP analysis, schema/meta/internal link tasks
  - Design / Creative agent: visual brief, asset requests, ad creative variants
  - QA / Editor agent: kiểm tra factual quality, brand consistency, formatting, plagiarism/process QA
  - Ops / Reporting agent: tổng hợp KPI, cost, output velocity, weekly review
- Với use case này, giá trị lớn nhất của Paperclip là:
  - chuyển từ chat-based planning sang task-based orchestration
  - giữ chain of command rõ ràng
  - lưu audit trail và session continuity giữa các lần chạy
  - tách strategy, execution, QA, reporting thành các agent chuyên trách

## Cách triển khai agency marketing thực dụng

1. Bắt đầu bằng một company duy nhất, không tạo nhiều công ty sớm.
2. Tạo 4 lớp nhân sự trước:
   - CEO
   - Planner/Strategist
   - Content
   - SEO
3. Chưa cần agent quá nhỏ ngay từ đầu. Mỗi phòng ban bắt đầu bằng 1 lead agent đa năng trước.
4. Chỉ tách thêm specialist khi backlog đủ lớn hoặc quality của lead agent không còn ổn.
5. Tất cả output nên đi qua QA/Editor trước khi publish hoặc handoff cho người thật.
6. Dùng approvals cho:
   - campaign strategy
   - publish plan
   - hiring agent mới
   - thay đổi budget
7. Dùng recurring heartbeats cho:
   - weekly content planning
   - keyword monitoring
   - SEO audit định kỳ
   - KPI/report recap

## Rule of thumb cho use case này

- Nếu mục tiêu là thay ChatGPT trong khâu planning và điều phối agency nội bộ, Paperclip là đúng hướng.
- Nếu mục tiêu chỉ là generate content từng lần, dùng trực tiếp ChatGPT/Codex vẫn nhẹ hơn.
- Paperclip chỉ đáng triển khai khi anh muốn một "agency operating system", không phải một chat assistant.

## Docker quickstart nhớ lâu

```bash
docker compose -f docker-compose.quickstart.yml up --build
```

- Compose mặc định mount data vào `./data/docker-paperclip:/paperclip`.
- Container chạy `HOST=0.0.0.0`, phù hợp để expose ra ngoài.
- Với auth/browser flow, luôn kiểm tra `PAPERCLIP_PUBLIC_URL` khớp URL truy cập thật.

## Rule of thumb

- Bắt đầu local: embedded Postgres + local disk + `local_trusted`
- Private ops: Docker + persistent volume + `authenticated/private`
- Public production: external Postgres + S3 storage + `authenticated/public` + strict secrets
