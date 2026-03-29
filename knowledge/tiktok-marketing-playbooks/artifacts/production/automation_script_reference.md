# Automation Script Reference — Slides & Templates

Tài liệu này tổng hợp logic code Python sử dụng thư viện `Pillow` để tự động hóa quy trình sản xuất content dạng Carousel cho TikTok.

## 1. Logic Generate Slides (Text Overlay)

Sử dụng khi đã có nội dung văn bản (SOP) và muốn xuất file hàng loạt để đăng ngay.

### Key Logic:
- **Chuẩn bị Background:** Resize, Crop (1080x1350), Blur nhẹ (GaussianBlur) và Darken để làm nổi bật text.
- **Vẽ Text:**
  - Sử dụng `draw.text` với bóng (shadow) để text dễ đọc trên nền ảnh.
  - Phân chia Slide Type (Hook, Key, Save, CTA) để tự động chọn font size và màu sắc (Trắng/Vàng Gold).
- **Phụ kiện Visual:** Vẽ đường accent (accent line) màu vàng và watermark thương hiệu ở mỗi slide.

### Code Snippet (Core Function):
```python
def create_slide(slide_data, bg_img):
    img = bg_img.copy()
    draw = ImageDraw.Draw(img)
    # 1. Vẽ Watermark & Slide Number
    # 2. Tính toán Box Text để căn giữa (Center Alignment)
    # 3. Vẽ Main Text (Headline) - Màu sắc tùy vào slide_type
    # 4. Vẽ Accent Line (Gold) & Subtitle
    # 5. Thêm Border Frame mỏng quanh ảnh
    return img.convert('RGB')
```

## 2. Logic Generate Templates (Clean Templates — Portable Skill)

Sử dụng khi muốn tạo ra bộ khung (templates) sạch. Script đã được chuyển đổi thành **Portable Skill** tại thư mục `~/.gemini/antigravity/skills/tiktok-carousel/` để có thể chạy linh hoạt ở bất kỳ đâu.

### 2.1 Cấu hình Standard (Argparse):
Script hiện hỗ trợ các tham số dòng lệnh (`argparse`) để tự động hóa:
- `-i, --input`: Thư mục chứa ảnh gốc (tự động quét `.jpg`, `.png`).
- `-o, --output`: Thư mục xuất template (mặc định `./TikTok_Templates`).
- `-b, --blur`: Độ mờ (mặc định **2**).
- `-l, --light`: Độ sáng (mặc định **0.40**).

### 2.2 Quy chuẩn Medium (User Approved):
Quy trình áp dụng các bộ lọc sau để đảm bảo thẩm mỹ đồng nhất:
- **Brightness (0.40):** Tối ưu hóa độ tương phản cho text trắng/vàng.
- **GaussianBlur (2.0):** Làm dịu chi tiết nền, tăng sự tập trung vào nội dung chữ.
- **Gradient & Border:** Thêm Gradient Top/Bottom và viền Gold mảnh (35 opacity).

### 2.3 Cách thực thi linh hoạt:
AI Agent hoặc người dùng có thể gọi script từ bất kỳ đâu:
```bash
python generate_templates.py -i <path_to_images> -o <path_to_output>
```

## 3. Pure Gradient Bonus
Khi không muốn dùng ảnh minh họa, các bộ code màu Gradient tối (Navy, Warm, Teal, Purple) kết hợp với viền Gold là phương án an toàn và thanh lịch cho các slide chứa nhiều giá trị cốt lõi. Script tự động tạo các bản này dưới tên `template_pure_{color}.jpg`.
