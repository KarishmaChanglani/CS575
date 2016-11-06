import click

from backend import app


@app.cli.command()
@click.argument('path')
def get(path: str) -> None:
    print(bytes.decode(app.test_client().get(path).data))
