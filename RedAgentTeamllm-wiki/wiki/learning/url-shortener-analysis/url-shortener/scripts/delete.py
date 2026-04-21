#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
URL Shortener - Delete a short URL

Usage:
    uv run scripts/delete.py <short_code>
    uv run scripts/delete.py <short_code> --confirm
"""

import argparse
import sqlite3
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()

DB_PATH = Path.home() / ".url-shortener" / "links.db"


def get_db_connection():
    """Get database connection."""
    if not DB_PATH.exists():
        console.print("[yellow]No database found.[/yellow]")
        sys.exit(1)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def delete_link(short_code: str, skip_confirm: bool = False):
    """Delete a short URL."""
    conn = get_db_connection()
    
    # Check if link exists
    link = conn.execute(
        "SELECT short_code, original_url, clicks FROM links WHERE short_code = ?",
        (short_code,)
    ).fetchone()
    
    if not link:
        console.print(f"[red]Link not found:[/red] {short_code}")
        conn.close()
        sys.exit(1)
    
    # Show link info
    console.print(Panel(
        f"[bold]Short Code:[/bold] {link['short_code']}\n"
        f"[bold]Original URL:[/bold] {link['original_url']}\n"
        f"[bold]Total Clicks:[/bold] {link['clicks']}",
        title="⚠️  About to Delete",
        border_style="yellow"
    ))
    
    # Confirm deletion
    if not skip_confirm:
        confirm = console.input("[bold red]Are you sure you want to delete this link? (y/N):[/bold red] ")
        if confirm.lower() != 'y':
            console.print("[yellow]Deletion cancelled.[/yellow]")
            conn.close()
            return
    
    # Delete click records first (foreign key)
    conn.execute("DELETE FROM clicks WHERE short_code = ?", (short_code,))
    
    # Delete link
    conn.execute("DELETE FROM links WHERE short_code = ?", (short_code,))
    conn.commit()
    conn.close()
    
    console.print(f"[green]✓ Link deleted successfully:[/green] {short_code}")


def main():
    parser = argparse.ArgumentParser(description="Delete a short URL")
    parser.add_argument("short_code", help="Short code to delete")
    parser.add_argument("--confirm", "-y", action="store_true", help="Skip confirmation prompt")
    
    args = parser.parse_args()
    
    delete_link(args.short_code, args.confirm)


if __name__ == "__main__":
    main()
