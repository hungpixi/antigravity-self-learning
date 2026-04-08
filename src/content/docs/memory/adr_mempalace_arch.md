---
name: Mempalace Architecture & AAAK Memory Dialect
description: Giao thức bộ nhớ dài hạn đa chiều (Vector + Temporal Knowledge Graph + SQLite) cho AI Agents và hệ ngôn ngữ nén AAAK.
type: reference
---

**Fact/Rule:** MemPalace là MCP Server quản lý bộ nhớ dài hạn với kiến trúc "Cung điện ký ức" lai (Hybrid RAG). Nếu dự án yêu cầu bộ nhớ dài hạn chống ảo giác (Memory Retention), sử dụng MemPalace thay vì vector DB thô.

**What (Các Component lõi):**
1. **Temporal Knowledge Graph (SQLite)**: Lưu trữ các Facts chặt chẽ dạng Triples `(Subject, Predicate, Object)` đi kèm trục thời gian `valid_from` và `valid_to`. Hỗ trợ triệt tiêu tri thức cũ (Graph Invalidation).
2. **Contradiction Detector (Fact Checker)**: Tự động bắt lỗi xung đột logic khi nạp fact (Vd: Task đã gán cho Allan nhưng lại ghi đè thành Ben).
3. **Palace Graph (ChromaDB)**: Tìm kiếm Semantic theo kiến trúc cây `Wing (Domain/Project) -> Room (Concept/Aspect) -> Drawer (Verbatim Text)`.
4. **AAAK Dialect**: Ngôn ngữ nén memory chuyên dụng giúp tiết kiệm token cho LLM:
   - Viết tắt tên bằng 3 ký tự hoa: `ALC=Alice`.
   - Bọc context/cảm xúc bằng hoa thị: `*warm*`, `*fierce*`.
   - Định dạng ngắn bằng pipe `|`: `FAM: ALC→♡JOR | 2D: RIL(18,sports)`.
5. **Agent Diary**: Nơi mỗi Agent ghi sổ nhật ký tự sướng sau ca làm việc (`mempalace_diary_write`).

**Why:** Khắc phục nhược điểm cốt lõi của Vector RAG truyền thống: AI dễ bị "nhầm lẫn dòng thời gian" khi fact đâm chồng chéo. Knowledge Graph + AAAK Dialect là cấu trúc bền vững nhất cho sự tiến hóa độc lập của bot.

**How to apply (MCP Protocol):**
1. **Init Session**: Gắn tool vào Agent. Chạy `mempalace_status` để fetch metadata và AAAK spec.
2. **Verify Before Speak**: Luôn check `mempalace_kg_query` hoặc `mempalace_search` MỖI KHI nhắc đến tên người/dự án trong Database. Tuyệt đối không đoán mò.
3. **Handling Updates**: Khi facts thay đổi, phải gọi `mempalace_kg_invalidate` xóa fact cũ, rồi mới `mempalace_kg_add`.
4. **Diary Tracking**: Cuối session (hoặc khi có insight mới quan trọng), gọi `mempalace_diary_write` lưu hành trình của chính Agenty bằng ngôn ngữ AAAK.
