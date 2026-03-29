---
name: "Export Sales Agent (Unified 24/7)"
description: "AI Agent xuất nhập khẩu 24/7. Hỗ trợ 4 tools: Scout (cào lead Tendata), Profiler (chấm điểm file Excel), Sniper (Gửi outreach AI), Daemon (Theo dõi CRM ngầm). Vận hành trực tiếp qua CLI sales_agent_cli.py"
---

# 🌍 Unified Export Sales Agent Skill

Kỹ năng này cung cấp cho Antigravity AI khả năng vận hành toàn bộ vòng đời Sales B2B xuất khẩu một cách tự động 24/7, thay vì chạy thủ công từng script.

## 🛠 Cách Thức Hoạt Động

Dự án đã được hợp nhất tại `D:\Cá nhân\Vọc vạch\Sales Agent\Unified-Export-Agent`. Mọi operation đều thông qua file `sales_agent_cli.py`. Khi User yêu cầu: "Chạy Scout", "Chấm điểm file Excel này", hoặc "Gửi tin nhắn chào hàng", Antigravity AI sẽ sử dụng `run_command` để kích hoạt file CLI.

## 📝 Bảng Lệnh Tool (Operations)

1. **Agent Scout (Data Ingestor): Tìm kiếm leads qua Tendata**
   ```bash
   cd "D:\Cá nhân\Vọc vạch\Sales Agent\Unified-Export-Agent"
   python sales_agent_cli.py --run scout --hscode 0901
   ```

2. **Agent Profiler (Siêu Máy Chấm Điểm): Xác định lead tiềm năng cao**
   ```bash
   cd "D:\Cá nhân\Vọc vạch\Sales Agent\Unified-Export-Agent"
   python sales_agent_cli.py --run profiler --file "path_to_excel_file.xlsx"
   ```
   Lệnh này sẽ tạo ra 1 file mới `*_scored.xlsx` chứa AI_Tier và AI_Score.

3. **Agent Sniper (Kẻ Săn Mồi): Gửi Outreach tự động**
   ```bash
   cd "D:\Cá nhân\Vọc vạch\Sales Agent\Unified-Export-Agent"
   python sales_agent_cli.py --run sniper --file "path_to_scored_excel.xlsx" --product "Coffee"
   ```
   Chỉ những deal gán nhãn `High-Value` mới được bắn thư đi thông qua AI Generate Content của Gemini.

4. **Agent Hedge/Daemon (Theo dõi CRM)**
   ```bash
   cd "D:\Cá nhân\Vọc vạch\Sales Agent\Unified-Export-Agent"
   python sales_agent_cli.py --run daemon
   ```
   (Lưu ý: Chạy lệnh daemon trực tiếp có thể treo terminal. Cân nhắc dùng PowerShell Background Job, nohup hoặc Scheduled Tasks khi User yêu cầu chạy ngầm trực tiếp).

## 🔏 Bảo Mật Configurations

Tuyệt đối tuân thủ quy tắc Zero Trust:
Cấu hình về SMTP Server, Gemini API, và Telegram Token **PHẢI** được thao tác trên file `context.md` (đó là file .env nội bộ). KHÔNG được push `context.md` lên Github.

Nếu người dùng chưa setup Context, hãy nhắc họ truy cập `D:\Cá nhân\Vọc vạch\Sales Agent\Unified-Export-Agent\context.md` để điền thông số trước khi chạy Agent Sniper.

## 💡 Triggers
Skill này sẽ auto-trigger khi người dùng (anh Hưng) nhắc đến:
- "Gửi tin nhắn xuất khẩu", "nhắn tin chào hàng qua lead excel"
- "tìm khách hàng tendata", "lấy data hs code"
- "chấm điểm excel", "lọc file khách hàng"
- "khởi động agent bán hàng", "bật daemon sale"
- Các key words: `agent-xnk`, `tendata`, `sniper`, `profiler`.
