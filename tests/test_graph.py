import pytest
from pathlib import Path
from antigravity_learn.brain.graph import KnowledgeGraph

@pytest.fixture
def graph(tmp_path):
    """Temporary graph database for testing."""
    db_path = tmp_path / "test_graph.db"
    return KnowledgeGraph(db_path)

def test_symbol_upsert(graph):
    """Test inserting and updating a symbol."""
    sym = {
        "name": "test_func",
        "type": "function",
        "file_path": "main.py",
        "line": 10,
        "end_line": 20,
        "docstring": "Initial doc",
        "calls": ["a", "b"]
    }
    
    # 1. Insert
    graph.update_symbol(sym)
    results = graph.query_symbol("test_func")
    assert len(results) == 1
    assert results[0]['docstring'] == "Initial doc"
    assert results[0]['calls'] == "a,b"
    
    # 2. Update (change docstring and calls)
    sym["docstring"] = "Updated doc"
    sym["calls"] = ["c"]
    graph.update_symbol(sym)
    
    results = graph.query_symbol("test_func")
    assert len(results) == 1
    assert results[0]['docstring'] == "Updated doc"
    assert results[0]['calls'] == "c"

def test_fuzzy_search(graph):
    """Test fuzzy search for symbols."""
    graph.update_symbol({"name": "process_data", "type": "function", "file_path": "p.py", "line": 1, "end_line": 1})
    graph.update_symbol({"name": "load_data", "type": "function", "file_path": "l.py", "line": 1, "end_line": 1})
    
    # Search for "data"
    results = graph.query_symbol("data")
    assert len(results) == 2
    
    # Search for "load"
    results = graph.query_symbol("load")
    assert len(results) == 1
    assert results[0]['name'] == "load_data"

def test_learning_patterns(graph):
    """Test adding and querying TIL/ADR patterns."""
    graph.add_pattern("TIL", "Async Python", "Content about async", "python,async")
    graph.add_pattern("ADR", "Use SQLite", "Content about sqlite", "db,arch")
    
    # 1. Search by name
    results = graph.query_patterns("Async")
    assert len(results) == 1
    assert results[0]['type'] == "TIL"
    assert results[0]['name'] == "Async Python"
    
    # 2. Search by tag
    results = graph.query_patterns("arch")
    assert len(results) == 1
    assert results[0]['type'] == "ADR"
    assert "sqlite" in results[0]['content']
