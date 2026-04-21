#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich", "qrcode"]
# ///
"""
URL Shortener - Generate QR code for a short URL

Usage:
    uv run scripts/qr.py <short_code>
    uv run scripts/qr.py <short_code> -o qr.png
"""

import argparse
import sqlite3
import sys
from pathlib import Path

from rich.console import Console

console = Console()

DB_PATH = Path.home() / ".url-shortener" / "links.db"
DEFAULT_DOMAIN = "short.link"


def get_db_connection():
    """Get database connection."""
    if not DB_PATH.exists():
        console.print("[yellow]No database found.[/yellow]")
        sys.exit(1)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def generate_qr(short_code: str, output_file: str = None):
    """Generate QR code for a short URL."""
    try:
        import qrcode
    except ImportError:
        console.print("[red]Error:[/red] qrcode library not installed.")
        console.print("Install with: pip install qrcode[pil]")
        sys.exit(1)
    
    conn = get_db_connection()
    
    # Get link info
    link = conn.execute(
        "SELECT short_code, original_url FROM links WHERE short_code = ?",
        (short_code,)
    ).fetchone()
    
    if not link:
        console.print(f"[red]Link not found:[/red] {short_code}")
        conn.close()
        sys.exit(1)
    
    conn.close()
    
    # Generate short URL
    import os
    domain = os.getenv("SHORTENER_DOMAIN", DEFAULT_DOMAIN)
    short_url = f"https://{domain}/{short_code}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(short_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save or display
    if output_file:
        output_path = Path(output_file)
        img.save(str(output_path))
        console.print(f"[green]✓ QR code generated:[/green] {output_file}")
        console.print(f"  [dim]URL: {short_url}[/dim]")
    else:
        # Default output
        default_output = f"{short_code}_qr.png"
        img.save(default_output)
        console.print(f"[green]✓ QR code generated:[/green] {default_output}")
        console.print(f"  [dim]URL: {short_url}[/dim]")


def main():
    parser = argparse.ArgumentParser(description="Generate QR code for a short URL")
    parser.add_argument("short_code", help="Short code to generate QR for")
    parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    generate_qr(args.short_code, args.output)


if __name__ == "__main__":
    main()
