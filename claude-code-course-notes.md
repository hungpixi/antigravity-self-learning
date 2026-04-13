# Claude Code Full Beginner Course - Key Takeaways & Huong Dan Ung Dung

> Muc dich: Rut trich nhung insight co the ap dung ngay vao viec build & sell cac du an AI.
> Nguon: "Claude Code Full Beginner Course Learn Agents In 2026" - Nick Sariah (LeftClick)

---

## PHAN 1: Setup & Nen Tang (00:00 - 08:00)

### Key Takeaways
- Claude Code chay **local tren may tinh**, khac voi chat web. No co the doc/ghi file, chay script, tuong tac truc tiep voi he thong.
- Chi can **Pro plan ($17/thang)** la du de bat dau. ROI cuc cao - nguoi day noi no mang lai ~$10-15K/thang productivity.
- **Context window** la tai nguyen quan trong nhat. Claude tu dong nen (compress) conversation history khi context tang len.
- Co the dung qua **terminal** (manh hon, nhieu chuc nang hon) hoac **GUI trong IDE** (VS Code / Antigravity).

### Ung Dung Cho Build & Sell AI Projects
- **Khoi diem re**: $17/thang de co tool co the build nhieu du an cung luc, ROI rat cao.
- **Hieu context limit**: Khi build du an lon, can chia nho task, quan ly context tot de tranh mat chat luong.
- **Chon terminal flow**: Khi ban da quen, terminal cho phep chay nhieu session song song - rat quan trong khi can build nhieu feature/project cung luc.

---

## PHAN 2: IDE - Visual Studio Code vs Antigravity (08:00 - 24:00)

### Key Takeaways
- IDE = File Explorer + Text Editor + AI Chat Widget.
- **VS Code**: OG, stable, extensible. Cai Claude Code extension tu Anthropic (chu y chi dung verified sources).
- **Antigravity**: VS Code 2.0, UI dep hon, focus AI nhieu hon. La Google product nen push Gemini, nhung van dung Claude Code duoc.
- **Permission modes** rat quan trong:
  - "Ask before edits" = an toan, nhung cham
  - "Edit automatically" = nhanh hon
  - "Bypass permissions" = nhanh nhat, dung khi ban hieu minh dang lam gi
- Co the **pause** Claude giua chung va thay doi huong.

### Ung Dung Cho Build & Sell AI Projects
- **Dung Antigravity** lam IDE chinh - modern hon, AI-first.
- **Bypass permissions** khi lam nhung task ban da hieu ro (vd: generate boilerplate, scaffold project). Chuyen sang "ask before edits" khi lam nhung phan nhay cam (auth, payment, database).
- **Pause & redirect**: Khi thay Claude di sai huong, dung ngay va redirect. Dung de no chay het context vao huong sai.

---

## PHAN 3: CLAUDE.md - Bo Nao Cua Project (24:00 - 30:00)

### Key Takeaways
- **CLAUDE.md** duoc inject vao DAU conversation, truoc ca message dau tien cua ban.
- Giong nhu goc ban dau cua con tau: sai 1 do luc xuat phat = lech hang ngan km o dich den.
- Cang **cu the va chat luong** cang tot - no thu hep "khong gian kha nang" cua AI, giup output chinh xac hon.
- Khong can tu viet - co the dung AI de tao CLAUDE.md tu best practices tren Twitter/internet.

### Ung Dung Cho Build & Sell AI Projects
- **Moi project can 1 CLAUDE.md rieng** voi:
  - Tech stack cu the (React, Next.js, Supabase, etc.)
  - Code conventions (naming, folder structure)
  - Business context (day la SaaS gi, phuc vu ai)
  - Design guidelines (brand colors, font, tone)
- **Tao template CLAUDE.md** cho tung loai du an ban hay lam:
  - Template cho landing page projects
  - Template cho SaaS dashboard
  - Template cho API/backend service
  - Template cho AI automation tool
- **Ban co the ban CLAUDE.md templates** nhu la starter kits cho nguoi khac!

---

## PHAN 4: 3 Cach Thiet Ke Website/App Voi Claude Code (30:00 - 46:00)

### Key Takeaways

#### Cach 1: Design Reference + Screenshot Loop (DUOC KHUYEN DUNG NHAT)
- Chup full-page screenshot cua website mau (Cmd+Shift+P > "Capture full size screenshot")
- Resize xuong < 4-5MB
- Feed vao Claude Code cung voi CSS styles (copy tu DevTools)
- Claude tao v1 (~80% match) > tu screenshot > tu so sanh > chinh sua > lap lai cho den ~99%

#### Cach 2: Voice Transcript Dump
- Noi nhanh hon go 2.5-3x (200 vs 70 words/min)
- Mo tieng > mo ta moi thu ban muon tren website
- Khong one-shot duoc nhung tiet kiem thoi gian input

#### Cach 3: Component Libraries (21st.dev, etc.)
- Copy prompt tu component > paste vao Claude Code
- Tot cho tung phan nho, nhung khong tot cho whole site

### Triet Ly Cot Loi: Task > Do > Verify Loop
- **KHONG BAO GIO** chi cho Claude lam xong roi nhan ket qua.
- LUON LUON co buoc **verify**: screenshot loop cho UI, automated tests cho code.
- AI khong one-shot 100% - nhung no di tu 0 > 80% > 90% > 95% > 99% trong **5 phut**, trong khi nguoi mat **5 gio**.
- **Toc do iterate** la gia tri thuc su cua AI, khong phai do chinh xac lan dau.

### Ung Dung Cho Build & Sell AI Projects

#### Dich Vu Ban Duoc:
1. **Website design service**: Lay inspiration tu godly.website/dribbble > Claude build > ban hoan thien. Co the lam 3-5 versions song song trong 30 phut.
2. **Landing page sprint**: Khach hang cung cap brand info > ban tao 3 designs song song > khach chon 1 > polish trong 1-2h. Gia: $500-2000/page.
3. **Redesign service**: Screenshot site cu cua khach > Claude rebuild voi design moi > delivery trong 1 ngay.

#### Workflow Toi Uu:
1. Tao CLAUDE.md template cho web design projects
2. Chup full-page screenshot inspiration
3. Chay 2-3 Claude instances song song voi cac design khac nhau
4. Chon ban tot nhat > customize content
5. Deploy len Netlify/Vercel (free)
6. Delivery cho khach

#### Meo Quan Trong:
- **Chay nhieu instance song song** = nhan nang suat gap boi. 1 nguoi co the output bang 5-10 designers.
- **Godly.website** la nguon inspiration tot nhat cho award-winning designs.
- **21st.dev** cho components rieng le khi can them tinh nang cu the.
- **Voice input** (Fn key) de mo ta nhanh - dung khi brainstorm y tuong voi khach hang.

---

---

## PHAN 5: .claude Directory - Cau Truc Nang Cao (55:00 - 65:00)

### Key Takeaways
- **`.claude/` folder** la noi chua cau hinh nang cao, an khoi file explorer (dot prefix).
- Cau truc day du:
  ```
  .claude/
  ├── settings.json        # Team permissions & hooks
  ├── settings.local.json  # Local-only settings (git ignored)
  ├── CLAUDE.md            # Project brain
  ├── CLAUDE.local.md      # Local brain (git ignored)
  ├── agents/              # Sub-agent definitions
  ├── skills/              # Custom slash commands
  ├── rules/               # Modular rules (tach tu CLAUDE.md)
  └── .mcp.json            # MCP server config
  ```
- **Rules folder**: Tach CLAUDE.md monolithic thanh cac file nho theo chuc nang (workflow, design, security, testing...). De quan ly, de chia se trong team.
- **3 tang CLAUDE.md**:
  1. **Enterprise** (managed system level) - cho cong ty lon
  2. **Global** (`~/.claude/CLAUDE.md`) - ap dung cho MOI workspace
  3. **Local** (`.claude/CLAUDE.md`) - chi cho workspace hien tai
- **`/init` command**: Tu dong scan codebase va tao CLAUDE.md. LUON chay khi bat dau workspace moi.

### Do's & Don'ts Cho CLAUDE.md
| DO | DON'T |
|---|---|
| Chay `/init` truoc | Dump nguyen API docs vao |
| Bullet points, ngan gon | Viet vague ("be smart") |
| Dieu quan trong nhat len DAU (primacy bias) | De qua 500 dong |
| Review & prune thuong xuyen | De Claude tu them ma khong kiem tra |
| Them rule khi Claude lap lai sai lam | Voice dump truc tiep khong edit |

### Ung Dung Cho Build & Sell AI Projects
- **Tao bo CLAUDE.md templates** cho cac loai du an khac nhau - day la san pham ban duoc!
- **Global CLAUDE.md** de set chuan cho moi du an: coding standards, security rules, commit conventions.
- **Rules folder** giup team cung lam: designer sua design rules, dev sua tech rules, manager sua workflow rules.
- **Meo hay**: Dung Grok/Twitter de tim best practices CLAUDE.md moi nhat. Cong nghe thay doi nhanh, Claude da hoc nhieu conventions pho bien roi.

---

## PHAN 6: Auto Memory & Sub-Agents (76:00 - 85:00)

### Key Takeaways

#### Auto Memory
- File `memory.md` duoc inject vao moi session, tach biet voi CLAUDE.md.
- Noi Claude "remember X" > no ghi vao memory > session sau no nho.
- Coi nhu "so tay cua Claude" - khong phai instruction set cua ban.

#### Sub-Agents (Agents Folder)
- Moi agent co: **tools access, model, max turns, description, instructions**.
- Agent con chay trong **context rieng** - khong lam ban context cua agent cha.
- **3 loai agent con QUAN TRONG NHAT**:

| Agent | Muc Dich | Tai Sao |
|---|---|---|
| **Research Agent** | Tim kiem, tong hop thong tin | Tranh pollute context cha. Dung model re (Sonnet/Haiku). Co the dung 100K tokens nhung chi tra ve 2K summary. Tiet kiem 50x. |
| **Reviewer Agent** | Review code voi zero context | Khong bi bias nhu agent cha (da "suy nghi" theo 1 huong). Nhin code bang "mat moi" > phat hien loi tot hon. |
| **QA/Testing Agent** | Chay tests tu dong | Kiem tra code thuc su hoat dong. Giong screenshot loop cho backend. |

### Ung Dung Cho Build & Sell AI Projects
- **Tiet kiem chi phi**: Research agent dung Sonnet/Haiku (re), chi agent chinh dung Opus (dat nhung thong minh).
- **Workflow chuan cho moi du an**:
  1. Agent cha nhan yeu cau tu khach
  2. Research agent di tim hieu yeu cau ky thuat
  3. Agent cha code
  4. Reviewer agent review code
  5. QA agent chay tests
  6. Agent cha fix va deliver
- **Ban co the ban workflow nay nhu SOP** cho cac agency khac!

---

## PHAN 7: Skills - Tu Dong Hoa Moi Thu (85:00 - 91:00)

### Key Takeaways
- **Skills** = instructions cho AGENT CHA (khac voi agents la tao agent con rieng).
- Dat trong `.claude/skills/` voi ten mo ta (vd: `shop-amazon.md`).
- Co the tu dong hoa **bat ky knowledge work nao**: mua sam Amazon, scrape Upwork, gui email chao mung khach, tao deliverables...
- **Cach tao skill**:
  1. Noi Claude: "Tao skill lam X, Y, Z"
  2. Claude tao draft skill file
  3. Test voi fresh Claude instance (khong co context cu)
  4. Neu sai > cho feedback > sua skill > test lai
  5. Lap lai cho den 98-99% accuracy
- **Skill marketplace** dang hinh thanh - nguoi ta chia se va ban skills.

### Vi Du Skills Co The Tao De Ban/Dung:
1. **Lead Scraper**: Tu dong tim leads tren LinkedIn/Upwork/Twitter
2. **Email Automator**: Gui welcome emails, follow-ups cho clients
3. **Proposal Generator**: Tu dong tao proposals tu brief cua khach
4. **Invoice Manager**: Tao va gui invoices tu dong
5. **Content Repurposer**: Lay 1 blog post > tao 10 social media posts
6. **Client Onboarding**: Tu dong setup project structure, send welcome kit
7. **Competitor Analyzer**: Scan doi thu va tao report

### Ung Dung Cho Build & Sell AI Projects
- **GOLDMINE**: Moi SOP trong business ban co the tro thanh 1 skill.
- **Dich vu moi**: "AI Automation Setup" - giup doanh nghiep tao skills cho workflow cua ho. Gia: $2-5K/skill set.
- **Passive income**: Tao va ban skill packs tren marketplace.
- **Competitive advantage**: Skills tot = output nhanh hon = lay nhieu khach hon = scale nhanh hon.

---

---

## PHAN 8: Permission Modes & Plan Mode (92:00 - 105:00)

### Key Takeaways

#### 4 Permission Modes:
| Mode | Mo Ta | Khi Nao Dung |
|---|---|---|
| **Ask Before Edits** | Hoi truoc moi thay doi | Code base nhay cam, high-risk. It nguoi dung. |
| **Edit Automatically** | Tu edit file co san, hoi khi tao file moi | Cai dat an toan nhat ma van nhanh |
| **Plan Mode** | Chi doc & nghien cuu, khong edit | LUON dung truoc khi build bat cu gi phuc tap |
| **Bypass Permissions** | Lam moi thu khong hoi | Khi ban hieu ro va muon toc do toi da |

- **Delegate mode**: Cho agent team leads - chi co quyen quan ly team, khong edit.
- Bat Bypass: VS Code > Extensions > Claude Code > Settings > "Allow dangerously skip permissions"
- Sub-agents thua ke permission mode tu parent.

#### Plan Mode - QUY TAC VANG:
> **"1 phut planning = 10 phut building"**

- Plan Mode = read-only. Claude chi: nghien cuu web, doc files, suy luan, tao plan document.
- **KHONG build** -> KHONG ton tokens vao code sai -> KHONG phai undo.
- So sanh:
  - **Khong plan**: Build 15' + Test 5' + Rebuild 15' = **35 phut + nhieu tokens**
  - **Co plan**: Plan 5' + Fix plan 5' + Build 5' = **15 phut + it tokens**

### Ung Dung Cho Build & Sell AI Projects
- **LUON bat dau voi Plan Mode** cho moi du an khach hang. No la bao hiem chong waste.
- **Plan document = deliverable ban duoc**: Khach nhin thay plan truoc khi ban code -> tang trust.
- **Parallel planning**: Chay plan mode cho 2-3 du an cung luc, review sau.

---

## PHAN 9: Full-Stack App Build Demo - Proposal Generator (105:00 - 133:00)

### Key Takeaways - Quy Trinh Build App Tu A-Z

#### Buoc 1: Voice Dump Specs
- Dung voice transcription de mo ta moi thu ban muon (nhanh 2.5-3x go phim)
- KHONG can dung tu ky thuat - chi mo ta NHU CAU kinh doanh

#### Buoc 2: Plan Mode
- Feed specs vao Claude Code o Plan Mode
- Claude hoi cac cau hoi ky thuat (framework, database, payment...) qua GUI
- Ban chi can chon options, khong can hieu ky thuat
- Claude tao plan chi tiet: tech stack, database schema, routes, file structure

#### Buoc 3: Chuyen Sang Build
- Chuyen tu Plan Mode sang Bypass Permissions
- Cung cap API keys (Supabase, Stripe, Anthropic) cho Claude
- DE CLAUDE LAM - di lam viec khac (nau an, tra loi email...)
- Hook chime bao khi xong

#### Buoc 4: Iterate & Polish
- Quay lai, test tung trang
- Cho feedback bang voice: "Logo to qua", "Font khong dep", "Spacing le"
- Claude tu fix, ban chi can mo ta visual problems

#### Buoc 5: Deploy
- Claude noi "push to GitHub, deploy to Netlify" -> nho CLAUDE TU LAM
- Them environment variables
- App live tren internet trong vai phut

### Ket Qua: Full-stack app (login, dashboard, AI proposal generation, e-signature, Stripe payments) trong ~20 phut.

### CANH BAO AN NINH QUAN TRONG:
1. **KHONG** publish app vibe-coded len internet cho nguoi la dung ma khong co security review
2. **KHONG** thu tien tu user data (passwords, payments) ma khong co dev review authentication
3. **Dung noi bo/cho client** la an toan. Sell ra public = can security audit ($200-500)
4. URL khong nen ngan/de doan - scanners se tim thay
5. "Software is not the moat" - code co the share, gia tri la y tuong + execution

### Ung Dung Cho Build & Sell AI Projects

#### Dich Vu Co The Ban Ngay:
1. **Internal Tools Builder**: Build dashboard/tool noi bo cho doanh nghiep. $2-5K/tool.
   - Proposal generators, CRM dashboards, inventory trackers
   - Khach khong can lo security vi chi dung noi bo
2. **MVP Sprint Service**: Build MVP trong 1-2 ngay thay vi 1-2 thang. $3-10K.
   - Voice dump specs > Plan Mode > Build > Deploy > Done
3. **SaaS Cloner**: Rebuild chuc nang cua tool dat tien (PandaDoc, DocuSign) cho khach dung rieng. $5-15K.
   - Khach het phai tra subscription hang thang
   - Ban chi ton 1 lan build + hosting re

#### Workflow Build & Sell Toi Uu:
```
1. Khach mo ta nhu cau (voice call 30 phut)
2. Voice dump > Claude Plan Mode > Plan document
3. Gui plan cho khach review & approve (DELIVERABLE #1)
4. Build voi Bypass Permissions (1-3 gio)
5. Iterate voi khach feedback (1-2 gio)
6. Security review nhanh (neu can)
7. Deploy + ban giao (DELIVERABLE #2)
8. Ho tro 30 ngay
```

#### Meo Scaling:
- **Chay nhieu build song song**: 3-4 tabs = 3-4 projects cung luc
- **Hook chime** de biet khi nao tab nao can attention
- **Khong de Claude ngoi khong** > 10-20% thoi gian. Neu vay, giam so tabs.
- **Template hoa**: Tao CLAUDE.md + skills cho tung loai project ban hay lam

---

## PHAN 10: Context Management (133:00 - 136:00+)

### Key Takeaways
- **`/context`** command: Xem chinh xac cai gi dang chiem context window.
- Opus 4.6 = 200K tokens. Sonnet co the len 1-2M tokens.
- **Context window size != model intelligence**. Model thong minh hon khong nhat thiet co context lon hon.
- **Chi phi an**: Moi session moi da ton 5-15K tokens cho system prompt, tool definitions, CLAUDE.md... TRUOC KHI ban go chu nao.
- **Auto-compaction**: Khi dat 100% context, Claude tu nen tat ca thanh high-density summary. "Netlify Rebuilds" > "Netlify Rebuilding". Thong tin giu nguyen, tokens giam.
- **Primacy & Recency bias**: Claude nho tot dau va cuoi prompt, quen giua. -> Dat thu quan trong o DAU CLAUDE.md.

### Ung Dung Cho Build & Sell AI Projects
- **Chay `/context` thuong xuyen** de hieu chi phi thuc te cua moi du an
- **Dung sub-agents** cho research (re, context rieng) thay vi lam trong parent agent (dat, chiem context)
- **Compact CLAUDE.md**: Moi token dem. Viet ngan, bullet points, high-density.
- **Chia du an lon thanh phases**: Moi phase = 1 session moi = context sach. Dung file plan de truyen context giua sessions.

---

---

## PHAN 11: Context Management Chi Tiet & Slash Commands (136:00 - 153:00)

### Key Takeaways

#### Cau Truc Context Window (thu tu inject):
```
1. System Prompt (CLAUDE.md global + local + enterprise + rules)
2. System Tools (~17K tokens - bash, read, write, grep, web search, etc.)
3. MCP Tools (tuy thiet lap - co the rat lon!)
4. Memory.md (~88 tokens)
5. Skills (chi front-matter, ~60 tokens/skill)
6. Messages (conversation thuc te cua ban)
7. Free space
8. Auto-compact buffer (~33K tokens du tru)
```

#### Cac Slash Commands Quan Trong:
| Command | Chuc Nang |
|---|---|
| `/context` | Xem chi tiet tung muc chiem bao nhieu tokens |
| `/compact` | Nen conversation thanh high-density summary |
| `/clear` | Xoa sach context, bat dau session moi |
| `/cost` | Xem chi phi tokens |
| `/init` | Tao CLAUDE.md tu dong tu codebase |
| `/model` | Doi model (Opus/Sonnet/Haiku) |
| `/status-line` | Tuy chinh thanh trang thai (chi terminal) |
| `/permissions` | Quan ly quyen truy cap cua tools |

#### Chien Luoc Tiet Kiem Tokens:
1. **Bat Extended Thinking** + yeu cau output ngan gon. Thinking khong tinh vao context nhung giup suy luan tot hon.
2. **Dung Sonnet cho sub-agents** (re hon, context lon hon).
3. **Giam MCP bloat**: 1 MCP tool co the ton nhieu hon TAT CA skills cong lai. Dung MCP de test > chuyen sang skill.
4. **Skills chi load front-matter** (~60 tokens) cho den khi duoc goi. MCP load TAT CA tools ngay lap tuc.
5. **Voice dump > model re > tom tat > gui cho Claude chinh**. Tranh gui text tho.
6. **Viet prompt cu the**: "Fix bug o file X dong Y" thay vi "improve this codebase".
7. **Plan truoc khi build**: Giam research tokens trong luc build.

### Ung Dung Cho Build & Sell AI Projects
- **Theo doi chi phi**: Chay `/cost` sau moi project de biet ROI thuc te.
- **MCP vs Skill decision**: MCP = nhanh setup, ton tokens. Skill = lau setup, re tokens. Cho du an lam 1 lan = MCP. Cho workflow lam lai nhieu lan = Skill.
- **Quy tac vang**: Moi skill chi ton ~60 tokens khi khong dung. MCP co the ton hang ngan tokens LUON. -> Skills scale tot hon.

---

## PHAN 12: Skills Nang Cao - Demo Thuc Te (153:00 - 170:00)

### Key Takeaways

#### Cac Skills Thuc Te Cua Nick (doanh thu $300K+/thang):
- **Scrape Leads**: Scrape 1000 leads trong 87 giay, upload Google Sheets, enrich emails
- **Literature Research**: Query PubMed, parallel searches, deep review
- **Website Designer**: Lay data tu Google Sheet > tao custom website cho prospect trong 30 giay
- **Classify Leads**: LLM phan loai leads
- **Email Auto-Reply**: Tu dong tra loi emails
- **YouTube Editor**: Edit videos
- **Client Onboarding**: Onboard khach moi
- **Upwork Apply**: Tu dong apply jobs

#### Cau Truc Skill Toi Uu:
```
skill-name/
├── SKILL.md          # Orchestrator (checklist + instructions)
└── scripts/          # Python scripts (musicians)
    ├── scrape.py
    ├── classify.py
    ├── upload.py
    └── enrich.py
```

- **SKILL.md** = conductor (chi huy dan nhac)
- **scripts/** = musicians (nhac cong thuc thi)
- Claude KHONG tu lam moi thu - no goi scripts da duoc viet san
- Khi co loi, Claude dung tri tue de fix real-time VA cap nhat skill cho lan sau

#### MCP > Skill Pipeline:
1. Tim MCP tool cho service ban muon dung (Gmail, ClickUp, etc.)
2. Test nhanh voi MCP - xac nhan chuc nang hoat dong
3. Noi Claude: "Chuyen thanh skill dung API truc tiep thay vi MCP"
4. Skill moi ton it tokens hon 50-100x

### Ung Dung Cho Build & Sell AI Projects

#### Dich Vu "Skill-as-a-Service":
1. **Lead Gen Automation**: $1-3K/setup. Scrape + classify + enrich + upload to CRM.
2. **Email Management**: $500-1K/setup. Label + auto-reply + priority routing.
3. **Content Pipeline**: $1-2K/setup. Blog > social posts > schedule > analytics.
4. **Client Onboarding Automation**: $2-5K/setup. Welcome kit + project setup + calendar booking.

#### Key Insight:
> "Day la ly do toi khong con thue nguoi nua. Doanh nghiep cua toi van tao ra $300K+/thang loi nhuan. Bat ky khi nao toi muon lam gi, toi chi can noi Claude lam voi 1 skill." - Nick

---

## PHAN 13: Sub-Agents Thuc Chien (191:00 - 206:00)

### Key Takeaways

#### Khi Nao Dung Sub-Agents:
- Khi can **parallelize** cong viec (10 chunks email cung luc thay vi 1 luc 1)
- Ket qua: 1000 emails trong ~1 phut thay vi 6 phut (tiet kiem 6x)

#### 3 Sub-Agents Nen Co Trong Moi Project:
1. **Code Reviewer**: Review code voi zero bias
2. **Researcher**: Tim kiem + tong hop thong tin (dung Sonnet = re)
3. **QA/Tester**: Viet tests + chay tests + bao cao

#### Workflow Chuan:
```
Write Code (Parent) > Code Review (Sub) > QA Test (Sub) > Fix Issues (Parent) > Ship
```

#### Luu Y Xac Suat:
- Moi sub-agent co 95% thanh cong
- 10 sub-agents = 0.95^10 = **59%** tat ca thanh cong
- 50 sub-agents = 0.95^50 = **7%** tat ca thanh cong
- -> Giu task don gian, giam so luong sub-agents khi co the

### Ung Dung Cho Build & Sell AI Projects
- **Parallel processing** la selling point cho khach hang: "Toi xu ly 1000 emails trong 1 phut"
- **Workflow template**: Research > Code > Review > QA > Ship = chuan cho moi du an ban giao

---

## PHAN 14: Agent Teams (206:00 - 236:00)

### Key Takeaways

#### Agent Teams vs Sub-Agents:
| | Sub-Agents | Agent Teams |
|---|---|---|
| Context | Chia se voi parent | Hoan toan doc lap |
| Communication | Chi voi parent | Voi nhau + team lead |
| Cost | Thap | **7x tokens** |
| Best for | 1 ket qua cu the | Collaboration phuc tap |
| Coordination | Parent quan ly | Shared task list |

#### Demo 1: 3 Website Designs Song Song
- 3 agents tao 3 designs khac nhau cung luc
- Chon thang tot nhat > spin up 3 agents nua de iterate
- Ket qua: Kham pha khong gian thiet ke rong hon nhieu

#### Demo 2: Security Audit OpenClaw Repo
- 10 scanner agents doc code base song song
- 4 agents ghi nhan security issues
- 2 "devil's advocate" agents tranh luan ve tung issue
- 15 fixer agents (1 per issue) - nhung bi huy vi ton qua nhieu tokens
- Chi phi: ~$80 trong 15 phut. 1.3M+ Sonnet tokens.

#### Uu & Nhuoc Diem:
- **Uu**: Research nhanh, explore design space rong, debate cai thien chat luong
- **Nhuoc**: DAT (7x tokens), phuc tap, de mat kiem soat chi phi
- **Kich hoat**: settings.json > `"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}`

### Ung Dung Cho Build & Sell AI Projects
- **THAN TRONG voi chi phi**. Agent teams = "vu khi hat nhan nham vao vi tien ban".
- **Dung cho**: Research rong (scan codebase, security audit, competitive analysis)
- **KHONG nen dung cho**: Task don gian co the lam voi sub-agents hoac parent agent
- **Meo**: Dung Sonnet cho teammates, giu team nho (3-5), tat agents khi xong

---

## PHAN 15: Git Worktrees - Parallel Development (236:00 - 242:00)

### Key Takeaways
- **Worktree** = tao ban sao folder rieng cho moi branch. Cac agents lam viec HOAN TOAN CACH LY.
- Khong co kha nang 2 agents sua cung 1 file (loai bo "agent conflicts")
- Workflow: Main branch > tao 3 worktrees (about, contact, services) > moi agent lam trong folder rieng > merge ve main
- Tot hon agent teams cho viec tranh xung dot file

### Ung Dung Cho Build & Sell AI Projects
- **Multi-page website service**: 3 agents lam 3 trang song song, merge lai = delivery nhanh gap 3x
- **Feature development**: Moi feature = 1 worktree = khong anh huong main code

---

## PHAN 16: Deployment & Automation Endpoints (242:00 - 250:00)

### Key Takeaways

#### Deployment Options:
| Platform | Dung Cho | Chi Phi |
|---|---|---|
| **Netlify** | Static sites, landing pages | Free tier |
| **Vercel** | Next.js apps, full-stack | Free tier |
| **Modal** | Backend functions, APIs, skills-as-URLs | $5 free credit, rat re |

#### Modal - Bien Skills Thanh URLs:
1. Tao tai khoan Modal (free $5-30 credit)
2. Lay API token
3. Noi Claude: "Deploy skill X len Modal"
4. Co URL cong khai trong vai phut
5. Ket noi voi Make.com, N8N, Zapier qua webhook

#### Demo: Scrape Leads Qua Web
- Tao form tren URL: nhap query + location + so luong
- Click submit > scraper chay > download CSV
- Bat ky ai co URL deu co the dung

### Ung Dung Cho Build & Sell AI Projects

#### Mo Hinh Kinh Doanh Moi - "Skill-as-a-Service URL":
1. **Tao skill** (scrape leads, generate proposals, classify data...)
2. **Deploy len Modal** co form input
3. **Ban access** cho khach hang qua URL + API key
4. **Thu phi**: $50-200/thang hoac per-use pricing
5. **Chi phi thuc te**: ~$0.01-0.05/request tren Modal

#### Pipeline Ban & Sell Hoan Chinh:
```
1. Identify client pain point (lead gen, email, proposals...)
2. Build skill voi Claude Code (1-2 gio)
3. Test & iterate cho den 98%+ accuracy
4. Deploy len Modal (5 phut)
5. Tao landing page (10 phut voi Claude)
6. Ban cho khach: $500-5000 setup + $50-200/thang
7. Chi phi van hanh: ~$5-20/thang (Modal + Claude API)
8. Margin: 90%+
```

---

## TONG KET - HANH DONG NGAY

### 5 Viec Lam Ngay Hom Nay:
1. **Cai dat Claude Code** + tao CLAUDE.md template cho loai du an ban muon ban
2. **Tao 1 skill** tu workflow ban lam hang ngay (email, lead gen, content...)
3. **Test skill** voi 3-5 fresh Claude instances, fix cho den 95%+
4. **Deploy 1 skill len Modal** de co demo URL
5. **Lam 1 landing page** bang screenshot loop method

### Gia Tri Lon Nhat Tu Khoa Hoc:
- **Task > Do > Verify loop** = cot loi cua moi thu
- **Plan Mode truoc khi build** = tiet kiem 50%+ thoi gian va tokens
- **Skills > MCP** cho workflow lam di lam lai
- **Sub-agents cho parallelization**, Agent Teams cho research rong
- **Ban workflow/skills**, khong chi ban code
- **Security review** truoc khi deploy public

### Cong Thuc Tinh Gia:
- Thoi gian tiet kiem cho khach/thang x Gia tri 1 gio cua ho = Gia tri mang lai
- Vi du: Tiet kiem 20h/thang x $50/h = $1000 gia tri/thang
- Ban $200-500/thang = win-win. Margin 90%+.
