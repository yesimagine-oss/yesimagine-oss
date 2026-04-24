#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich", "pyperclip"]
# ///
"""
Clipboard Manager - Copy content to clipboard

Usage:
    uv run scripts/copy.py <id>
    uv run scripts/copy.py <id> --show
"""

import argparse
import sqlite3
import sys
from pathlib import Path

try:
    import pyperclip
except ImportError:
    print("Error: pyperclip not installed. Install with: pip install pyperclip")
    sys.exit(1)

from rich.console import Console
from rich.panel import Panel

console = Console()

DB_PATH = Path.home() / ".clipboard-manager" / "history.db"


def get_db_connection():
    """Get database connection."""
    if not DB_PATH.exists():
        console.print("[yellow]No clipboard history found.[/yellow]")
        sys.exit(1)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def copy_to_clipboard(item_id: int, show: bool = False):
    """Copy content to clipboard."""
    conn = get_db_connection()
    
    # Get item
    row = conn.execute(
        "SELECT * FROM clipboard_history WHERE id = ?",
        (item_id,)
    ).fetchone()
    
    if not row:
        console.print(f"[red]Item not found:[/red] {item_id}")
        conn.close()
        sys.exit(1)
    
    content = row["content"]
    
    # Copy to clipboard
    try:
        pyperclip.copy(content)
    except Exception as e:
        console.print(f"[red]Error copying to clipboard:[/red] {e}")
        conn.close()
        sys.exit(1)
    
    # Update copied count
    conn.execute("""
        UPDATE clipboard_history 
        SET copied_count = copied_count + 1, last_copied = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (item_id,))
    conn.commit()
    conn.close()
    
    # Display success
    if show:
        preview = content[:200] + "..." if len(content) > 200 else content
        console.print(Panel(
            f"[bold]ID:[/bold] {row['id']}\n"
            f"[bold]Content:[/bold]\n{preview}\n"
            f"[bold]Type:[/bold] {row['content_type']}",
            title="✓ Copied to Clipboard",
            border_style="green"
        ))
    else:
        console.print(f"[green]✓ Copied item {item_id} to clipboard[/green]")
        console.print(f"  [dim]Type: {row['content_type']} | Category: {row['category']}[/dim]")


def main():
    parser = argparse.ArgumentParser(description="Copy content to clipboard")
    parser.add_argument("id", type=int, help="Item ID to copy")
    parser.add_argument("--show", "-s", action="store_true", help="Show content after copying")
    
    args = parser.parse_args()
    
    copy_to_clipboard(args.id, args.show)


if __name__ == "__main__":
    main()
