#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unified workflow script for processing PS-Wiki terms.

This script provides a complete pipeline for:
1. Formatting Markdown files (MD → JSON → MD roundtrip)
2. Converting Markdown to JSON
3. Adding schema references
4. Validating against JSON schema
5. Building index files for API

Processing Philosophy:
- Format & Convert: Always run (keeps files in sync)
- Validate: Optional (checking only, use --no-validate to skip)
- Index: Always run (or use --index-only to build just the index)

Usage:
    # Process all terms (default - full pipeline)
    python database/pyscripts/process.py

    # Process specific terms by ID
    python database/pyscripts/process.py --terms stability frequency-control

    # Build index files only (skip term processing)
    python database/pyscripts/process.py --index-only

    # Skip validation for faster processing
    python database/pyscripts/process.py --no-validate

    # Dry-run mode (show what would be done)
    python database/pyscripts/process.py --dry-run

    # Verbose output
    python database/pyscripts/process.py --verbose
"""

import argparse
import sys
from pathlib import Path
from typing import List
from collections import Counter
from datetime import datetime, timezone

# Import from existing scripts and shared utilities
from md2json import build_json_from_md
from json2md import convert_term_to_md
from utils import (
    DEFAULT_WIKI_DIR,
    DEFAULT_JSON_DIR,
    DEFAULT_SCHEMA_PATH,
    DEFAULT_BUILD_DIR,
    load_json,
    load_term_json,
    write_json,
    write_if_changed,
    validate_term_schema,
    ensure_schema_reference,
    ProgressReporter,
    Colors,
)


# ---------- Pipeline Steps ----------


def format_markdown(md_path: Path, json_dir: Path, dry_run: bool = False) -> bool:
    """
    Format a Markdown file via MD → JSON → MD roundtrip.

    Args:
        md_path: Path to Markdown file
        json_dir: Directory for JSON files (for field preservation)
        dry_run: If True, don't actually write files

    Returns:
        True if successful, False otherwise
    """
    try:
        # Determine corresponding JSON path for field preservation
        term_id = md_path.stem
        json_path = json_dir / f"{term_id}.json"

        # Convert to JSON (in memory, with field preservation)
        term_json = build_json_from_md(md_path, override_id=None, json_path=json_path)

        # Normalize fields
        term_json.setdefault("tags", [])
        term_json.setdefault("related", [])
        term_json.setdefault("authors", [])
        term_json.setdefault("dates", {})

        # Convert back to Markdown
        formatted_md = convert_term_to_md(term_json)

        # Write if changed (unless dry-run)
        if not dry_run:
            write_if_changed(md_path, formatted_md)
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
        json_path = json_dir / f"{md_path.stem}.json"
        term_json = build_json_from_md(md_path, override_id=None, json_path=json_path)

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
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
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
        if not format_markdown(md_path, json_dir, dry_run):
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
        description="Process PS-Wiki terms through the complete pipeline.",
        epilog="Examples:\n"
        "  All terms:        %(prog)s\n"
        "  Specific terms:   %(prog)s --terms stability frequency-control\n"
        "  Index only:       %(prog)s --index-only\n"
        "  Skip validation:  %(prog)s --no-validate\n"
        "  Dry run:          %(prog)s --dry-run --verbose",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Term selection arguments
    parser.add_argument(
        "--terms",
        nargs="+",
        help="Process specific terms by ID",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Explicitly process all terms (default behavior)",
    )

    # Directory arguments
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

    # Behavior flags
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Only build index files (skip term processing)",
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
        "--no-validate",
        action="store_true",
        help="Skip validation step (checking only)",
    )

    args = parser.parse_args()

    # Handle index-only mode
    if args.index_only:
        print(Colors.info(f"\n{'='*60}"))
        print(Colors.info(f"Building Index Files Only"))
        print(Colors.info(f"{'='*60}\n"))

        if not args.json_dir.exists():
            print(
                Colors.error(f"ERROR: JSON directory not found: {args.json_dir}"),
                file=sys.stderr,
            )
            sys.exit(1)

        if build_index_files(args.json_dir, args.build_dir, args.dry_run):
            print(Colors.success("\n✓ Index files built successfully!"))
            sys.exit(0)
        else:
            print(Colors.error("\n✗ Index build failed"))
            sys.exit(1)

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

    # Get list of Markdown files to process
    if args.terms:
        # Process specific terms
        md_files = []
        for term_id in args.terms:
            md_file = args.wiki_dir / f"{term_id}.md"
            if not md_file.exists():
                print(
                    Colors.error(f"ERROR: Markdown file not found: {md_file}"),
                    file=sys.stderr,
                )
                sys.exit(1)
            md_files.append(md_file)
        md_files = sorted(md_files)
    else:
        # Process all files (default or --all)
        md_files = sorted(args.wiki_dir.glob("*.md"))

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
            skip_format=False,  # Always format
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

    # Build index files (always run unless dry-run)
    if not args.dry_run:
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
