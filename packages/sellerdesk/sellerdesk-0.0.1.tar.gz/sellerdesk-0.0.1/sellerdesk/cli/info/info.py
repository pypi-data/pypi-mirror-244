import time
from typing import Optional

import typer

app = typer.Typer()


@app.command
def info():
    ...


if __name__ == "__main__":
    app()
