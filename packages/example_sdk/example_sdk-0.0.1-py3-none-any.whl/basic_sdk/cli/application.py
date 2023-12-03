import typer

from basic_sdk.cli.crm.application import app as crm

app = typer.Typer()

app.add_typer(crm, name="info")

if __name__ == "__main__":
    app()
