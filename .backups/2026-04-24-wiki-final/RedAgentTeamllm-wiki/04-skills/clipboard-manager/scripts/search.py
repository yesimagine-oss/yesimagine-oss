#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
Clipboard Manager - Search clipboard history

Usage:
    uv run scripts/search.py "keyword"
    uv run scripts/search.py "github" --category code
"""

import argparse
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
        console.print("[yellow]No clipboard history found.[/yellow]")
        sys.exit(0)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def search_clipboard(query: str, category: str = None, exact: bool = False, date_from: str = None):
    """Search clipboard history."""
    conn = get_db_connection()
    
    # Build query
    sql = """
        SELECT id, content, content_type, category, created_at, copied_count
        FROM clipboard_history
        WHERE 1=1
    """
    params = []
    
    if exact:
        sql += " AND content = ?"
        params.append(query)
    else:
        sql += " AND content LIKE ?"
        params.append(f"%{query}%")
    
    if category:
        sql += " AND category = ?"
        params.append(category)
    
    if date_from:
        sql += " AND created_at >= ?"
        params.append(date_from)
    
    sql += " ORDER BY created_at DESC LIMIT 50"
    
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    
    if not rows:
        console.print(f"[yellow]No results found for:[/yellow] '{query}'")
        return
    
    # Display results
    console.print(Panel(
        f"[bold]Query:[/bold] '{query}'\n"
        f"[bold]Results:[/bold] {len(rows)} items found",
        title="🔍 Search Results",
        border_style="blue"
    ))
    
    table = Table(show_lines=True)
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Type", style="magenta", width=10)
    table.add_column("Category", style="blue", width=12)
    table.add_column("Content", style="white")
    table.add_column("Date", style="dim", width=19)
    
    for row in rows:
        # Highlight search term in content
        content = row["content"][:80].replace('\n', ' ')
        if len(row["content"]) > 80:
            content += "..."
        
        table.add_row(
            str(row["id"]),
            row["content_type"],
            row["category"],
            content,
            str(row["created_at"])[:19]
        )
    
    console.print(table)
    
    console.print(f"\n[dim]Tip: Use 'uv run scripts/copy.py <ID>' to copy a result[/dim]")


def main():
    parser = argparse.ArgumentParser(description="Search clipboard history")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--exact", "-e", action="store_true", help="Exact match")
    parser.add_argument("--date-from", help="Search from date (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if not args.query:
        console.print("[red]Error:[/red] Search query required")
        parser.print_help()
        sys.exit(1)
    
    if args.json:
        conn = get_db_connection()
        # ... JSON output implementation
        conn.close()
    else:
        search_clipboard(args.query, args.category, args.exact, args.date_from)


if __name__ == "__main__":
    main()
