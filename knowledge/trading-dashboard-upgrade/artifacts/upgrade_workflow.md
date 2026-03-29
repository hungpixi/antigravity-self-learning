# Trading Dashboard PROMAX Upgrade — Quy Trình

## Tổng Quan
Upgrade trading signal dashboard từ SQLite/basic UI → PostgreSQL + Redis + S3 + PROMAX UI/UX.

## Điều Kiện Tiên Quyết
- Free dev resources: xem KI `free-dev-resources` (PostgreSQL, Redis, S3 từ hoctuthien.com)
- UI/UX Pro Max skill: `npx -y uipro-cli init --ai antigravity`

## Quy Trình 5 Phase

### Phase 1: Database Migration (SQLite → PostgreSQL)
1. Tạo DB riêng trên shared PostgreSQL: `CREATE DATABASE <project_name>`
2. Rewrite `database.py` dual-mode — auto-detect `DATABASE_URL` env var
3. Placeholder abstraction: `%s` cho PG, `?` cho SQLite
4. Test: `python test_connections.py`

### Phase 2: Redis Cache
1. Tạo `cache.py` với graceful fallback (no-op khi Redis unavailable)
2. Cache patterns: stats (5s TTL), prices (2s TTL), pub/sub cho WebSocket
3. Bot status tracking qua Redis keys

### Phase 3: S3/MinIO Integration
1. Dùng `boto3` client với custom endpoint
2. Chart exports, trade screenshots backup

### Phase 4: Frontend PROMAX (UI/UX Pro Max Skill)
```bash
# Step 1: Generate design system
python .agent/skills/ui-ux-pro-max/scripts/search.py "fintech crypto trading dashboard dark" --design-system -p "Project Name"

# Step 2: Chart recommendations
python .agent/skills/ui-ux-pro-max/scripts/search.py "real-time trading P&L analytics" --domain chart

# Step 3: UX guidelines
python .agent/skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux
```
4. Apply checklist: no emoji icons → SVG, cursor-pointer, 150-300ms transitions, WCAG contrast

### Phase 5: Push GitHub
- Comarai branding
- `.env` và `context.md` trong `.gitignore`
- README portfolio-grade

## Lưu Ý Quan Trọng
- **KHÔNG** push API keys/credentials lên GitHub
- Database credentials lưu trong `.env` (gitignored) và `context.md` (gitignored)
- Free resources chỉ dùng cho dev/test, KHÔNG production
- Redis có thể timeout do firewall → code phải có graceful fallback
