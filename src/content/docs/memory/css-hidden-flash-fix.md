---
title: "css-hidden-flash-fix"
name: CSS Hidden Element Flash Fix
description: "Fix element flash khi page load do .hidden chỉ dùng opacity 0 với transition — cần thêm visibility hidden."
type: feedback
---

## Vấn đề: Element flash trên page load

Khi dùng `opacity: 0` + `transition: opacity 0.8s` cho `.hidden` class, elements có thể flash lên trong vài frame đầu khi browser render page.

### Root cause:
- Browser render elements trước khi CSS fully apply
- `opacity: 0` + transition = browser có thể hiện element rồi mới fade out
- Elements có background color (red, blue) sẽ flash rõ

### Fix:
```css
/* BAD — flash on load */
.hidden { opacity: 0; pointer-events: none; }

/* GOOD — no flash */
.hidden { opacity: 0; pointer-events: none; visibility: hidden; }
```

Khi showScreen cần set lại visibility:
```js
function showScreen(screen) {
  screen.classList.remove('hidden');
  screen.style.visibility = 'visible';
}
```

**Why:** `visibility: hidden` ẩn element ngay lập tức, không cần chờ transition.

**How to apply:** Bất kì khi nào dùng opacity-based show/hide pattern, luôn thêm `visibility: hidden` vào class ẩn.
