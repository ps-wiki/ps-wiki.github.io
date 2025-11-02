#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UNDER DEVELOPMENT!

Build a single, organized PDF "book" from all ps-wiki term JSONs using Pandoc.

Pipeline:
  JSON terms  -> combined Markdown book -> pandoc -> PDF

Features:
- Scans a JSON dir (default: database/json).
- Sorts terms by title (fallback: id).
- Each term becomes a chapter:
    # <Title>
    <Description>
    Authors, Dates, Tags
    ## Section title
    [figures as regular Markdown images with captions]
    Source: [@citekey] pN  (if --bib is provided; otherwise leave literal <d-cite ...>)
    (body_md verbatim)
- Converts <d-cite key="..."></d-cite> to [@key] when --bib is provided (so citeproc works).
- Optional CSL style.
- Optional LaTeX template (e.g., Eisvogel).
- Writes an intermediate Markdown for inspection.

Usage:
  python database/pyscripts/export_pdf.py \
    --json-dir database/json \
    --out-pdf build/pswiki-book.pdf \
    --tmp-md build/pswiki-book.md \
    --title "Power Systems Glossary" \
    --author "ps-wiki" \
    --date "2025-11-01" \
    --bib references.bib \
    --csl ieee.csl \
    --template eisvogel.latex \
    --toc --toc-depth 2

Requirements:
- pandoc available in PATH
- LaTeX engine (e.g., TeX Live) for PDF output
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

DCITE_RE = re.compile(r'<d-cite\s+key="([^"]+)"></d-cite>')

SECTION_TYPE_HDR = {
    "definition": "##",
    "note": "##",
    "example": "##",
    "other": "##",
}

def die(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

def load_term(p: Path) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[WARN] failed to parse {p.name}: {e}", file=sys.stderr)
        return None

def md_escape(text: str) -> str:
    # Minimal—don’t over-escape; titles/descriptions are fairly clean
    return text.strip()

def join_authors(authors: Any) -> str:
    if not isinstance(authors, list):
        return ""
    names = []
    for a in authors:
        if isinstance(a, dict) and a.get("name"):
            names.append(a["name"])
    return ", ".join(names)

def join_tags(tags: Any) -> str:
    if not isinstance(tags, list):
        return ""
    return ", ".join([str(t) for t in tags if isinstance(t, str)])

def normalize_page_suffix(page: Optional[str]) -> str:
    return f" {page.strip()}" if isinstance(page, str) and page.strip() else ""

def convert_dcite_to_pandoc(body: str) -> str:
    # Replace <d-cite key="xxx"></d-cite> with [@xxx]
    return DCITE_RE.sub(lambda m: f"[@{m.group(1)}]", body)

def figure_block_to_md(fig: Dict[str, Any]) -> str:
    """
    Convert a figure object to pure Markdown with caption.
    Uses Pandoc's image caption syntax:
      ![Caption](path)
    The caption may include citations (already converted if --bib was set).
    """
    path = fig.get("path", "")
    caption = fig.get("caption_md", "").strip()
    # Strip any leading "Fig. ..." label to avoid doubling; leave as-is otherwise
    # (Pandoc will keep it verbatim.)
    if not path:
        return ""
    return f"![{caption}]({path})\n"

def render_term_to_md(term: Dict[str, Any], use_bib: bool) -> str:
    title = md_escape(term.get("title", term.get("id", "")))
    description = term.get("description", "")
    authors_str = join_authors(term.get("authors", []))
    tags_str = join_tags(term.get("tags", []))
    dates = term.get("dates", {})
    created = dates.get("created", "")
    lastmod = dates.get("last_modified", "")

    lines: List[str] = []
    # Chapter heading
    lines.append(f"# {title}\n")
    if description:
        lines.append(f"{description}\n")

    meta_bits = []
    if authors_str:
        meta_bits.append(f"**Authors:** {authors_str}")
    if created:
        meta_bits.append(f"**Date:** {created}")
    if lastmod:
        meta_bits.append(f"**Last modified:** {lastmod}")
    if tags_str:
        meta_bits.append(f"**Tags:** {tags_str}")
    if meta_bits:
        lines.append("\n" + "  \n".join(meta_bits) + "\n")

    sections = (term.get("content", {}) or {}).get("sections", [])
    # stable sort by order then title
    sections = sorted(sections, key=lambda s: (s.get("order") is None, s.get("order", 10**9), s.get("title","")))

    for s in sections:
        stitle = s.get("title", "")
        stype = s.get("type", "definition")
        hdr = SECTION_TYPE_HDR.get(stype, "##")

        lines.append(f"{hdr} {stitle}\n")

        # Figures first (each one)
        figs = s.get("figures", []) or []
        for fig in figs:
            fig_block = figure_block_to_md(fig)
            if use_bib:
                fig_block = convert_dcite_to_pandoc(fig_block)
            lines.append(fig_block)

        # Source line
        src_keys = s.get("source_keys", []) or []
        page = s.get("page", None)
        if src_keys:
            if use_bib:
                # Source: [@a] [@b] pN
                cites = " ".join([f"[@{k}]" for k in src_keys])
                lines.append(f"Source: {cites}{normalize_page_suffix(page)}\n")
            else:
                # Leave original <d-cite> form so it’s visible in PDF even without citeproc
                cites = " ".join([f'<d-cite key="{k}"></d-cite>' for k in src_keys])
                lines.append(f"Source: {cites}{normalize_page_suffix(page)}\n")

        # Body
        body = s.get("body_md", "")
        if use_bib:
            body = convert_dcite_to_pandoc(body)
        lines.append(body.rstrip() + "\n")

    return "\n".join(lines).rstrip() + "\n\n"

def build_book_markdown(json_dir: Path, doc_title: str, doc_author: str, doc_date: str, use_bib: bool) -> str:
    # Front matter for the entire book (Pandoc YAML metadata block)
    fm_lines = [
        "---",
        f'title: "{doc_title}"' if doc_title else 'title: "ps-wiki glossary"',
        f'author: "{doc_author}"' if doc_author else 'author: ""',
        f'date: "{doc_date}"' if doc_date else "",
        "fontsize: 11pt",
        "linestretch: 1.1",
        "---",
        "",
        "\\newpage\n"
    ]
    # Collect terms
    terms: List[Dict[str, Any]] = []
    for p in sorted(json_dir.glob("*.json")):
        t = load_term(p)
        if not t:
            continue
        terms.append(t)
    # Sort by title then id
    terms.sort(key=lambda t: (t.get("title") or t.get("id") or ""))

    body_parts: List[str] = []
    for t in terms:
        body_parts.append(render_term_to_md(t, use_bib))

    return "\n".join(fm_lines) + "\n".join(body_parts)

def check_pandoc_available():
    if not shutil.which("pandoc"):
        die("pandoc not found in PATH. Please install pandoc.")

def run_pandoc(md_path: Path, out_pdf: Path, template: Optional[Path], bib: Optional[Path], csl: Optional[Path], toc: bool, toc_depth: int):
    cmd = ["pandoc", str(md_path), "-o", str(out_pdf), "--pdf-engine=xelatex"]
    if toc:
        cmd += ["--toc", f"--toc-depth={toc_depth}"]
    if template and template.exists():
        cmd += ["--template", str(template)]
    if bib and bib.exists():
        cmd += ["--citeproc", "--bibliography", str(bib)]
    if csl and csl.exists():
        cmd += ["--csl", str(csl)]

    print("Running:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        die(f"pandoc failed with exit code {e.returncode}")

def main():
    ap = argparse.ArgumentParser(description="Assemble all JSON terms into a single PDF via Pandoc.")
    ap.add_argument("--json-dir", default="database/json", help="Directory containing term JSON files.")
    ap.add_argument("--out-pdf", required=True, help="Output PDF path, e.g., build/pswiki.pdf")
    ap.add_argument("--tmp-md", default="build/pswiki-book.md", help="Path to write intermediate combined Markdown.")
    ap.add_argument("--title", default="Power Systems Glossary", help="Document title.")
    ap.add_argument("--author", default="ps-wiki", help="Document author.")
    ap.add_argument("--date", default="", help="Document date (string).")
    ap.add_argument("--template", help="Optional Pandoc LaTeX template (e.g., eisvogel.latex).")
    ap.add_argument("--bib", help="Optional bibliography file (e.g., references.bib).")
    ap.add_argument("--csl", help="Optional CSL style (e.g., ieee.csl).")
    ap.add_argument("--toc", action="store_true", help="Include table of contents.")
    ap.add_argument("--toc-depth", type=int, default=2, help="TOC depth (default 2).")
    args = ap.parse_args()

    json_dir = Path(args.json_dir)
    out_pdf = Path(args.out_pdf)
    tmp_md = Path(args.tmp_md)
    template = Path(args.template) if args.template else None
    bib = Path(args.bib) if args.bib else None
    csl = Path(args.csl) if args.csl else None

    if not json_dir.exists():
        die(f"JSON dir not found: {json_dir}")

    check_pandoc_available()

    use_bib = bib is not None and bib.exists()
    book_md = build_book_markdown(json_dir, args.title, args.author, args.date, use_bib)

    tmp_md.parent.mkdir(parents=True, exist_ok=True)
    tmp_md.write_text(book_md, encoding="utf-8")
    print(f"Wrote combined Markdown: {tmp_md}")

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    run_pandoc(tmp_md, out_pdf, template, bib, csl, args.toc, args.toc_depth)
    print(f"PDF written: {out_pdf}")

if __name__ == "__main__":
    main()
