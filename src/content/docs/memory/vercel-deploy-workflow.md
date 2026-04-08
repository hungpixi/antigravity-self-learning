---
name: Vercel Deploy Workflow
description: "Quy trình deploy static Vite site lên Vercel từ CLI — bao gồm gotchas về VERCEL_TOKEN, project linking, và dist folder reset."
type: feedback
---

## Vercel CLI Deploy — Bài học thực tế

### Vấn đề gặp phải:
1. **VERCEL_TOKEN env var cũ** ghi đè token mới từ `vercel login` → phải clear bằng `$env:VERCEL_TOKEN = ''`
2. **`npm run build` xóa thư mục `dist`** → mất `.vercel` config → phải link lại mỗi lần build
3. **`--name` flag deprecated** trong Vercel CLI mới → phải tạo project riêng bằng `vercel project add`
4. **Netlify MCP** không hỗ trợ rename site → Vercel CLI nhanh hơn cho static sites

### Workflow chuẩn:
```bash
# 1. Build
npm run build

# 2. Link (chỉ cần khi dist bị reset)
$env:VERCEL_TOKEN = ''
cd dist
npx -y vercel link --project <project-name> --yes

# 3. Deploy
npx -y vercel --prod --yes
```

**Why:** Tránh mất thời gian debug token/linking issues khi deploy.

**How to apply:** Mỗi lần deploy Vite project → luôn link lại sau build vì dist bị xóa.
