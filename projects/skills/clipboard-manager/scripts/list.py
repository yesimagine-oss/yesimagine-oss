#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
Clipboard Manager - List clipboard history

Usage:
    uv run scripts/list.py
    uv run scripts/list.py --limit 20
    uv run scripts/list.py --category links
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

DB_PATH = Path.home() / ".clipboard-manager" / "history.db"


def get_db_connection():
    """Get database connection."""
    if not DB_PATH.exists():
        console.print("[yellow]No clipboard history found. Save something first![/yellow]")
        sys.exit(0)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def list_history(limit: int = 20, category: str = None, detail: bool = False, item_id: int = None):
    """List clipboard history."""
    conn = get_db_connection()
    
    if item_id:
        # Get specific item
        row = conn.execute(
            "SELECT * FROM clipboard_history WHERE id = ?",
            (item_id,)
        ).fetchone()
        
        if not row:
            console.print(f"[red]Item not found:[/red] {item_id}")
            conn.close()
            return
        
        # Display detail panel
        content_preview = row["content"][:500] + "..." if len(row["content"]) > 500 else row["content"]
        
        console.print(Panel(
            f"[bold]ID:[/bold] {row['id']}\n"
            f"[bold]Content:[/bold]\n{content_preview}\n"
            f"[bold]Type:[/bold] {row['content_type']}\n"
            f"[bold]Category:[/bold] {row['category']}\n"
            f"[bold]Created:[/bold] {row['created_at']}\n"
            f"[bold]Copied:[/bold] {row['copied_count']} times",
            title="📋 Clipboard Item Details",
            border_style="blue"
        ))
        conn.close()
        return
    
    # Build query
    query = """
        SELECT id, content, content_type, category, created_at, copied_count
        FROM clipboard_history
    """
    params = []
    
    if category:
        query += " WHERE category = ?"
        params.append(category)
    
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    if not rows:
        if category:
            console.print(f"[yellow]No items in category:[/yellow] {category}")
        else:
            console.print("[yellow]No clipboard history found.[/yellow]")
        return
    
    # Display table
    table = Table(title=f"📋 Clipboard History ({len(rows)} items)", show_lines=True)
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Type", style="magenta", width=10)
    table.add_column("Category", style="blue", width=12)
    table.add_column("Preview", style="white")
    table.add_column("Copied", justify="right", style="green")
    table.add_column("Created", style="dim", width=19)
    
    for row in rows:
        preview = row["content"][:60].replace('\n', ' ')
        if len(row["content"]) > 60:
            preview += "..."
        
        table.add_row(
            str(row["id"]),
            row["content_type"],
            row["category"],
            preview,
            str(row["copied_count"]),
            str(row["created_at"])[:19]
        )
    
    console.print(table)
    
    # Summary
    total = conn.execute("SELECT COUNT(*) FROM clipboard_history").fetchone()[0]
    console.print(f"\n[dim]Total items in history: {total} | Showing: {len(rows)}[/dim]")


def list_categories():
    """List all categories with counts."""
    conn = get_db_connection()
    
    rows = conn.execute("""
        SELECT category, content_type, COUNT(*) as count
        FROM clipboard_history
        GROUP BY category, content_type
        ORDER BY count DESC
    """).fetchall()
    
    conn.close()
    
    if not rows:
        console.print("[yellow]No items to categorize.[/yellow]")
        return
    
    table = Table(title="📂 Categories", show_lines=False)
    table.add_column("Category", style="blue")
    table.add_column("Type", style="magenta")
    table.add_column("Count", justify="right", style="green")
    
    for row in rows:
        table.add_row(row["category"], row["content_type"], str(row["count"]))
    
    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="List clipboard history")
    parser.add_argument("--limit", "-n", type=int, default=20, help="Maximum items to show")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--id", "-i", type=int, help="Show specific item by ID")
    parser.add_argument("--detail", "-d", action="store_true", help="Show detailed view")
    parser.add_argument("--categories", action="store_true", help="List all categories")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.categories:
        list_categories()
        return
    
    if args.json:
        conn = get_db_connection()
        query = "SELECT * FROM clipboard_history ORDER BY created_at DESC LIMIT ?"
        rows = conn.execute(query, (args.limit,)).fetchall()
        conn.close()
        print(json.dumps([dict(row) for row in rows], indent=2, default=str))
    else:
        list_history(args.limit, args.category, args.detail, args.id)


if __name__ == "__main__":
    main()
