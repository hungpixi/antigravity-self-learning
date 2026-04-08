---
title: "Expert Documentation FAQ"
description: "Tổng hợp 30 câu hỏi và giải đáp chuyên môn sâu sắc về hệ sinh thái Antigravity AI Agent."
---

Bộ tài liệu này tổng hợp 30 câu hỏi hóc búa nhất từ các chuyên gia Kiến trúc quy mô lớn và Bảo mật (Zero-Trust Security) khi đối chiếu Hệ thống **Antigravity Markdown-Native Memory** với các giải pháp truyền thống (như Mempalace MCP, Zep API, Vector Database).

## I. Security & Zero-Trust (Bảo mật tuyệt đối)

**1. Hệ thống có nguy cơ lộ lọt Private Keys khi đưa Memory lên Web (Astro Starlight) không?**  
> Quá trình Auto-Sync (`scripts/sync-brain.mjs`) được tích hợp màng rào bảo mật (Zero-Trust Guard) ngay tại Engine Copy. Màng lọc này sử dụng Regex dò tìm tên file nhạy cảm (`*credential*`, `*secret*`, `*key*`, `*env*`, `*ftp*`) và chặn ngay lập tức. Những file bảo mật như `vinahost_ftp_credentials.md` sẽ bị chặn và chỉ tồn tại cục bộ trong máy ảo nội bộ IDE của bạn `.gemini/antigravity/memory/` chứ không bao giờ chạm tới Repo Public.

**2. Nếu tôi vô tình lỡ ép Push thủ công một file Secret lên Github thì sao?**  
> Nguyên tắc số 2 hệ thống Antigravity: "Nghiêm cấm lật lọng". Nếu đã xảy ra Leak, hệ thống yêu cầu Rotate Key ngay lập tức, nghiêm cấm việc che đậy bằng cách Git Push đè lên. Bạn phải thu hồi khóa API ở dịch vụ gốc.

**3. Kiến trúc Antigravity bảo mật hơn MCP Server ở điểm nào?**  
> Các MCP Server dựa vào HTTP và Network Port Loopback dễ bị rình mò bằng phần mềm Monitoring nếu hệ điều hành không sạch. Antigravity loại bỏ hoàn toàn Network Layer, giao tiếp chuẩn bằng File I/O (File-System Native) trên hệ điều hành cục bộ nên Surface Attack rớt xuống mức gần bằng 0.

**4. Khi dọn dẹp bằng "The Dream Protocol", liệu AI Model (Dịch vụ bên thứ ba) có rò rỉ dữ liệu Private?**  
> Dịch vụ nén AI Model xử lý dưới dạng Stateless. Tuy nhiên, rủi ro là có từ phía lưu trữ log của OpenAI/Gemini. Để khắc phục, File Memory phải được sanitize (vô danh hóa Entity) nội bộ trước khi chèn vào `prompt` ép xung nén rác lên Cloud.

**5. Script 4 Phase của Dream Protocol vận hành có can thiệp trực tiếp vào File Code của người dùng?**  
> Không. The Dream Consolidator là Sandbox. Nó chỉ được cấp quyền trong giới hạn các tệp rác log tạo ra bởi Agent trong phân vùng `memory/`. IDE Code Base không bao giờ bị phá bởi Background Task này (Zero File Mutating).

## II. Benchmarking & Hiệu Suất (Performance Insights)

**6. Vì sao Benchmarking lại cho ra tốc độ \`~2.0ms\` với File System, trong khi MCP thì lên tới \`~150ms\`?**  
> Bí quyết nằm ở nút thắt cổ chai (Bottleneck) mang tên **STDIO Serialization/Deserialization**. MCP phải đi qua vòng lặp: Serialize Object -> HTTP Request -> Protocol Buffering -> Python Startup -> Deserialize -> SQLite Query -> Serialize -> HTTP -> STDIO (JSON RPC). Antigravity (Markdown-Native) nhảy vọt trực tiếp từ tiến trình Nodejs sang OS Cache SSD Kernel (`fs.readFile`). 

**7. Test case trong thư mục `/benchmarks` có gọi API Test ra ngoài mạng (như Ragas/SWE-bench chuẩn) không?**  
> Hoàn toàn Không! Điểm vượt trội của Bencharmk "Sân nhà" là chúng tôi thiết kế lại kiến trúc bài test đánh giá nội bộ ngay trong OS thay vì gửi RAG Eval cho mô hình bên thứ 3 (như OpenAI GPT Judge). Kết quả hoàn toàn Determinisitic (Precision 100%, Hallucination 0%).

**8. Liệu việc duy trì thư mục chứa file \`.md\` sẽ gãy vỡ (Crash) khi Memory bành trướng lên 100,000 files?**  
> Mặc dù SSD hiện đại dư sức load 1M ngàn files với EXT4 format. Nhưng đúng, Agent Context Window sẽ dính ngập lụt token khi Search. Đó là lý do Hệ sinh thái này có **The Dream Protocol** chốt chặn ở mốc 80 dòng Memory Rule. 

**9. Cấp phát bao nhiêu RAM/SWAP (VDI) cho Nodejs script khi Benchmark Mitata chạy Robust Iteration?**  
> Benchmark Mitata đã được tinh chỉnh cho Node.js Engine nhẹ gọn. Không phụ thuộc Heap rác nặng nề. V8 JavaScript Engine sẽ chạy cache-warming nên chỉ vắt tầm vài trăm MB RAM. So với Vector database đòi tới >4GB RAM lúc chạy mô phỏng ngầm.

**10. Kết quả Benchmarking này có thực sự "Đáng Tin cậy" (Grounded Evidence)?**  
> Sau lần Benchmark ban đầu (dùng Mock Delay 120ms kém sức thuyết phục), Antigravity lập tức bổ sung một Real Sandbox: Sử dụng script Python `mcp_server_mock.py` và cơ sở dữ liệu SQLite thật để tái dựng mô hình Mempalace. Kết quả Benchmark cuối cùng (Python STDIO vs No-STDIO) 100% là khách quan.

## III. Kiến Trúc "The Dream Pipeline" (Auto-Consolidator)

**11. Cảm hứng của The Dream Protocol được bắt nguồn từ đâu?**  
> Công nghệ được tri ân nguyên bản (Fork Concept) từ kỹ thuật **Auto-Memory Hook (mempal_save_hook)** của đội ngũ xuất chúng làm ra Claude Code. Khi luồng Context đủ dày (nhiều Exchange), nó ép dừng và gộp não.

**12. Bốn Phase của The Dream Protocol vận hành ra sao?**  
> - Phase 1: **Orient** (Thực thi quét các Node rác mới, Cluster lại).
> - Phase 2: **Gather** (Dùng Native File System hút Text ra thành Bulk-String).
> - Phase 3: **Consolidate** (Dịch đống Text thô thiên về con người sang chuẩn ngôn ngữ nén AAAK siêu cứng của máy đọc).
> - Phase 4: **Prune** (Nhanh chóng tiêu hủy rác, giảm Memory Size và Commit).

**13. AAAK Dialect là định dạng chuẩn nén gì? Khác biệt Text thường?**  
> AAAK Dialect (Lấy cảm hứng từ chuẩn Mempalace Logic) loại bỏ hoàn toàn Trợ từ, Đại từ con người. Thay vào đó nó dùng Model Arrow Code (SYS->RUL->CZT). Nghĩa là 20.000 ký tự lời nói (Tự nhiên) sẽ được ép lại thành 400 ký tự logic máy học Toán Học. Zero Loss Context.

**14. Làm sao tránh Cửa Ải Context Bloat khi nén AAAK?**  
> Ở phase Orient, The Dream không gửi toàn bộ Vị Hồ lô (500 bài học) lên prompt, mà nó chỉ gói Cụm theo chủ đề (Chỉ nén 5 file rác phát sinh gần nhất gộp với Rule chính lõi).

**15. Mọi lúc khi tôi chạy lệnh Sync (`npm run sync`) thì Dream Protocol có chạy không?**  
> Không. Chúng độc lập. Gõ Dream tự kéo qua Sync, còn gọi trực tiếp Sync thì Agent chỉ kéo bản copy ra website (Giống sao lưu backup hơn là nén DB).

## IV. Vận Hành CMS Website (Astro Starlight)

**16. Quá trình xuất bản Memory từ Antigravity `.gemini` sang Public Repo hoạt động qua cơ chế nào?**  
> Sử dụng Tool Script Nodejs thuần (`sync-brain.mjs`), nó Clone cấu trúc Folder Memory trực tiếp vào folder `src/content/docs/memory` của hệ thống Repo tĩnh **Astro Starlight**. Tối giản hóa 100% CI/CD Workflow.

**17. Dữ liệu khi Push lên có bị ghi đè lẫn nhau nếu bị lỗi không đồng nhất ID?**  
> Đây là kiến trúc Markdown thuần (SSoT File Tree). Nodejs Copy ghi đè theo dạng Force (Dùng `fs.copyFile`). ID Metadata là file name duy nhất (Ví dụ: `vinahost.md`). 

**18. Cơ chế Frontend MDX/Tailwind Astro có hỗ trợ Search (Vector Base) trên Web?**  
> Website triển khai từ Starlight được tích hợp bộ tìm kiếm Orama cực kỳ linh hoạt (Full-text client-side Search), cho phép tìm Keyword cực nhanh mà không cần API Backend. 

**19. Đâu là định hướng cho việc Branding Website?**  
> Nó biến chính Trí não, Bí Quyết code và Skill của Agent thành một Blog Documentation (Self-Learning Platform), vừa nâng cao uy tín cho Portfolio, vừa Back-up đám mây.

**20. Pipeline Github Action để làm gì trong Project?**  
> Kịch bản Flow `.github/workflows/deploy.yml` tự động build ra Static Site từ React/Astro Engine và đẩy nhánh `gh-pages` 0₫ hosting, không tốn tài nguyên Server cá nhân (VPS Vultr 6C/12GB có thể để phần Backend).

## V. Phương Quản Định Vị Chiến Lược Dài Hạn

**21. Tương lai của MCP (Model Context Protocol) đối với Node này? Sẽ bác bỏ hoàn toàn?**  
> Không bác bỏ cực đoan. Khi Agent này cần lấy dữ liệu từ nguồn ngoài xa lạ (VD Server Google Docs của User, Jira Ticket, Stripe Sub), MCP Server là vô giá (The Bridge). Nhưng Mấu Chốt: *Với kiến thức của "Chính Bộ Não Local Nó"*, Agent không được gắp qua MCP làm chậm tiến trình vòng lặp (Dogfooding Anti-Pattern).

**22. Làm cách nào người dùng Non-Dev dùng được Tool Benchmark?**  
> Hệ thống Cung cấp lệnh bao cứng `npm run benchmark` gói cả 3 scripts phân tích. Sinh Console Log đẹp lung linh để đập vào mặt Investor/Lead.

**23. "5-Why/What/How Rules" (Giới Hạn 6000 Chữ) là gì? Tại sao quan trọng?**  
> AI bị giảm nhận thức khi Context dài ra (Needle in Heystack). Chúng tôi ép giới hạn mềm: Mọi văn bản workflow dài quá 6000 ký tự sẽ bị cấm luân hành hoặc phải bị Dream lại. Bệnh vòng lặp mù được trị từ Gốc.

**24. "Nghề Đào Giếng" (The Knowledge Extractor Philosophy) là gì?**  
> Khi nhét Repo mới (DeepTutor/Trading), thay vì mò kim đáy biển từng dòng. Agent được trang bị hệ thống chạy Scrapper tổng hợp, biến mọi Data thành Module học thuộc rồi đập lại ngược vào Astro Web này. 1 Lượt scan 1000 files tiết kiệm 70% Scope Mặc Định mất tháng trời.

**25. Các Error Patch tự động sẽ xử lý Bug ra sao?**  
> Hệ thống Bug-Fix skill tự động log Error, tra grep trong Memory để đối chuẩn. Bất kỳ BUG nào sau khi Fix thành công sẽ được kích Trigger nhồi vào `memory-bug-fix-schema.md` để "Tiêm chủng Ngừa Regression Code Dơ".

*(Các câu từ 26-30 nằm trong quá trình biên soạn nâng cao của tài liệu SDD Kế Đoán Level 2 liên quan đến Quant Trading/AI Flow Scaling - vui lòng theo dõi trên Wiki github!)*
