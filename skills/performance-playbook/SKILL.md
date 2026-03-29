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

### PERF-004: Tối ưu Token Budget bằng Lazy-Loading Affiliate Skills

> 📅 2026-03-28 — Dự án: Antigravity IDE (Comarai Agency)

**Problem**: Customization token budget bị over limit do loading cùng lúc 33+ thư mục skills cực nặng vào global memory (~8,500 tokens).
**Solution**: Gộp 33+ thư mục con vào 1 "Master Playbook" skill, định tuyến agent đọc file on-demand thay vì load tất cả lúc khởi động (`/affiliate-playbook/SKILL.md`).
**Before**: > 8,500 tokens consumed, gây crash hoặc limit errors cho các task thông thường của agent.
**After**: ~400 tokens consumed by the master playbook.
**Stack**: Prompt Engineering / MCP Schema Optimization
**Rule**: **Không load toàn bộ chi tiết skills dạng global instructions. Dùng Master Playbook để trỏ (Lazy-load) nội dung khi user thực sự gọi lệnh/keyword.**

---

### PERF-005: Ngăn MQL5 Memory Exhausted trong Tester & Loại bỏ StringSplit

> 📅 2026-03-29 — Dự án: CCBSN_EA

**Problem**: MT5 báo lỗi `no memory for ticks generating` hoặc Agent memory cạn kiệt sập 663MB RAM khi test. Nguyên nhân 1: Dùng `StringSplit` trên OnTick() tạo ra triệu lượt cấp phát mảng rác. Nguyên nhân 2: Khởi tạo tất cả 7+ indicator handles bằng hàm `iMA()`, `iBB()` trong `OnInit()` kể cả khi InpSignalMode hiện tại KHÔNG SỬ DỤNG tới.
**Solution**: 1. Tiền xử lý (Parse) chuỗi thời gian thành Integer một lần duy nhất ở `OnInit`, OnTick() chỉ so sánh số nguyên. 2. Xét điều kiện `InpSignalMode` ngay trong `OnInit()`, chỉ cấp phát bộ nhớ (handle) cho Indicator nào thực sự có trong chiến thuật.
**Before**: MT5 Tester ngốn 600MB+ RAM/Agent, Sập lỗi OOM (Out of Memory) trong 5-10s đầu Optimization.
**After**: MT5 Tester mượt mà, RAM < 50MB/Agent, backtest siêu tốc độ cao hơn gấp 10 lần.
**Stack**: MQL5, MT5 Strategy Tester
**Rule**: **Tuyệt đối không cấp phát mảng String trong OnTick(). Luôn bọc điều kiện `if()` quanh hàm khởi tạo Handle Indi trong OnInit().**

---

## 📋 Performance Changelog

| # | Ngày | Pattern | Improvement |
|---|------|---------|-------------|
| 001 | 2026-03-05 | Connection Pooling | 10s → <100ms |
| 002 | 2026-03-17 | Lookback Limit | Labels fix + performance |
| 003 | 2026-03-16 | Cache GetPipPoint | 60 calls/min → 1 call |
| 004 | 2026-03-28 | Lazy-Loading Custom Skills | 8,500 tokens → ~400 tokens |
| 005 | 2026-03-29 | MQL5 No Memory Fix | MT5 Crash Fix, 10x Tester Speed |

<!-- PERF_APPEND_MARKER — AI append pattern mới TRƯỚC dòng này -->
