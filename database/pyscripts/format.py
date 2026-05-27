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

from md2json import build_json_from_md
from json2md import convert_term_to_md
from utils import DEFAULT_WIKI_DIR, DEFAULT_JSON_DIR


def format_markdown_file(
    md_path: Path, json_dir: Path, dry_run: bool = False
) -> tuple[bool, bool]:
    """
    Format a single Markdown file via MD → JSON → MD roundtrip.

    Returns:
        (success, changed) — changed is True when the file content was or would be updated.
    """
    try:
        term_id = md_path.stem
        json_path = json_dir / f"{term_id}.json"

        term_json = build_json_from_md(md_path, override_id=None, json_path=json_path)
        term_json.setdefault("tags", [])
        term_json.setdefault("related", [])
        term_json.setdefault("authors", [])
        term_json.setdefault("dates", {})

        formatted_md = convert_term_to_md(term_json)

        existing_md = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
        changed = existing_md != formatted_md

        if changed and not dry_run:
            md_path.write_text(formatted_md, encoding="utf-8")

        return True, changed
    except Exception as e:
        print(f"ERROR  {md_path.name}: {e}", file=sys.stderr)
        return False, False


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

        success, changed = format_markdown_file(md_path, args.json_dir, args.dry_run)
        if success:
            status = "WOULD FORMAT" if args.dry_run and changed else (
                "FORMATTED" if changed else "SKIP (already formatted)"
            )
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

        success, changed = format_markdown_file(md_path, args.json_dir, args.dry_run)
        if not success:
            errors += 1
        elif changed:
            print(f"{'WOULD FORMAT' if args.dry_run else 'FORMAT'} {term_id}.md")
            formatted += 1
        else:
            print(f"SKIP   {term_id}.md (already formatted)")
            unchanged += 1

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
