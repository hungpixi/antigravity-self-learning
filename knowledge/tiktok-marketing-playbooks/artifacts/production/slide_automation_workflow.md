# Slide Automation Workflow — TikTok Carousel (35 Slides)

Quy trình tự động hóa thay thế thao tác thủ công trên Canva, cho phép tạo ra hàng loạt slide (35 slides cho 5 chủ đề) trong thời gian ngắn (mục tiêu 1 giờ cho 2-3 carousel khi đã thông thạo).

## 1. Prerequisites (Yêu cầu kỹ thuật)
- **Library:** `Pillow` (PIL) cho việc vẽ chữ lên hình.
- **Backgrounds:** Sử dụng 5 nền dark cinematic được tạo từ `generate_image` (DALL-E).
- **Fonts:** Ưu tiên font tiếng Việt (Unicode) có độ dày (Bold) cao như **Montserrat, Inter, Segoe UI Bold hoặc Arial Bold**.

## 2. Tìm kiếm Font tiếng Việt (Windows Discovery Logic)
Dưới đây là đoạn code để xác định font Unicode sẵn có trên máy:
```python
import os, glob
font_dirs = [r'C:\Windows\Fonts']
viet_fonts = []
for d in font_dirs:
    for f in glob.glob(os.path.join(d, '*.ttf')):
        name = os.path.basename(f).lower()
        if any(k in name for k in ['arial', 'segoe', 'tahoma', 'times', 'verdana', 'calibri', 'roboto', 'inter', 'montserrat', 'bebas', 'oswald', 'poppins', 'nunito']):
            viet_fonts.append(f)
# Chọn Segoe UI Bold hoặc Arial Bold cho Text lớn (Headers)
```

## 3. Automation Script Logic (Python/Pillow)
Quy trình thực hiện trong script:
1.  **Load Background:** Mở 5 ảnh nền (1080x1350) đại diện cho 5 carousel.
2.  **Define Text Content:** Dữ liệu text cho 7 slide mỗi carousel từ SOP.
3.  **Overlay Text:**
    - Header: Chữ in hoa (ALL CAPS), font thick/bold (size 80-100), mầu trắng/vàng (#FFD700).
    - Content: Chữ thường (Sentence case), font regular (size 40-50).
    - Watermark: `@NgườiLườiChămChỉ` ở góc dưới.
4.  **Save:** Xuất 35 ảnh ra thư mục `output/`.

*Lưu ý: Phong cách này không yêu cầu AI diễn hề/lộ mặt (Faceless), sức mạnh nằm ở Text & Vibe.*
