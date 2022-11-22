"""Test intensive brew CLI."""

from typer.testing import CliRunner

from intensive_brew.cli import app

runner = CliRunner()


def test_help() -> None:
    """Test that the --help command works as expected."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
