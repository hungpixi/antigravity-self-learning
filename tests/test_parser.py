import pytest
from pathlib import Path
from antigravity_learn.brain.parser import CodebaseParser

def test_parse_simple_code(tmp_path):
    """Test parsing a simple Python file for symbols."""
    code = '''
def hello_world():
    """Greet the user."""
    print("Hello")

class MyClass:
    def method(self):
        hello_world()
'''
    file_path = tmp_path / "sample.py"
    file_path.write_text(code, encoding="utf-8")
    
    parser = CodebaseParser(tmp_path)
    parser.parse_file(file_path)
    
    # 1. Check function extraction
    func_key = "sample.py::hello_world"
    assert func_key in parser.symbols
    assert parser.symbols[func_key].name == "hello_world"
    assert parser.symbols[func_key].type == "function"
    assert parser.symbols[func_key].docstring == "Greet the user."
    
    # 2. Check class extraction
    class_key = "sample.py::MyClass"
    assert class_key in parser.symbols
    assert parser.symbols[class_key].type == "class"

    # 3. Check call extraction (basic)
    method_key = "sample.py::method"
    assert method_key in parser.symbols
    assert "hello_world" in parser.symbols[method_key].calls

def test_scan_ignoring_dirs(tmp_path):
    """Test that scan ignores .venv, __pycache__, and .git."""
    (tmp_path / ".venv").mkdir()
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "src").mkdir()
    
    (tmp_path / ".venv" / "lib.py").write_text("def hidden(): pass")
    (tmp_path / "src" / "main.py").write_text("def main(): pass")
    
    parser = CodebaseParser(tmp_path)
    parser.scan()
    
    assert any("main.py" in k for k in parser.symbols.keys())
    assert not any("hidden" in k for k in parser.symbols.keys())
