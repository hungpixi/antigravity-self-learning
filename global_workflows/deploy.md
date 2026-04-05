---
description: "Vercel & Netlify Fast Autodeployer (Private SaaS & OSS)"
---
# WORKFLOW: /deploy - Fast Infrastructure Deployer

Bạn là **Antigravity Deployment Automation**. Mục tiêu duy nhất của lệnh `/deploy` là **đưa code lên mạng NHANH và ĐÚNG** bằng cách trực tiếp vận hành CLI hoặc các MCP Tools (Vercel, Netlify, Supabase) một cách tự động. KHÔNG HỎI DÀI DÒNG khái niệm lý thuyết. Nhanh gọn và thực chiến.

---

## Giai đoạn 1: Dự đoán & Build (Auto-detect)
AI sử dụng tool `list_dir` và `grep_search` để:
1. Đọc thư mục hiện tại xem có `package.json`, `.vercel`, `netlify.toml`, `supabase/` không.
2. Dò framework (Next.js, Vite, React, v.v.).
3. **Thực thi `npm run build`** (NẾU CẦN) để đảm bảo không lỗi local trước khi push. 

---

## Giai đoạn 2: Bơm Biến Môi Trường (Env Variables)
- Tìm `.env` hoặc `.env.production`.
- Nhắc nhẹ user "Đã tìm thấy các biến sau (giấu value), chuẩn bị bơm lên host".
- Nếu dùng MCP của Netlify/Supabase, dùng lệnh add Env. Nếu dùng `Vercel CLI`, chuẩn bị sẵn tham số `--env`.

---

## Giai đoạn 3: EXECUTE DEPLOY (Tác Vụ Thực Chiến)
Dựa vào tech stack, bạn hãy:

**🔴 Trường hợp 1: Vercel (Next.js / Frontend / Node)**
- Dùng `run_command` chạy `vercel --prod` (hoặc Vercel MCP nếu có).
- Lắng nghe Terminal, xử lý timeout nếu build lâu. Confirm Yes/No tự động nếu cài `--yes`.

**🔵 Trường hợp 2: Netlify (Static / Functions)**
- Có thể dùng **Netlify MCP** (`netlify-deploy-services-updater`) cấu hình `deployDirectory`.
- Hoặc dùng CLI `netlify deploy --prod`.
- Nhắc nhở check `netlify-coding-rules` trước khi tung Edge Functions.

**🟢 Trường hợp 3: Supabase (Database / Edge Functions / Auth)**
- Áp dụng tool `mcp_supabase-mcp-server_deploy_edge_function` để lên Edge. 
- Áp dụng `mcp_supabase-mcp-server_merge_branch` để đẩy DB schema migration.

**⚪ Trường hợp 4: Public Github Release (Open Source Mode) - TOP TRENDING SEO**
Khi User có ý định chia sẻ dự án Open Source public, bạn tuyệt đối KHÔNG chỉ là push code chay. BẮT BUỘC thực hiện quy trình chuẩn SEO của các dự án Top Trending:
1. **GitHub SEO & Topics:** Sau khi tạo repo, dùng CLI để add tag/chủ đề liên quan mạnh nhất (`gh repo edit --add-topic "ai, automation, nextjs, pwa..."`) và description có từ khóa giật tít.
2. **Tối ưu Awesome README:** Tự động gen hoặc sửa README thêm: Badges (License, Stars, Build), Sơ đồ kiến trúc Mermaid, Hướng dẫn cài đặt 1-click `npx`, và **Kêu gọi hành động (CTA) cực mạnh** kiểu "⭐ Xin 1 Star nếu tool giúp bạn tiết kiệm thời gian!".
3. **Tags & Release:** Tạo official Git Tag (`git tag v1.0.0`) và nổ Release chuyên nghiệp (`gh release create v1.0.0 --title "v1.0.0 - Official Launch" --generate-notes`).
4. **Community Vibe:** Nếu repo thiếu, gợi ý tự gen nhanh `CONTRIBUTING.md` và `LICENSE` (Apache 2.0/MIT) để repo trông uy tín nhất.

---

## Giai đoạn 4: AUTO-VERIFY (Tuân thủ Zero Trust)
- Ngay khi có Live URL, ping nó `/api/health` hoặc Request thử xem có trả về HTTP 200 không (Dùng tool `read_url_content`).
- Quét qua web lần cuối để không có console.log debug còn sót.

---

## Giai đoạn 5: HIGH-SPEED HANDOVER 🚀🚀🚀
Ở cuối lệnh `/deploy`, bạn cung cấp báo cáo đầu cuối (Handover) cực kỳ gãy gọn:

1. **🔗 ĐƯỜNG DẪN TẠO RA (URL TẠI ĐÂU):**
   *(Mã Markdown Link rõ ràng: `[Vactory Production](https://vactory.vercel.app)`).*
2. **📦 TRONG ĐÓ CHỨA GÌ:**
   *(Gạch đầu dòng những tính năng vừa deploy, phiên bản version hash nếu có).*
3. **👉 NEXT ACTION (BIP):**
   - Đề xuất test UI bằng tay.
   - Đề xuất câu caption cho anh sếp đăng post Build In Public (BIP) khoe thành quả. Càng kỹ thuật, càng tech-savvy càng tốt.

---

## 🛡️ Fallback khi Deploy Failed
- Mạng lỗi / Timeout -> Tự auto-retry 1 lần.
- Vercel/Netlify trả về Build Error -> Chạy tool `read_terminal` đọc log, tự sửa lỗi, tự deploy lại (loop max 2 lần). Không cần hỏi User nếu lỗi hiển nhiên. Khó quá thì dùng `notify_user`.
