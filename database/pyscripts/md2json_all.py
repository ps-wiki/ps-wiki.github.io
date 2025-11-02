#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch-convert all Jekyll term Markdown files in a directory into JSON terms.

Philosophy:
- Reuse the single-file converter from md2json.py (imports build_json_from_md).
- Iterate all .md files (configurable via --pattern).
- Derive output name from the JSON's 'id' (fallback: source filename stem).
- Write only when content changes (reduces noisy diffs).
- Continue on errors by default; optional --fail-fast to stop at first error.

Usage:
  python database/pyscripts/md2json_all.py --in-dir _wiki --out-dir database/json --pattern "*.md" [--fail-fast]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Import the single-term converter
try:
    from md2json import build_json_from_md  # must be in the same folder or on PYTHONPATH
except Exception as e:
    print("ERROR: Could not import build_json_from_md from md2json.py:", e, file=sys.stderr)
    sys.exit(1)


def write_if_changed(out_path: Path, doc: Dict[str, Any]) -> bool:
    """Write JSON only if content differs. Returns True if written."""
    new_text = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    if out_path.exists():
        try:
            old_text = out_path.read_text(encoding="utf-8")
        except Exception:
            old_text = None
        if old_text == new_text:
            return False
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(new_text, encoding="utf-8")
    return True


def out_name_for(term: Dict[str, Any], src_path: Path) -> str:
    """Prefer term['id']; fallback to filename stem."""
    term_id = term.get("id") or src_path.stem
    return f"{term_id}.json"


def main():
    ap = argparse.ArgumentParser(description="Batch convert Markdown terms to JSON.")
    ap.add_argument("--in-dir", required=True, help="Directory with term Markdown files (e.g., _wiki).")
    ap.add_argument("--out-dir", required=True, help="Output directory for term JSON files (e.g., database/json).")
    ap.add_argument("--pattern", default="*.md", help='Glob for input files (default: "*.md").')
    ap.add_argument("--fail-fast", action="store_true", help="Stop on first error.")
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)

    if not in_dir.exists():
        print(f"ERROR: Input directory not found: {in_dir}", file=sys.stderr)
        sys.exit(1)

    paths = sorted(in_dir.glob(args.pattern))
    if not paths:
        print(f"No Markdown files matched {args.pattern} in {in_dir}")
        return

    total = 0
    written = 0
    errors = 0

    for p in paths:
        # skip non-files or hidden files if any
        if not p.is_file():
            continue
        if p.name.startswith("."):
            continue

        total += 1
        try:
            term = build_json_from_md(p)
            out_name = out_name_for(term, p)
            out_path = out_dir / out_name
            changed = write_if_changed(out_path, term)
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
