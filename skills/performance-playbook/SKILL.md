---
name: Performance Optimization Playbook
description: Patterns tối ưu hiệu suất đã chứng minh bằng metrics. Auto-trigger khi optimize, slow, latency, memory, performance. Triggers on "chậm", "slow", "optimize", "performance", "latency", "memory", "cache", "tối ưu", "nhanh hơn", "giảm thời gian".
---

# ⚡ Performance Optimization Playbook

> Mỗi optimization có metrics trước/sau. AI check playbook này trước khi optimize — nếu đã có pattern → áp dụng ngay, không phải rediscover.

## Format Entry

```
### PERF-xxx: [Tên Pattern]

> 📅 [YYYY-MM-DD] — Dự án: [tên]

**Problem**: [Vấn đề gì, metrics trước]
**Solution**: [Làm gì]
**Before**: [Metric cụ thể]
**After**: [Metric cụ thể]
**Stack**: [Công nghệ liên quan]
**Rule**: [1 dòng để nhớ]
```

---

## Active Patterns

### PERF-001: Connection Pooling cho Remote PostgreSQL

> 📅 2026-03-05 — Dự án: telegram-copy-signal

**Problem**: Mỗi request tạo TCP connection mới tới VPS Nhật → latency cực cao
**Solution**: Dùng `psycopg2.pool.SimpleConnectionPool` giữ connections sẵn
**Before**: 10-12 giây per request
**After**: <100ms per request
**Stack**: Python + psycopg2 + PostgreSQL remote
**Rule**: **LUÔN pool khi database remote. Không bao giờ tạo connection mới mỗi request.**

---

### PERF-002: PineScript Lookback Limit cho Labels

> 📅 2026-03-17 — Dự án: pinescript-ict

**Problem**: PineScript ~500 labels limit. Tạo label mỗi bar → label cũ bị xoá → entry signal biến mất
**Solution**: Input `Show Last N Bars` (default 2000) + `size.tiny` labels + tooltip
**Before**: Labels biến mất sau ~500 bars, chart lag
**After**: Chỉ render N bars gần nhất, chart mượt, labels đầy đủ
**Stack**: PineScript v5 + TradingView
**Rule**: **PineScript luôn cần lookback limit. Labels dùng size.tiny + tooltip chi tiết.**

---

### PERF-003: Cache `GetPipPoint()` Trong MQL5

> 📅 2026-03-16 — Dự án: IchiDCA_CCBSN

**Problem**: `GetPipPoint()` gọi lặp mỗi tick → thừa computation
**Solution**: Cache vào global `g_pipPoint` trong `OnInit()`
**Before**: Gọi `SymbolInfoDouble()` ~60 lần/phút
**After**: Gọi 1 lần duy nhất khi init
**Stack**: MQL5
**Rule**: **Giá trị không đổi (pip size, lot step) → cache trong OnInit(), không gọi lặp.**

---

## 📋 Performance Changelog

| # | Ngày | Pattern | Improvement |
|---|------|---------|-------------|
| 001 | 2026-03-05 | Connection Pooling | 10s → <100ms |
| 002 | 2026-03-17 | Lookback Limit | Labels fix + performance |
| 003 | 2026-03-16 | Cache GetPipPoint | 60 calls/min → 1 call |

<!-- PERF_APPEND_MARKER — AI append pattern mới TRƯỚC dòng này -->
