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
        click.echo(f"   {status_icon} #{entry['id']} [{entry['created_at']}] {entry['message']}")
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
        
    click.echo("No entry found")

# ── COMMAND 4: summary ─────────────────────────────────────────
@cli.command()
@click.option("--date",default=None,help="Date to summarise (YYYY-MM-DD). Defaults to today")
def summary(date):
    """Show a summary of your work for a given day"""
    entries = load_data()

    target_date = date if date else datetime.now().strftime("%d/%m/%Y")

    target_entries = [
        e for e in entries
        if e['created_at'].startswith(target_date)

    ]

    if not target_entries:
        click.echo(f"No entries found in {target_date}.")   #May have a problem
        return
    
    total = len(target_entries)
    completed = [e for e in target_entries if e['status']=="done"]
    pending = [e for e in target_entries if e['status']=="pending"]
    done_count = len(completed)
    pct = int((done_count/total)*100)


    # ── Header ───────────────────────────────────────────────
    click.echo(f"\n── DevLog Summary: {target_date} ──────────────────")
    click.echo(f"  Total logged : {total}")
    click.echo(f"  Completed    : {done_count}")
    click.echo(f"  Pending      : {len(pending)}")
    click.echo(f"  Progress     : {pct}%  {'█' * (pct // 10)}{'░' * (10 - pct // 10)}")

     # ── Completed tasks ───────────────────────────────────────────
    if completed:
        click.echo("\n  ✔ Done:")
        for e in completed:
            click.echo(f"   #{e['id']}: {e['message']}")

     # ── Pending tasks ───────────────────────────────────────────
    if pending:
        click.echo("\n o Pending:")
        for e in pending:
            click.echo(f"   #{e['id']}: {e['message']}")

    click.echo("─────────────────────────────────────────────────────\n")


if __name__ == "__main__":
    cli()