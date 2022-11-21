"""intensive brew CLI."""
import logging as log

import typer

from intensive_brew.sys_config.config import get_logging_level

log.basicConfig(level=get_logging_level(), force=True)

app = typer.Typer()


@app.command(name="validate-configuration")
def validate_configuration(config_file: str = typer.Option(..., "--configuration-file", "-f")) -> None:
    """Validate YAML configuration."""
    typer.echo(f"{config_file=}")
