import pytest
from typer.testing import CliRunner
from antigravity_learn.cli import app

runner = CliRunner()

def test_cli_learn_command(tmp_path, monkeypatch):
    """Test the 'learn' CLI command."""
    # Point the local DB to the temp directory
    db_dir = tmp_path / ".antigravity"
    db_dir.mkdir()
    db_path = db_dir / "graph.db"
    
    # We need to monkeypatch the CLI's LOCAL_DB_PATH
    import antigravity_learn.cli as cli
    monkeypatch.setattr(cli, "LOCAL_DB_DIR", db_dir)
    monkeypatch.setattr(cli, "LOCAL_DB_PATH", db_path)
    
    # Execute learn command
    result = runner.invoke(app, ["learn", "TIL", "Test lesson", "--content", "This is a test lesson", "--tags", "test"])
    assert result.exit_code == 0
    assert "Learned new TIL: Test lesson" in result.stdout
    
    # Execute query command
    result = runner.invoke(app, ["query", "Test lesson", "--type", "pattern"])
    assert result.exit_code == 0
    assert "LEARNED:TIL" in result.stdout
    assert "This is a test lesson" in result.stdout

def test_cli_ask_brain(tmp_path, monkeypatch):
    """Test the 'ask-brain' CLI command."""
    db_dir = tmp_path / ".antigravity"
    db_dir.mkdir()
    db_path = db_dir / "graph.db"
    
    import antigravity_learn.cli as cli
    monkeypatch.setattr(cli, "LOCAL_DB_DIR", db_dir)
    monkeypatch.setattr(cli, "LOCAL_DB_PATH", db_path)
    
    # Seed data
    runner.invoke(app, ["learn", "TIL", "Python AST", "--content", "How to use AST", "--tags", "python"])
    
    # Ask brain
    result = runner.invoke(app, ["ask-brain", "Python"])
    assert result.exit_code == 0
    assert "[TIL] Python AST" in result.stdout
    assert "How to use AST" in result.stdout

def test_cli_ask_brain_not_found(tmp_path, monkeypatch):
    """Test 'ask-brain' when no results match."""
    db_dir = tmp_path / ".antigravity"
    db_dir.mkdir()
    
    import antigravity_learn.cli as cli
    monkeypatch.setattr(cli, "LOCAL_DB_DIR", db_dir)
    monkeypatch.setattr(cli, "LOCAL_DB_PATH", db_dir / "graph.db")
    
    result = runner.invoke(app, ["ask-brain", "Unknown"])
    assert result.exit_code == 0
    assert "Brain has no memory" in result.stdout
