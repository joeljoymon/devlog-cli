import click

@click.group()
def cli():
    """DevLog — your personal developer journal."""
    pass

@cli.command()
@click.argument("message")
def log(message):
    """Log a new entry."""
    click.echo(f"Logged: {message}")

if __name__ == "__main__":
    cli()