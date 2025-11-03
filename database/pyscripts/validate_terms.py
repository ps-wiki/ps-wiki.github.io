#!/usr/bin/env python3
"""
Validate all term JSON files in ./database/json/ against:
  - JSON Schema (./database/schema/v1/term.schema.json)
  - Unique IDs across files
  - Existence of IDs referenced in `related`
Optional:
  - Ensure filename (without .json) == `id`

Usage:
  python ./database/pyscripts/validate_terms.py
  python ./database/pyscripts/validate_terms.py --dir ./database/json --schema ./database/schema/v1/term.schema.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from jsonschema.validators import Draft202012Validator
except Exception:
    print("Please install jsonschema:  pip install jsonschema", file=sys.stderr)
    sys.exit(2)

DEFAULT_DIR = Path("./database/json")
DEFAULT_SCHEMA = Path("./database/schema/v1/term.schema.json")

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def validate_with_schema(validator: Draft202012Validator, data: Any, name: str) -> List[str]:
    errs: List[str] = []
    for e in validator.iter_errors(data):
        loc = "".join([f"[{p}]" if isinstance(p, int) else (("." if loc and not loc.endswith("]") else "") + str(p)) for loc in [""] for p in list(e.path)])
        errs.append(f"{name}: {loc or '(root)'}: {e.message}")
    return errs

def main():
    ap = argparse.ArgumentParser(description="Validate PS-Wiki term JSONs.")
    ap.add_argument("--dir", type=Path, default=DEFAULT_DIR, help="Directory with term JSON files")
    ap.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Path to term.schema.json")
    ap.add_argument("--no-related-check", action="store_true", help="Skip checking that `related` IDs exist")
    ap.add_argument("--filename-match", action="store_true", help="Also check filename stem == `id`")
    ap.add_argument("--fail-fast", action="store_true", help="Stop on first failure group")
    args = ap.parse_args()

    if not args.schema.exists():
        print(f"Schema not found: {args.schema}", file=sys.stderr)
        sys.exit(2)
    if not args.dir.exists():
        print(f"Terms directory not found: {args.dir}", file=sys.stderr)
        sys.exit(2)

    # Load/compile schema
    try:
        schema = load_json(args.schema)
        validator = Draft202012Validator(schema)
    except Exception as e:
        print(f"Failed to load/compile schema: {e}", file=sys.stderr)
        sys.exit(2)

    files = sorted(args.dir.glob("*.json"))
    if not files:
        print(f"No JSON files in {args.dir}")
        sys.exit(0)

    # First pass: schema validation + collect ids
    all_errors: List[str] = []
    id_to_file: Dict[str, Path] = {}
    file_to_id: Dict[Path, str] = {}
    valid_docs: Dict[str, Dict[str, Any]] = {}

    for fp in files:
        try:
            data = load_json(fp)
        except Exception as e:
            all_errors.append(f"{fp.name}: failed to parse JSON: {e}")
            if args.fail_fast: break
            continue

        errors = validate_with_schema(validator, data, fp.name)
        if errors:
            all_errors.extend(errors)
            if args.fail_fast: break
            continue

        # Extract ID (assumed required by schema)
        term_id = str(data.get("id"))
        file_to_id[fp] = term_id

        # Duplicate ID check
        if term_id in id_to_file:
            prev = id_to_file[term_id].name
            all_errors.append(f"{fp.name}: duplicate id '{term_id}' also in {prev}")
            if args.fail_fast: break
        else:
            id_to_file[term_id] = fp
            valid_docs[term_id] = data

        # Optional filename == id check
        if args.filename_match:
            if fp.stem != term_id:
                all_errors.append(f"{fp.name}: filename stem '{fp.stem}' != id '{term_id}'")
                if args.fail_fast: break

    # Second pass: related references (only for docs that passed schema)
    if not args.no_related_check and not args.fail_fast:
        known_ids = set(id_to_file.keys())
        for term_id, data in valid_docs.items():
            related = data.get("related") or []
            for rid in related:
                if rid not in known_ids:
                    src_file = id_to_file[term_id].name
                    all_errors.append(f"{src_file}: related id '{rid}' not found among JSON files")

    # Report
    if all_errors:
        print("\nValidation errors:\n------------------")
        for e in all_errors:
            print(e)
        print(f"\nSummary: {len(all_errors)} error(s) across {len(files)} file(s).")
        sys.exit(1)
    else:
        print(f"All good: {len(files)} files validated; IDs unique; related references resolved.")
        sys.exit(0)

if __name__ == "__main__":
    main()
