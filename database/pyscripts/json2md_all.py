#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch-convert all term JSON files in a directory into Jekyll Markdown files.

- Reuses the single-file converter from json2md.py (imports its functions).
- Writes _wiki/{id}.md by default (falls back to filename stem if id missing).
- Only writes when the generated content differs (avoids needless rebuilds).
- Continues on errors but prints a summary at the end (configurable).

Usage:
  python database/pyscripts/json2md_all.py --in-dir database/json --out-dir _wiki --pattern "*.json" [--fail-fast] [--overwrite]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Import the converter from the single-file script.
# Ensure json2md.py is in the same folder as this script.
# If you renamed/moved things, adjust the import accordingly.
try:
    from json2md import convert_term_to_md  # uses your existing converter
except Exception as e:
    print("ERROR: Could not import convert_term_to_md from json2md.py:", e, file=sys.stderr)
    sys.exit(1)


def safe_load_json(p: Path) -> Dict[str, Any]:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise RuntimeError(f"Failed to parse JSON: {p} ({e})")


def out_name_for(term: Dict[str, Any], src_path: Path) -> str:
    # Prefer the declared id; fallback to filename stem.
    term_id = term.get("id") or src_path.stem
    return f"{term_id}.md"


def write_if_changed(out_path: Path, content: str, overwrite: bool = False) -> bool:
    """Write Markdown only if content differs (or always if overwrite=True)."""
    if not overwrite and out_path.exists():
        try:
            old = out_path.read_text(encoding="utf-8")
        except Exception:
            old = None
        if old == content:
            return False
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser(description="Batch convert JSON terms to Markdown.")
    ap.add_argument("--in-dir", required=True, help="Directory with term JSON files (e.g., database/json).")
    ap.add_argument("--out-dir", required=True, help="Output directory for Markdown files (e.g., _wiki).")
    ap.add_argument("--pattern", default="*.json", help="Glob pattern for JSON files (default: *.json).")
    ap.add_argument("--fail-fast", action="store_true", help="Stop on first error.")
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="Rewrite Markdown files even if identical (force consistency).",
    )
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)

    if not in_dir.exists():
        print(f"ERROR: Input directory not found: {in_dir}", file=sys.stderr)
        sys.exit(1)

    paths = sorted(in_dir.glob(args.pattern))
    if not paths:
        print(f"No JSON files matched {args.pattern} in {in_dir}")
        return

    total = 0
    written = 0
    errors = 0

    for p in paths:
        total += 1
        try:
            term = safe_load_json(p)
            md = convert_term_to_md(term)
            out_name = out_name_for(term, p)
            out_path = out_dir / out_name
            changed = write_if_changed(out_path, md, overwrite=args.overwrite)
            written += 1 if changed else 0
            status = "WROTE" if changed else "SKIP "
            print(f"{status}  {p.name}  ->  {out_name}")
        except Exception as e:
            errors += 1
            print(f"ERROR  {p.name}: {e}", file=sys.stderr)
            if args.fail_fast:
                break

    print("\nSummary:")
    print(f"  Files scanned : {total}")
    print(f"  Files written : {written}")
    print(f"  Errors        : {errors}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
