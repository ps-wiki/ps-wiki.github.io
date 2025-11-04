#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert a single term JSON (lean schema) into a Jekyll Markdown file.

Rules:
- Front matter: title, description, tags, related, authors{name,url}, date (created), lastmod.
- Sections sorted by `order` ascending (missing order go last).
- tags/related/authors may be missing or empty -> emit [].
- dates.created / dates.last_modified may be missing or empty -> derive 
- Each section:
  - Figures (if any) appear BEFORE text, each figure block followed by a literal <br>.
  - Then a "Source: <d-cite key="..."></d-cite>" line; append page if provided.
  - Then the section body_md verbatim.
- No new prose is introduced; body_md and caption_md are passed through as-is.

Usage:
  python database/pyscripts/json2md.py -i database/json/stability.json -o _wiki/stability.md
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


# ---------- YAML helpers (very small, purpose-built) ----------

def yaml_list_block(key: str, items: List[str], indent: int = 0) -> str:
    """Render a simple YAML list block: key:\n  - item1\n  - item2\n"""
    ind = " " * indent
    if not items:
        return f"{ind}{key}: []\n"
    lines = [f"{ind}{key}:"]
    for v in items:
        lines.append(f"{ind}  - {v}")
    return "\n".join(lines) + "\n"


def yaml_authors_block(authors: List[Dict[str, Any]], indent: int = 0) -> str:
    """Render authors:
    authors:
      - name: ...
        url: ...
    """
    ind = " " * indent
    if not authors:
        return f"{ind}authors: []\n"
    lines = [f"{ind}authors:"]
    for a in authors:
        name = a.get("name", "")
        url = a.get("url", "")
        lines.append(f"{ind}  - name: {name}")
        if url:
            lines.append(f"{ind}    url: {url}")
    return "\n".join(lines) + "\n"


# ---------- file timestamp helpers ----------

def iso_date_from_ts(ts: float) -> str:
    """Return YYYY-MM-DD string from a POSIX timestamp (local time)."""
    return datetime.fromtimestamp(ts).date().isoformat()


def derive_file_dates(json_path: Path) -> Dict[str, str]:
    """
    Derive dates from the JSON file:
      - created: st_birthtime if available (macOS), else st_ctime
      - last_modified: st_mtime
    """
    st = json_path.stat()
    created_ts = getattr(st, "st_birthtime", None)
    if created_ts is None:  # Linux typically lacks birthtime
        created_ts = st.st_ctime
    lastmod_ts = st.st_mtime
    return {
        "created": iso_date_from_ts(created_ts),
        "last_modified": iso_date_from_ts(lastmod_ts),
    }


# ---------- front matter ----------

def render_front_matter(term: Dict[str, Any]) -> str:
    """Build the Jekyll front matter from the JSON term."""
    title = term.get("title", "")
    description = term.get("description", "")
    tags = term.get("tags", [])
    related = term.get("related", [])
    authors = term.get("authors", [])
    dates = term.get("dates", {})
    created = dates.get("created", "")
    lastmod = dates.get("last_modified", "")
    version = term.get("version", "")
    generated = datetime.now().strftime("%Y-%m-%d")

    fm = ["---"]
    fm.append(f"title: {title}")
    fm.append(f"description: {description}")
    fm.append(yaml_list_block("tags", tags).rstrip())
    fm.append(yaml_list_block("related", related).rstrip())
    fm.append(yaml_authors_block(authors).rstrip())
    fm.append(f"version: {version}")
    fm.append(f"date: {created}")
    fm.append(f"lastmod: {lastmod}")
    fm.append(f"generated: {generated}")
    fm.append("---")
    return "\n".join(fm) + "\n\n"


# ---------- Section/figure rendering ----------

def render_figure_block(fig: Dict[str, Any]) -> str:
    """Render one figure include block; add a literal <br> after it."""
    path = fig.get("path", "")
    zoomable = fig.get("zoomable", True)
    zoom_val = "true" if zoomable else "false"
    caption = fig.get("caption_md", "")  # verbatim

    lines = []
    lines.append('<div class="row mt-3">')
    lines.append('    <div class="col-sm mt-3 mt-md-0">')
    lines.append("        {% include figure.liquid")
    lines.append(f'        path="{path}"')
    # Avoid f-string braces issue by concatenating the closing `%}`
    lines.append(f"        zoomable={zoom_val} " + "%}")
    if caption:
        lines.append(f"        {caption}")
    lines.append("    </div>")
    lines.append("</div>")
    lines.append("")   # blank line
    lines.append("<br>")
    lines.append("")   # blank line
    return "\n".join(lines)


def render_cite_line(source_keys: List[str], page: Any) -> str:
    """Render 'Source: <d-cite key="..."></d-cite> ...' with optional page suffix."""
    if not source_keys:
        return ""
    cites = " ".join([f'<d-cite key="{k}"></d-cite>' for k in source_keys])
    page_suffix = f" {page}" if page else ""
    return f"Source: {cites}{page_suffix}\n"


def render_section(sec: Dict[str, Any]) -> str:
    """Render a section: heading -> figures -> source line -> body."""
    title = sec.get("title", "")
    body_md = sec.get("body_md", "")
    source_keys = sec.get("source_keys", [])
    page = sec.get("page", None)
    figures = sec.get("figures", [])

    out: List[str] = []
    # H3 heading
    out.append(f"### {title}\n")

    # Figures first (each followed by <br>)
    if figures:
        for fig in figures:
            out.append(render_figure_block(fig))

    # Source line
    cite_line = render_cite_line(source_keys, page)
    if cite_line:
        out.append(cite_line)

    # Body (verbatim)
    if body_md:
        out.append(body_md.strip() + "\n")

    return "\n".join(out).rstrip() + "\n\n"


def convert_term_to_md(term: Dict[str, Any]) -> str:
    """Convert a term dict to a complete Markdown document."""
    parts: List[str] = [render_front_matter(term)]

    sections = term.get("content", {}).get("sections", [])
    # Sort: by order (missing order -> end), tie-break by title
    sections_sorted = sorted(
        sections,
        key=lambda s: (s.get("order") is None, s.get("order", 10**9), s.get("title", "")),
    )

    for sec in sections_sorted:
        parts.append(render_section(sec))

    return "".join(parts).rstrip() + "\n"


# ---------- CLI ----------

def main():
    parser = argparse.ArgumentParser(
        description="Convert a term JSON (lean schema) into a Jekyll Markdown file."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the term JSON file.")
    parser.add_argument("-o", "--output", required=True, help="Output Markdown file path.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Rewrite output even if it already exists (force consistency).",
    )
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        print(f"ERROR: JSON file not found: {in_path}", file=sys.stderr)
        sys.exit(1)
    # --- Skip if exists and not overwrite ---
    if out_path.exists() and not args.overwrite:
        print(f"Skipping {out_path} (exists, use --overwrite to force).")
        return

    try:
        term = json.loads(in_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: Failed to read/parse JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # ---- normalize optional fields ----
    # tags/related/authors may be missing or None -> default to []
    if not term.get("tags"):
        term["tags"] = []
    if not term.get("related"):
        term["related"] = []
    if not term.get("authors"):
        term["authors"] = []

    # dates may be missing/empty -> derive from file timestamps
    file_dates = derive_file_dates(in_path)
    dates = term.get("dates", {}) or {}
    created = dates.get("created") or file_dates["created"]
    lastmod = dates.get("last_modified") or file_dates["last_modified"]
    term["dates"] = {"created": created, "last_modified": lastmod}

    md = convert_term_to_md(term)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
