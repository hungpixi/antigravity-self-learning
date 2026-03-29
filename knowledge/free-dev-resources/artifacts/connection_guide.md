# Free Dev Resources — Hướng Dẫn Sử Dụng

## Quy Tắc
1. **KHÔNG đổi mật khẩu** — community dùng chung
2. **CHỈ cho dev/test** — không production, không data nhạy cảm
3. **Tạo DB riêng** cho mỗi project để tránh conflict

## Connection Strings

### PostgreSQL
```
postgres://codelung:dungthaydoimatkhau@163.44.96.79:5432/postgres
```

### MySQL
```
mysql://codelung:dungthaydoimatkhau@163.44.96.79:3306/default
```

### Redis
```
redis://codelung:dungthaydoimatkhau@163.44.96.79:6379
```

### MinIO S3
```
S3_ENDPOINT=https://minio.hoctuthien.com
S3_ACCESS_KEY=codelung
S3_SECRET_KEY=dungthaydoimatkhau
S3_CONSOLE=https://console.hoctuthien.com
```

## Web Tools
- **Drizzle Studio**: https://drizzle.hoctuthien.com (pass: dungthaydoimatkhau)
- **RedisInsight**: https://redisinsight.hoctuthien.com
- **Coolify**: https://coolify.buppou.com (Google login)
- **Affine**: https://affine.buppou.com

## Cách Dùng Trong Project Mới
1. Copy connection string vào `.env`
2. Tạo database riêng: `CREATE DATABASE ten_project;`
3. Thêm `context.md` vào `.gitignore` để không leak credentials
4. Dùng `context.md` trong project để lưu settings
