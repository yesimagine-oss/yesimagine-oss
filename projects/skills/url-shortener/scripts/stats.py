#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
URL Shortener - View statistics for a short URL

Usage:
    uv run scripts/stats.py <short_code>
    uv run scripts/stats.py <short_code> --detail
"""

import argparse
import sqlite3
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
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


def get_stats(short_code: str, detail: bool = False):
    """Get statistics for a short URL."""
    conn = get_db_connection()
    
    # Get link info
    link = conn.execute(
        "SELECT * FROM links WHERE short_code = ?",
        (short_code,)
    ).fetchone()
    
    if not link:
        console.print(f"[red]Link not found:[/red] {short_code}")
        conn.close()
        sys.exit(1)
    
    # Display basic info
    console.print(Panel.fit(
        f"[bold]Short Code:[/bold] {link['short_code']}\n"
        f"[bold]Original URL:[/bold] {link['original_url']}\n"
        f"[bold]Created:[/bold] {link['created_at']}\n"
        f"[bold]Total Clicks:[/bold] [green]{link['clicks']}[/green]",
        title="📊 Link Statistics",
        border_style="blue"
    ))
    
    if detail:
        # Get click details
        clicks = conn.execute(
            "SELECT * FROM clicks WHERE short_code = ? ORDER BY clicked_at DESC LIMIT 10",
            (short_code,)
        ).fetchall()
        
        if clicks:
            table = Table(title="Recent Clicks (Last 10)", show_lines=False)
            table.add_column("Time", style="dim")
            table.add_column("Referrer", style="blue")
            table.add_column("User Agent", style="dim")
            
            for click in clicks:
                referrer = click["referrer"] or "Direct"
                ua = click["user_agent"] or "Unknown"
                if len(ua) > 40:
                    ua = ua[:40] + "..."
                table.add_row(
                    str(click["clicked_at"])[:19],
                    referrer[:30],
                    ua
                )
            
            console.print(table)
    
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="View statistics for a short URL")
    parser.add_argument("short_code", help="Short code to view stats for")
    parser.add_argument("--detail", "-d", action="store_true", help="Show detailed click information")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.json:
        conn = get_db_connection()
        link = conn.execute(
            "SELECT * FROM links WHERE short_code = ?",
            (args.short_code,)
        ).fetchone()
        conn.close()
        
        if not link:
            print(f'{{"error": "Link not found"}}')
            sys.exit(1)
        
        import json
        print(json.dumps(dict(link), indent=2, default=str))
    else:
        get_stats(args.short_code, args.detail)


if __name__ == "__main__":
    main()
