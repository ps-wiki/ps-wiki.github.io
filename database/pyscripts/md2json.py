#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert a single Jekyll term Markdown file into the lean JSON term format.

Rules:
- Parse YAML front matter for: title, description, tags, related, authors, date, lastmod.
- Body is split into sections by '### ' headings (H3).
- For each section block:
  - Extract figure blocks that contain '{% include figure.liquid ... %}' inside the <div class="row mt-3"> wrapper.
  - Extract a 'Source:' line with one or more '<d-cite key="..."></d-cite>' tags; trailing text on that same line becomes 'page'.
  - Remaining text is 'body_md' verbatim.
  - Section 'type' is 'definition' if the first non-empty body line starts with '>'; otherwise 'note'.
- Defaults:
  - tags/related/authors -> [] when missing.
  - dates.created / dates.last_modified -> derived from file timestamps if missing.

Usage:
  python database/pyscripts/md2json.py -i _wiki/automatic-generation-control.md -o database/json/automatic-generation-control.json
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, date as date_cls
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

# Import shared constants and utilities from utils module
from utils import (
    DEFAULT_WIKI_DIR,
    DEFAULT_JSON_DIR,
    SCHEMA_URL,
    json_content_differs,
    iso_date_from_ts,
    derive_file_dates,
)


H3_RE = re.compile(r"^###\s+(.*)\s*$")
DCITE_RE = re.compile(r'<d-cite\s+key="([^"]+)"></d-cite>')
INCLUDE_FIG_RE = re.compile(r"{%\s*include\s+figure\.liquid")
PATH_RE = re.compile(r'path="([^"]+)"')
ZOOM_RE = re.compile(r"zoomable\s*=\s*(true|false)", re.IGNORECASE)

# ---------- utils ----------


def slugify_kebab(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "untitled"


def load_existing_json(json_path: Path) -> Optional[Dict[str, Any]]:
    """Load existing JSON file if it exists, return None otherwise."""
    if not json_path.exists():
        return None
    try:
        return json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(
            f"WARNING: Failed to load existing JSON {json_path}: {e}", file=sys.stderr
        )
        return None


def merge_preserved_fields(
    new_term: Dict[str, Any], existing_term: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Merge fields from existing JSON that should be preserved.

    Preserved fields (not derived from Markdown):
    - $schema: schema reference URL
    - aliases: alternative names for the term
    """
    if existing_term is None:
        return new_term

    # Preserve $schema if it exists in the old version
    if "$schema" in existing_term and "$schema" not in new_term:
        new_term["$schema"] = existing_term["$schema"]

    # Preserve aliases if it exists in the old version
    if "aliases" in existing_term and "aliases" not in new_term:
        new_term["aliases"] = existing_term["aliases"]

    return new_term


def coerce_date_str(v: Any) -> str:
    """Return an ISO YYYY-MM-DD string for date-like values; empty string otherwise."""
    if isinstance(v, datetime):
        return v.date().isoformat()
    if isinstance(v, date_cls):
        return v.isoformat()
    if isinstance(v, str):
        return v.strip()
    return ""


def ensure_list(v: Any) -> List[Any]:
    """Normalize YAML field that may be missing/None/singleton into a list."""
    if v is None:
        return []
    if isinstance(v, list):
        return v
    # If someone wrote a single string instead of a list
    return [v]


# ---------- parsing front matter ----------


def split_front_matter(text: str) -> (Dict[str, Any], str):
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if len(lines) < 3:
        return {}, text
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}, text
    fm_text = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1 :]) + ("\n" if text.endswith("\n") else "")
    try:
        fm = yaml.safe_load(fm_text) or {}
        if not isinstance(fm, dict):
            fm = {}
    except Exception as e:
        print(f"WARNING: Failed to parse YAML front matter: {e}", file=sys.stderr)
        fm = {}
    return fm, body


# ---------- figure block extraction ----------


@dataclass
class Figure:
    path: str
    caption_md: str
    zoomable: bool
    source_keys: List[str]


def extract_figures_from_section(
    lines: List[str], start_idx: int
) -> (Optional[Figure], int):
    i = start_idx
    if i >= len(lines):
        return None, i
    if lines[i].strip().startswith('<div class="row'):
        i += 1

    include_idx = None
    j = i
    while j < len(lines):
        if INCLUDE_FIG_RE.search(lines[j]):
            include_idx = j
            break
        if H3_RE.match(lines[j]):
            break
        j += 1

    if include_idx is None:
        return None, start_idx

    path = ""
    zoomable = True
    k = include_idx
    found_close = False
    while k < len(lines):
        line = lines[k]
        if not path:
            m = PATH_RE.search(line)
            if m:
                path = m.group(1)
        mz = ZOOM_RE.search(line)
        if mz:
            zoomable = mz.group(1).lower() == "true"
        if "%}" in line:
            found_close = True
            k += 1
            break
        k += 1

    caption_md = ""
    while k < len(lines):
        s = lines[k].strip()
        if s == "" or s.startswith("{%"):
            k += 1
            continue
        if s.startswith("</div>"):
            break
        # Strip leading whitespace to avoid indentation drift
        caption_md = lines[k].strip()
        k += 1
        break

    while k < len(lines):
        if lines[k].strip().startswith("</div>"):
            k += 1
            if k < len(lines) and lines[k].strip().startswith("</div>"):
                k += 1
            break
        k += 1

    source_keys = DCITE_RE.findall(caption_md) if caption_md else []
    fig = Figure(
        path=path, caption_md=caption_md, zoomable=zoomable, source_keys=source_keys
    )
    return fig, (k if found_close else include_idx + 1)


# ---------- section parsing ----------


@dataclass
class Section:
    order: int
    id: str
    title: str
    type: str  # "definition" or "note" (or "other")
    source_keys: List[str]
    page: Optional[str]
    body_md: str
    figures: List[Figure]


def parse_sections(body_md: str) -> List[Section]:
    lines = body_md.splitlines()
    indices: List[int] = []
    titles: List[str] = []
    for idx, line in enumerate(lines):
        m = H3_RE.match(line)
        if m:
            indices.append(idx)
            titles.append(m.group(1).strip())

    blocks: List[Section] = []
    if not indices:
        content = body_md.strip()
        if content:
            blocks.append(
                Section(
                    order=1,
                    id="section-1",
                    title="",
                    type="note",
                    source_keys=[],
                    page=None,
                    body_md=content + "\n",
                    figures=[],
                )
            )
        return blocks

    indices.append(len(lines))
    for s_idx in range(len(indices) - 1):
        start = indices[s_idx]
        end = indices[s_idx + 1]
        title = titles[s_idx]
        raw_block = lines[start:end]

        sec_id = slugify_kebab(title) or f"section-{s_idx+1}"
        order = s_idx + 1

        content_lines = raw_block[1:]

        figures: List[Figure] = []
        cleaned: List[str] = []
        i = 0
        while i < len(content_lines):
            line = content_lines[i]
            if INCLUDE_FIG_RE.search(line) or line.strip().startswith(
                '<div class="row'
            ):
                fig, next_i = extract_figures_from_section(content_lines, i)
                if fig:
                    figures.append(fig)
                    i = next_i
                    continue
            cleaned.append(line)
            i += 1

        source_keys: List[str] = []
        page: Optional[str] = None
        cleaned2: List[str] = []
        for line in cleaned:
            # Skip standalone <br> tags to avoid accumulation
            if line.strip() == "<br>":
                continue
            if line.strip().startswith("Source:"):
                tail = line.split("Source:", 1)[1].strip()
                keys = DCITE_RE.findall(tail)
                source_keys.extend(keys)
                tail_stripped = DCITE_RE.sub("", tail).strip()
                page = tail_stripped if tail_stripped else None
            else:
                cleaned2.append(line)

        while cleaned2 and cleaned2[0].strip() == "":
            cleaned2.pop(0)
        while cleaned2 and cleaned2[-1].strip() == "":
            cleaned2.pop()

        body_md_block = "\n".join(cleaned2).rstrip()
        if body_md_block:
            body_md_block += "\n"

        sec_type = "note"
        for ln in cleaned2:
            if ln.strip():
                if ln.lstrip().startswith(">"):
                    sec_type = "definition"
                break

        blocks.append(
            Section(
                order=order,
                id=sec_id,
                title=title,
                type=sec_type,
                source_keys=sorted(set(source_keys)),
                page=page,
                body_md=body_md_block,
                figures=figures,
            )
        )

    return blocks


# ---------- main conversion ----------


def build_ordered_dict(
    term_data: Dict[str, Any], existing_term: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Build term dictionary with consistent field ordering.

    If existing_term is provided, preserve its field order.
    Otherwise, use standard schema order.

    Standard order: $schema, id, title, description, language, tags, related,
                   aliases, version, breaking, dates, authors, content

    Args:
        term_data: Dictionary with all term data
        existing_term: Optional existing JSON to preserve field order from

    Returns:
        Ordered dictionary with same data but consistent field order
    """
    # Define standard field order
    standard_order = [
        "$schema",
        "id",
        "title",
        "description",
        "language",
        "tags",
        "related",
        "aliases",
        "version",
        "breaking",
        "dates",
        "authors",
        "content",
    ]

    # If we have an existing term, use its field order
    if existing_term:
        # Get the order from existing term, then add any new fields
        existing_keys = list(existing_term.keys())
        new_keys = [k for k in term_data.keys() if k not in existing_keys]
        field_order = existing_keys + new_keys
    else:
        # Use standard order, then add any extra fields
        field_order = [k for k in standard_order if k in term_data]
        extra_keys = [k for k in term_data.keys() if k not in standard_order]
        field_order.extend(extra_keys)

    # Build ordered dictionary
    ordered = {}
    for key in field_order:
        if key in term_data:
            ordered[key] = term_data[key]

    return ordered


def build_json_from_md(
    md_path: Path, override_id: Optional[str] = None, json_path: Optional[Path] = None
) -> Dict[str, Any]:
    text = md_path.read_text(encoding="utf-8")

    front, body = split_front_matter(text)
    title = (front.get("title") or "").strip()
    description = (front.get("description") or "").strip()
    version = (front.get("version") or "1.0.0").strip()
    tags = ensure_list(front.get("tags"))
    related = ensure_list(front.get("related"))
    authors = ensure_list(front.get("authors"))

    # Coerce dates to strings first (handles datetime/date objects from YAML)
    created_str = coerce_date_str(front.get("date"))
    lastmod_str = coerce_date_str(front.get("lastmod"))

    file_dates = derive_file_dates(md_path)
    if not created_str:
        created_str = file_dates["created"]
    if not lastmod_str:
        lastmod_str = file_dates["last_modified"]

    term_id = override_id or slugify_kebab(title) or md_path.stem
    sections = parse_sections(body)

    term: Dict[str, Any] = {
        "id": term_id,
        "title": title,
        "description": description,
        "language": "en",
        "tags": tags,
        "related": related,
        "version": version,
        "breaking": False,
        "dates": {"created": created_str, "last_modified": lastmod_str},
        "authors": authors,
        "content": {
            "sections": [
                {
                    "order": s.order,
                    "id": s.id,
                    "title": s.title,
                    "type": s.type,
                    "source_keys": s.source_keys,
                    "page": s.page,
                    "body_md": s.body_md,
                    **(
                        {
                            "figures": [
                                {
                                    "path": f.path,
                                    "caption_md": f.caption_md,
                                    "zoomable": f.zoomable,
                                    "source_keys": f.source_keys,
                                }
                                for f in s.figures
                            ]
                        }
                        if s.figures
                        else {}
                    ),
                }
                for s in sections
            ]
        },
    }

    # Load existing term for field preservation and ordering
    existing_term = None
    if json_path:
        existing_term = load_existing_json(json_path)

    # Preserve fields from existing JSON
    if existing_term:
        term = merge_preserved_fields(term, existing_term)

    # Always ensure $schema is present
    if "$schema" not in term:
        # SCHEMA_URL is imported from utils, or uses a fallback
        term["$schema"] = SCHEMA_URL

    # Apply consistent field ordering
    term = build_ordered_dict(term, existing_term)

    return term


# ---------- CLI ----------


def main():
    ap = argparse.ArgumentParser(
        description="Convert Jekyll term Markdown file(s) to JSON.",
        epilog="Examples:\n"
        "  Single file:  %(prog)s -i _wiki/stability.md -o database/json/stability.json\n"
        "  By term ID:   %(prog)s --terms stability frequency-control\n"
        "  All files:    %(prog)s --all\n"
        "  With force:   %(prog)s --all --force",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Single-file mode arguments
    ap.add_argument(
        "-i", "--input", help="Path to the term Markdown file (single-file mode)."
    )
    ap.add_argument(
        "-o", "--output", help="Path to write the JSON file (single-file mode)."
    )
    ap.add_argument("--id", help="Override JSON 'id' (otherwise derived from title).")

    # Multi-term mode arguments
    ap.add_argument(
        "--terms", nargs="+", help="Process specific terms by ID (multi-term mode)."
    )
    ap.add_argument(
        "--all",
        action="store_true",
        help="Process all Markdown files in wiki directory.",
    )

    # Directory arguments (used in multi-term mode)
    ap.add_argument(
        "--wiki-dir",
        type=Path,
        default=DEFAULT_WIKI_DIR,
        help="Directory with Markdown files (default: _wiki).",
    )
    ap.add_argument(
        "--json-dir",
        type=Path,
        default=DEFAULT_JSON_DIR,
        help="Output directory for JSON files (default: database/json).",
    )

    # Behavior flags
    ap.add_argument(
        "--force", action="store_true", help="Force write even if content is identical."
    )

    args = ap.parse_args()

    # Validate argument combinations
    single_file_mode = args.input or args.output
    multi_term_mode = args.terms or args.all

    if single_file_mode and multi_term_mode:
        print(
            "ERROR: Cannot use both single-file mode (-i/-o) and multi-term mode (--terms/--all).",
            file=sys.stderr,
        )
        sys.exit(1)

    if single_file_mode and not (args.input and args.output):
        print(
            "ERROR: Both -i/--input and -o/--output are required for single-file mode.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not single_file_mode and not multi_term_mode:
        print(
            "ERROR: Must specify either -i/-o (single-file mode) or --terms/--all (multi-term mode).",
            file=sys.stderr,
        )
        ap.print_help()
        sys.exit(1)

    # Single-file mode
    if single_file_mode:
        md_path = Path(args.input)
        out_path = Path(args.output)

        if not md_path.exists():
            print(f"ERROR: Markdown file not found: {md_path}", file=sys.stderr)
            sys.exit(1)

        try:
            term = build_json_from_md(md_path, override_id=args.id, json_path=out_path)
        except Exception as e:
            print(f"ERROR: Failed to convert {md_path.name}: {e}", file=sys.stderr)
            sys.exit(1)

        # Check if content differs (unless --force)
        if not args.force and not json_content_differs(out_path, term):
            print(f"SKIP   {md_path.name} (content identical)")
            return

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(term, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"WROTE  {out_path}")
        return

    # Multi-term mode
    if not args.wiki_dir.exists():
        print(f"ERROR: Wiki directory not found: {args.wiki_dir}", file=sys.stderr)
        sys.exit(1)

    args.json_dir.mkdir(parents=True, exist_ok=True)

    # Get list of terms to process
    if args.all:
        # Process all .md files in wiki directory
        md_files = sorted(args.wiki_dir.glob("*.md"))
        term_ids = [f.stem for f in md_files]
        if not term_ids:
            print(f"No Markdown files found in {args.wiki_dir}", file=sys.stderr)
            sys.exit(0)
    else:
        # Process specific terms
        term_ids = args.terms

    total = 0
    written = 0
    skipped = 0
    errors = 0

    for term_id in term_ids:
        total += 1
        md_path = args.wiki_dir / f"{term_id}.md"
        out_path = args.json_dir / f"{term_id}.json"

        if not md_path.exists():
            print(
                f"ERROR  {term_id}: Markdown file not found: {md_path}", file=sys.stderr
            )
            errors += 1
            continue

        try:
            term = build_json_from_md(md_path, override_id=None, json_path=out_path)

            # Check if content differs (unless --force)
            if not args.force and not json_content_differs(out_path, term):
                print(f"SKIP   {term_id}.md -> {term_id}.json (content identical)")
                skipped += 1
                continue

            out_path.write_text(
                json.dumps(term, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            print(f"WROTE  {term_id}.md -> {term_id}.json")
            written += 1
        except Exception as e:
            print(f"ERROR  {term_id}: {e}", file=sys.stderr)
            errors += 1

    # Print summary for multi-term mode
    print(f"\nSummary:")
    print(f"  Total terms : {total}")
    print(f"  Written     : {written}")
    print(f"  Skipped     : {skipped}")
    print(f"  Errors      : {errors}")

    if errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
