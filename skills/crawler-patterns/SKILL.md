---
name: Crawler & Scraping Architecture Patterns
description: 12 production patterns from MediaCrawler (24k+ stars). Covers Playwright CDP, anti-detection, async concurrency, multi-storage, proxy pools, and graceful shutdown. Auto-trigger khi build crawler, scraper, browser automation. Triggers on "crawler", "scraper", "playwright", "puppeteer", "selenium", "crawl", "scrape", "browser automation", "anti-detect", "headless", "CDP", "proxy pool", "stealth", "captcha".
---

# 🕷️ Crawler & Scraping Architecture Patterns

> Extracted from [NanmiCoder/MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) (24k+ ⭐, Python 3.11, Playwright)
> 📅 2026-03-19 — Audit by hungpixi

## Pattern Format

```
### CP-xxx: [Pattern Name]

> Source: [file/module]

**When**: [When to use this pattern]
**How**: [Code example]
**Why**: [Rationale]
```

---

## CP-001: Factory + ABC Multi-Platform Architecture

> Source: `main.py`, `base/base_crawler.py`

**When**: Building tool that supports multiple platforms/backends
**How**:
```python
from abc import ABC, abstractmethod

class AbstractCrawler(ABC):
    @abstractmethod
    async def start(self): pass
    
    @abstractmethod
    async def search(self): pass

class CrawlerFactory:
    CRAWLERS = {"xhs": XhsCrawler, "dy": DyCrawler, ...}
    
    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        cls = CrawlerFactory.CRAWLERS.get(platform)
        if not cls:
            raise ValueError(f"Unknown platform: {platform}")
        return cls()
```

**Why**: Thêm platform mới = thêm 1 class, KHÔNG sửa main.py. Open/Closed principle.

---

## CP-002: Playwright CDP Mode — Dùng Chrome Thật

> Source: `tools/cdp_browser.py`, `tools/browser_launcher.py`

**When**: Cần anti-detect tốt nhất, dùng real browser environment
**How**:
```python
class CDPBrowserManager:
    async def launch_and_connect(self, playwright, ...):
        browser_path = self._detect_browser()           # 1
        debug_port = self._find_available_port(9222)    # 2
        self._launch_subprocess(browser_path, port)     # 3
        self._register_cleanup_handlers()               # 4
        browser = await playwright.chromium.connect_over_cdp(
            f"ws://localhost:{debug_port}"              # 5
        )
        return browser.contexts[0]                      # 6
```

**Why**: Playwright built-in Chromium dễ bị detect. Chrome/Edge thật có real fingerprint, extensions, cookies.

---

## CP-003: Anti-Detection Stack

> Source: `libs/stealth.min.js`, `tools/browser_launcher.py`

**When**: Crawl sites có anti-bot (Cloudflare, reCAPTCHA, etc.)
**How**:
```python
# 1. Stealth JS injection
await browser_context.add_init_script(path="libs/stealth.min.js")

# 2. Browser launch args
args = [
    "--disable-blink-features=AutomationControlled",
    "--exclude-switches=enable-automation",
    "--disable-infobars",
]

# 3. Real user-agent + persistent context (keeps cookies)
context = await chromium.launch_persistent_context(
    user_data_dir="browser_data/xhs_user_data_dir",
    user_agent="Mozilla/5.0 (Macintosh; ...)"
)
```

**Why**: 3-layer defense: JS patches → browser flags → real user context.

---

## CP-004: Semaphore-Controlled Async Concurrency

> Source: `media_platform/xhs/core.py`

**When**: Crawl nhiều items nhưng cần rate limit
**How**:
```python
semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)  # e.g., 3

async def fetch_item(item_id, semaphore):
    async with semaphore:  # Only N concurrent
        result = await client.get_item(item_id)
        await asyncio.sleep(config.CRAWLER_MAX_SLEEP_SEC)  # Rate limit
        return result

tasks = [fetch_item(id, semaphore) for id in item_ids]
results = await asyncio.gather(*tasks)
```

**Why**: `asyncio.gather` không có concurrency limit. Semaphore = "N slots" pattern. Sleep = rate limit.

---

## CP-005: Graceful Shutdown with Timeout

> Source: `tools/app_runner.py`

**When**: Async app cần cleanup resources (browser, DB, files) khi exit
**How**:
```python
async def _runner():
    shutdown_requested = False
    
    def _on_signal(signum):
        nonlocal shutdown_requested
        if shutdown_requested:
            os._exit(130)  # Double Ctrl+C = force exit
        shutdown_requested = True
        runner_task.cancel()
    
    signal.signal(signal.SIGINT, lambda s, f: _on_signal(s))
    
    try:
        await app_main()
    except asyncio.CancelledError:
        pass
    finally:
        await asyncio.wait_for(cleanup(), timeout=15.0)  # BOUNDED
        # Cancel all remaining orphan tasks
        for t in asyncio.all_tasks():
            if t is not asyncio.current_task():
                t.cancel()
```

**Why**: Không timeout = cleanup treo mãi. Double Ctrl+C = escape hatch. Orphan task cancel = clean exit.

---

## CP-006: Proxy IP Pool with Auto-Refresh

> Source: `proxy/proxy_ip_pool.py`

**When**: Cần rotate IP để tránh ban
**How**:
```python
from tenacity import retry, stop_after_attempt, wait_fixed

class ProxyIpPool:
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def get_proxy(self) -> IpInfoModel:
        if len(self.proxy_list) == 0:
            await self._reload_proxies()  # Auto-refill
        proxy = random.choice(self.proxy_list)
        self.proxy_list.remove(proxy)  # Once used, remove
        return proxy
    
    async def get_or_refresh_proxy(self, buffer_seconds=30):
        if self.current_proxy.is_expired(buffer_seconds):
            return await self.get_proxy()  # Auto-refresh
        return self.current_proxy
```

**Why**: Pool tự refill + retry + expiry check. `get_or_refresh_proxy()` gọi trước mỗi request = always fresh.

---

## CP-007: Multi-Storage Factory (7 Backends)

> Source: `store/xhs/__init__.py`

**When**: Cần output data ra nhiều format
**How**:
```python
class StoreFactory:
    STORES = {
        "csv": CsvStore,
        "json": JsonStore,
        "jsonl": JsonlStore,
        "excel": ExcelStore,
        "sqlite": SqliteStore,
        "db": MysqlStore,       # MySQL
        "postgres": PostgresStore,
        "mongodb": MongoStore,
    }
    
    @staticmethod
    def create_store() -> AbstractStore:
        return StoreFactory.STORES[config.SAVE_DATA_OPTION]()
```

**Why**: 1 config var → switch toàn bộ storage backend. Thêm backend mới = thêm 1 class.

---

## CP-008: Cross-OS Browser Detection

> Source: `tools/browser_launcher.py`

**When**: Tool cần tìm Chrome/Edge trên mọi OS
**How**:
```python
def detect_browser_paths(self):
    if platform.system() == "Windows":
        paths = [
            os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe"),
        ]
    elif platform.system() == "Darwin":
        paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", ...]
    else:  # Linux
        paths = ["/usr/bin/google-chrome", "/snap/bin/chromium", ...]
    
    return [p for p in paths if os.path.isfile(p) and os.access(p, os.X_OK)]
```

**Why**: Không hardcode path. Detect tất cả variants (Chrome, Edge, Beta, Dev, Canary).

---

## CP-009: Slider CAPTCHA Auto-Solve (OpenCV)

> Source: `tools/slider_util.py`, `tools/easing.py`

**When**: Bypass slider verification
**How**:
```python
# 1. Download gap + background images
# 2. Edge detection (Canny)
slide = cv2.Canny(gap_img, 100, 200)
back = cv2.Canny(bg_img, 100, 200)

# 3. Template matching → find position
result = cv2.matchTemplate(back, slide, cv2.TM_CCOEFF_NORMED)
_, _, _, max_loc = cv2.minMaxLoc(result)
x_position = max_loc[0]

# 4. Human-like mouse movement (accelerate then decelerate)
def get_track(distance):
    mid = distance * 4/5  # Accelerate 80%, decelerate 20%
    # Physics: v = v0 + a*t, s = v0*t + 0.5*a*t²
```

**Why**: Constant speed = detected. Easing functions simulate human hand tremor.

---

## CP-010: ContextVar for Async-Safe Global State

> Source: `var.py`

**When**: Cần global state trong async code mà không race condition
**How**:
```python
from contextvars import ContextVar

crawler_type_var = ContextVar("crawler_type")  # "search" | "detail" | "creator"
source_keyword_var = ContextVar("source_keyword")  # Current search keyword

# Set in main flow:
crawler_type_var.set("search")

# Read anywhere (task-local, no race):
keyword = source_keyword_var.get()
```

**Why**: Global variables → race condition trong async. ContextVar = task-local storage.

---

## CP-011: Hybrid Browser+HTTP Architecture

> Source: `media_platform/xhs/core.py`, `media_platform/xhs/client.py`

**When**: Cần browser cho auth/signing nhưng HTTP cho speed
**How**:
```python
class XhsClient:
    def __init__(self, playwright_page, headers, proxy):
        self.playwright_page = playwright_page  # For JS execution
        self.headers = headers                  # Pre-extracted cookies
    
    async def get_note_by_id(self, note_id):
        # 1. Use Playwright page to execute JS signing
        sign = await self.playwright_page.evaluate("window._sign(...)")
        
        # 2. Use httpx for actual HTTP request (faster)
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers={**self.headers, "X-Sign": sign})
```

**Why**: Browser = slow but needed for JS crypto. HTTP = fast for data fetching. Hybrid = best of both.

---

## CP-012: uv-Based Project Setup

> Source: `pyproject.toml`, `.python-version`

**When**: Mọi Python project mới
**How**:
```toml
# pyproject.toml
[project]
requires-python = ">=3.11"
dependencies = [...]

# .python-version
3.11
```

```bash
uv sync               # Install everything (venv + deps)
uv run main.py        # Run with correct env
uv run playwright install  # Install tool deps
```

**Why**: `uv` = 10-100x faster than pip. Auto-manages Python version + venv. Reproducible via lock file.

---

## Quick Reference

| Pattern | Use When |
|---------|----------|
| CP-001 Factory+ABC | Multi-platform tools |
| CP-002 CDP Mode | Anti-detect critical |
| CP-003 Stealth Stack | Anti-bot sites |
| CP-004 Semaphore | Rate-limited concurrency |
| CP-005 Graceful Shutdown | Async apps with resources |
| CP-006 Proxy Pool | IP rotation needed |
| CP-007 Multi-Storage | Flexible output formats |
| CP-008 Browser Detect | Cross-OS browser tools |
| CP-009 Slider CAPTCHA | Auto bypass verification |
| CP-010 ContextVar | Async-safe global state |
| CP-011 Hybrid Browser+HTTP | Auth + speed |
| CP-012 uv Setup | Every new Python project |

<!-- PATTERN_APPEND_MARKER — AI append pattern mới TRƯỚC dòng này -->
