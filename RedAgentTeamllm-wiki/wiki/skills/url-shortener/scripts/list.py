#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["click", "rich"]
# ///
"""
URL Shortener - List all shortened URLs

Usage:
    uv run scripts/list.py
    uv run scripts/list.py --limit 20
    uv run scripts/list.py --sort clicks
"""

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()

DB_PATH = Path.home() / ".url-shortener" / "links.db"


def get_db_connection():
    """Get database connection."""
    if not DB_PATH.exists():
        console.print("[yellow]No links found. Create some short URLs first![/yellow]")
        sys.exit(0)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def list_links(limit: int = 50, sort_by: str = "created_at"):
    """List all shortened URLs."""
    conn = get_db_connection()
    
    # Validate sort column
    valid_columns = {"created_at", "clicks", "short_code", "original_url"}
    if sort_by not in valid_columns:
        console.print(f"[red]Invalid sort column. Choose from: {', '.join(valid_columns)}[/red]")
        sys.exit(1)
    
    # Query links
    query = f"""
        SELECT short_code, original_url, created_at, clicks, last_clicked
        FROM links
        ORDER BY {sort_by} DESC
        LIMIT ?
    """
    
    rows = conn.execute(query, (limit,)).fetchall()
    conn.close()
    
    if not rows:
        console.print("[yellow]No links found.[/yellow]")
        return
    
    # Display table
    table = Table(title=f"Shortened URLs ({len(rows)} links)", show_lines=True)
    table.add_column("Short Code", style="cyan")
    table.add_column("Original URL", style="blue")
    table.add_column("Clicks", justify="right", style="green")
    table.add_column("Created", style="dim")
    
    for row in rows:
        created = row["created_at"][:10] if row["created_at"] else "N/A"
        table.add_row(
            row["short_code"],
            row["original_url"][:50] + "..." if len(row["original_url"]) > 50 else row["original_url"],
            str(row["clicks"]),
            created
        )
    
    console.print(table)
    
    # Summary
    total_clicks = sum(row["clicks"] for row in rows)
    console.print(f"\n[dim]Total clicks across all links: {total_clicks}[/dim]")


def main():
    parser = argparse.ArgumentParser(description="List all shortened URLs")
    parser.add_argument("--limit", "-n", type=int, default=50, help="Maximum number of links to show")
    parser.add_argument("--sort", "-s", default="created_at", 
                       choices=["created_at", "clicks", "short_code"],
                       help="Sort by column")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.json:
        # JSON output for programmatic use
        conn = get_db_connection()
        query = f"""
            SELECT short_code, original_url, created_at, clicks, last_clicked
            FROM links
            ORDER BY {args.sort} DESC
            LIMIT ?
        """
        rows = conn.execute(query, (args.limit,)).fetchall()
        conn.close()
        
        import json
        print(json.dumps([dict(row) for row in rows], indent=2))
    else:
        list_links(args.limit, args.sort)


if __name__ == "__main__":
    main()
