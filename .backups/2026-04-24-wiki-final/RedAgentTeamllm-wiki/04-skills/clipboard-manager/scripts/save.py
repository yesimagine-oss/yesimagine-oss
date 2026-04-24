#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich", "pyperclip"]
# ///
"""
Clipboard Manager - Save clipboard content

Usage:
    uv run scripts/save.py
    uv run scripts/save.py --text "content"
    uv run scripts/save.py --file snippets.txt
"""

import argparse
import hashlib
import re
import sqlite3
import sys
from datetime import datetime
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
    """Get database connection, creating tables if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clipboard_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            content_hash TEXT UNIQUE,
            content_type TEXT DEFAULT 'text',
            category TEXT DEFAULT 'text',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            copied_count INTEGER DEFAULT 0,
            last_copied TIMESTAMP,
            tags TEXT,
            metadata TEXT
        )
    """)
    
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_content_type ON clipboard_history(content_type)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_category ON clipboard_history(category)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_created ON clipboard_history(created_at DESC)
    """)
    
    conn.commit()
    return conn


def detect_content_type(content: str) -> str:
    """Detect the type of content."""
    if re.match(r'https?://\S+', content):
        return 'link'
    elif re.match(r'\S+@\S+\.\S+', content):
        return 'email'
    elif re.match(r'^\+?\d[\d\s-]{8,}\d$', content):
        return 'phone'
    elif re.match(r'\d{4}-\d{2}-\d{2}', content):
        return 'date'
    elif re.search(r'(function|def|class|import|from|var|let|const)\s', content, re.IGNORECASE):
        return 'code'
    elif len(content) >= 8 and calculate_entropy(content) > 3.5:
        return 'password'
    else:
        return 'text'


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of text."""
    import math
    if not text:
        return 0.0
    
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    entropy = 0.0
    length = len(text)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    
    return entropy


def detect_category(content_type: str, content: str) -> str:
    """Detect category based on content type and content."""
    if content_type == 'link':
        if 'github' in content.lower():
            return 'github'
        elif 'twitter' in content.lower() or 'x.com' in content.lower():
            return 'social'
        else:
            return 'links'
    elif content_type == 'code':
        return 'code'
    elif content_type == 'password':
        return 'passwords'
    elif content_type == 'email':
        return 'emails'
    else:
        return 'notes'


def save_clipboard(text: str = None, from_file: str = None):
    """Save clipboard content to database."""
    # Get content
    if text:
        content = text
    elif from_file:
        file_path = Path(from_file)
        if not file_path.exists():
            console.print(f"[red]Error:[/red] File not found: {from_file}")
            sys.exit(1)
        content = file_path.read_text()
    else:
        try:
            content = pyperclip.paste()
        except Exception as e:
            console.print(f"[red]Error reading clipboard:[/red] {e}")
            sys.exit(1)
    
    if not content or not content.strip():
        console.print("[yellow]Clipboard is empty.[/yellow]")
        return
    
    # Detect type and category
    content_type = detect_content_type(content)
    category = detect_category(content_type, content)
    
    # Generate hash for deduplication
    content_hash = hashlib.md5(content.encode()).hexdigest()
    
    conn = get_db_connection()
    
    try:
        # Check for duplicates
        existing = conn.execute(
            "SELECT id FROM clipboard_history WHERE content_hash = ?",
            (content_hash,)
        ).fetchone()
        
        if existing:
            console.print(f"[yellow]⚠ Content already saved (ID: {existing['id']})[/yellow]")
            return {
                "id": existing["id"],
                "exists": True
            }
        
        # Insert new record
        cursor = conn.execute("""
            INSERT INTO clipboard_history 
            (content, content_hash, content_type, category, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            content,
            content_hash,
            content_type,
            category,
            f'{{"length": {len(content)}, "source": "manual"}}'
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        
        # Display success
        preview = content[:100] + "..." if len(content) > 100 else content
        preview = preview.replace('\n', ' ')
        
        console.print(Panel(
            f"[bold]ID:[/bold] {record_id}\n"
            f"[bold]Type:[/bold] {content_type}\n"
            f"[bold]Category:[/bold] {category}\n"
            f"[bold]Preview:[/bold] {preview}",
            title="✓ Clipboard Saved",
            border_style="green"
        ))
        
        return {
            "id": record_id,
            "content_type": content_type,
            "category": category,
            "exists": False
        }
    
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Save clipboard content")
    parser.add_argument("--text", "-t", help="Text to save (instead of clipboard)")
    parser.add_argument("--file", "-f", help="File to import content from")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only output the ID")
    
    args = parser.parse_args()
    
    if args.text and args.file:
        console.print("[red]Error:[/red] Cannot use both --text and --file")
        sys.exit(1)
    
    result = save_clipboard(text=args.text, from_file=args.file)
    
    if args.quiet and result:
        console.print(str(result["id"]))


if __name__ == "__main__":
    main()
