---
name: Architecture Decision Records (ADR)
description: Log quyết định tech/architecture để tránh flip-flop. Auto-trigger khi chọn framework, library, database, design pattern. Triggers on "chọn framework", "dùng gì", "so sánh", "alternative", "tech stack", "nên dùng", "which library", "compare", "vs", "or".
---

# 📝 Architecture Decision Records

> Mỗi quyết định tech quan trọng được log ở đây. AI PHẢI check file này trước khi đề xuất tech mới — nếu đã có ADR cho quyết định tương tự → follow ADR, KHÔNG flip-flop.

## Format ADR Entry

```
### ADR-xxx: [Tên Quyết Định]

> 📅 [YYYY-MM-DD] — Dự án: [tên]

**Context**: [Tại sao cần quyết định này?]
**Options**:
  - A: [Option A] — Pros: ... / Cons: ...
  - B: [Option B] — Pros: ... / Cons: ...
**Decision**: [Chọn gì và TẠI SAO]
**Consequences**: ✅ [Lợi] / ❌ [Hại]
**Status**: Active | Superseded by ADR-xxx
```

---

## Active Decisions

### ADR-001: pandas-ta thay TA-Lib cho Technical Analysis

> 📅 2026-03-15 — Dự án: moondev-agent

**Context**: Cần tính technical indicators (EMA, MACD, Ichimoku) trên Windows.
**Options**:
  - A: `TA-Lib` — Pros: chuẩn industry, nhanh / Cons: cần compile C binary, Windows install cực khó
  - B: `pandas-ta` — Pros: pure Python, pip install, cross-platform / Cons: chậm hơn ~10%, thiếu vài indicator niche
**Decision**: Chọn **pandas-ta** — cross-platform quan trọng hơn speed cho scope dự án.
**Consequences**: ✅ Windows/Mac/Linux đều chạy ngay / ❌ Thiếu vài indicator exotic
**Status**: Active

---

### ADR-002: psycopg2 Connection Pool thay SQLAlchemy

> 📅 2026-03-05 — Dự án: telegram-copy-signal

**Context**: PostgreSQL remote (VPS Nhật), mỗi request mất 10-12s vì tạo TCP connection mới.
**Options**:
  - A: `SQLAlchemy` ORM — Pros: abstraction đẹp / Cons: heavy, thêm ~15 dependencies, overkill cho project nhỏ
  - B: `psycopg2.pool.SimpleConnectionPool` — Pros: lightweight, 0 thêm dependency / Cons: raw SQL
**Decision**: Chọn **psycopg2 pool** — project nhỏ, raw SQL đủ, không cần ORM overhead.
**Consequences**: ✅ Latency 10s → <100ms / ❌ Phải viết SQL thủ công
**Status**: Active

---

### ADR-003: OpenClaw cho Multi-Agent Framework

> 📅 2026-03-16 — Dự án: comarai-agents

**Context**: Cần framework multi-agent (Sales, Content, Marketing, Trading) cho Comarai.
**Options**:
  - A: `LangGraph` — Pros: 40K+ stars, LangChain ecosystem / Cons: heavy, complex graph setup
  - B: `CrewAI` — Pros: 25K+ stars, simple API / Cons: opinionated, lock-in
  - C: `OpenClaw` — Pros: lightweight Chinese framework, simple, active / Cons: smaller community
**Decision**: Chọn **OpenClaw** — simplest API, đủ cho use case, no lock-in.
**Consequences**: ✅ Nhanh setup / ❌ Ít docs tiếng Anh
**Status**: Active

---

## 📋 ADR Changelog

| # | Ngày | Decision | Dự án |
|---|------|----------|-------|
| 001 | 2026-03-15 | pandas-ta > TA-Lib | moondev-agent |
| 002 | 2026-03-05 | psycopg2 pool > SQLAlchemy | telegram-copy-signal |
| 005 | 2026-03-19 | localStorage cho MVP Gamification | vietfi-advisor |
| 006 | 2026-03-21 | Vision OCR > DOM/APIs | tv-vision-ocr |
| 007 | 2026-03-22 | Hybrid localStorage + Supabase sync | vietfi-advisor |

<!-- ADR_APPEND_MARKER — AI append ADR mới TRƯỚC dòng này -->

### ADR-006: Vision OCR (EasyOCR) thay vì Web Scraping/Private APIs cho TradingView

> 📅 2026-03-21 — Dự án: tv-vision-ocr (Báo Cáo Big Plan 2026)

**Context**: Cần lấy data (VNINDEX, OHLC) từ TradingView nhưng API nội địa bị chặn rate-limit. Đồ thị vẽ bằng HTML5 Canvas nên DOM scraper (BeautifulSoup, Selenium) mù hoàn toàn.
**Options**:
  - A: `Reverse APIs` — Pros: Data sạch / Cons: Bị block thường xuyên, đổi token liên tục.
  - B: `DOM Scraping` — Pros: Đơn giản / Cons: Bó tay với Canvas.
  - C: `Computer Vision (EasyOCR)` — Pros: Bypass 100% block mạng, đọc chính xác màn hình hiển thị / Cons: Regex phức tạp, nặng CPU.
**Decision**: Chọn **Computer Vision (EasyOCR)** — Độc lập và miễn nhiễm với giới hạn luồng mạng, thậm chí push lên thành siêu phẩm Portfolio `tv-vision-ocr`.
**Consequences**: ✅ Miễn nhiễm block API / ✅ Giải quyết bài toán Canvas / ❌ Setup ban đầu 1GB (PyTorch/OpenCV)
**Status**: Active

---


### ADR-005: LocalStorage thay vì Database (Supabase) cho Gamification Engine MVP

> 📅 2026-03-19 — Dự án: vietfi-advisor

**Context**: Cần lưu trữ state gamification (XP, streak, quests, lessons) cho MVP đi thi.

**Options**:
  - A: `Supabase/PostgreSQL` — Pros: Sync cross-device, data an toàn / Cons: Cần setup Auth, DB schema, RLS, overkill cho MVP chạy demo
  - B: `LocalStorage (Client-side)` — Pros: Code cực nhanh, zero latency, không cần Auth, demo mượt / Cons: Mất data khi clear cache/đổi máy, dễ bị cheat

**Decision**: Chọn **LocalStorage** — Ưu tiên tốc độ hoàn thiện UI/UX và gamification loop cho cuộc thi. Migrate sang Supabase sau khi validation xong.

**Consequences**: ✅ Tốc độ dev x3 / ❌ Gặp lỗi SSR Hydration (đã fix bằng Pattern 22) / ❌ Data không cross-device

**Status**: Superseded by ADR-007

---


### ADR-004: VieNeu-TTS Fork thay FPT.AI/ElevenLabs cho VietFi TTS

> 📅 2026-03-19 — Dự án: vietfi-advisor

**Context**: Cần giọng TTS tiếng Việt tự nhiên cho Vẹt Vàng mascot. Yêu cầu: choe choé, tự nhiên, voice cloning, số lần gọi API tối thiểu.

**Options**:
  - A: `Web Speech API` — Pros: zero setup / Cons: không có vi-VN trên Windows, nghe robot
  - B: `FPT.AI TTS` — Pros: 100k chars/tháng free, 18+ giọng Việt / Cons: cần API key, phụ thuộc external service
  - C: `ElevenLabs` — Pros: voice cloning tốt, hỗ trợ Vietnamese từ July 2024 / Cons: chỉ 10k chars/tháng free
  - D: `VieNeu-TTS (pnnbao97)` — Pros: open source Apache 2.0, Vietnamese focus, voice cloning 3-5s, offline, fork được / Cons: Python backend, dependency conflicts, cần venv riêng

**Decision**: Chọn **VieNeu-TTS fork** — offline hoàn toàn sau pre-render, zero API cost, voice cloning được, có thể nâng cấp và push portfolio.

**Strategy**: Pre-render 40 quotes thành MP3 1 lần → demo chạy offline 100%. Tương lai: FastAPI wrapper + IndexedDB cache cho dynamic text.

**Consequences**: ✅ Zero runtime cost / ✅ Portfolio value / ❌ Setup phức tạp hơn / ❌ Cần venv riêng tránh conflict numpy/tokenizers

**Bug known**: `'NoneType' object is not callable` ở destructor VieNeuTTS — không ảnh hưởng output, bọc try/finally.

**Status**: Active


### ADR-007: Hybrid localStorage + Supabase Sync cho VietFi Advisor

> 📅 2026-03-22 — Dự án: vietfi-advisor (supersedes ADR-005)

**Context**: MVP dùng localStorage (ADR-005) đã validate thành công. Giờ cần sync cross-device cho cuộc thi WDA 2026, nhưng vẫn giữ guest mode.

**Options**:
  - A: `Full Supabase only` — Pros: 1 source of truth / Cons: Bắt buộc login, mất guest mode
  - B: `Hybrid: localStorage + Supabase background sync` — Pros: Giữ guest mode, zero-latency UI, sync khi login / Cons: 2 data sources
  - C: `IndexedDB + sync` — Pros: Capacity lớn / Cons: API phức tạp, overkill

**Decision**: Chọn **Hybrid localStorage + Supabase** — localStorage = instant cache, Supabase = persistent store. Background sync non-blocking.

**Pattern**:
```
Guest:      UI ←→ localStorage
Logged-in:  UI ←→ localStorage ←→ Supabase (background)
First login: localStorage → migrate → Supabase (one-time)
```

**Key Files**: `user-data.ts`, `migrate-local.ts`

**Consequences**: ✅ Zero-latency UI / ✅ Guest mode OK / ✅ Cross-device sync / ❌ 2 data sources / ❌ Need `any` cast (no generated types)

**Status**: Active
