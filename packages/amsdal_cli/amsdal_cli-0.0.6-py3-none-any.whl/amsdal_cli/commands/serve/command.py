from pathlib import Path

import typer

from amsdal_cli.app import app
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.serve.services.supervisor import Supervisor
from amsdal_cli.commands.serve.utils import cleanup_app
from amsdal_cli.utils.cli_config import CliConfig


@app.command(name='serve')
def serve_command(
    ctx: typer.Context,
    *,
    cleanup: bool = typer.Option(
        False,
        help='Cleanup the generated models, warehouse and files after stopping',
    ),
    config: Path = typer.Option(None, help='Path to custom config.yml file'),  # noqa: B008
    host: str = typer.Option('0.0.0.0', help='Host to run the server on'),  # noqa: S104
    port: int = typer.Option(8000, help='Port to run the server on'),
) -> None:
    """
    Build the app and generate the models and other files.
    """
    cli_config: CliConfig = ctx.meta['config']
    app_source_path = cli_config.app_directory / SOURCES_DIR
    supervisor = Supervisor(
        app_source_path=app_source_path,
        output_path=cli_config.app_directory,
        config_path=config or cli_config.config_path,
        host=host,
        port=port,
    )
    try:
        supervisor.run()
    finally:
        supervisor.wait()

        if cleanup:
            cleanup_app(output_path=cli_config.app_directory)
