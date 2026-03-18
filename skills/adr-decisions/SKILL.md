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
| 003 | 2026-03-16 | OpenClaw > LangGraph/CrewAI | comarai-agents |

<!-- ADR_APPEND_MARKER — AI append ADR mới TRƯỚC dòng này -->
