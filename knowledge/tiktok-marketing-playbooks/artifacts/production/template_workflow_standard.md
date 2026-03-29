# Template Generation Standard — "Người Lười Chăm Chỉ"

Đây là quy chuẩn đã được tối ưu hóa cho việc sản xuất khung nền (templates) sạch cho kênh TikTok "Người Lười Chăm Chỉ", cho phép người dùng tự do thêm Text và Credit trên Canva/Photoshop.

## 1. Cấu hình "Gold Standard" (User Approved)
Sau quá trình thử nghiệm, cấu hình **Medium** được xác định là tối ưu nhất cho việc hiển thị nội dung:

| Tham số | Quy chuẩn Medium | Mục tiêu |
|---|---|---|
| **Độ sáng (Brightness)** | 0.40 | Giữ được chi tiết ảnh nền nhưng đủ tối để text trắng/vàng nổi bật. |
| **Độ mờ (Blur)** | 2.0 | Xử lý nhiễu của ảnh AI và tạo độ sâu trường ảnh giả lập. |
| **Kích thước** | 1080 x 1350 px | Tỷ lệ 4:5 chuẩn TikTok Carousel (ảnh lướt). |
| **Viền (Border)** | Margin 25px, Opacity 35 | Màu Vàng Gold (218, 185, 80) tạo khung sang trọng. |
| **Gradient Overlay** | Top 180α, Bottom 200α | Tối ở đầu/cuối để tập trung thị giác vào trung tâm. |

## 2. Quy trình Thực thi /tiktok-carousel (Full-Stack Agent Workflow)

Quy trình sản xuất được chia làm 2 chặng chính, kết hợp giữa tư duy văn chương và tự động hóa kỹ thuật:

### Chặng 1: Khai thác Ý tưởng & Viết Content (Phong cách Chuyên Văn)
Trước khi tạo Visual, AI Agent phải nặn ra kịch bản 7 Slide đạt chuẩn "Chuyên Văn":
1.  **Slide 1 (Hook):** Dùng sự thật tàn nhẫn hoặc triết lý (VD: "Có những người chết ở tuổi 25...").
2.  **Slide 2, 3 (Pain & Insight):** Đào sâu nỗi đau bằng ẩn dụ (VD: "Hành trình mộng du dưới ánh sáng xanh"). Thi vị hóa sự mệt mỏi để tạo sự đồng cảm sâu sắc.
3.  **Slide 4, 5 (The Shift & Solution):** Giới thiệu giải pháp (Hệ thống, AI Agents) như một sự cứu rỗi, một cách giải phóng bản ngã khỏi sự lặp lại vô hồ.
4.  **Slide 6, 7 (Vision & CTA):** Tầm nhìn về tự do tài chính/thời gian và lời mời gia nhập "Bộ lạc" tinh tế.

### Chặng 2: Sản xuất Visual (Template Khung Chữ)
Sau khi chốt Content, thực thực hiện tạo visual đồng bộ:
*   **Bước 1 (Sourcing):** Tìm kiếm/Generate ảnh nền theo mood của chữ (Dark Cinematic, Tech, Operator aesthetic).
*   **Bước 2 (Processing):** Chạy portable script `generate_templates.py` với cấu hình **Medium** (Blur 2, Brightness 0.40).
*   **Bước 3 (Delivery):** Giao bộ templates sạch cho user để chèn text theo kịch bản ở Chặng 1.

## 3. Các Palette Gradient Thuần (Bonus)
Trong trường hợp không dùng ảnh nền, sử dụng các dải màu Gradient tối sau:
- **Navy Deep:** `(10, 15, 25)` -> `(25, 30, 45)`
- **Warm Coffee:** `(15, 10, 10)` -> `(35, 20, 15)`
- **Teal Forest:** `(5, 15, 15)` -> `(15, 35, 30)`
- **Dark Amethyst:** `(10, 10, 15)` -> `(20, 18, 30)`
