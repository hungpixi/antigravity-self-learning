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

from antigravity_learn import __version__

app = typer.Typer(
    name="antigravity-learn",
    help="🧠 Self-learning system for AI coding assistants",
    no_args_is_help=True,
)
console = Console()

# Default Antigravity skills directory
DEFAULT_SKILLS_DIR = Path.home() / ".gemini" / "antigravity" / "skills"

# Skills bundled with this package
PACKAGE_DIR = Path(__file__).parent
SKILLS_SOURCE = PACKAGE_DIR.parent.parent / "skills"


def _get_skills_dir(target: Optional[str] = None) -> Path:
    """Resolve target skills directory."""
    if target:
        return Path(target)
    return DEFAULT_SKILLS_DIR


def _count_patterns(skill_path: Path) -> int:
    """Count pattern entries in a SKILL.md file."""
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return 0
    content = skill_file.read_text(encoding="utf-8", errors="replace")
    # Count ### headings that look like pattern entries
    count = 0
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("### ") and any(
            marker in stripped
            for marker in ["P", "RB-", "ADR-", "PP-", "CS-", "PERF-", "SA-"]
        ):
            count += 1
    return count


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
def version():
    """Show version."""
    console.print(f"antigravity-learn v{__version__}")


if __name__ == "__main__":
    app()
