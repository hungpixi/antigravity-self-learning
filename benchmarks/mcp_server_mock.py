import sqlite3
import json
import sys
import os

def main():
    # Only run if DB exists (it will be created by the Node setup)
    if not os.path.exists('mempalace_mock.db'):
        print(json.dumps({"error": "DB missing"}))
        return

    # 1. Kết nối SQLite trên ổ cứng (Cấu trúc thật của Mempalace)
    conn = sqlite3.connect('mempalace_mock.db')
    cursor = conn.cursor()
    
    # 2. Truy xuất 20 Node Memory
    try:
        cursor.execute('SELECT content FROM memory LIMIT 20')
        rows = cursor.fetchall()
    except Exception:
        rows = []

    # 3. Đóng gói chuẩn JSON-RPC của MCP gởi về qua đường STDIO
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "result": {
            "matches": rows,
            "architecture": "Python SQLite MCP Server"
        }
    }
    
    # Dump out qua stdout
    sys.stdout.write(json.dumps(payload))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
