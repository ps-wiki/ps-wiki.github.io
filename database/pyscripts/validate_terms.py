#!/usr/bin/env python3
"""
Validate all term JSON files in ./database/json/ against the local schema:
./database/schema/v1/term.schema.json

Usage:
  python ./database/pyscripts/validate_terms.py --dir ./database/json --schema ./database/schema/v1/term.schema.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    # jsonschema >= 4.x
    from jsonschema.validators import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except Exception as e:
    print("Please install jsonschema:  pip install jsonschema", file=sys.stderr)
    raise

DEFAULT_DIR = Path("./database/json")
DEFAULT_SCHEMA = Path("./database/schema/v1/term.schema.json")

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def dotted_path(error: ValidationError) -> str:
    """Turn error.path (deque) into a dotted string for readability."""
    parts: List[str] = []
    for p in list(error.path):
        if isinstance(p, int):
            parts.append(f"[{p}]")
        else:
            if parts and parts[-1].endswith("]"):
                parts.append(f".{p}")
            else:
                parts.append(p if not parts else f".{p}")
    return "".join(parts) or "(root)"

def validate_file(validator: Draft202012Validator, file_path: Path) -> List[str]:
    data = load_json(file_path)
    errors: List[str] = []
    for error in validator.iter_errors(data):
        location = dotted_path(error)
        # Keep messages concise
        msg = error.message
        errors.append(f"{file_path.name}: {location}: {msg}")
    return errors

def main():
    parser = argparse.ArgumentParser(description="Validate PS-Wiki term JSON files against schema.")
    parser.add_argument("--dir", type=Path, default=DEFAULT_DIR, help="Directory with term JSON files")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Path to term.schema.json")
    parser.add_argument("--fail-fast", action="store_true", help="Stop at first file with errors")
    args = parser.parse_args()

    terms_dir: Path = args.dir
    schema_path: Path = args.schema

    if not schema_path.exists():
        print(f"Schema not found at {schema_path}", file=sys.stderr)
        sys.exit(2)
    if not terms_dir.exists():
        print(f"Terms directory not found at {terms_dir}", file=sys.stderr)
        sys.exit(2)

    try:
        schema: Dict[str, Any] = load_json(schema_path)
        validator = Draft202012Validator(schema)
    except Exception as e:
        print(f"Failed to load/compile schema: {e}", file=sys.stderr)
        sys.exit(2)

    json_files = sorted(terms_dir.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in {terms_dir}")
        sys.exit(0)

    total = 0
    failed = 0
    all_errors: List[str] = []

    for fp in json_files:
        total += 1
        errs = validate_file(validator, fp)
        if errs:
            failed += 1
            all_errors.extend(errs)
            if args.fail_fast:
                break

    if all_errors:
        print("\nValidation errors:\n------------------")
        for line in all_errors:
            print(line)
        print(f"\nSummary: {failed}/{total} files failed.")
        # Non-zero exit so CI can fail the job
        sys.exit(1)
    else:
        print(f"All good: {total}/{total} files validated successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
