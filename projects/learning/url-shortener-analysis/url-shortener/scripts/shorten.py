#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["click", "rich", "sqlite-vec"]
# ///
"""
URL Shortener - Generate short URLs

Usage:
    uv run scripts/shorten.py <url>
    uv run scripts/shorten.py <url> --alias my-link
    uv run scripts/shorten.py --batch urls.txt
"""

import argparse
import hashlib
import json
import random
import string
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from rich.console import Console
from rich.table import Table

console = Console()

# Configuration
DB_PATH = Path.home() / ".url-shortener" / "links.db"
DEFAULT_CODE_LENGTH = 6
DEFAULT_DOMAIN = "short.link"


def get_db_connection():
    """Get database connection, creating tables if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    # Create tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS links (
            short_code TEXT PRIMARY KEY,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            clicks INTEGER DEFAULT 0,
            last_clicked TIMESTAMP
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT NOT NULL,
            clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_hash TEXT,
            referrer TEXT,
            user_agent TEXT,
            FOREIGN KEY (short_code) REFERENCES links(short_code)
        )
    """)
    
    conn.commit()
    return conn


def validate_url(url: str) -> bool:
    """Validate URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def generate_short_code(length: int = DEFAULT_CODE_LENGTH) -> str:
    """Generate a random short code."""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def url_to_short_code(url: str) -> str:
    """Generate a deterministic short code from URL (for deduplication check)."""
    return hashlib.md5(url.encode()).hexdigest()[:8]


def shorten_url(url: str, alias: str = None) -> dict:
    """
    Shorten a URL.
    
    Args:
        url: The original URL to shorten
        alias: Optional custom alias
    
    Returns:
        Dict with short_code and original_url
    """
    # Validate URL
    if not validate_url(url):
        raise ValueError(f"Invalid URL format: {url}")
    
    conn = get_db_connection()
    
    try:
        # Check if URL already shortened
        existing = conn.execute(
            "SELECT short_code FROM links WHERE original_url = ?",
            (url,)
        ).fetchone()
        
        if existing:
            console.print(f"[yellow]URL already shortened:[/yellow] {existing['short_code']}")
            return {
                "short_code": existing["short_code"],
                "original_url": url,
                "exists": True
            }
        
        # Generate short code
        if alias:
            # Validate alias
            if not re.match(r'^[a-z0-9-]+$', alias):
                raise ValueError("Alias must contain only lowercase letters, numbers, and hyphens")
            
            # Check if alias exists
            existing = conn.execute(
                "SELECT short_code FROM links WHERE short_code = ?",
                (alias,)
            ).fetchone()
            
            if existing:
                raise ValueError(f"Alias '{alias}' already exists")
            
            short_code = alias
        else:
            # Generate unique short code
            for _ in range(100):  # Max 100 attempts
                short_code = generate_short_code()
                existing = conn.execute(
                    "SELECT short_code FROM links WHERE short_code = ?",
                    (short_code,)
                ).fetchone()
                if not existing:
                    break
            else:
                raise RuntimeError("Failed to generate unique short code")
        
        # Insert new link
        conn.execute(
            "INSERT INTO links (short_code, original_url) VALUES (?, ?)",
            (short_code, url)
        )
        conn.commit()
        
        domain = get_domain()
        short_url = f"https://{domain}/{short_code}"
        
        return {
            "short_code": short_code,
            "original_url": url,
            "short_url": short_url,
            "exists": False
        }
    
    finally:
        conn.close()


def get_domain() -> str:
    """Get configured domain."""
    import os
    return os.getenv("SHORTENER_DOMAIN", DEFAULT_DOMAIN)


def main():
    parser = argparse.ArgumentParser(
        description="URL Shortener - Generate short URLs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://example.com/very/long/url
  %(prog)s https://example.com --alias my-link
  %(prog)s --batch urls.txt
        """
    )
    
    parser.add_argument("url", nargs="?", help="URL to shorten")
    parser.add_argument("--alias", "-a", help="Custom alias for the short URL")
    parser.add_argument("--batch", "-b", help="File containing URLs to shorten (one per line)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only output the short URL")
    
    args = parser.parse_args()
    
    # Import re here to avoid issues
    import re
    
    # Batch mode
    if args.batch:
        batch_file = Path(args.batch)
        if not batch_file.exists():
            console.print(f"[red]Error:[/red] File not found: {batch_file}")
            sys.exit(1)
        
        urls = [line.strip() for line in batch_file.read_text().splitlines() if line.strip()]
        
        if not args.quiet:
            console.print(f"[bold]Processing {len(urls)} URLs...[/bold]\n")
        
        results = []
        for i, url in enumerate(urls, 1):
            try:
                result = shorten_url(url)
                results.append(result)
                
                if args.quiet:
                    console.print(result.get("short_url", ""))
                else:
                    status = "[yellow]exists[/yellow]" if result.get("exists") else "[green]created[/green]"
                    console.print(f"[{i}/{len(urls)}] {status}: {result.get('short_url')}")
            
            except Exception as e:
                console.print(f"[red]Error:[/red] {url} - {e}")
        
        if not args.quiet:
            console.print(f"\n[green]✓[/green] Processed {len(results)}/{len(urls)} URLs")
        
        return
    
    # Single URL mode
    if not args.url:
        parser.print_help()
        sys.exit(1)
    
    try:
        result = shorten_url(args.url, args.alias)
        
        if args.quiet:
            console.print(result.get("short_url", ""))
        else:
            domain = get_domain()
            
            if result.get("exists"):
                console.print(f"[yellow]⚠ URL already shortened:[/yellow]")
            else:
                console.print(f"[green]✓ Short URL created:[/green]")
            
            console.print(f"\n  [bold]Original:[/bold]  {result['original_url']}")
            console.print(f"  [bold]Short:[/bold]     https://{domain}/{result['short_code']}")
            console.print(f"  [bold]Code:[/bold]      {result['short_code']}")
    
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
