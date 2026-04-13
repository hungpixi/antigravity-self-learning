import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional

class KnowledgeGraph:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database for symbols and self-learning patterns."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 1. Symbols Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS symbols (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                file_path TEXT,
                line INTEGER,
                end_line INTEGER,
                docstring TEXT,
                calls TEXT, -- Comma-separated list of function names
                last_indexed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # 2. Self-Learning Patterns (TIL, ADR, RCA)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT, -- 'TIL', 'ADR', 'RCA', 'PERF', 'SMELL'
                name TEXT,
                content TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            conn.commit()

    def update_symbol(self, symbol_data: Dict[str, Any]):
        """Upsert a symbol into the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Check if exists
            cursor.execute("SELECT id FROM symbols WHERE name = ? AND file_path = ?", 
                           (symbol_data['name'], symbol_data['file_path']))
            row = cursor.fetchone()
            
            if row:
                cursor.execute("""
                UPDATE symbols SET 
                    type = ?, line = ?, end_line = ?, docstring = ?, calls = ?, last_indexed = CURRENT_TIMESTAMP
                WHERE id = ?
                """, (symbol_data['type'], symbol_data['line'], symbol_data['end_line'], 
                      symbol_data.get('docstring'), ",".join(symbol_data.get('calls', [])), row[0]))
            else:
                cursor.execute("""
                INSERT INTO symbols (name, type, file_path, line, end_line, docstring, calls)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (symbol_data['name'], symbol_data['type'], symbol_data['file_path'], 
                      symbol_data['line'], symbol_data['end_line'], symbol_data.get('docstring'), 
                      ",".join(symbol_data.get('calls', []))))
            conn.commit()

    def query_symbol(self, query: str) -> List[Dict[str, Any]]:
        """Search for symbols by name or file path."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # fuzzy search
            cursor.execute("SELECT * FROM symbols WHERE name LIKE ? OR file_path LIKE ?", (f"%{query}%", f"%{query}%"))
            return [dict(row) for row in cursor.fetchall()]

    def add_pattern(self, pattern_type: str, name: str, content: str, tags: str = ""):
        """Add a self-learning pattern (TIL, ADR, etc.)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO patterns (type, name, content, tags)
            VALUES (?, ?, ?, ?)
            """, (pattern_type.upper(), name, content, tags))
            conn.commit()

    def query_patterns(self, query: str) -> List[Dict[str, Any]]:
        """Search for self-learning patterns."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patterns WHERE name LIKE ? OR content LIKE ? OR tags LIKE ?", 
                           (f"%{query}%", f"%{query}%", f"%{query}%"))
            return [dict(row) for row in cursor.fetchall()]
