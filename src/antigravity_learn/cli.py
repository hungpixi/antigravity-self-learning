# -*- coding: utf-8 -*-
"""
Antigravity Self-Learning CLI
Install, sync, and manage AI coding assistant skill files.
"""

import os
import shutil
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from antigravity_learn import __version__, KnowledgeGraph, CodebaseParser

app = typer.Typer(
    name="antigravity-learn",
    help="🧠 Self-learning system for AI coding assistants",
    no_args_is_help=True,
)
console = Console()

# Default Antigravity skills directory
DEFAULT_SKILLS_DIR = Path.home() / ".gemini" / "antigravity" / "skills"

# Local knowledge graph database
LOCAL_DB_DIR = Path(".antigravity")
LOCAL_DB_PATH = LOCAL_DB_DIR / "graph.db"

# Skills bundled with this package
PACKAGE_DIR = Path(__file__).parent
SKILLS_SOURCE = PACKAGE_DIR.parent.parent / "skills"

def _get_graph() -> KnowledgeGraph:
    """Initialize and return local knowledge graph."""
    LOCAL_DB_DIR.mkdir(exist_ok=True)
    return KnowledgeGraph(LOCAL_DB_PATH)

@app.command()
def index(
    root: str = typer.Option(".", "--root", "-r", help="Root directory to scan"),
    full: bool = typer.Option(False, "--full", "-f", help="Force full scan instead of incremental"),
):
    """🔍 Build/Update local knowledge graph (Smart & Incremental)."""
    root_path = Path(root)
    graph = _get_graph()
    parser = CodebaseParser(root_path)
    
    files_to_scan = None
    status_msg = "Scanning all files..."
    
    # Smart Detection: Use git to find modified files if not a full scan
    if not full and (root_path / ".git").exists():
        try:
            import subprocess
            # Get modified and untracked files
            git_out = subprocess.check_output(
                ["git", "status", "--porcelain"], 
                cwd=root_path, text=True
            )
            files_to_scan = []
            for line in git_out.splitlines():
                if line.endswith(".py"):
                    # Extract path (line format: ' M path/to/file.py' or '?? path/to/file.py')
                    rel_path = line[3:].strip()
                    files_to_scan.append(root_path / rel_path)
            
            if files_to_scan:
                status_msg = f"Incremental scan: {len(files_to_scan)} files changed."
            else:
                console.print("[blue]ℹ️  No changes detected in Git. Use --full to force re-index.[/blue]")
                return
        except Exception:
            pass # Fallback to full scan if git fails
            
    with console.status(f"[bold green]{status_msg}"):
        parser.scan(files=files_to_scan)
        
        indexed_count = 0
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
            indexed_count += 1
            
    console.print(Panel(
        f"✅ Indexed [bold]{indexed_count}[/bold] symbols from {len(files_to_scan) if files_to_scan else 'all'} files.\n"
        f"📁 Database: {LOCAL_DB_PATH}",
        title="🧠 Smart Indexing Complete",
        border_style="green",
    ))

@app.command()
def ask_brain(
    query: str = typer.Argument(..., help="What problem are you trying to solve?"),
):
    """🧠 Ask the brain for past solutions, bug fixes, or architectural choices."""
    graph = _get_graph()
    results = graph.query_patterns(query)
    
    if not results:
        console.print(f"[yellow]Brain has no memory of '{query}'. Recording a new TIL might help later.[/yellow]")
        return

    console.print(Panel(f"🧠 Searching brain for: [bold cyan]{query}[/bold cyan]", border_style="blue"))
    
    for r in results:
        color = "green" if r['type'] == "TIL" else "magenta" if r['type'] == "ADR" else "red"
        title = f"[{r['type']}] {r['name']}"
        
        content = r['content']
        if r['tags']:
            content += f"\n\n[dim]Tags: {r['tags']}[/dim]"
            
        console.print(Panel(content, title=title, border_style=color))

@app.command()
def query(
    q: str = typer.Argument(..., help="Search query (symbol name, file path, or pattern)"),
    type: Optional[str] = typer.Option(None, "--type", "-t", help="Search type (symbol or pattern)"),
):
    """🔎 Query the knowledge graph for symbols or learned patterns."""
    graph = _get_graph()
    
    results = []
    if type == "symbol" or not type:
        results.extend(graph.query_symbol(q))
    if type == "pattern" or not type:
        results.extend(graph.query_patterns(q))
        
    if not results:
        console.print(f"[yellow]No results found for '{q}'[/yellow]")
        return

    table = Table(title=f"🔎 Search Results for '{q}'")
    table.add_column("Type", style="cyan")
    table.add_column("Name", style="bold green")
    table.add_column("Location/Meta", style="dim")
    
    for r in results:
        if 'file_path' in r: # Symbol
            loc = f"{r['file_path']}:{r['line']}"
            table.add_row(r['type'].upper(), r['name'], loc)
        else: # Pattern
            table.add_row(f"LEARNED:{r['type']}", r['name'], r['tags'] or "—")
            
    console.print(table)
    
    # If exactly one result, show details
    if len(results) == 1:
        r = results[0]
        if 'docstring' in r and r['docstring']:
            console.print(Panel(r['docstring'], title="Docstring", border_style="blue"))
        if 'content' in r and r['content']:
            console.print(Panel(r['content'], title="Content", border_style="magenta"))

@app.command()
def learn(
    pattern_type: str = typer.Argument(..., help="Pattern type (TIL, ADR, RCA, PERF, SMELL)"),
    name: str = typer.Argument(..., help="Brief title of the pattern"),
    content: str = typer.Option(..., "--content", "-c", help="Full description of the pattern"),
    tags: str = typer.Option("", "--tags", help="Comma-separated tags"),
):
    """🧠 Record a new self-learned pattern to the local graph."""
    graph = _get_graph()
    graph.add_pattern(pattern_type, name, content, tags)
    
    # Also sync to Markdown skills if possible
    # (Future: implement auto-markdown-sync)
    
    console.print(f"[green]✅ Learned new {pattern_type}: [bold]{name}[/bold][/green]")

@app.command()
def install(
    target: Optional[str] = typer.Option(
        None, "--target", "-t", help="Custom target directory (default: ~/.gemini/antigravity/skills/)"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing skill files"
    ),
):
    """📦 Install skill files to Antigravity IDE."""
    skills_dir = _get_skills_dir(target)
    skills_dir.mkdir(parents=True, exist_ok=True)

    if not SKILLS_SOURCE.exists():
        console.print("[red]❌ Skills source not found. Package may be corrupted.[/red]")
        raise typer.Exit(1)

    installed = 0
    skipped = 0
    for skill_folder in sorted(SKILLS_SOURCE.iterdir()):
        if not skill_folder.is_dir() or skill_folder.name.startswith("."):
            continue
        dest = skills_dir / skill_folder.name
        if dest.exists() and not force:
            skipped += 1
            console.print(f"  ⏭️  {skill_folder.name} (exists, use --force to overwrite)")
            continue
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(skill_folder, dest)
        installed += 1
        console.print(f"  ✅ {skill_folder.name}")

    console.print()
    console.print(Panel(
        f"[green]Installed: {installed}[/green] | Skipped: {skipped}\n"
        f"📁 Target: {skills_dir}",
        title="🧠 Antigravity Self-Learning",
        border_style="green",
    ))


@app.command()
def sync(
    target: Optional[str] = typer.Option(
        None, "--target", "-t", help="Custom target directory"
    ),
):
    """🔄 Sync skills — update existing, add new, keep custom entries."""
    skills_dir = _get_skills_dir(target)
    if not skills_dir.exists():
        console.print("[yellow]⚠️  Skills dir not found. Running install instead...[/yellow]")
        install(target=target, force=False)
        return

    if not SKILLS_SOURCE.exists():
        console.print("[red]❌ Skills source not found.[/red]")
        raise typer.Exit(1)

    updated = 0
    added = 0
    for skill_folder in sorted(SKILLS_SOURCE.iterdir()):
        if not skill_folder.is_dir() or skill_folder.name.startswith("."):
            continue
        dest = skills_dir / skill_folder.name
        if dest.exists():
            # Replace with latest version
            shutil.rmtree(dest)
            shutil.copytree(skill_folder, dest)
            updated += 1
            console.print(f"  🔄 {skill_folder.name} (updated)")
        else:
            shutil.copytree(skill_folder, dest)
            added += 1
            console.print(f"  ✨ {skill_folder.name} (new)")

    console.print()
    console.print(Panel(
        f"[blue]Updated: {updated}[/blue] | [green]Added: {added}[/green]\n"
        f"📁 Target: {skills_dir}",
        title="🔄 Sync Complete",
        border_style="blue",
    ))


@app.command()
def status(
    target: Optional[str] = typer.Option(
        None, "--target", "-t", help="Custom target directory"
    ),
):
    """📊 Show installed skill file stats."""
    skills_dir = _get_skills_dir(target)
    if not skills_dir.exists():
        console.print("[yellow]⚠️  No skills installed. Run: antigravity-learn install[/yellow]")
        raise typer.Exit(1)

    table = Table(title="🧠 Antigravity Self-Learning — Status")
    table.add_column("Skill", style="cyan", no_wrap=True)
    table.add_column("Entries", justify="right", style="green")
    table.add_column("Size", justify="right", style="dim")
    table.add_column("Status", style="bold")

    total_patterns = 0
    for skill_folder in sorted(skills_dir.iterdir()):
        if not skill_folder.is_dir() or skill_folder.name.startswith("."):
            continue
        skill_file = skill_folder / "SKILL.md"
        if not skill_file.exists():
            continue

        count = _count_patterns(skill_folder)
        total_patterns += count
        size = skill_file.stat().st_size
        size_str = f"{size / 1024:.1f} KB" if size > 1024 else f"{size} B"

        table.add_row(
            skill_folder.name,
            str(count) if count > 0 else "—",
            size_str,
            "✅ Active",
        )

    console.print(table)
    console.print(f"\n📊 Total: [bold green]{total_patterns}[/bold green] patterns across all skills")
    console.print(f"📁 Location: {skills_dir}")


@app.command()
def export(
    output: str = typer.Option(
        "antigravity-skills-export.md", "--output", "-o", help="Output file path"
    ),
    target: Optional[str] = typer.Option(
        None, "--target", "-t", help="Custom skills directory"
    ),
):
    """📤 Export all patterns to a single markdown file."""
    skills_dir = _get_skills_dir(target)
    if not skills_dir.exists():
        console.print("[yellow]⚠️  No skills installed.[/yellow]")
        raise typer.Exit(1)

    lines = [
        "# 🧠 Antigravity Self-Learning — Full Export\n",
        f"> Generated by antigravity-learn v{__version__}\n",
        "---\n",
    ]

    for skill_folder in sorted(skills_dir.iterdir()):
        if not skill_folder.is_dir() or skill_folder.name.startswith("."):
            continue
        skill_file = skill_folder / "SKILL.md"
        if not skill_file.exists():
            continue

        content = skill_file.read_text(encoding="utf-8", errors="replace")
        # Skip YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2]

        lines.append(f"\n## 📁 {skill_folder.name}\n")
        lines.append(content)
        lines.append("\n---\n")

    output_path = Path(output)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    console.print(f"[green]✅ Exported to: {output_path.absolute()}[/green]")


@app.command()
def skeleton(
    root: str = typer.Option(".", "--root", "-r", help="Root directory"),
):
    """🦴 Show codebase skeleton (signatures only) to minimize prompt tokens."""
    graph = _get_graph()
    # Fuzzy search for everything to get all symbols
    results = graph.query_symbol("")
    
    if not results:
        console.print("[yellow]No symbols indexed. Run: antigravity-learn index --full[/yellow]")
        return

    # Group by file
    files: Dict[str, List[Dict[str, Any]]] = {}
    for r in results:
        files.setdefault(r['file_path'], []).append(r)
        
    output = ["# 🦴 Codebase Skeleton\n"]
    for file_path, symbols in sorted(files.items()):
        output.append(f"## 📄 {file_path}")
        for s in sorted(symbols, key=lambda x: x['line']):
            indent = "  " if s['type'] == "method" else ""
            sig = s['signature'] or f"{s['type']} {s['name']}"
            output.append(f"{indent}{sig}:")
            if s['docstring']:
                # Shorten docstring to first line
                doc = s['docstring'].splitlines()[0].strip()
                output.append(f"{indent}    \"\"\"{doc}...\"\"\"")
        output.append("")
        
    console.print("\n".join(output))

@app.command()
def mcp():
    """🚀 Start the MCP server for Antigravity Self-Learning."""
    from antigravity_learn.mcp_server import mcp as server
    console.print("[bold blue]🚀 Starting Antigravity MCP Server...[/bold blue]")
    server.run()

@app.command()
def version():
    """Show version."""
    console.print(f"antigravity-learn v{__version__}")


if __name__ == "__main__":
    app()
