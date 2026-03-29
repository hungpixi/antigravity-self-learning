---
name: Character Image Animation (Split & Animate)
description: "Tách ảnh PNG character thành bộ phận (head, body, wings...) rồi animate từng layer bằng Framer Motion hoặc Lottie image assets. Trigger khi cần animate character từ ảnh tĩnh, mascot animation, hoặc character rigging từ PNG/illustration."
---

# Character Image Animation — Split & Animate

> Biến 1 ảnh PNG tĩnh thành animation sống động bằng cách tách bộ phận + animate riêng.

## Khi nào dùng
- Có sẵn ảnh character/mascot PNG (illustration, AI-generated)
- Muốn animate cánh vỗ, mắt chớp, đầu gật, tay vẫy...
- Không có access vào Rive/Spine/After Effects

## Workflow

### Bước 1: Phân tích ảnh gốc
Xác định các bộ phận có thể tách & animate:
- **Đầu** (head) — gật, xoay, nghiêng
- **Thân** (body) — nhún, bob up/down
- **Cánh/tay trái** (left_wing/arm) — vỗ, vẫy
- **Cánh/tay phải** (right_wing/arm) — vỗ, vẫy
- **Mắt** (eyes) — chớp (scale Y → 0 → 100)
- **Mỏ/miệng** (beak/mouth) — mở/đóng
- **Đuôi** (tail) — lắc, xoay nhẹ
- **Phụ kiện** (hat, glasses, tie...) — theo chuyển động đầu/thân

### Bước 2: Tách ảnh bằng AI generate_image
Dùng `generate_image` tool với prompt pattern:

```
"Isolate ONLY the [BODY_PART] of this [CHARACTER_DESCRIPTION] on a fully transparent background. 
Keep EXACT same art style, colors, lighting. No other body parts visible. 
PNG with alpha transparency. [PART_SPECIFIC_DETAILS]"
```

Ví dụ cho con vẹt vàng:
- Head: "Isolate ONLY the head of this golden parrot character wearing a blue suit, on transparent background..."
- Body: "Isolate ONLY the torso/body (no head, no arms) of this golden parrot..."
- Left wing: "Isolate ONLY the left wing/arm..."

**Lưu files**: `public/animations/parts/[character]-[part].png`

### Bước 3: Tạo React component animate

#### Option A: Framer Motion (đơn giản hơn, recommend)

```tsx
"use client";
import { motion } from "framer-motion";
import Image from "next/image";

const PARTS = {
  body: { src: "/animations/parts/parrot-body.png", x: 0, y: 20, w: 120, h: 160 },
  head: { src: "/animations/parts/parrot-head.png", x: 10, y: -10, w: 80, h: 80 },
  wing_l: { src: "/animations/parts/parrot-wing-l.png", x: -30, y: 30, w: 50, h: 80 },
  wing_r: { src: "/animations/parts/parrot-wing-r.png", x: 70, y: 30, w: 50, h: 80 },
};

// Animation variants per state
const idleVariants = {
  body: { y: [0, -4, 0], transition: { duration: 2, repeat: Infinity, ease: "easeInOut" } },
  head: { y: [0, -6, 0], rotate: [0, 2, 0, -2, 0], transition: { duration: 2.5, repeat: Infinity } },
  wing_l: { rotate: [0, -8, 0], transition: { duration: 1.5, repeat: Infinity } },
  wing_r: { rotate: [0, 8, 0], transition: { duration: 1.5, repeat: Infinity } },
};

export function AnimatedCharacter({ state = "idle", size = 200 }) {
  const variants = state === "idle" ? idleVariants : /* other states */;
  const scale = size / 200;

  return (
    <div style={{ position: "relative", width: size, height: size * 1.2 }}>
      {Object.entries(PARTS).map(([key, part]) => (
        <motion.div
          key={key}
          animate={variants[key]}
          style={{
            position: "absolute",
            left: part.x * scale,
            top: part.y * scale,
            width: part.w * scale,
            height: part.h * scale,
            transformOrigin: key.includes("wing") ? "top center" : "center",
          }}
        >
          <Image src={part.src} alt={key} fill style={{ objectFit: "contain" }} />
        </motion.div>
      ))}
    </div>
  );
}
```

#### Option B: Lottie với image assets

```js
// Trong Lottie JSON, embed ảnh PNG dưới dạng base64
{
  "assets": [
    { "id": "body", "w": 200, "h": 300, "u": "/animations/parts/", "p": "parrot-body.png" },
    { "id": "head", "w": 150, "h": 150, "u": "/animations/parts/", "p": "parrot-head.png" }
  ],
  "layers": [
    {
      "ty": 2, // Image layer (NOT shape layer ty:4)
      "refId": "body",
      "ks": { /* animated transforms */ }
    }
  ]
}
```

### Bước 4: Thêm animation states

Mỗi state là 1 bộ variants khác nhau:

| State | Head | Body | Wings | Eyes | Tail |
|-------|------|------|-------|------|------|
| idle | bob nhẹ | bob nhẹ | vỗ chậm | chớp 1x/3s | lắc nhẹ |
| celebrate | ngẩng lên | nhảy lên | vỗ nhanh | mở to | vẫy nhanh |
| sleepy | cúi xuống | chìm dần | khép lại | nhắm | rũ xuống |  
| angry | rung lắc | rung | dang ra | nhíu | dựng đứng |
| thinking | nghiêng | xoay nhẹ | chắp tay | nhìn lên | cuộn |

### Bước 5: Transform origin cho từng phần

Quan trọng! Mỗi bộ phận cần đúng transform origin:
- **Cánh**: `transformOrigin: "top center"` (xoay từ vai)
- **Đầu**: `transformOrigin: "bottom center"` (xoay từ cổ)
- **Đuôi**: `transformOrigin: "top center"` (xoay từ gốc)
- **Mắt**: `transformOrigin: "center"` (scale từ giữa khi chớp)

## Tips
- Ảnh tách PHẢI có **transparent background** (alpha PNG)
- Overlap các phần 5-10px để không bị hở khi animate
- Test với `mix-blend-mode: multiply` nếu cần blend mượt
- Frame rate 30fps là đủ mượt cho web

## Tools cần
- `generate_image` (tách parts bằng AI)
- `sharp` hoặc Python PIL (crop/resize nếu cần)
- `framer-motion` hoặc `lottie-react`

## Example Projects
- VietFi Advisor: Vẹt Vàng mascot (5 levels, 10 animation states)
