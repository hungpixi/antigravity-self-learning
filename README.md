# 🧠 Antigravity Self-Learning System

> **Biến AI coding assistant thành hệ thống tự học** — mỗi session code, debug, refactor đều tạo ra knowledge mới. AI không bao giờ mắc lại cùng 1 lỗi.

[![Made with Antigravity](https://img.shields.io/badge/Made_with-Antigravity_IDE-blueviolet?style=for-the-badge)](https://github.com/hungpixi)
[![Skills](https://img.shields.io/badge/Skills-6_Active-green?style=for-the-badge)](#-6-skill-modules)
[![Patterns](https://img.shields.io/badge/Patterns-41_Initial-orange?style=for-the-badge)](#-tổng-hợp)

## 🎯 Vấn Đề Giải Quyết

| Vấn đề | Trước | Sau |
|--------|-------|-----|
| AI dùng thư viện cũ | Suggest TA-Lib (cần C binary) | Search GitHub → chọn pandas-ta (pure Python) |
| Fix bug xong quên ngay | Bug lặp lại 2-3 lần | TIL auto-append → không bao giờ lặp |
| Mỗi session hỏi lại quy trình | "Compile MQL5 bằng gì?" lần thứ 5 | Runbook ghi sẵn → AI tự theo |
| Chọn tech rồi đổi ý | SQLAlchemy → psycopg2 → SQLAlchemy → ... | ADR log quyết định → không flip-flop |
| Code mới nhưng lỗi cũ | Partial close lot quá nhỏ → infinite loop | Code Smell Catalog cảnh báo trước |

## 🏗️ Kiến Trúc

```
┌──────────────────────────────────────────────────┐
│              GEMINI.md (Global Rules)            │
│  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Tech Radar   │  │ Self-Learning Protocol   │  │
│  │ (chống tech  │  │ (7 models auto-trigger)  │  │
│  │  cũ)         │  │                          │  │
│  └──────────────┘  └──────────────────────────┘  │
└─────────────────────┬────────────────────────────┘
                      │ triggers
    ┌─────────────────┼─────────────────┐
    ▼                 ▼                 ▼
┌────────┐    ┌────────────┐    ┌────────────┐
│ /code  │    │  /debug    │    │ /refactor  │
│ §6.1   │    │  §5.1      │    │ §6.1       │
│ Self-  │    │  TIL/RCA   │    │ Code Smell │
│ Learn  │    │  Update    │    │ Update     │
└───┬────┘    └─────┬──────┘    └─────┬──────┘
    │               │                 │
    ▼               ▼                 ▼
┌──────────────────────────────────────────────┐
│           6 Skill Files (Auto-Append)        │
│                                              │
│  📋 bug-fix-patterns   21 patterns (TIL)     │
│  📝 adr-decisions       3 decisions (ADR)    │
│  🏃 runbooks            4 runbooks           │
│  ⚡ performance-playbook 3 patterns          │
│  🔍 code-smell-catalog   5 smells            │
│  🎯 prompt-patterns      5 patterns          │
│                                              │
│  Total: 41 entries từ audit 14 dự án thực tế │
└──────────────────────────────────────────────┘
```

## 🧠 7 Self-Learning Models

| # | Model | Trigger | Khi nào | Ví dụ |
|---|-------|---------|---------|-------|
| 1 | **TIL** | Fix bug thành công | `/debug` xong | Đệ quy vô hạn → append P22 |
| 2 | **ADR** | Chọn tech/architecture | `/code` chọn lib | pandas-ta > TA-Lib, logged |
| 3 | **Runbook** | Task lặp lại >3 bước | Deploy, compile | MQL5 compile → 7 steps |
| 4 | **RCA** | Bug tái phát lần 2+ | `/debug` lần 2 | 5 Whys → root cause |
| 5 | **Performance** | Optimize có metrics | `/code` optimize | 10s → 100ms, logged |
| 6 | **Code Smell** | Pattern xấu khi review | `/refactor` | Global Flag Orchestra |
| 7 | **Prompt** | Prompt hiệu quả đáng kể | Meta-optimization | 3-Round Self-Review |

## 📦 6 Skill Modules

### 1. `bug-fix-patterns/` — TIL (21 patterns)
Tổng hợp bug patterns từ audit 14 dự án thực tế:
- 🔴 Đệ quy vô hạn, State không reset
- 🟠 Hardcode values, Guard conditions thiếu, Partial close overflow
- Kèm debug checklist 12 bước và 10 anti-pattern rules

### 2. `adr-decisions/` — Architecture Decisions (3 entries)
Log quyết định tech đã làm:
- pandas-ta > TA-Lib (cross-platform)
- psycopg2 pool > SQLAlchemy (lightweight)
- OpenClaw > LangGraph/CrewAI (simple API)

### 3. `runbooks/` — Operational Procedures (4 entries)
Quy trình chuẩn hóa:
- MQL5 Compile & Backtest (7 steps)
- GitHub Push Portfolio (6 steps + security check)
- Netlify Deploy (4 steps)
- n8n Workflow Setup (5 steps)

### 4. `performance-playbook/` — Optimization Patterns (3 entries)
Có metrics before/after:
- Connection Pooling: 10-12s → <100ms
- PineScript Lookback Limit: labels fix + performance
- Cache GetPipPoint: 60 calls/min → 1 call

### 5. `code-smell-catalog/` — Code Smells (5 entries)
Chủ động phòng tránh:
- Global Flag Orchestra (>5 booleans → enum state machine)
- Dead Function (viết nhưng không gọi)
- Close Without Reset, Partial No Fallback

### 6. `prompt-patterns/` — AI Meta-Optimization (5 entries)
- Search-Before-Code, 3-Round Self-Review
- Critic-Then-Fix (+60% bug detection)
- Instrument-Aware Defaults, Grep-After-Write

## 🔬 Quá Trình Tư Duy

### Tại sao không chỉ dùng documentation thông thường?

Documentation **tĩnh** — viết 1 lần, quên update. Hệ thống này **động**:

1. **Mỗi skill file có `APPEND_MARKER`** — AI append entries mới tự động, không sửa entries cũ
2. **TIL Protocol kiểm tra 3 điều kiện** trước khi lưu: (1) fix thành công, (2) chưa có trong catalog, (3) đủ general để tái sử dụng
3. **Workflows tích hợp hooks** — `/debug` xong tự trigger TIL check, `/code` xong tự trigger ADR check
4. **Không lưu rác** — typo, import sai tên, lỗi 1 lần → bỏ qua

### Nguồn dữ liệu ban đầu

41 entries không phải "nghĩ ra" — được **audit từ 14 conversations và 12+ walkthroughs** thực tế:
- Trading bots: IchiDCA, CCBSN, ICT System EA
- Web: comarai.com, BizClaw, VietFi
- Python: moondev-agent, telegram-copy-signal
- Scripting: BDR Kit installer

## 🚀 Cách Sử Dụng

### Cài đặt cho Antigravity IDE

```bash
# Clone repo
git clone https://github.com/hungpixi/antigravity-self-learning.git

# Copy skills vào Antigravity
cp -r skills/* ~/.gemini/antigravity/skills/
```

### Thêm vào GEMINI.md (Global Rules)

Copy 2 blocks từ `examples/gemini-rules.md` vào `~/.gemini/GEMINI.md`:
- **Tech Radar** — chống dùng công nghệ cũ
- **Self-Learning Protocol** — bảng 7 models với triggers

### Cập nhật Workflows

Thêm Self-Learning hooks vào workflows hiện tại (xem `examples/workflow-hooks.md`).

## 📊 Tổng Hợp

| Metric | Giá trị |
|--------|---------|
| Skill files | 6 |
| Total entries (ban đầu) | 41 |
| Bug patterns | 21 |
| ADR decisions | 3 |
| Runbooks | 4 |
| Performance patterns | 3 |
| Code smells | 5 |
| Prompt patterns | 5 |
| Workflows updated | 4 (code, debug, refactor, review) |
| Source conversations | 14 |

## 🗺️ Hướng Đi Tương Lai

- [ ] **Auto-analytics**: Đếm số TIL entries/tuần, track growth rate
- [ ] **Cross-referencing**: Link patterns liên quan giữa các skills (smell → bug → fix)
- [ ] **Priority scoring**: Rank patterns theo tần suất trigger
- [ ] **Export to Obsidian**: Sync với knowledge graph
- [ ] **Team sharing**: Merge skill files từ nhiều developers

---

## 📜 Credits

- **Author**: [Phạm Phú Nguyễn Hưng](https://github.com/hungpixi)
- **Company**: [Comarai](https://comarai.com) — Companion for Marketing & AI Automation
- **Built with**: [Antigravity IDE](https://github.com/google-deepmind) by Google DeepMind
- **Source data**: 14 real project conversations, 12+ walkthroughs

---

## 🤝 Bạn muốn hệ thống AI tự học tương tự?

| Bạn cần | Chúng tôi đã làm ✅ |
|---------|---------------------|
| AI coding assistant thông minh hơn | 7 self-learning models tích hợp |
| Không lặp lại sai lầm cũ | TIL + RCA auto-append |
| Chọn tech đúng từ đầu | Tech Radar + ADR system |
| Quy trình chuẩn hóa | Runbook auto-capture |
| Code review tự động | Code Smell Catalog |

### 📞 Liên hệ

| | |
|---|---|
| 🌐 **Website** | [comarai.com](https://comarai.com) |
| 💬 **Zalo** | [0834422439](https://zalo.me/0834422439) |
| 📧 **Email** | hungphamphunguyen@gmail.com |
| 🐙 **GitHub** | [hungpixi](https://github.com/hungpixi) |

> *"Tôi không có thời gian debug cùng 1 bug 2 lần. Nên tôi dạy AI nhớ giúp."*
> — Hưng, Founder @ Comarai

**Comarai** — 4 nhân viên AI chạy 24/7: Em Sale 🤝 Em Content ✍️ Em Marketing 📢 Em Trade 📈
