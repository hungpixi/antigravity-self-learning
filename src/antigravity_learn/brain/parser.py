import ast
from pathlib import Path
from typing import List, Dict, Any, Optional

class Symbol:
    def __init__(self, name: str, type: str, line: int, end_line: int, file_path: str, docstring: Optional[str] = None, signature: Optional[str] = None):
        self.name = name
        self.type = type  # 'function', 'class', 'method'
        self.line = line
        self.end_line = end_line
        self.file_path = file_path
        self.docstring = docstring
        self.signature = signature # e.g. "def func(a, b):"
        self.calls: List[str] = []
        self.callers: List[str] = []

class CodebaseParser:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.symbols: Dict[str, Symbol] = {}

    def parse_file(self, file_path: Path):
        """Parse a single Python file and extract symbols."""
        if not file_path.suffix == ".py":
            return

        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(content)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return

        relative_path = str(file_path.relative_to(self.root_dir))
        
        lines = content.splitlines()
        
        for node in ast.walk(tree):
            # Extract Functions
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Get signature (first line of definition)
                signature = lines[node.lineno - 1].strip()
                if signature.endswith(":"):
                    signature = signature[:-1]

                symbol = Symbol(
                    name=node.name,
                    type="function" if not self._is_method(node) else "method",
                    line=node.lineno,
                    end_line=getattr(node, "end_lineno", node.lineno),
                    file_path=relative_path,
                    docstring=ast.get_docstring(node),
                    signature=signature
                )
                
                # Simple call extraction (functions called within this function)
                for subnode in ast.walk(node):
                    if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Name):
                        symbol.calls.append(subnode.func.id)
                
                # Store by full name (simplification: just name for now)
                self.symbols[f"{relative_path}::{node.name}"] = symbol

            # Extract Classes
            elif isinstance(node, ast.ClassDef):
                signature = lines[node.lineno - 1].strip()
                if signature.endswith(":"):
                    signature = signature[:-1]

                symbol = Symbol(
                    name=node.name,
                    type="class",
                    line=node.lineno,
                    end_line=getattr(node, "end_lineno", node.lineno),
                    file_path=relative_path,
                    docstring=ast.get_docstring(node),
                    signature=signature
                )
                self.symbols[f"{relative_path}::{node.name}"] = symbol

    def _is_method(self, node: ast.AST) -> bool:
        """Check if node is a method (inside a class)."""
        # Simplification: we'd need more context during walk
        return False 

    def scan(self, files: Optional[List[Path]] = None):
        """Scan directory or a specific list of files."""
        if files:
            for path in files:
                if path.exists() and path.suffix == ".py":
                    self.parse_file(path)
            return

        for path in self.root_dir.rglob("*.py"):
            if ".venv" in str(path) or "__pycache__" in str(path) or ".git" in str(path):
                continue
            self.parse_file(path)

if __name__ == "__main__":
    parser = CodebaseParser(Path("."))
    parser.scan()
    for name, sym in parser.symbols.items():
        print(f"{sym.type.upper()}: {name} (L{sym.line}-{sym.end_line})")
        if sym.calls:
            print(f"  Calls: {', '.join(set(sym.calls))}")
