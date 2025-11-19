#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format a Jekyll term Markdown file by performing a full MD -> JSON -> MD roundtrip
conversion, which normalizes the file's structure and front matter.

Requires:
- md2json.py (must be in the same directory or accessible on the Python path)
- json2md.py (must be in the same directory or accessible on the Python path)

Usage:
  python database/pyscripts/md_format.py -i _wiki/automatic-generation-control.md
"""

import argparse
import sys
from pathlib import Path

# Assuming md2json.py and json2md.py are in the same directory
# We import the main conversion functions directly.
try:
    from md2json import build_json_from_md
    from json2md import convert_term_to_md
except ImportError:
    print("ERROR: Could not import 'build_json_from_md' from md2json.py or 'convert_term_to_md' from json2md.py.", file=sys.stderr)
    print("Ensure these files are in the same directory as md_format.py.", file=sys.stderr)
    sys.exit(1)


def format_markdown_file(md_path: Path):
    """Performs the MD -> JSON -> MD roundtrip formatting."""
    print(f"--- Processing {md_path.name} ---")

    # 1. MD -> JSON (in memory)
    try:
        # Note: We pass None for override_id to use the default title-derived ID
        term_json = build_json_from_md(md_path, override_id=None)
        print("✅ MD converted to internal JSON structure.")
    except Exception as e:
        print(f"❌ ERROR: Failed MD -> JSON conversion for {md_path.name}: {e}", file=sys.stderr)
        return

    # 2. Normalize fields for json2md's expectations
    # This block ensures fields like 'tags', 'related', 'authors', and 'dates'
    # are present and correctly structured, even if they were missing or None in the MD.
    term_json.setdefault("tags", [])
    term_json.setdefault("related", [])
    term_json.setdefault("authors", [])
    # Dates are already derived in build_json_from_md, but we ensure the structure exists
    if not term_json.get("dates"):
        # This is unlikely to happen with the current md2json logic, but safe to include
        term_json["dates"] = {} 
    
    # 3. JSON -> MD (formatted string)
    try:
        # We need a temporary structure to simulate derive_file_dates, 
        # but since we are writing back to the *same* file, we use the original path.
        # json2md's convert_term_to_md doesn't rely on file system stats, only the CLI does.
        formatted_md = convert_term_to_md(term_json)
        print("✅ JSON structure converted back to formatted MD string.")
    except Exception as e:
        print(f"❌ ERROR: Failed JSON -> MD conversion for {md_path.name}: {e}", file=sys.stderr)
        return

    # 4. Overwrite original MD file
    try:
        md_path.write_text(formatted_md, encoding="utf-8")
        print(f"🎉 Successfully wrote standardized format to: {md_path}")
    except Exception as e:
        print(f"❌ ERROR: Failed to write output file {md_path.name}: {e}", file=sys.stderr)
        return


def main():
    ap = argparse.ArgumentParser(
        description="Format a Jekyll term Markdown file via MD -> JSON -> MD roundtrip."
    )
    ap.add_argument("-i", "--input", required=True, help="Path to the term Markdown file to format.")
    args = ap.parse_args()

    md_path = Path(args.input)

    if not md_path.exists():
        print(f"ERROR: Markdown file not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    format_markdown_file(md_path)


if __name__ == "__main__":
    main()
