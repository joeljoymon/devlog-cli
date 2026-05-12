import click
import json
import os
from datetime import datetime

# Path to the file where all logs are saved
DATA_FILE = os.path.expanduser("~/.devlog.json")

def load_data():
    """Load existing logs from JSON file"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE,'r')as f:
        return json.load(f)
    
def save_data(entries):
    """Save logs back to the JSON file"""
    with open(DATA_FILE,"w")as f:
        json.dump(entries,f,indent=2)



@click.group()
def cli():
    """DevLog — your personal developer journal."""
    pass

# ── COMMAND 1: log ──────────────────────────────────────────
@cli.command()
@click.argument("message")
def log(message):
    """Log a new Task, or note"""
    entries = load_data()

    new_entry = {
        "id": len(entries) + 1,
        "message":message,
        "status":"pending",
        "created_at": datetime.now().strftime("%d/%m/%Y,%H:%M:%S")
    }

    entries.append(new_entry)
    save_data(entries)
    click.echo(f"✔ Logged #{new_entry['id']}: {message}")

# ── COMMAND 2: list ─────────────────────────────────────────
@cli.command(name="list")
def list_entries():
    """Show all logged Tasks."""
    entries = load_data()

    if not entries:
        click.echo("No entries yet. Use 'log' to add one.")
        return
    
    click.echo("\n-----Your Devlogs----------------------")
    for entry in entries:
        status_icon = "✔" if entry['status']=="done" else 'o'
        click.echo(f"  {status_icon} #{entry['id']} [{entry['created_at']}] {entry['message']}")
    click.echo("────────────────────────────────\n")


# ── COMMAND 3: done ─────────────────────────────────────────
@cli.command()
@click.argument("entry_id", type=int)
def done(entry_id):
    """Mark a task as Done by its ID."""
    entries = load_data()

    for entry in entries:
        if entry['id'] == entry_id:
            entry['status'] = "done"
            save_data(entries)
            click.echo(f"✔ Marked #{entry['id']} as done: {entry['message']}")
            return
        
    click.echo("No entry found with the given id")

if __name__ == "__main__":
    cli()