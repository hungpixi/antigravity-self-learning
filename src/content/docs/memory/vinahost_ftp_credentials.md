---
name: Vinahost FTP Credentials
description: Thông tin đăng nhập cPanel/FTP domain phamphunguyenhung.com tại Vinahost
type: reference
---
**Fact:**
- Host: `phamphunguyenhung.com` hoặc `vdc-whm-cheaphosting-1112.vinahost.org`
- Username: `ybatkukh`
- Password: `O4!cc7i86IuE!Y`
- Nameservers: `ns1.vinahost.vn`, `ns2.vinahost.vn`

**How to apply:**
- Khi cần deploy các project web/blog lên domain này, sẽ gọi FTP qua Python script/ftplib.
- **Tuân thủ Zero-Trust:** Khi code script deploy tự động thực tế, thông tin password này sẽ chỉ được nạp từ file `.env` cục bộ (đã được đưa vào thư mục `.gitignore`), tuyệt đối không hardcode thẳng vào script `deploy.py` để tránh rủi ro bảo mật nếu push lên GitHub.
