from pathlib import Path
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP
from antigravity_learn import KnowledgeGraph, CodebaseParser

# Initialize FastMCP server
mcp = FastMCP("Antigravity Self-Learning")

def _get_graph() -> KnowledgeGraph:
    """Helper to get the local graph."""
    db_dir = Path(".antigravity")
    db_dir.mkdir(exist_ok=True)
    return KnowledgeGraph(db_dir / "graph.db")

@mcp.tool()
def index_codebase(root_dir: str = ".") -> str:
    """
    Scan the codebase and build/update the local knowledge graph (Grapuco-lite).
    This helps the AI understand the project structure and symbols.
    """
    root_path = Path(root_dir)
    graph = _get_graph()
    parser = CodebaseParser(root_path)
    parser.scan()
    
    count = 0
    for name, sym in parser.symbols.items():
        graph.update_symbol({
            "name": sym.name,
            "type": sym.type,
            "file_path": sym.file_path,
            "line": sym.line,
            "end_line": sym.end_line,
            "docstring": sym.docstring,
            "calls": sym.calls
        })
        count += 1
        
    return f"Successfully indexed {count} symbols into the local knowledge graph."

@mcp.tool()
def search_symbols(query: str) -> str:
    """
    Search for function or class definitions in the codebase (Grapuco-lite).
    Use this to find where a symbol is defined and its docstring.
    """
    graph = _get_graph()
    results = graph.query_symbol(query)
    
    if not results:
        return f"No symbols found matching '{query}'"
    
    output = []
    for r in results:
        output.append(f"[{r['type'].upper()}] {r['name']} at {r['file_path']}:{r['line']}")
        if r['docstring']:
            output.append(f"  Docstring: {r['docstring']}")
            
    return "\n".join(output)

@mcp.tool()
def record_learning(type: str, name: str, content: str, tags: str = "") -> str:
    """
    Record a new self-learned pattern (TIL, ADR, RCA, PERF, SMELL).
    This helps the AI remember bug fixes and architectural decisions.
    """
    graph = _get_graph()
    graph.add_pattern(type, name, content, tags)
    return f"Successfully recorded new {type}: {name}"

@mcp.tool()
def search_learned_patterns(query: str) -> str:
    """
    Search the local knowledge base for previously learned bug fixes or patterns.
    Use this to avoid repeating past mistakes.
    """
    graph = _get_graph()
    results = graph.query_patterns(query)
    
    if not results:
        return f"No patterns found matching '{query}'"
    
    output = []
    for r in results:
        output.append(f"--- {r['type']}: {r['name']} ---")
        output.append(r['content'])
        if r['tags']:
            output.append(f"Tags: {r['tags']}")
            
    return "\n\n".join(output)

if __name__ == "__main__":
    mcp.run()
