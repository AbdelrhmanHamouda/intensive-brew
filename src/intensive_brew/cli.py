"""intensive brew CLI."""
import logging as log

import typer

from intensive_brew.core.yaml.validation import Validation
from intensive_brew.sys_config.config import get_logging_level

log.basicConfig(level=get_logging_level(), force=True)

app = typer.Typer()


@app.command(name="validate-configuration")
def validate_configuration(config_file: str = typer.Option(..., "--configuration-file", "-f")) -> None:
    """Validate YAML configuration."""
    configuration = Validation.validate(config_file)

    if configuration:
        typer.echo("Provided configuration is valid.")
    else:
        typer.echo("Provided configuration is invalid.", err=True)
        typer.Exit(code=1)


@app.command(name="generate")
def generate_custom_resource(
    config_file: str = typer.Option(..., "--configuration-file", "-f"), output_path: str = typer.Option(..., "--output", "-o")
) -> None:
    """Generate LocustTest custom resource from YAML configuration."""
    typer.echo(f"{config_file=}")
    typer.echo(f"{output_path=}")
