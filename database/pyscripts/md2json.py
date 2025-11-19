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

H3_RE = re.compile(r"^###\s+(.*)\s*$")
DCITE_RE = re.compile(r'<d-cite\s+key="([^"]+)"></d-cite>')
INCLUDE_FIG_RE = re.compile(r"{%\s*include\s+figure\.liquid")
PATH_RE = re.compile(r'path="([^"]+)"')
ZOOM_RE = re.compile(r'zoomable\s*=\s*(true|false)', re.IGNORECASE)

# ---------- utils ----------

def slugify_kebab(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "untitled"

def iso_date_from_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts).date().isoformat()

def derive_file_dates(path: Path) -> Dict[str, str]:
    st = path.stat()
    created_ts = getattr(st, "st_birthtime", None)
    if created_ts is None:  # linux fallback
        created_ts = st.st_ctime
    return {
        "created": iso_date_from_ts(created_ts),
        "last_modified": iso_date_from_ts(st.st_mtime),
    }

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

def extract_figures_from_section(lines: List[str], start_idx: int) -> (Optional[Figure], int):
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
            zoomable = (mz.group(1).lower() == "true")
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
        caption_md = lines[k].rstrip()
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
    fig = Figure(path=path, caption_md=caption_md, zoomable=zoomable, source_keys=source_keys)
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
            blocks.append(Section(
                order=1, id="section-1", title="", type="note",
                source_keys=[], page=None, body_md=content + "\n", figures=[]
            ))
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
            if INCLUDE_FIG_RE.search(line) or line.strip().startswith('<div class="row'):
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

        blocks.append(Section(
            order=order,
            id=sec_id,
            title=title,
            type=sec_type,
            source_keys=sorted(set(source_keys)),
            page=page,
            body_md=body_md_block,
            figures=figures,
        ))

    return blocks

# ---------- main conversion ----------

def build_json_from_md(md_path: Path, override_id: Optional[str] = None) -> Dict[str, Any]:
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
                        {"figures": [
                            {
                                "path": f.path,
                                "caption_md": f.caption_md,
                                "zoomable": f.zoomable,
                                "source_keys": f.source_keys,
                            } for f in s.figures
                        ]}
                        if s.figures else {}
                    ),
                }
                for s in sections
            ]
        },
    }

    return term

# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser(description="Standardize one Jekyll term .md into JSON.")
    ap.add_argument("-i", "--input", required=True, help="Path to the term Markdown file.")
    ap.add_argument("-o", "--output", required=True, help="Path to write the JSON file.")
    ap.add_argument("--id", help="Override JSON 'id' (otherwise derived from title).")
    args = ap.parse_args()

    md_path = Path(args.input)
    out_path = Path(args.output)

    if not md_path.exists():
        print(f"ERROR: Markdown file not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    try:
        term = build_json_from_md(md_path, override_id=args.id)
    except Exception as e:
        print(f"ERROR: Failed to convert {md_path.name}: {e}", file=sys.stderr)
        sys.exit(1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(term, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote: {out_path}")

if __name__ == "__main__":
    main()
