#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
URL Shortener - Export links to CSV or JSON

Usage:
    uv run scripts/export.py
    uv run scripts/export.py --format csv
    uv run scripts/export.py --format json -o links.json
"""

import argparse
import csv
import json
import sqlite3
import sys
from pathlib import Path

from rich.console import Console

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


def export_links(format: str = "json", output_file: str = None):
    """Export links to file."""
    conn = get_db_connection()
    
    # Query all links
    rows = conn.execute("""
        SELECT short_code, original_url, created_at, clicks, last_clicked
        FROM links
        ORDER BY created_at DESC
    """).fetchall()
    
    conn.close()
    
    if not rows:
        console.print("[yellow]No links to export.[/yellow]")
        return
    
    # Convert to list of dicts
    links = [dict(row) for row in rows]
    
    # Export based on format
    if format == "json":
        output = json.dumps(links, indent=2, default=str)
    elif format == "csv":
        # CSV export
        import io
        output_buffer = io.StringIO()
        writer = csv.DictWriter(output_buffer, fieldnames=["short_code", "original_url", "created_at", "clicks", "last_clicked"])
        writer.writeheader()
        writer.writerows(links)
        output = output_buffer.getvalue()
    else:
        console.print(f"[red]Unsupported format:[/red] {format}")
        sys.exit(1)
    
    # Write to file or stdout
    if output_file:
        output_path = Path(output_file)
        output_path.write_text(output)
        console.print(f"[green]✓ Exported {len(links)} links to:[/green] {output_file}")
    else:
        # Print to stdout
        print(output)


def main():
    parser = argparse.ArgumentParser(description="Export links to CSV or JSON")
    parser.add_argument("--format", "-f", default="json", choices=["json", "csv"], help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--stats", action="store_true", help="Include click statistics")
    
    args = parser.parse_args()
    
    export_links(args.format, args.output)


if __name__ == "__main__":
    main()
