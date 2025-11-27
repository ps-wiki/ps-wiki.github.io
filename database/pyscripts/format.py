#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format Jekyll term Markdown file(s) by performing a full MD → JSON → MD roundtrip
conversion, which normalizes the file's structure and front matter.

This script now leverages the enhanced md2json and json2md modules with:
- Field preservation ($schema, aliases)
- Conversion invariance (roundtrip produces identical results)
- Support for single file, multiple terms, or all files

Usage:
  # Format a single file
  python database/pyscripts/format.py -i _wiki/stability.md

  # Format specific terms by ID
  python database/pyscripts/format.py --terms stability frequency-control

  # Format all files
  python database/pyscripts/format.py --all
"""

import argparse
import sys
from pathlib import Path
from typing import List

# Import conversion functions and shared constants from utils module
from md2json import build_json_from_md
from json2md import convert_term_to_md
from utils import DEFAULT_WIKI_DIR, DEFAULT_JSON_DIR


def format_markdown_file(md_path: Path, json_dir: Path, dry_run: bool = False) -> bool:
    """
    Format a single Markdown file via MD → JSON → MD roundtrip.

    Args:
        md_path: Path to Markdown file
        json_dir: Directory where corresponding JSON file exists (for field preservation)
        dry_run: If True, don't actually write the file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Determine corresponding JSON path for field preservation
        term_id = md_path.stem
        json_path = json_dir / f"{term_id}.json"

        # MD → JSON (with field preservation from existing JSON)
        term_json = build_json_from_md(md_path, override_id=None, json_path=json_path)

        # Normalize optional fields
        term_json.setdefault("tags", [])
        term_json.setdefault("related", [])
        term_json.setdefault("authors", [])
        term_json.setdefault("dates", {})

        # JSON → MD
        formatted_md = convert_term_to_md(term_json)

        # Check if content changed
        if md_path.exists():
            existing_md = md_path.read_text(encoding="utf-8")
            if existing_md == formatted_md:
                return True  # No changes needed

        # Write formatted content
        if not dry_run:
            md_path.write_text(formatted_md, encoding="utf-8")

        return True
    except Exception as e:
        print(f"ERROR  {md_path.name}: {e}", file=sys.stderr)
        return False


def main():
    ap = argparse.ArgumentParser(
        description="Format Jekyll term Markdown file(s) via MD → JSON → MD roundtrip.",
        epilog="Examples:\n"
        "  Single file:  %(prog)s -i _wiki/stability.md\n"
        "  By term ID:   %(prog)s --terms stability frequency-control\n"
        "  All files:    %(prog)s --all\n"
        "  Dry run:      %(prog)s --all --dry-run",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Single-file mode
    ap.add_argument(
        "-i", "--input", help="Path to the term Markdown file (single-file mode)."
    )

    # Multi-term mode
    ap.add_argument(
        "--terms", nargs="+", help="Process specific terms by ID (multi-term mode)."
    )
    ap.add_argument(
        "--all",
        action="store_true",
        help="Process all Markdown files in wiki directory.",
    )

    # Directory arguments
    ap.add_argument(
        "--wiki-dir",
        type=Path,
        default=DEFAULT_WIKI_DIR,
        help="Directory with Markdown files (default: _wiki).",
    )
    ap.add_argument(
        "--json-dir",
        type=Path,
        default=DEFAULT_JSON_DIR,
        help="Directory with JSON files for field preservation (default: database/json).",
    )

    # Behavior flags
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files.",
    )

    args = ap.parse_args()

    # Validate argument combinations
    single_file_mode = args.input
    multi_term_mode = args.terms or args.all

    if single_file_mode and multi_term_mode:
        print(
            "ERROR: Cannot use both single-file mode (-i) and multi-term mode (--terms/--all).",
            file=sys.stderr,
        )
        sys.exit(1)

    if not single_file_mode and not multi_term_mode:
        print(
            "ERROR: Must specify either -i (single-file mode) or --terms/--all (multi-term mode).",
            file=sys.stderr,
        )
        ap.print_help()
        sys.exit(1)

    # Single-file mode
    if single_file_mode:
        md_path = Path(args.input)
        if not md_path.exists():
            print(f"ERROR: Markdown file not found: {md_path}", file=sys.stderr)
            sys.exit(1)

        if format_markdown_file(md_path, args.json_dir, args.dry_run):
            status = "DRY RUN" if args.dry_run else "FORMATTED"
            print(f"{status}: {md_path}")
        else:
            sys.exit(1)
        return

    # Multi-term mode
    if not args.wiki_dir.exists():
        print(f"ERROR: Wiki directory not found: {args.wiki_dir}", file=sys.stderr)
        sys.exit(1)

    # Get list of terms to process
    if args.all:
        md_files = sorted(args.wiki_dir.glob("*.md"))
        term_ids = [f.stem for f in md_files]
        if not term_ids:
            print(f"No Markdown files found in {args.wiki_dir}", file=sys.stderr)
            sys.exit(0)
    else:
        term_ids = args.terms

    # Process each term
    total = 0
    formatted = 0
    unchanged = 0
    errors = 0

    for term_id in term_ids:
        total += 1
        md_path = args.wiki_dir / f"{term_id}.md"

        if not md_path.exists():
            print(
                f"ERROR  {term_id}: Markdown file not found: {md_path}", file=sys.stderr
            )
            errors += 1
            continue

        # Check if content would change
        try:
            term_id_name = md_path.stem
            json_path = args.json_dir / f"{term_id_name}.json"
            term_json = build_json_from_md(
                md_path, override_id=None, json_path=json_path
            )
            term_json.setdefault("tags", [])
            term_json.setdefault("related", [])
            term_json.setdefault("authors", [])
            term_json.setdefault("dates", {})
            formatted_md = convert_term_to_md(term_json)

            existing_md = md_path.read_text(encoding="utf-8")
            if existing_md == formatted_md:
                print(f"SKIP   {term_id}.md (already formatted)")
                unchanged += 1
                continue

            if not args.dry_run:
                md_path.write_text(formatted_md, encoding="utf-8")
                print(f"FORMAT {term_id}.md")
            else:
                print(f"WOULD FORMAT {term_id}.md")
            formatted += 1
        except Exception as e:
            print(f"ERROR  {term_id}: {e}", file=sys.stderr)
            errors += 1

    # Print summary
    print(f"\nSummary:")
    print(f"  Total terms : {total}")
    print(f"  Formatted   : {formatted}")
    print(f"  Unchanged   : {unchanged}")
    print(f"  Errors      : {errors}")

    if errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
