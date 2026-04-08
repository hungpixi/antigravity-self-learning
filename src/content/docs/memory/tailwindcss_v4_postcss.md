---
title: "tailwindcss v4 postcss"
name: Tailwind CSS v4 PostCSS Error
description: Fix lỗi Vite/PostCSS khi dùng tailwindcss bản mới nhất (v4)
type: feedback
---
**Fact:** Khi cài Tailwind bằng lệnh `npm install -D tailwindcss postcss autoprefixer`, bản v4 không còn hỗ trợ khai báo `tailwindcss: {}` trực tiếp trong `postcss.config.js`. Lỗi hiển thị: `The PostCSS plugin has moved to a separate package...`

**Why:** Tailwind v4 đã tách riêng PostCSS plugin ra package `@tailwindcss/postcss`.

**How to apply:** 
1. `npm install -D @tailwindcss/postcss`
2. Đổi trong `postcss.config.js`: thay `tailwindcss: {}` bằng `'@tailwindcss/postcss': {}`. Hoặc xài thẳng plugin `@tailwindcss/vite` trong `vite.config.ts`.
