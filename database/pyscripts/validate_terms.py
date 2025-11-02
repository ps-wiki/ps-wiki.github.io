#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validate ps-wiki JSON terms for basic consistency.

Checks per file:
- JSON is readable.
- Filename stem == term["id"] (kebab-case).
- Required top-level fields exist & types look right.
- version matches SemVer; breaking is bool.
- dates.created / dates.last_modified are YYYY-MM-DD and last_modified >= created.
- authors is a list of objects with at least "name".
- content.sections is a non-empty list.
  - order: int >= 1, unique, strictly increasing.
  - title: non-empty string.
  - type ∈ {"definition","note","example","other"}.
  - source_keys: list[str].
  - page: absent | string | null.
  - body_md: string (can be empty).
  - figures: list with objects having {path, caption_md, zoomable?, source_keys?}.
- related: each id has a corresponding JSON file (warning if missing).

Options:
  --json-dir    directory containing JSON files (default: database/json)
  --wiki-dir    directory with .md (optional: only used to warn if missing output)
  --fail-fast   stop on first error

Exit code: 0 on success, 1 if any errors.

Usage:
  python database/pyscripts/validate_terms.py --json-dir database/json --wiki-dir _wiki
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SECTION_TYPES = {"definition", "note", "example", "other"}

def is_iso_date(s: str) -> bool:
    if not isinstance(s, str) or not DATE_RE.match(s):
        return False
    try:
        y, m, d = map(int, s.split("-"))
        _ = date(y, m, d)
        return True
    except Exception:
        return False

def load_json(p: Path) -> Dict[str, Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def check_filename_matches_id(path: Path, data: Dict[str, Any], errs: List[str]):
    stem = path.stem
    term_id = data.get("id")
    if not isinstance(term_id, str) or not term_id:
        errs.append("missing or invalid 'id'")
        return
    if stem != term_id:
        errs.append(f"filename/id mismatch: filename='{stem}' id='{term_id}'")

def check_required_top_level(data: Dict[str, Any], errs: List[str]):
    for key in ["title", "description", "version", "breaking", "dates", "content"]:
        if key not in data:
            errs.append(f"missing required top-level key '{key}'")

    if "version" in data and not (isinstance(data["version"], str) and SEMVER_RE.match(data["version"])):
        errs.append("version must be SemVer like '1.0.0'")

    if "breaking" in data and not isinstance(data["breaking"], bool):
        errs.append("breaking must be boolean")

    # authors (optional but if present must be list of objects with name)
    authors = data.get("authors", [])
    if authors is not None and not isinstance(authors, list):
        errs.append("authors must be a list")
    else:
        for i, a in enumerate(authors or []):
            if not isinstance(a, dict) or not isinstance(a.get("name"), str) or not a.get("name"):
                errs.append(f"authors[{i}] must have non-empty 'name'")

def check_dates(data: Dict[str, Any], errs: List[str]):
    dates = data.get("dates", {})
    if not isinstance(dates, dict):
        errs.append("dates must be an object with 'created' and 'last_modified'")
        return
    created = dates.get("created")
    lastmod = dates.get("last_modified")
    if not (isinstance(created, str) and is_iso_date(created)):
        errs.append("dates.created must be YYYY-MM-DD")
    if not (isinstance(lastmod, str) and is_iso_date(lastmod)):
        errs.append("dates.last_modified must be YYYY-MM-DD")
    # order check
    if isinstance(created, str) and isinstance(lastmod, str) and is_iso_date(created) and is_iso_date(lastmod):
        if lastmod < created:
            errs.append(f"dates.last_modified ('{lastmod}') earlier than dates.created ('{created}')")

def ensure_list_of_str(name: str, v: Any, errs: List[str]) -> List[str]:
    if v is None:
        return []
    if not isinstance(v, list):
        errs.append(f"{name} must be a list")
        return []
    bad = [x for x in v if not isinstance(x, str)]
    if bad:
        errs.append(f"{name} must contain only strings")
    return [x for x in v if isinstance(x, str)]

def check_sections(data: Dict[str, Any], errs: List[str]):
    content = data.get("content", {})
    if not isinstance(content, dict):
        errs.append("content must be an object")
        return
    sections = content.get("sections")
    if not isinstance(sections, list) or not sections:
        errs.append("content.sections must be a non-empty list")
        return

    seen_orders: List[int] = []
    prev = 0
    for idx, s in enumerate(sections):
        if not isinstance(s, dict):
            errs.append(f"sections[{idx}] must be an object")
            continue
        # order
        order = s.get("order")
        if not isinstance(order, int) or order < 1:
            errs.append(f"sections[{idx}].order must be integer >= 1")
        else:
            if order in seen_orders:
                errs.append(f"sections[{idx}].order duplicates an earlier section (order={order})")
            if prev and order <= prev:
                errs.append(f"sections[{idx}].order must be strictly increasing (prev={prev}, got={order})")
            seen_orders.append(order)
            prev = order
        # title
        if not isinstance(s.get("title"), str):
            errs.append(f"sections[{idx}].title must be string")
        # type
        t = s.get("type")
        if t not in SECTION_TYPES:
            errs.append(f"sections[{idx}].type must be one of {sorted(SECTION_TYPES)}")
        # source_keys
        ensure_list_of_str(f"sections[{idx}].source_keys", s.get("source_keys", []), errs)
        # page
        page = s.get("page", None)
        if page is not None and not isinstance(page, str):
            errs.append(f"sections[{idx}].page must be string or null")
        # body_md
        if not isinstance(s.get("body_md", ""), str):
            errs.append(f"sections[{idx}].body_md must be string")
        # figures
        figs = s.get("figures", [])
        if figs is not None:
            if not isinstance(figs, list):
                errs.append(f"sections[{idx}].figures must be a list if present")
            else:
                for j, f in enumerate(figs):
                    if not isinstance(f, dict):
                        errs.append(f"sections[{idx}].figures[{j}] must be object")
                        continue
                    if not isinstance(f.get("path"), str) or not f.get("path"):
                        errs.append(f"sections[{idx}].figures[{j}].path must be non-empty string")
                    if not isinstance(f.get("caption_md", ""), str):
                        errs.append(f"sections[{idx}].figures[{j}].caption_md must be string")
                    if "zoomable" in f and not isinstance(f.get("zoomable"), bool):
                        errs.append(f"sections[{idx}].figures[{j}].zoomable must be boolean when present")
                    ensure_list_of_str(f"sections[{idx}].figures[{j}].source_keys", f.get("source_keys", []), errs)

def warn_related_exist(data: Dict[str, Any], json_index: Dict[str, Path], warns: List[str]):
    related = data.get("related", [])
    if not isinstance(related, list):
        return
    for rid in related:
        if isinstance(rid, str) and rid and rid not in json_index:
            warns.append(f"related id '{rid}' has no corresponding JSON file")

def main():
    ap = argparse.ArgumentParser(description="Validate ps-wiki JSON terms for basic consistency.")
    ap.add_argument("--json-dir", default="database/json", help="Directory containing JSON files")
    ap.add_argument("--wiki-dir", default="_wiki", help="Directory with Markdown files (optional; used for warnings)")
    ap.add_argument("--fail-fast", action="store_true", help="Stop on first error")
    args = ap.parse_args()

    json_dir = Path(args.json_dir)
    wiki_dir = Path(args.wiki_dir)

    if not json_dir.exists():
        print(f"ERROR: JSON directory not found: {json_dir}", file=sys.stderr)
        sys.exit(1)

    json_paths = sorted(p for p in json_dir.glob("*.json") if p.is_file())
    if not json_paths:
        print(f"No JSON files found in {json_dir}")
        sys.exit(0)

    # Index of ids -> path, for related checks
    id_index: Dict[str, Path] = {}
    for p in json_paths:
        try:
            data = load_json(p)
            tid = data.get("id") if isinstance(data, dict) else None
            if isinstance(tid, str) and tid:
                id_index[tid] = p
        except Exception:
            # ignore parse errors here; they’ll be caught in the real pass
            pass

    total = 0
    errors = 0
    warnings = 0

    for path in json_paths:
        total += 1
        errs: List[str] = []
        warns: List[str] = []
        try:
            data = load_json(path)
        except Exception as e:
            errors += 1
            print(f"[ERROR] {path.name}: cannot parse JSON ({e})")
            if args.fail_fast:
                break
            else:
                continue

        # core checks
        check_filename_matches_id(path, data, errs)
        check_required_top_level(data, errs)
        check_dates(data, errs)
        # optional list type checks
        _ = ensure_list_of_str("tags", data.get("tags", []), errs)
        _ = ensure_list_of_str("related", data.get("related", []), errs)
        check_sections(data, errs)
        warn_related_exist(data, id_index, warns)

        # optional: warn if no corresponding md (only a warning)
        term_id = data.get("id")
        if isinstance(term_id, str) and term_id:
            md_path = wiki_dir / f"{term_id}.md"
            if not md_path.exists():
                warns.append(f"no corresponding Markdown: {md_path}")

        if errs:
            errors += 1
            print(f"[ERROR] {path.name}:")
            for e in errs:
                print(f"  - {e}")
            if args.fail_fast:
                break

        if warns:
            warnings += len(warns)
            print(f"[WARN ] {path.name}:")
            for w in warns:
                print(f"  - {w}")

        if not errs and not warns:
            print(f"[OK   ] {path.name}")

    print("\nSummary")
    print(f"  Files checked : {total}")
    print(f"  Errors        : {errors}")
    print(f"  Warnings      : {warnings}")

    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
