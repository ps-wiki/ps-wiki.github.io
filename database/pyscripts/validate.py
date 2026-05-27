#!/usr/bin/env python3
"""
Validate term JSON files in ./database/json/ against:
  - JSON Schema (./database/schema/v1/term.schema.json)
  - Unique IDs across files
  - Existence of IDs referenced in `related` (always checks against full directory)

Supports validating all files (default) or specific terms by ID.

Usage:
  # Validate all files (default)
  python database/pyscripts/validate.py

  # Validate specific terms by ID
  python database/pyscripts/validate.py --terms stability adequacy

  # Explicitly validate all files
  python database/pyscripts/validate.py --all

  # Custom directories
  python database/pyscripts/validate.py --dir database/json --schema database/schema/v1/term.schema.json

Note: When using --terms, the related ID check still validates against ALL files
in the directory, not just the subset being validated.
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

from utils import DEFAULT_JSON_DIR, DEFAULT_SCHEMA_PATH, load_json, validate_term_schema


def validate_corpus(
    json_dir: Path,
    schema_path: Path,
    term_ids: List[str] | None = None,
    no_related_check: bool = False,
    filename_match: bool = False,
    fail_fast: bool = False,
) -> List[str]:
    """Validate term JSON files against schema and cross-file constraints.

    Args:
        json_dir: Directory containing term JSON files.
        schema_path: Path to term.schema.json.
        term_ids: Specific term IDs to validate (default: all files in json_dir).
        no_related_check: Skip checking that `related` IDs exist.
        filename_match: Also verify filename stem matches the `id` field.
        fail_fast: Stop collecting errors after the first failure group.

    Returns:
        List of error strings. Empty list means all files are valid.
    """
    # Resolve file list
    if term_ids:
        files = []
        for tid in term_ids:
            fp = json_dir / f"{tid}.json"
            if not fp.exists():
                return [f"Term file not found: {fp}"]
            files.append(fp)
        files = sorted(files)
    else:
        files = sorted(json_dir.glob("*.json"))

    if not files:
        return []

    all_errors: List[str] = []
    id_to_file: Dict[str, Path] = {}
    valid_docs: Dict[str, Dict[str, Any]] = {}

    for fp in files:
        try:
            data = load_json(fp)
        except Exception as e:
            all_errors.append(f"{fp.name}: failed to parse JSON: {e}")
            if fail_fast:
                return all_errors
            continue

        errors = validate_term_schema(data, schema_path)
        if errors:
            all_errors.extend([f"{fp.name}: {e}" for e in errors])
            if fail_fast:
                return all_errors
            continue

        term_id = str(data.get("id"))

        if term_id in id_to_file:
            prev = id_to_file[term_id].name
            all_errors.append(f"{fp.name}: duplicate id '{term_id}' also in {prev}")
            if fail_fast:
                return all_errors
        else:
            id_to_file[term_id] = fp
            valid_docs[term_id] = data

        if filename_match and fp.stem != term_id:
            all_errors.append(
                f"{fp.name}: filename stem '{fp.stem}' != id '{term_id}'"
            )
            if fail_fast:
                return all_errors

    if not no_related_check and not (fail_fast and all_errors):
        all_json_files = sorted(json_dir.glob("*.json"))
        known_ids: Set[str] = set()
        for jf in all_json_files:
            try:
                d = load_json(jf)
                if "id" in d:
                    known_ids.add(str(d["id"]))
            except Exception:
                pass

        for term_id, data in valid_docs.items():
            for rid in (data.get("related") or []):
                if rid not in known_ids:
                    src = id_to_file[term_id].name
                    all_errors.append(
                        f"{src}: related id '{rid}' not found among JSON files"
                    )

    return all_errors


def main():
    ap = argparse.ArgumentParser(
        description="Validate PS-Wiki term JSONs.",
        epilog="Examples:\n"
        "  All files:        %(prog)s\n"
        "  Specific terms:   %(prog)s --terms stability frequency-control\n"
        "  Explicit all:     %(prog)s --all",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--terms", nargs="+", help="Validate specific terms by ID")
    ap.add_argument("--all", action="store_true", help="Validate all terms (default)")
    ap.add_argument(
        "--dir", type=Path, default=DEFAULT_JSON_DIR,
        help="Directory with term JSON files (default: database/json)",
    )
    ap.add_argument(
        "--schema", type=Path, default=DEFAULT_SCHEMA_PATH,
        help="Path to term.schema.json",
    )
    ap.add_argument("--no-related-check", action="store_true",
                    help="Skip checking that `related` IDs exist")
    ap.add_argument("--filename-match", action="store_true",
                    help="Also check filename stem == `id`")
    ap.add_argument("--fail-fast", action="store_true",
                    help="Stop on first failure group")
    args = ap.parse_args()

    if not args.schema.exists():
        print(f"Schema not found: {args.schema}", file=sys.stderr)
        sys.exit(2)
    if not args.dir.exists():
        print(f"Terms directory not found: {args.dir}", file=sys.stderr)
        sys.exit(2)

    errors = validate_corpus(
        args.dir, args.schema,
        term_ids=args.terms,
        no_related_check=args.no_related_check,
        filename_match=args.filename_match,
        fail_fast=args.fail_fast,
    )

    if errors:
        print("\nValidation errors:\n------------------")
        for e in errors:
            print(e)
        print(f"\nSummary: {len(errors)} error(s).")
        sys.exit(1)
    else:
        n = len(args.terms) if args.terms else len(sorted(args.dir.glob("*.json")))
        print(f"All good: {n} files validated; IDs unique; related references resolved.")
        sys.exit(0)


if __name__ == "__main__":
    main()
