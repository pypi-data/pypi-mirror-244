import typer

from basic_sdk.cli.info.application import app as info

app = typer.Typer()

app.add_typer(info, name="info")

if __name__ == "__main__":
    app()
