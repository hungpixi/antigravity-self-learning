---
name: Performance Optimization Playbook
description: "Patterns tối ưu hiệu suất đã chứng minh bằng metrics. Auto-trigger khi optimize, slow, latency, memory, performance. Triggers on \"chậm\", \"slow\", \"optimize\", \"performance\", \"latency\", \"memory\", \"cache\", \"tối ưu\", \"nhanh hơn\", \"giảm thời gian\"."
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
| 006 | 2026-03-30 | VSCode Extension Poll Optimization | 2000ms → 300ms accept |
| 007 | 2026-03-30 | DOM Scope Constraint & Tick Throttling | Fix CPU Lag khi Polling siêu tốc |
| 008 | 2026-04-02 | Request Interception CDP | Tiết kiệm 70% Network Bandwidth và Máy ảo RAM |
| 009 | 2026-04-02 | WMI Process Check Throttling | Tránh 100% CPU do WMI query liên tục |
| 010 | 2026-04-02 | UI Update Rate Limiting | Chống treo Event Loop của PyQt6 |
| 011 | 2026-04-02 | Headless Rendering Disable | Bổ sung flag Chrome `--disable-gpu`, `--blink-settings` |
| 012 | 2026-04-02 | Asynchronous Token Check | Tránh Thread Sleep ghim chết Worker |

### PERF-007: DOM Scope Constraint & Tick Throttling cho Auto Accept
> 📅 2026-03-30 — Dự án: MPA Extension Fork (hungpixi-multi-purpose-agent v2.0.1)

**Problem**: Vòng lặp `pollLoop` chạy siêu tốc 300ms quét đệ quy rác DOM (toàn bộ iframe) và tính `getComputedStyle` liên tục trên hàng ngàn `div`, gây CPU cao, làm lag Frontend VSCode.
**Solution**: 1. *Giới hạn vùng quét (Scope Constraint)*: Chỉ search bên trong root panel nếu panel tồn tại, bớt đi 99% DOM rác. 2. *Tick Throttling*: Rút chu kỳ tính CSS đắt đỏ (`autoScrollChatToBottom`) thành mỗi 1200ms (kiểm tra ở mỗi tick thứ 4), chỉ giữ phần tử click button là nhịp 300ms.
**Before**: CPU Usage cao, khựng màn hình mỗi 300ms, rủi ro sập trình duyệt.
**After**: CPU về gần 0, duy trì click auto accept độ trễ 0.
**Stack**: UI Optimization, JavaScript, Extension
**Rule**: **Luôn giới hạn WebQuery (querySelectorAll) trong container nhỏ nhất có thể. Dùng Tick Throttling để tách riêng logic click nhẹ và logic tínhCSS/DOM reflow nặng.**

<!-- PERF_APPEND_MARKER — AI append pattern mới TRƯỚC dòng này -->

### PERF-008 đến PERF-012: Optimizations từ hệ thống Bot VEO_TOOL
> 📅 2026-04-02 — Dự án: VEO_TOOL

Tool VEO chạy rất nặng do tải Chrome Render engine. Đã áp dụng các chốt tản nhiệt hệ thống sau:
* **PERF-008 (Request Interception)**: Dùng `cdp.send("Network.setBlockedURLs", {"urls": ["*aisandbox-pa*"]})` không cho phép Chrome tải Video Preview / Image Thumbnail từ Server trả về rác băng thông.
* **PERF-009 (WMI Tick Throttling)**: Khảo sát trạng thái Chrome sống/chết bằng hàm WMI của Windows (`Get-CimInstance`) gây giật CPU cực mạnh nếu gọi trong loop <1000ms. Refactor cache state WMI sau mỗi 5-10s.
* **PERF-010 (UI Update Rate Limiter)**: Update text của TextBrowser/Label `log_message.emit()` 1000 lần/giây sẽ kill luôn Thread UI. Refactor bằng batch update.
* **PERF-011 (Chrome Flags)**: Thêm args để tắt hoàn toàn Translate, GPU, âm thanh ( `--disable-features=Translate,BackForwardCache`, `--mute-audio`, `--blink-settings=imagesEnabled=false`).
* **PERF-012 (Async Check)**: Kiểm tra DOM stable thay vì dùng `time.sleep(30)`, sử dụng `await _first_visible_locator` chạy ngầm. Hạ độ trễ Automation từ trung bình 30s xuống mức Minimum theo phản hồi Server.

### PERF-006: VSCode Extension Auto-Accept Poll Optimization

> 📅 2026-03-30 — Dự án: MPA Extension Fork (hungpixi-multi-purpose-agent)

**Problem**: Extension auto-accept quá chậm — user phải chờ 1-2 giây sau khi button hiện mới được click. Nguyên nhân: `pollFrequency = 2000` (extension-impl.js) và `config.pollInterval || 1000` (full_cdp_script.js poll loop).
**Solution**: Giảm default poll frequency từ 2000ms → 500ms (extension-side), fallback từ 1000ms → 300ms (browser CDP script poll loop). Thêm `autoExpandStepInputSections()` vào mỗi poll cycle để auto-expand collapsed "step input required" sections.
**Before**: Accept delay 1-2s, step input required không auto-expand
**After**: Accept response ~300ms, step input auto-expand
**Stack**: VSCode Extension API + Chrome DevTools Protocol (CDP)
**Rule**: **Poll interval cho auto-accept nên ≤ 500ms. Luôn expand collapsed UI sections trước khi scan buttons.**
