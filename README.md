# 🧠 Antigravity Self-Learning System

> **Biến AI coding assistant thành hệ thống tự học** — mỗi session code, debug, refactor đều tạo ra knowledge mới. AI không bao giờ mắc lại cùng 1 lỗi.

[![Made with Antigravity](https://img.shields.io/badge/Made_with-Antigravity_IDE-blueviolet?style=for-the-badge)](https://github.com/hungpixi)
[![Skills](https://img.shields.io/badge/Skills-9_Active-green?style=for-the-badge)](#-9-skill-modules)
[![Patterns](https://img.shields.io/badge/Patterns-56+-orange?style=for-the-badge)](#-tổng-hợp)
[![PyPI](https://img.shields.io/badge/pip_install-antigravity--learn-blue?style=for-the-badge)](#-cài-đặt)

## 🚀 Cài Đặt

### Cách 1: `pip install` (Recommended)

```bash
pip install git+https://github.com/hungpixi/antigravity-self-learning.git

# Install skills vào Antigravity IDE
antigravity-learn install
```

### Cách 2: `uv` (Faster)

```bash
uv tool install git+https://github.com/hungpixi/antigravity-self-learning.git

# Hoặc clone + run
git clone https://github.com/hungpixi/antigravity-self-learning.git
cd antigravity-self-learning
uv sync
uv run antigravity-learn install
```

### CLI Commands

```bash
antigravity-learn install   # 📦 Cài skills vào ~/.gemini/antigravity/skills/
antigravity-learn sync      # 🔄 Update skills, thêm mới, giữ custom entries
antigravity-learn status    # 📊 Xem stats: bao nhiêu patterns, size, etc.
antigravity-learn export    # 📤 Export tất cả patterns ra 1 file markdown
antigravity-learn version   # Show version
```

## 🎯 Vấn Đề Giải Quyết

| Vấn đề | Trước | Sau |
|--------|-------|-----|
| AI dùng thư viện cũ | Suggest TA-Lib (cần C binary) | Search GitHub → chọn pandas-ta (pure Python) |
| Fix bug xong quên ngay | Bug lặp lại 2-3 lần | TIL auto-append → không bao giờ lặp |
| Mỗi session hỏi lại quy trình | "Compile MQL5 bằng gì?" lần thứ 5 | Runbook ghi sẵn → AI tự theo |
| Chọn tech rồi đổi ý | SQLAlchemy → psycopg2 → SQLAlchemy → ... | ADR log quyết định → không flip-flop |
| Build crawler không biết best practice | Copy-paste spaghetti | 12 production patterns từ MediaCrawler (24k⭐) |

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
│ Self-  │    │  TIL/RCA   │    │  Code Smell│
│ Learn  │    │  Update    │    │  Update    │
└───┬────┘    └─────┬──────┘    └─────┬──────┘
    │               │                 │
    ▼               ▼                 ▼
┌──────────────────────────────────────────────┐
│           9 Skill Files (Auto-Append)        │
│                                              │
│  🐛 bug-fix-patterns    24 patterns (TIL)    │
│  📝 adr-decisions        3 decisions (ADR)   │
│  🏃 runbooks             7 runbooks          │
│  ⚡ performance-playbook  3 patterns         │
│  🔍 code-smell-catalog    5 smells           │
│  🎯 prompt-patterns       5 patterns         │
│  🕷️ crawler-patterns     12 patterns         │
│  ⚡ antigravity-cdp-fix   auto-fix script    │
│  ⏱️ session-analytics    per-session report   │
│                                              │
│  Total: 57+ entries from 14+ real projects   │
└──────────────────────────────────────────────┘
```

## 🧠 7 Self-Learning Models + Session Analytics

| # | Model | Trigger | Khi nào | Ví dụ |
|---|-------|---------|---------|-------|
| 1 | **TIL** | Fix bug thành công | `/debug` xong | PyPI mirror fail → append P22 |
| 2 | **ADR** | Chọn tech/architecture | `/code` chọn lib | pandas-ta > TA-Lib, logged |
| 3 | **Runbook** | Task lặp lại >3 bước | Deploy, compile | Clone Chinese project → 8 steps |
| 4 | **RCA** | Bug tái phát lần 2+ | `/debug` lần 2 | 5 Whys → root cause |
| 5 | **Performance** | Optimize có metrics | `/code` optimize | 10s → 100ms, logged |
| 6 | **Code Smell** | Pattern xấu khi review | `/refactor` | Global Flag Orchestra |
| 7 | **Prompt** | Prompt hiệu quả đáng kể | Meta-optimization | 3-Round Self-Review |
| 📊 | **Session Analytics** | Cuối mỗi session | Tự động | 30 phút, 79% AI, ⭐⭐⭐⭐⭐ |

## 📦 9 Skill Modules

### 1. `bug-fix-patterns/` — 24 patterns ⬆️
Tổng hợp bug patterns từ 14+ dự án thực tế:
- 🔴 Đệ quy vô hạn, State không reset
- 🟠 PyPI mirror download fail, Windows UTF-8 encoding, CDP process leak
- Kèm debug checklist 12 bước và 10 anti-pattern rules

### 2. `adr-decisions/` — 3 Architecture Decisions
- pandas-ta > TA-Lib (cross-platform)
- psycopg2 pool > SQLAlchemy (lightweight)
- OpenClaw > LangGraph/CrewAI (simple API)

### 3. `runbooks/` — 7 Operational Procedures ⬆️
- MQL5 Compile & Backtest (7 steps)
- GitHub Push Portfolio (6 steps + security check)
- **Clone Chinese Python Projects (8 steps)** 🆕
- **Playwright CDP Crawler Setup (6 steps)** 🆕

### 4. `performance-playbook/` — 3 patterns
- Connection Pooling: 10-12s → <100ms
- PineScript Lookback Limit
- Cache GetPipPoint: 60 calls/min → 1

### 5. `code-smell-catalog/` — 5 Code Smells
- Global Flag Orchestra, Dead Function
- Close Without Reset, Partial No Fallback

### 6. `prompt-patterns/` — 5 AI Meta-Optimization
- Search-Before-Code, 3-Round Self-Review
- Critic-Then-Fix (+60% bug detection)

### 7. `crawler-patterns/` — 12 patterns 🆕
Extracted từ [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) (24k+ ⭐):
- **CP-001**: Factory + ABC multi-platform architecture
- **CP-002**: Playwright CDP mode — dùng Chrome thật
- **CP-003**: Anti-detection stack (stealth.js + flags + persistent context)
- **CP-004**: Semaphore-controlled async concurrency
- **CP-005**: Graceful shutdown with timeout
- **CP-006**: Proxy IP pool with auto-refresh
- **CP-007**: Multi-storage Factory (7 backends)
- **CP-008**: Cross-OS browser detection
- **CP-009**: Slider CAPTCHA auto-solve (OpenCV)
- **CP-010**: ContextVar for async-safe state
- **CP-011**: Hybrid Browser+HTTP architecture
- **CP-012**: uv-based project setup

### 8. `antigravity-cdp-fix/` — Auto-Fix CDP Port 🆕
Tự động sửa lỗi "Multi Purpose Agent could not connect to CDP port 9004":
- Script PowerShell tự detect + fix tất cả Antigravity shortcuts
- Install 1 lần → auto-fix mỗi lần Windows boot
- Kèm standalone repo: [hungpixi/antigravity-cdp-fix](https://github.com/hungpixi/antigravity-cdp-fix)

### 9. `session-analytics/` — Per-Session Reports
- Phân bổ thời gian: AI Work vs User Think
- Deliverables count, tốc độ (files/phút)
- Rating ⭐ system (1-5)

## 🔬 Quá Trình Tư Duy

### v2.0: Từ "copy files" → "pip install"

**Vấn đề v1**: Cài đặt = `cp -r skills/* ~/.gemini/...` — thủ công, dễ quên, không version.

**Giải pháp v2**: Đóng gói thành Python package:
```bash
pip install git+https://github.com/hungpixi/antigravity-self-learning.git
antigravity-learn install  # 1 command, xong.
```

**Học từ MediaCrawler**: Dùng `uv` + `pyproject.toml` thay vì `setup.py` + `requirements.txt`.

### Tại sao thêm crawler-patterns?

Audit [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) → 20+ files → rút ra 12 patterns production-grade. Không phải "nghĩ ra" — là **reverse-engineer từ project 24k stars**.

### Nguồn dữ liệu

| Source | Patterns |
|--------|----------|
| 14 project conversations (trading bots, web, Python) | 41 initial entries |
| MediaCrawler codebase analysis (24k⭐) | 15 new entries |
| **Total** | **56+** |

## 📊 Tổng Hợp

| Metric | v1.0 | v2.0 |
|--------|------|------|
| Skill modules | 7 | **9** |
| Total patterns | 41 | **57+** |
| Install method | `cp -r` | `pip install` / `uv` |
| CLI tool | ❌ | ✅ (`antigravity-learn`) |
| Crawler patterns | ❌ | **12 patterns** |
| CDP auto-fix | ❌ | **Script + Startup** |
| Bug patterns | 21 | **24** |
| Runbooks | 5 | **7** |

## 🗺️ Hướng Đi Tương Lai

- [x] **Package + CLI**: `pip install` thay vì copy files ✅
- [x] **Crawler patterns**: 12 patterns từ MediaCrawler ✅
- [x] **Session analytics**: Đo lường hiệu quả mỗi phiên ✅
- [ ] **PyPI publish**: `pip install antigravity-learn` (không cần GitHub URL)
- [ ] **Weekly digest**: Tổng hợp TIL entries/tuần
- [ ] **Cross-referencing**: Link patterns giữa skills (smell → bug → fix)
- [ ] **Team sharing**: Merge skill files từ nhiều developers

---

## 📜 Credits

- **Author**: [Phạm Phú Nguyễn Hưng](https://github.com/hungpixi)
- **Company**: [Comarai](https://comarai.com) — Companion for Marketing & AI Automation
- **Built with**: [Antigravity IDE](https://github.com/google-deepmind) by Google DeepMind
- **Crawler patterns source**: [NanmiCoder/MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) (24k+ ⭐)
- **Source data**: 14+ real project conversations, 12+ walkthroughs

---

## 🤝 Bạn muốn hệ thống AI tự học tương tự?

| Bạn cần | Chúng tôi đã làm ✅ |
|---------|---------------------|
| AI coding assistant thông minh hơn | 8 self-learning models tích hợp |
| Không lặp lại sai lầm cũ | TIL + RCA auto-append (24 patterns) |
| Chọn tech đúng từ đầu | Tech Radar + ADR system |
| Build crawler chuyên nghiệp | 12 production patterns từ codebase 24k⭐ |
| Fix lỗi IDE tự động | CDP port fix — set-and-forget |
| Cài đặt 1 lệnh | `pip install` + `antigravity-learn install` |

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
