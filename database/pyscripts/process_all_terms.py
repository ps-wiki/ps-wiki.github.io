#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unified workflow script for processing all PS-Wiki terms.

This script provides a complete pipeline for:
1. Formatting Markdown files (MD → JSON → MD roundtrip)
2. Converting Markdown to JSON
3. Adding schema references
4. Validating against JSON schema
5. Building index files for API

Usage:
    # Process all terms (full pipeline)
    python database/pyscripts/process_all_terms.py

    # Dry-run mode (show what would be done)
    python database/pyscripts/process_all_terms.py --dry-run

    # Verbose output
    python database/pyscripts/process_all_terms.py --verbose

    # Process only specific terms
    python database/pyscripts/process_all_terms.py --only stability frequency-control

    # Skip certain steps
    python database/pyscripts/process_all_terms.py --no-validate --no-index
"""

import argparse
import sys
from pathlib import Path
from typing import List, Set

# Import from existing scripts
try:
    from md2json import build_json_from_md
    from json2md import convert_term_to_md
    from utils import (
        load_term_json,
        write_json,
        write_if_changed,
        validate_term_schema,
        ensure_schema_reference,
        ProgressReporter,
        Colors,
    )
except ImportError as e:
    print(f"ERROR: Failed to import required modules: {e}", file=sys.stderr)
    print(
        "Ensure md2json.py, json2md.py, and utils.py are in the same directory.",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------- Configuration ----------

DEFAULT_WIKI_DIR = Path("_wiki")
DEFAULT_JSON_DIR = Path("database/json")
DEFAULT_SCHEMA_PATH = Path("database/schema/v1/term.schema.json")
DEFAULT_BUILD_DIR = Path("database/build")


# ---------- Pipeline Steps ----------


def format_markdown(md_path: Path, dry_run: bool = False) -> bool:
    """
    Format a Markdown file via MD → JSON → MD roundtrip.

    Args:
        md_path: Path to Markdown file
        dry_run: If True, don't actually write files

    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert to JSON (in memory)
        term_json = build_json_from_md(md_path, override_id=None)

        # Normalize fields
        term_json.setdefault("tags", [])
        term_json.setdefault("related", [])
        term_json.setdefault("authors", [])
        term_json.setdefault("dates", {})

        # Convert back to Markdown
        formatted_md = convert_term_to_md(term_json)

        # Write if changed (unless dry-run)
        if not dry_run:
            changed = write_if_changed(md_path, formatted_md)
            return True
        return True
    except Exception as e:
        print(Colors.error(f"  Format failed: {e}"), file=sys.stderr)
        return False


def convert_to_json(md_path: Path, json_dir: Path, dry_run: bool = False) -> bool:
    """
    Convert Markdown file to JSON.

    Args:
        md_path: Path to Markdown file
        json_dir: Output directory for JSON
        dry_run: If True, don't actually write files

    Returns:
        True if successful, False otherwise
    """
    try:
        term_json = build_json_from_md(md_path, override_id=None)
        term_id = term_json.get("id", md_path.stem)
        json_path = json_dir / f"{term_id}.json"

        if not dry_run:
            write_json(json_path, term_json)
        return True
    except Exception as e:
        print(Colors.error(f"  Conversion failed: {e}"), file=sys.stderr)
        return False


def add_schema_ref(json_path: Path, dry_run: bool = False) -> bool:
    """
    Add $schema reference to JSON file if missing.

    Args:
        json_path: Path to JSON file
        dry_run: If True, don't actually write files

    Returns:
        True if successful, False otherwise
    """
    try:
        term_json = load_term_json(json_path)

        if "$schema" in term_json:
            return True  # Already has schema

        term_json = ensure_schema_reference(term_json)

        if not dry_run:
            write_json(json_path, term_json)
        return True
    except Exception as e:
        print(Colors.error(f"  Schema ref failed: {e}"), file=sys.stderr)
        return False


def validate_json(json_path: Path, schema_path: Path) -> List[str]:
    """
    Validate JSON file against schema.

    Args:
        json_path: Path to JSON file
        schema_path: Path to schema file

    Returns:
        List of validation errors (empty if valid)
    """
    try:
        term_json = load_term_json(json_path)
        return validate_term_schema(term_json, schema_path)
    except Exception as e:
        return [f"Failed to load: {e}"]


def build_index_files(json_dir: Path, build_dir: Path, dry_run: bool = False) -> bool:
    """
    Build index.json and tags.json for API.

    Args:
        json_dir: Directory with term JSON files
        build_dir: Output directory for index files
        dry_run: If True, don't actually write files

    Returns:
        True if successful, False otherwise
    """
    try:
        from collections import Counter
        from datetime import datetime

        items = []
        tags_counter = Counter()

        for json_path in sorted(json_dir.glob("*.json")):
            try:
                term = load_term_json(json_path)
                item = {
                    "id": term["id"],
                    "title": term["title"],
                    "summary": term.get("description", ""),
                    "tags": term.get("tags", []),
                    "updated_at": term.get("dates", {}).get("last_modified", ""),
                }
                items.append(item)
                tags_counter.update(item["tags"])
            except Exception as e:
                print(
                    Colors.warning(f"  Skipping {json_path.name}: {e}"), file=sys.stderr
                )

        index = {
            "items": items,
            "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        tags = {
            "tags": [
                {"tag": k, "count": v}
                for k, v in sorted(tags_counter.items(), key=lambda kv: (-kv[1], kv[0]))
            ]
        }

        if not dry_run:
            build_dir.mkdir(parents=True, exist_ok=True)
            write_json(build_dir / "index.json", index)
            write_json(build_dir / "tags.json", tags)

        return True
    except Exception as e:
        print(Colors.error(f"Index build failed: {e}"), file=sys.stderr)
        return False


# ---------- Main Pipeline ----------


def process_term(
    md_path: Path,
    json_dir: Path,
    schema_path: Path,
    dry_run: bool = False,
    skip_format: bool = False,
    skip_validate: bool = False,
) -> dict:
    """
    Process a single term through the pipeline.

    Args:
        md_path: Path to Markdown file
        json_dir: Output directory for JSON
        schema_path: Path to schema file
        dry_run: If True, don't actually write files
        skip_format: If True, skip formatting step
        skip_validate: If True, skip validation step

    Returns:
        Dictionary with processing results
    """
    result = {
        "term_id": md_path.stem,
        "success": True,
        "errors": [],
        "warnings": [],
    }

    # Step 1: Format Markdown
    if not skip_format:
        if not format_markdown(md_path, dry_run):
            result["success"] = False
            result["errors"].append("Formatting failed")
            return result

    # Step 2: Convert to JSON
    if not convert_to_json(md_path, json_dir, dry_run):
        result["success"] = False
        result["errors"].append("Conversion failed")
        return result

    # Step 3: Add schema reference
    term_id = md_path.stem
    json_path = json_dir / f"{term_id}.json"

    if not dry_run:  # Only if file exists
        if not add_schema_ref(json_path, dry_run):
            result["warnings"].append("Schema ref failed")

    # Step 4: Validate
    if not skip_validate and not dry_run:
        errors = validate_json(json_path, schema_path)
        if errors:
            result["success"] = False
            result["errors"].extend(errors)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Process all PS-Wiki terms through the complete pipeline."
    )
    parser.add_argument(
        "--wiki-dir",
        type=Path,
        default=DEFAULT_WIKI_DIR,
        help=f"Directory with Markdown files (default: {DEFAULT_WIKI_DIR})",
    )
    parser.add_argument(
        "--json-dir",
        type=Path,
        default=DEFAULT_JSON_DIR,
        help=f"Output directory for JSON files (default: {DEFAULT_JSON_DIR})",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help=f"Path to JSON schema (default: {DEFAULT_SCHEMA_PATH})",
    )
    parser.add_argument(
        "--build-dir",
        type=Path,
        default=DEFAULT_BUILD_DIR,
        help=f"Output directory for index files (default: {DEFAULT_BUILD_DIR})",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        help="Process only specific terms (by ID)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show verbose output",
    )
    parser.add_argument(
        "--no-format",
        action="store_true",
        help="Skip Markdown formatting step",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip validation step",
    )
    parser.add_argument(
        "--no-index",
        action="store_true",
        help="Skip index building step",
    )

    args = parser.parse_args()

    # Validate paths
    if not args.wiki_dir.exists():
        print(
            Colors.error(f"ERROR: Wiki directory not found: {args.wiki_dir}"),
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.no_validate and not args.schema.exists():
        print(
            Colors.error(f"ERROR: Schema file not found: {args.schema}"),
            file=sys.stderr,
        )
        sys.exit(1)

    # Find Markdown files
    md_files = sorted(args.wiki_dir.glob("*.md"))

    # Filter if --only specified
    if args.only:
        only_set = set(args.only)
        md_files = [f for f in md_files if f.stem in only_set]

    if not md_files:
        print(Colors.warning("No Markdown files found to process."))
        sys.exit(0)

    # Print header
    print(Colors.info(f"\n{'='*60}"))
    print(Colors.info(f"PS-Wiki Term Processing Pipeline"))
    print(Colors.info(f"{'='*60}\n"))

    if args.dry_run:
        print(Colors.warning("DRY RUN MODE - No files will be modified\n"))

    print(f"Found {len(md_files)} term(s) to process\n")

    # Process each term
    progress = ProgressReporter(len(md_files), verbose=args.verbose)
    results = []

    for md_path in md_files:
        term_id = md_path.stem

        if args.verbose:
            print(f"\nProcessing: {Colors.info(term_id)}")

        result = process_term(
            md_path,
            args.json_dir,
            args.schema,
            dry_run=args.dry_run,
            skip_format=args.no_format,
            skip_validate=args.no_validate,
        )

        results.append(result)

        # Update progress
        if result["success"]:
            progress.update("OK", term_id)
        else:
            progress.update("ERROR", f"{term_id}: {', '.join(result['errors'])}")
            for error in result["errors"]:
                print(Colors.error(f"    {error}"))

        if result["warnings"]:
            for warning in result["warnings"]:
                print(Colors.warning(f"    {warning}"))

    # Build index files
    if not args.no_index and not args.dry_run:
        print(f"\n{Colors.info('Building index files...')}")
        if build_index_files(args.json_dir, args.build_dir, args.dry_run):
            print(Colors.success("✓ Index files built successfully"))
        else:
            print(Colors.error("✗ Index build failed"))

    # Print summary
    print(f"\n{Colors.info('='*60)}")
    print(Colors.info("Summary"))
    print(Colors.info("=" * 60))

    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful

    print(f"Total terms: {len(results)}")
    print(Colors.success(f"Successful: {successful}"))
    if failed > 0:
        print(Colors.error(f"Failed: {failed}"))

    # Exit with error code if any failed
    if failed > 0:
        sys.exit(1)
    else:
        print(Colors.success("\n✓ All terms processed successfully!"))
        sys.exit(0)


if __name__ == "__main__":
    main()
