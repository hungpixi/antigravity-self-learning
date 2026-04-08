---
title: "architecture serverless youtube"
name: Serverless YouTube Bypass Architecture
description: Chiến lược xử lý khi bị YouTube chặn IP (Bot detection) tại Vercel/Cloudflare
type: project
---

Khi phát triển các luồng lấy link hoặc livestream YouTube từ hạ tầng Serverless (Vercel, AWS):

- **Rule/Fact**: IP datacenter/Serverless của Vercel mặc định bị YouTube gắn cờ bot (trả về lỗi "Sign in to confirm you're not a bot"). Điều này dẫn đến sự sụp đổ (HTTP 500) của mọi Request từ các thư viện NodeJS scraping (ytdl-core, play-dl, v.v) đang chạy qua API Route.

**Why:**
YouTube có module chống cào dữ liệu siết rất chặt traffic từ các ASN public datacenter. Thiếu Cookie xác thực, Vercel Server sẽ vĩnh viễn bị kẹt ngoài cổng Captcha proxy HTTP. Nếu cố dùng youtubei.js giả dạng Android/iOS thì vẫn dễ bị block.

**How to apply:**
1. **Ưu tiên Client-Side Architectures**: Nếu user đang report lỗi 500 liên tục không bắt được link youtube (như trên dự án YT SlideX), đổi thiết kế sang việc User trực tiếp sử dụng Local Upload (`<input type="file" />`). Kéo processing về `ffmpeg.wasm` hoặc xử lý trên thiết bị user (trực tiếp trình duyệt) - Tránh 100% Server Proxying Rate Limit. Bỏ qua hoàn toàn logic Proxy Server cồng kềnh.
2. **Sử Dụng External Bypass Proxies**: Nếu bắt buộc phải crawl URL, hãy request qua HTTPS tới những dự án chuyên dụng như endpoint API `cobalt.tools`, `Invidious Pipeline`, hạn chế trực tiếp gọi node `fetch` tới Youtube thông qua Vercel.
