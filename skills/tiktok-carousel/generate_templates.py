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
        print(f"   ✅ {filename}")

def main():
    parser = argparse.ArgumentParser(description="Tạo template TikTok Carousel (Dark Cinematic)")
    parser.add_argument('-i', '--input', help="Thư mục chứa ảnh gốc (Mặc định: Tự tìm ảnh trong thư mục hiện tại)", default=os.getcwd())
    parser.add_argument('-o', '--output', help="Thư mục xuất ảnh (Mặc định: ./TikTok_Templates)", default=os.path.join(os.getcwd(), 'TikTok_Templates'))
    parser.add_argument('-b', '--blur', type=int, help="Độ mờ", default=2)
    parser.add_argument('-l', '--light', type=float, help="Độ sáng", default=0.40)
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    print("🎨 Tạo template khung nền TikTok Carousel...")
    print(f"📂 Thư mục chứa ảnh: {args.input}")
    print(f"📂 Output lưu tại: {args.output}\n")

    # Tìm các file ảnh trong input dir
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        image_files.extend(glob.glob(os.path.join(args.input, ext)))
    
    # Loại trừ các file đã nằm trong thư mục output
    image_files = [f for f in image_files if args.output not in f]

    if not image_files:
        print("⚠️ Không tìm thấy ảnh nền (.jpg, .png) trong thư mục này.")
        print("💡 Gợi ý: Truyền đường dẫn thư mục ảnh bằng lệnh: python generate_templates.py -i <thư_mục_ảnh>")
    else:
        for index, bg_path in enumerate(image_files, 1):
            name = os.path.splitext(os.path.basename(bg_path))[0]
            print(f"\n📌 Frame {index}: {name}")
            try:
                img = create_template(bg_path, blur=args.blur, brightness=args.light)
                filename = f"template_{index}_{name}.jpg"
                filepath = os.path.join(args.output, filename)
                img.save(filepath, 'JPEG', quality=95)
                print(f"   ✅ {filename}")
            except Exception as e:
                print(f"   ❌ Lỗi xử lý ảnh {name}: {e}")

    print(f"\n📌 Bonus: Pure Dark Gradients (Không cần ảnh gốc)")
    create_pure_gradients(args.output)
    
    print(f"\n🎉 HOÀN THÀNH template tại: {args.output}")

if __name__ == "__main__":
    main()
