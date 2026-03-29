# PostgreSQL Remote Latency Fix — Connection Pooling

## Vấn Đề
Khi dùng `psycopg2.connect()` cho mỗi request với PostgreSQL remote (VPS Nhật Bản):
- Mỗi request mở TCP connection mới → SSL handshake → DNS lookup
- Latency: **10-12 giây mỗi request** (bất kể query đơn giản đến đâu)
- Dashboard gần như unusable

## Root Cause
```python
# ❌ BAD — mỗi request tạo connection mới
def _get_conn(self):
    conn = psycopg2.connect(DATABASE_URL)  # 10s TCP handshake!
    return conn

def some_query(self):
    conn = self._get_conn()
    # ... query ...
    conn.close()  # Connection bị hủy, lần sau phải handshake lại
```

## Fix: Connection Pool
```python
from psycopg2 import pool

# ✅ GOOD — pool giữ connections sẵn
class DatabaseManager:
    def __init__(self):
        self._pool = pool.SimpleConnectionPool(
            minconn=2,  # Luôn giữ 2 connections sẵn
            maxconn=5,  # Tối đa 5 concurrent connections
            dsn=DATABASE_URL
        )

    def _get_conn(self):
        return self._pool.getconn()  # <1ms — lấy từ pool

    def _put_conn(self, conn):
        self._pool.putconn(conn)  # Trả về pool, không đóng

    def some_query(self):
        conn = self._get_conn()
        try:
            # ... query ...
            conn.commit()
        finally:
            self._put_conn(conn)  # ✅ Trả về pool
```

## Kết Quả
| Metric | Trước | Sau |
|--------|-------|-----|
| Latency/request | 10-12s | <100ms |
| Dashboard load | ~60s | <1s |

## Lưu Ý
- **QUAN TRỌNG**: Phải dùng `_put_conn()` thay vì `conn.close()` — nếu close thì connection bị hủy
- SQLite không cần pool (local file, fast), dùng `conn.close()` bình thường
- `SimpleConnectionPool` KHÔNG thread-safe — nếu dùng multi-threading, dùng `ThreadedConnectionPool`
- Pool size 2-5 phù hợp cho dev; production nên 5-20 tùy load
