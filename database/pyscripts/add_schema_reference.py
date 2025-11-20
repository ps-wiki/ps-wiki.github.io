#!/usr/bin/env python3
"""
Add $schema field to all JSON files in database/json
if it doesn't already exist.

Usage:
    python database/pyscripts/add_schema_reference.py
"""

import json
from pathlib import Path

# Adjust if needed
BASE_DIR = Path(__file__).resolve().parent.parent / "json"
SCHEMA_URL = "https://ps-wiki.github.io/schema/v1/term.schema.json"


def main():
    updated = 0
    skipped = 0

    for file in sorted(BASE_DIR.glob("*.json")):
        try:
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[!] Failed to read {file.name}: {e}")
            continue

        if "$schema" in data:
            skipped += 1
            continue

        data = {"$schema": SCHEMA_URL, **data}

        try:
            with file.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            updated += 1
        except Exception as e:
            print(f"[!] Failed to write {file.name}: {e}")

    print(
        f"✔ Added $schema to {updated} file(s). Skipped {skipped} already containing it."
    )


if __name__ == "__main__":
    main()
