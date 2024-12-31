import typer

from src.containers.container import container

container.init_resources()
app = typer.Typer()
