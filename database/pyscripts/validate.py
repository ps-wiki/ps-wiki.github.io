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


def main():
    ap = argparse.ArgumentParser(
        description="Validate PS-Wiki term JSONs.",
        epilog="Examples:\n"
        "  All files:        %(prog)s\n"
        "  Specific terms:   %(prog)s --terms stability frequency-control\n"
        "  Explicit all:     %(prog)s --all",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Term selection arguments
    ap.add_argument("--terms", nargs="+", help="Validate specific terms by ID")
    ap.add_argument(
        "--all",
        action="store_true",
        help="Explicitly validate all terms (default behavior)",
    )

    # Directory arguments
    ap.add_argument(
        "--dir",
        type=Path,
        default=DEFAULT_JSON_DIR,
        help="Directory with term JSON files (default: database/json)",
    )
    ap.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Path to term.schema.json (default: database/schema/v1/term.schema.json)",
    )

    # Validation options
    ap.add_argument(
        "--no-related-check",
        action="store_true",
        help="Skip checking that `related` IDs exist",
    )
    ap.add_argument(
        "--filename-match",
        action="store_true",
        help="Also check filename stem == `id`",
    )
    ap.add_argument(
        "--fail-fast", action="store_true", help="Stop on first failure group"
    )
    args = ap.parse_args()

    if not args.schema.exists():
        print(f"Schema not found: {args.schema}", file=sys.stderr)
        sys.exit(2)
    if not args.dir.exists():
        print(f"Terms directory not found: {args.dir}", file=sys.stderr)
        sys.exit(2)

    # Get list of files to validate
    if args.terms:
        # Validate specific terms
        files = []
        for term_id in args.terms:
            json_file = args.dir / f"{term_id}.json"
            if not json_file.exists():
                print(f"ERROR: Term file not found: {json_file}", file=sys.stderr)
                sys.exit(2)
            files.append(json_file)
        files = sorted(files)
    else:
        # Validate all files (default or --all)
        files = sorted(args.dir.glob("*.json"))

    if not files:
        print(f"No JSON files to validate")
        sys.exit(0)

    # First pass: schema validation + collect ids
    all_errors: List[str] = []
    id_to_file: Dict[str, Path] = {}
    valid_docs: Dict[str, Dict[str, Any]] = {}

    for fp in files:
        try:
            data = load_json(fp)
        except Exception as e:
            all_errors.append(f"{fp.name}: failed to parse JSON: {e}")
            if args.fail_fast:
                break
            continue

        # Use shared validation function
        errors = validate_term_schema(data, args.schema)
        if errors:
            # Prefix errors with filename
            all_errors.extend([f"{fp.name}: {e}" for e in errors])
            if args.fail_fast:
                break
            continue

        # Extract ID (assumed required by schema)
        term_id = str(data.get("id"))

        # Duplicate ID check
        if term_id in id_to_file:
            prev = id_to_file[term_id].name
            all_errors.append(f"{fp.name}: duplicate id '{term_id}' also in {prev}")
            if args.fail_fast:
                break
        else:
            id_to_file[term_id] = fp
            valid_docs[term_id] = data

        # Optional filename == id check
        if args.filename_match:
            if fp.stem != term_id:
                all_errors.append(
                    f"{fp.name}: filename stem '{fp.stem}' != id '{term_id}'"
                )
                if args.fail_fast:
                    break

    # Second pass: related references (only for docs that passed schema)
    if not args.no_related_check and not (args.fail_fast and all_errors):
        # Build set of ALL known IDs in the directory (not just validated files)
        all_json_files = sorted(args.dir.glob("*.json"))
        known_ids = set()
        for json_file in all_json_files:
            try:
                file_data = load_json(json_file)
                if "id" in file_data:
                    known_ids.add(str(file_data.get("id")))
            except Exception:
                # Skip files that can't be loaded
                pass

        # Check related IDs for validated docs
        for term_id, data in valid_docs.items():
            related = data.get("related") or []
            for rid in related:
                if rid not in known_ids:
                    src_file = id_to_file[term_id].name
                    all_errors.append(
                        f"{src_file}: related id '{rid}' not found among JSON files"
                    )

    # Report
    if all_errors:
        print("\nValidation errors:\n------------------")
        for e in all_errors:
            print(e)
        print(f"\nSummary: {len(all_errors)} error(s) across {len(files)} file(s).")
        sys.exit(1)
    else:
        print(
            f"All good: {len(files)} files validated; IDs unique; related references resolved."
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
