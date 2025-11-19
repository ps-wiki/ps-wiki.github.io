#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Round-trip standardization for PS-Wiki terms.

Steps:
1. Read a Jekyll Markdown term file.
2. Convert to JSON using md2json.build_json_from_md().
3. Write the JSON file.
4. Convert the JSON term back to Markdown using json2md.convert_term_to_md().
5. Write the standardized Markdown.

This lets you use Markdown as your drafting surface but keep a canonical
JSON representation, and also normalize Markdown formatting.

Usage examples:

  # Basic: MD -> JSON (same directory) and overwrite MD with standardized MD
  python roundtrip.py -m _wiki/automatic-generation-control.md

  # Explicit JSON path
  python roundtrip.py -m _wiki/automatic-generation-control.md \
      -j database/json/automatic-generation-control.json

  # Write standardized MD to a separate file instead of overwriting
  python roundtrip.py -m _wiki/automatic-generation-control.md \
      -o _wiki/automatic-generation-control.std.md

  # Override JSON id (passed through to md2json)
  python roundtrip.py -m _wiki/automatic-generation-control.md \
      --id automatic-generation-control

Notes:
- If -j/--json is omitted, JSON path defaults to `<markdown_dir>/<stem>.json`.
- If -o/--output-md is omitted, the input Markdown is overwritten in-place.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Import from your existing scripts (assumes they are importable)
try:
    from md2json import build_json_from_md
except ImportError as e:
    print("ERROR: Failed to import md2json.build_json_from_md. "
          "Make sure md2json.py is on PYTHONPATH or in the same directory.",
          file=sys.stderr)
    raise

try:
    from json2md import convert_term_to_md
except ImportError as e:
    print("ERROR: Failed to import json2md.convert_term_to_md. "
          "Make sure json2md.py is on PYTHONPATH or in the same directory.",
          file=sys.stderr)
    raise


def get_default_json_path(md_path: Path) -> Path:
    """
    If user doesn't specify a JSON output, default to:
      <md_dir>/<md_stem>.json
    You can tweak this to e.g. database/json/<stem>.json if you prefer.
    """
    return md_path.with_suffix(".json")


def roundtrip(
    md_path: Path,
    json_path: Optional[Path] = None,
    output_md_path: Optional[Path] = None,
    override_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Do the full round-trip:
      MD -> JSON (dict) -> write JSON -> MD (string) -> write MD.

    Returns the term dict for potential further processing.
    """
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    # ---------- Step 1: MD -> JSON dict ----------
    term = build_json_from_md(md_path, override_id=override_id)

    # ---------- Step 2: determine JSON path ----------
    if json_path is None:
        json_path = get_default_json_path(md_path)

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(term, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[INFO] Wrote JSON: {json_path}")

    # ---------- Step 3: JSON dict -> canonical MD ----------
    # We use the in-memory term (no need to re-read the JSON file).
    md_text = convert_term_to_md(term)

    # ---------- Step 4: decide output markdown path ----------
    if output_md_path is None:
        output_md_path = md_path  # overwrite in-place

    output_md_path.parent.mkdir(parents=True, exist_ok=True)
    output_md_path.write_text(md_text, encoding="utf-8")
    print(f"[INFO] Wrote standardized Markdown: {output_md_path}")

    return term


def main():
    parser = argparse.ArgumentParser(
        description="Round-trip a term Markdown file through JSON to standardize formatting."
    )
    parser.add_argument(
        "-m",
        "--markdown",
        required=True,
        help="Path to the input Jekyll term Markdown file.",
    )
    parser.add_argument(
        "-j",
        "--json",
        help="Path to write the JSON file. "
             "Defaults to <markdown_dir>/<stem>.json if omitted.",
    )
    parser.add_argument(
        "-o",
        "--output-md",
        help="Path to write the standardized Markdown. "
             "Defaults to overwriting the input Markdown in-place.",
    )
    parser.add_argument(
        "--id",
        help="Override JSON 'id' (passed through to md2json.build_json_from_md).",
    )

    args = parser.parse_args()

    md_path = Path(args.markdown)
    json_path = Path(args.json) if args.json else None
    out_md_path = Path(args.output_md) if args.output_md else None

    try:
        roundtrip(
            md_path=md_path,
            json_path=json_path,
            output_md_path=out_md_path,
            override_id=args.id,
        )
    except Exception as e:
        print(f"ERROR: Round-trip failed for {md_path}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
