---
title: "SKILL"
name: AI Agent Architecture Reference & Playbook
description: "Tổng hợp kiến thức thiết kế hệ thống AI Agent từ ProductiveTechTalk. Auto-trigger khi thiết kế agent system, AI workflow, bot automation. Triggers on 'thiết kế agent', 'xây dựng AI', 'agent architecture', 'bot workflow', 'AI team', 'tự động hoàn toàn', 'agent playbook', 'agentic ai'."
type: reference
---

# 🤖 AI Agent Architecture & Playbook

> Tập hợp hệ thống tri thức xây dựng AI Agents, được máy tự động cào và tổng hợp bằng framework Crawl4AI. 
> Phân loại theo các quy luật vận hành, bài học triển khai và cấu trúc kỹ thuật cốt lõi.

## Phần 1: Các mô hình kiến trúc cốt lõi

### 1. Kiến Trúc 2-Layer Agent-Native (Mô hình DeepTutor)
- **Vấn đề:** Khi AI ecosystem phình to, không thể ném 50 tools ngẫu nhiên cho 1 Agent tự chọn, sẽ làm loạn Router và giảm độ chính xác.
- **Giải pháp:** Tách hoàn toàn hệ thống làm 2 Layers: 
  - **Level 1 (Tools):** Các hàm tiện ích gọi 1 lần (Web Search, File Execute, RAG).
  - **Level 2 (Capabilities):** Các luồng Agent độc lập (Research, Problem Solve) có workflow cứng. Khi User gọi, hệ thống dồn toàn bộ quyền Controller (vòng lặp hội thoại) sang cho Capability đó.
- **Lợi ích:** Plug-n-play cực mượt, mở rộng quy mô dễ không làm phình Orchestrator gốc.

### 2. Phân Rã Kiến Trúc: Đa Tác Vụ (Multi-Agent) Thay Vì Monolith
- **Vấn đề:** Dùng 1 Prompt khổng lồ cho 1 model duy nhất (monolithic) làm giảm reliability khi task dài.
- **Giải pháp:** Sử dụng mô hình chuyên môn hóa. Ví dụ framework **G-Stack** chia thành 28 vai trò khác nhau (Security Reviewer, Test Writer, Architect). AI không chỉ làm coder mà làm thành viên nhóm phần mềm.
- **Lợi ích:** Dễ rollback nếu 1 module lỗi không ảnh hưởng toàn hệ thống (Isolated units). Cross-validation qua nhiều models.

### 2. Giao Thức Tích Hợp: CLI+Skills vs MCP
- **MCP (Model Context Protocol):** Overhead Context cực kỳ cao (~55,000 tokens chỉ cho Tool description), dẫn đến tốn kém nghiêm trọng (ví dụ 10,000 users = burn $1,600/day). Rất tốt cho Enterprise (Centralized control, compliance).
- **CLI + Skills:** Giải pháp "thực dụng" cho Solo Builder/Nhỏ. Nhanh hơn, tiết kiệm token đến 32 lần, và không rơi vào tình trạng "Mất tập trung giữa Context" (hiệu ứng Lost-in-the-Middle) của các LLM.

## Phần 2: Workflow & Framework cho Solo Builders

### 1. Kiến Trúc "Senior-Junior" Agents trong Vận Hành (Open Claude)
- Đừng để Agent chạy độc lập 1 mình và bắt con người quản lý. Hãy dùng kiến trúc "Senior + Junior": 1 Agent quản lý chất lượng/kiểm duyệt (Senior) và 1 Agent thực thi (Junior).
- Tự động hóa được vòng lặp Feedback (Self-Correction), tự Agent đọc, phê bình và sửa task.
- Build "Shared Memory" tại một nơi chung (Slack/Telegram) thay vì Local. Cả công ty dùng chung và share skills qua lệnh command ngắn gọn.

### 2. Phương pháp "6 Socratic Questions" trước khi Code
- Cơ chế của G-Stack chặn việc bắt tay vào code ngay: dùng AI rà soát triết lý và kiến trúc qua 6 câu hỏi truy vấn sâu (Why/What) để gọt giũa logic trước khi thực thi.

## Phần 3: Giao Tiếp Hệ Thống & Tự Động Hóa (System Control & RPA)

### 1. Visual RPA (Claude Computer Use)
- Thay vì chọc API hoặc dùng Playwright selector dễ gãy, Agent chụp ảnh màn hình, tính tọa độ XY và giả lập thao tác chuột/phím. 
- Ưu điểm: Điều khiển được mọi UI (Discord, iOS Simulator). Nhược điểm: Bị kẹt khi có overlay popup đè lên.

### 2. Định Dạng Chuyển Giao: `design.md` Handoff
- Design tool (như Google Stitch) xuất Layout/UI kit dưới định dạng file text `design.md`. Các AI Coding Agents sẽ đọc file `.md` này thay vì nhìn ảnh mockup, loại bỏ hoàn toàn Human Designer bottleneck.

### 3. Cơ chế Dynamic Heartbeat (2-Phase Decision)
- **Vấn đề:** Các Auto-bot nếu dùng cronjob tĩnh thì khô khan, spam. Nhưng bắt LLM scan database liên tục thì burn token dữ dội.
- **Giải pháp (Pattern từ DeepTutor):**
  - **Phase 1 (Wake & Decide):** Cron đánh thức Agent, bắt nó đọc lướt qua file `HEARTBEAT.md`. Agent phải gọi 1 Virtual Tool trả về JSON `{action: 'skip' | 'run', tasks: '...'}`.
  - **Phase 2 (Execute):** Nếu `skip`, tắt bot ngay lập tức, tiết kiệm token. Nếu `run`, mới chạy Agent loop xịn, sau đó qua bước Evaluator xem Log có đáng để đánh thức (Push Noti) gọi User không.
- **Lợi ích:** Tạo ra Auto-bot cực thông minh, tự ngủ, tự thức dậy báo cáo khi có sự cố, y chang con người không hề spam.

### 4. Kiến Trúc Always-On: Background Agents & Repo Daemons
- Xu hướng dịch chuyển AI từ "Assistant" thành "Partner": Chạy agent ngầm dạng Daemon để tự cron-job review code ban đêm, chạy test và refactor liên tục.

## Phần 4: Security & An toàn thực thi (Harness Engineering)

### 1. Harness Engineering & Security Hooks
- Không để AI tự ý xài công cụ nguy hiểm ở mọi nơi. Sử dụng "Routing Rules" và "Security Hooks" (vd: chặn không cho AI xài Trình duyệt để chọc vào URL nội bộ, hoặc Salary Guard chặn quyền fetch database lương). 
- **Bảo mật bằng Code, không phải bằng Niềm tin (Prompt).** Dùng hệ thống hook chốt chặt ngay lớp hạ tầng.

### 2. Kiến trúc Planner - Generator - Evaluator (Cảm hứng từ mạng GAN)
- Tránh tình trạng AI tự code tự khen mình đúng. Chia làm 3 Agent: Planner (Lên Spec) -> Generator (Viết Code) -> Evaluator (Chạy test bằng Playwright thực tế).
- Evaluator chê -> Generator sửa. Buộc AI rà soát triệt để edge cases.

### 3. Dynamic Ontology (Mô hình Palantir)
- Enterprise Agent không kết nối lỏng lẻo với Data + LLM, mà hoạt động trên Ontology (Mô hình khái niệm hóa doanh nghiệp). Agent tự động thừa kế mọi Rule Governance của con người, không thể xem data vượt quyền.
- **Shared Sandbox:** Cho phép Manager là người thật nhảy vào cùng mô phỏng Sandbox giả lập với AI trước khi commit thay đổi vào DB.

### 4. Codebase Context Graph (Tích hợp Grapuco Local)
- **Kiểm soát Dependency bằng Knowledge Graph:** Cải thiện hệ thống Harness bằng việc sử dụng Grapuco. Thay vì để AI tự dò dẫm file cấu trúc (rất tốn token và dễ bị Lost-in-context), Harness bắt buộc AI phải dùng **Local Grapuco CLI (AST-based)** để phân tích cấu trúc (outline) và trích xuất hàm (extract) chính xác 100%.
- **Security Dependency Lock (Kiểm duyệt Kiến trúc):** Grapuco đóng vai trò như một lớp "Security Hook" thứ hai, khóa các thay đổi có nguy cơ phá vỡ dependency cốt lõi. Bất kỳ refactor nào cũng phải chạy lệnh dò dependency (`deps`) trước khi sang bước sửa code, giảm thiểu rủi ro regression tối đa.
- **Tối ưu Hiệu suất bằng AST Caching (Performance Tuning):** Kỹ thuật đột phá cho phép tăng tốc độ truy vấn Grapuco lên gấp 50 lần. Hệ thống băm đường dẫn file thành hash MD5 và so sánh Modification Time (`mtime`). Kết quả JSON (`outline`, `deps`) được lưu vào `.cache/` để AI có thể đọc ngay lập tức mà không phải chờ nạp và phân tích AST lại từ đầu, biến luồng chạy Agentic thành tốc độ phản hồi tức thì (Real-time).

## Phần 5: The Virtual Company Framework & Định Hướng Mới

1. **Framework "Paper Clip" (Cost Tracking & Roles):** Tổ chức AI như công ty ảo (CEO, CTO, CMO...). Đặc biệt phải có Ledger theo dõi Costs (Token API) realtime trên từng Agent để thay đổi Model đắt/rẻ hợp lý.
2. **Kỷ nguyên "Hết thời Micro-SaaS cồng kềnh":** Kỹ năng code không còn là hào nước (moat). Cơ hội trong kỷ nguyên AI là lắp ráp APIs hạ tầng theo luồng workflow sát nhất cho Domain Khách Hàng (Custom glue software), loại bỏ các nền tảng SaaS khổng lồ nhiều tính năng thừa.
