# Portable Template Generator (TikTok Carousel)

Script Python sử dụng library Pillow để tự động hóa việc sản xuất khung nền TikTok Carousel (ảnh lướt). Được thiết kế để chạy linh hoạt ở bất kỳ đâu thông qua tham số dòng lệnh.

## 1. Cài đặt yêu cầu
```bash
pip install Pillow
```

## 2. Mã nguồn Script (`generate_templates.py`)

```python
import sys
import os
import argparse
import glob
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

CANVAS_W, CANVAS_H = 1080, 1350

def prepare_background(bg_path, blur_amount=2, brightness=0.40):
    bg = Image.open(bg_path).convert('RGBA')
    bg_ratio = max(CANVAS_W / bg.size[0], CANVAS_H / bg.size[1])
    new_size = (int(bg.size[0] * bg_ratio), int(bg.size[1] * bg_ratio))
    bg = bg.resize(new_size, Image.LANCZOS)
    left = (bg.size[0] - CANVAS_W) // 2
    top = (bg.size[1] - CANVAS_H) // 2
    bg = bg.crop((left, top, left + CANVAS_W, top + CANVAS_H))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_amount))
    enhancer = ImageEnhance.Brightness(bg)
    bg = enhancer.enhance(brightness)
    return bg

def add_gradient(img, top_alpha=180, bottom_alpha=200, mid_alpha=80):
    gradient = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)
    h = img.size[1]
    for y in range(h):
        ratio = y / h
        if ratio < 0.25:
            alpha = int(top_alpha * (1 - ratio * 4) + mid_alpha * (ratio * 4))
        elif ratio < 0.7:
            alpha = mid_alpha
        else:
            progress = (ratio - 0.7) / 0.3
            alpha = int(mid_alpha + (bottom_alpha - mid_alpha) * progress)
        draw.line([(0, y), (img.size[0], y)], fill=(0, 0, 0, alpha))
    return Image.alpha_composite(img.convert('RGBA'), gradient)

def add_subtle_border(img, margin=25, color=(218, 185, 80), opacity=35):
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle(
        [margin, margin, CANVAS_W - margin, CANVAS_H - margin],
        outline=(*color, opacity), width=1
    )
    return Image.alpha_composite(img.convert('RGBA'), overlay)

def create_template(bg_path, blur=2, brightness=0.40):
    bg = prepare_background(bg_path, blur_amount=blur, brightness=brightness)
    bg = add_gradient(bg)
    bg = add_subtle_border(bg)
    return bg.convert('RGB')

def create_pure_gradients(output_dir):
    dark_colors = [
        ((10, 15, 25), (25, 30, 45), "navy"),
        ((15, 10, 10), (35, 20, 15), "warm"),
        ((5, 15, 15), (15, 35, 30), "teal"),
        ((10, 10, 15), (20, 18, 30), "purple"),
    ]
    for base, accent, cname in dark_colors:
        img = Image.new('RGB', (CANVAS_W, CANVAS_H), base)
        draw = ImageDraw.Draw(img)
        for y in range(CANVAS_H):
            ratio = y / CANVAS_H
            r = int(base[0] + (accent[0] - base[0]) * ratio)
            g = int(base[1] + (accent[1] - base[1]) * ratio)
            b = int(base[2] + (accent[2] - base[2]) * ratio)
            draw.line([(0, y), (CANVAS_W, y)], fill=(r, g, b))
        img_rgba = img.convert('RGBA')
        img_rgba = add_subtle_border(img_rgba)
        img = img_rgba.convert('RGB')
        filename = f"template_pure_{cname}.jpg"
        filepath = os.path.join(output_dir, filename)
        img.save(filepath, 'JPEG', quality=95)

def main():
    parser = argparse.ArgumentParser(description="Tạo template TikTok Carousel (Dark Cinematic)")
    parser.add_argument('-i', '--input', help="Thư mục chứa ảnh gốc", default=os.getcwd())
    parser.add_argument('-o', '--output', help="Thư mục xuất ảnh", default=os.path.join(os.getcwd(), 'TikTok_Templates'))
    parser.add_argument('-b', '--blur', type=int, help="Độ mờ", default=2)
    parser.add_argument('-l', '--light', type=float, help="Độ sáng", default=0.40)
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        image_files.extend(glob.glob(os.path.join(args.input, ext)))
    
    image_files = [f for f in image_files if args.output not in f]

    for index, bg_path in enumerate(image_files, 1):
        name = os.path.splitext(os.path.basename(bg_path))[0]
        try:
            img = create_template(bg_path, blur=args.blur, brightness=args.light)
            filename = f"template_{index}_{name}.jpg"
            filepath = os.path.join(args.output, filename)
            img.save(filepath, 'JPEG', quality=95)
            print(f"✅ Created: {filename}")
        except Exception as e:
            print(f"❌ Error {name}: {e}")

    create_pure_gradients(args.output)
    print(f"🎉 Done! Templates saved at: {args.output}")

if __name__ == "__main__":
    main()
```

## 3. Cách sử dụng
Chạy script tại thư mục chứa ảnh:
```bash
python generate_templates.py
```
Hoặc chỉ định rõ thư mục:
```bash
python generate_templates.py -i ./my_photos -o ./output_folder -b 3 -l 0.35
```
