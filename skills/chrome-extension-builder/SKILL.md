---
name: Chrome Extension Pro-Builder (Manifest V3)
description: "Kỹ năng chuẩn chỉnh để thiết lập, thiết kế và phát triển Chrome Extension cho các mục đích tự động hóa mạng và workflow AI (Vượt qua Playwright/Puppeteer bot detection)."
---

# 🚀 Chrome Extension Pro-Builder

Đây là Playbook chuẩn để xây dựng Chrome Extension (Native in-browser) thay cho các giải pháp Automation bằng Playwright hoặc Selenium cổ điển. Native Chrome Extension tận dụng được Caching, Session/Cookies thực tế của User để vượt bảo mật (Cloudflare, Google Login).

**Trigger:** tự động trigger khi user nói về "làm extension", "tạo chrome extension", "chuyển tool thành extension".

## 1. 📂 Cấu trúc Thư Mục (Best Practice)
Một extension sạch sẽ nên có cấu trúc:
```text
extension-project/
├── manifest.json       # Trái tim của Extension
├── background.js       # Service worker chạy ngầm
├── sidepanel.html      # UI hiển thị bên phải (Modern approach)
├── sidepanel.css       # Style
├── js/
│   ├── sidepanel.js    # Logic cho giao diện
│   └── api.js          # Xử lý fetch calls (Ví dụ cho OpenRouter)
└── icons/              # Thư mục icon (TÙY CHỌN)
```

## 2. 📝 Nguyên tắc Vàng của `manifest.json`
- Bắt buộc phải là `"manifest_version": 3`.
- **LỖI KINH ĐIỂN:** ĐỪNG khai báo block `"icons": { ... }` nếu bạn CHƯA tạo file ảnh thực tế. Chrome sẽ báo lỗi `Failed to load extension`. Nếu làm nháp, hãy xóa cmn block `icons`.
- Quyền (Permissions) thông dụng:
  - `"sidePanel"`: Cho phép Extension mở bảng điều khiển bền vững kế bên tab đang duyệt.
  - `"activeTab"`: Cho phép đụng vào dữ liệu tab hiện tại một cách an toàn mà không bị Google vịn vì "xin quyền diện rộng".
  - `"scripting"`: Kết hợp `activeTab` để `chrome.scripting.executeScript()`.
  - `"storage"`: Để gọi `chrome.storage.local` (Lưu thông tin đăng nhập, API key, preferences).

Ví dụ một Manifest V3 chuẩn:
```json
{
  "manifest_version": 3,
  "name": "Super AI Extension",
  "version": "1.0.0",
  "description": "AI Sidepanel automation",
  "permissions": ["sidePanel", "storage", "activeTab", "scripting"],
  "host_permissions": ["https://openrouter.ai/*"],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_title": "Open Side Panel"
  }
}
```

## 3. 🖥 Tại sao lại là Side Panel thay vì Popup?
- **Vấn đề của Popup:** Khi người dùng click ra trang web, Popup sẽ mất và reset trạng thái. Không dùng để làm Workflow hoặc Chat AI dài hơi được.
- **Lợi ích Side Panel:** Nằm cứng bên phải/trái. Người dùng vừa chọn lọc content trên web vừa đẩy sang AI. Đăng ký bật với dòng lệnh gọn nhẹ trong `background.js`:
```javascript
chrome.action.onClicked.addListener((tab) => {
  chrome.sidePanel.open({ windowId: tab.windowId });
});
```

## 4. 🪝 Đọc Dữ Liệu Web Đang Mở (Context Extraction)
Để lấy dữ liệu web truyền cho LLM (System Prompt Context), đừng xin quyền `<all_urls>`, hãy dùng `chrome.scripting` truyền thẳng từ `background.js` hoặc `sidepanel.js`:

```javascript
// Function chạy trên content web
function extractPageInfo() {
  return document.body.innerText;
}

// Hàm tiêm script
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  if(tabs[0].url.startsWith("http")) {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: extractPageInfo
    }, (results) => {
      let pageText = results[0].result;
      console.log("Đã lấy được dữ liệu!");
    });
  }
});
```

## 5. 🔒 Lưu Trữ Dữ Liệu Nhạy Cảm (API Key)
Không lưu API Key trên biến môi trường (.env) trong Extension. Bắt User tự điền và lưu vào bộ nhớ cục bộ ảo của extension:
```javascript
// Save
chrome.storage.local.set({ myApiKey: "sk-or-v1-xxx" }, () => { ... });

// Get
chrome.storage.local.get(["myApiKey"], (res) => { console.log(res.myApiKey); });
```

## 6. 🎨 Pro-Max UI/UX (Aesthetics Guideline)
- Extension cho workflow BẮT BUỘC phải dùng `CSS Variables` cho màu sắc để dễ hỗ trợ Dark/Light mode.
- Trình bày dạng các Thẻ (Workflows) thay vì bắt user gõ tay (0-Logic Setup).
- Sử dụng Glassmorphism (độ trong suốt có opacity ở border) cho hộp chat.
- Tham khảo màu nền `--bg-color: #0f172a; --panel-bg: #1e293b;`.

## 7. Troubleshooting (Lỗi hay gặp)
- `Unchecked runtime.lastError`: Bạn không bắt `.catch()` từ một Promise của thư viện Chrome. Thường do người dùng chưa grant permissions.
- `Could not load icon ...`: Do khai báo trong Manifest mà quên mất chưa cho ảnh vào. Mở file JSON lên xóa các path không tồn tại! Tạm gác đồ họa thay vì làm code gãy.
- `Content Security Policy (CSP)` ban API Call: nhớ khai báo `host_permissions` nếu gọi API từ service worker.
- **[Bug Fix 03/04/2026] Service worker registration failed / Unexpected property: 'openPanelOnAction'**: Nguyên nhân là do có một số phiên bản Chrome không nhận diện được syntax `setPanelBehavior({ openPanelOnAction: true })` làm Service worker gãy ngay lúc load. -> Nhất quyết thay bằng cục Event Listener: `chrome.action.onClicked.addListener((tab) => { chrome.sidePanel.open({ windowId: tab.windowId }); });`
- **[Bug Fix 03/04/2026] Error: No active side panel for windowId**: Lỗi này xảy ra khi quên khai báo block `"side_panel": { "default_path": "sidepanel.html" }` bên trong `manifest.json`. Trình duyệt sẽ không biết lấy file HTML nào để nạp vào giao diện. Cách sửa: Chèn block `side_panel` vào manifest.

## 8. 🧠 Continuous Evolution & "Dream Mode"
Đây là cơ chế tự học (Self-learning) và mơ ("Dreaming" giống Claude Code):

**A. Trigger Tự Động Cập Nhật Skill (Fix Bug Loop):**
Mỗi khi phát hiện và fix xong một bug liên quan đến Chrome Extension (manifest, permission, content script injection, message passing):
1. **BẮT BUỘC** gọi tool cập nhật vào mục `7. Troubleshooting` của file này.
2. Form lưu: `[Bug Name]: [Nguyên nhân cốt lõi] -> [Cách fix]`.

**B. "Dream Mode" (Background Ideation):**
Sau khi hoàn thành phần Code/Cơ bản, AI phải TỰ ĐỘNG dành 5 giây (hoặc tạo một background artifact `DREAM_VISION.md`) để nghĩ về:
- Các Edge Case (Người dùng login nhiều tài khoản, rớt mạng).
- Cách extension này ăn sâu vào OS/Local File (ví dụ kết nối Native Messaging Host).
- Nâng cấp UI (Làm sao để nó giống mượt như macOS Spotlight / ChatGPT app).
AI sẽ chủ động đề xuất hoặc âm thầm lưu vào `docs/visions/` để User duyệt dần trong các buổi làm việc sau mà không cần User yêu cầu.
