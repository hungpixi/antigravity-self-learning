---
title: "port registry"
name: port_registry
description: Central registry of ports used across development projects to avoid conflicts.
type: reference
---

# Danh Sách Cổng (Ports) Đã Dùng

Để tránh bị trùng lặp port sinh ra lỗi "Address already in use", đây là danh sách các port đã quy hoạch cho các dự án:

- **23333**: VieNeu-TTS (Self-hosted Voice Cloning Server)
- **7860**: Gradio/Gradio Web UI mặc định
- **3000**: Next.js / Vite development server (mặc định)
- **5432**: PostgreSQL (Database)
- **6379**: Redis (Cache)
- **3010**: yt-slide (Next.js Frontend)
- **8010**: yt-slide (FastAPI Backend)
- *Thêm các port đang dùng vào đây khi phát sinh...*

**Why:** Khi khởi động các service, AI hoặc người dùng sẽ biết trước port nào đang rảnh để bind.
**How to apply:** Trước khi tạo một service web, worker, api mới, hãy check và update file này. Nếu port đã bị lấy, hãy tăng index lên (vd: 3001, 23334).
