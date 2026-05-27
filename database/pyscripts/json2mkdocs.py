"""
json2mkdocs.py — Generate MkDocs pages from database/json/*.json term files.

Usage:
    python database/pyscripts/json2mkdocs.py [--terms id1 id2 ...] [--out-dir docs/wiki]

Run from the repo root.
"""

import argparse
import json
import os
import re
import sys

# Allow importing render.py from the same directory as this script.
sys.path.insert(0, os.path.dirname(__file__))
from render import callouts_to_admonitions, cite_to_footnotes  # noqa: E402

# ---------------------------------------------------------------------------
# Paths (relative to repo root, where the script is invoked from)
# ---------------------------------------------------------------------------
REPO_ROOT = os.getcwd()
BIB_JSON = os.path.join(REPO_ROOT, "database", "build", "bib.json")
INDEX_JSON = os.path.join(REPO_ROOT, "database", "build", "index.json")
JSON_DIR = os.path.join(REPO_ROOT, "database", "json")
DEFAULT_OUT_DIR = os.path.join(REPO_ROOT, "docs", "wiki")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
ASSETS_LINK = os.path.join(DOCS_DIR, "assets")
ASSETS_TARGET = os.path.join("..", "assets")  # relative symlink

GITHUB_EDIT_BASE = "https://github.com/ps-wiki/ps-wiki.github.io/edit/main/_wiki/"

_DCITE_RE = re.compile(r'<d-cite key="([^"]+)"></d-cite>')
_HTML_TAG_RE = re.compile(r"<[^>]+>")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _strip_citations_and_html(text: str) -> str:
    """Return plain text suitable for an image alt attribute."""
    text = _DCITE_RE.sub("", text)
    text = _HTML_TAG_RE.sub("", text)
    return text.strip()


def _ensure_symlink():
    """Create docs/assets -> ../assets symlink if it doesn't exist."""
    if not os.path.exists(ASSETS_LINK) and not os.path.islink(ASSETS_LINK):
        os.symlink(ASSETS_TARGET, ASSETS_LINK)


def _load_bib() -> dict:
    with open(BIB_JSON, encoding="utf-8") as f:
        data = json.load(f)
    return data["entries"]  # dict of {key: {key, type, fields}}


def _load_terms(term_ids: list[str] | None) -> list[dict]:
    if term_ids:
        paths = [os.path.join(JSON_DIR, f"{tid}.json") for tid in term_ids]
    else:
        paths = sorted(
            [
                os.path.join(JSON_DIR, fn)
                for fn in os.listdir(JSON_DIR)
                if fn.endswith(".json")
            ]
        )
    terms = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            terms.append(json.load(f))
    return sorted(terms, key=lambda t: t["id"])


def _load_index() -> list[dict]:
    with open(INDEX_JSON, encoding="utf-8") as f:
        data = json.load(f)
    return sorted(data["items"], key=lambda x: x["title"])


# ---------------------------------------------------------------------------
# Per-term page generation
# ---------------------------------------------------------------------------

def _generate_term_page(term: dict, bib_entries: dict, prev_item: dict | None, next_item: dict | None) -> str:
    """Return the full Markdown text for a single term page."""
    tid = term["id"]
    title = term["title"]
    description = term["description"]
    tags = term.get("tags", [])
    related = term.get("related", [])
    last_modified = term.get("dates", {}).get("last_modified", "")
    sections = term.get("content", {}).get("sections", [])

    lines: list[str] = []

    # --- Front matter ---
    tags_yaml = ", ".join(tags)
    lines.append("---")
    lines.append(f'title: "{title}"')
    if tags:
        lines.append(f"tags: [{tags_yaml}]")
    lines.append(f"edit_url: {GITHUB_EDIT_BASE}{tid}.md")
    lines.append("---")
    lines.append("")

    # --- Title + description ---
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> {description}")
    lines.append("")

    # --- Sections ---
    # Sort: sections with order come first (ascending), then those without (by title).
    sorted_sections = sorted(
        sections,
        key=lambda s: (s.get("order") is None, s.get("order", 0), s.get("title", "")),
    )

    # Accumulate ALL footnote defs across the page; deduplicate by key.
    all_footnote_defs: dict[str, str] = {}  # key -> full "[^key]: ..." string

    def _collect_defs(defs: list[str]) -> None:
        for defn in defs:
            # Extract key from "[^key]: ..."
            m = re.match(r"\[\^([^\]]+)\]:", defn)
            if m:
                k = m.group(1)
                if k not in all_footnote_defs:
                    all_footnote_defs[k] = defn

    for sec in sorted_sections:
        sec_title = sec.get("title", "")
        source_keys = sec.get("source_keys", [])
        page = sec.get("page")
        body_md = sec.get("body_md", "")
        figures = sec.get("figures", [])

        lines.append(f"### {sec_title}")
        lines.append("")

        # --- Figures (before body_md) ---
        for fig in figures:
            fig_path = fig.get("path", "")
            caption_md = fig.get("caption_md", "")

            # Image alt text: strip d-cite and HTML tags
            alt_text = _strip_citations_and_html(caption_md)

            # External URLs used as-is; local paths kept as absolute site-root refs
            if fig_path.startswith("http://") or fig_path.startswith("https://"):
                fig_path_rel = fig_path
            elif not fig_path.startswith("/"):
                fig_path_rel = "/" + fig_path
            else:
                fig_path_rel = fig_path

            lines.append(f"![{alt_text}]({fig_path_rel})")
            lines.append("")

            # Caption line: pass through both transforms
            if caption_md:
                cap_after_callouts = callouts_to_admonitions(caption_md)
                cap_transformed, cap_defs = cite_to_footnotes(
                    cap_after_callouts, bib_entries
                )
                _collect_defs(cap_defs)
                lines.append(f"*{cap_transformed.strip()}*")
                lines.append("")

        # --- Source line ---
        if source_keys:
            # Emit as d-cite tags and pass through cite_to_footnotes
            src_dcites = " ".join(
                f'<d-cite key="{k}"></d-cite>' for k in source_keys
            )
            if page:
                src_line = f"Source: {src_dcites} ({page})"
            else:
                src_line = f"Source: {src_dcites}"
            src_transformed, src_defs = cite_to_footnotes(src_line, bib_entries)
            _collect_defs(src_defs)
            lines.append(src_transformed)
            lines.append("")

        # --- Body ---
        if body_md:
            after_callouts = callouts_to_admonitions(body_md)
            after_cites, body_defs = cite_to_footnotes(after_callouts, bib_entries)
            _collect_defs(body_defs)
            lines.append(after_cites.rstrip("\n"))
            lines.append("")

    # --- Footnote definitions (collected by the footnotes extension, rendered at page bottom) ---
    if all_footnote_defs:
        lines.append("")
        for defn in all_footnote_defs.values():
            lines.append(defn)
        lines.append("")

    # --- Footer ---
    lines.append("---")
    lines.append("")
    lines.append(f"**Last modified:** {last_modified}")
    lines.append("")

    if related:
        related_links = " · ".join(f"[{r}]({r}.md)" for r in related)
        lines.append(f"**Related:** {related_links}")
        lines.append("")

    nav_parts = []
    if prev_item:
        nav_parts.append(f"[← {prev_item['title']}]({prev_item['id']}.md)")
    if next_item:
        nav_parts.append(f"[{next_item['title']} →]({next_item['id']}.md)")
    if nav_parts:
        lines.append(" · ".join(nav_parts))
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Index page generation
# ---------------------------------------------------------------------------

def _generate_index_page(index_items: list[dict]) -> str:
    lines: list[str] = []
    lines.append("---")
    lines.append("title: All Terms")
    lines.append("---")
    lines.append("")
    lines.append("| Term | Tags | Last Updated |")
    lines.append("|------|------|-------------|")
    for item in index_items:
        title = item["title"]
        tid = item["id"]
        tags = ", ".join(item.get("tags", []))
        updated = item.get("updated_at", "")
        lines.append(f"| [{title}]({tid}.md) | {tags} | {updated} |")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate(
    term_ids: list[str] | None = None, out_dir: str | None = None
) -> int:
    """Generate docs/wiki/ pages from JSON term files.

    Args:
        term_ids: Term IDs to generate (default: all).
        out_dir: Output directory (default: docs/wiki/).

    Returns:
        Number of term pages written.
    """
    if out_dir is None:
        out_dir = DEFAULT_OUT_DIR

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)
    _ensure_symlink()

    bib_entries = _load_bib()
    terms = _load_terms(term_ids)
    index_items = _load_index()
    id_to_index_pos = {item["id"]: i for i, item in enumerate(index_items)}

    for term in terms:
        tid = term["id"]
        pos = id_to_index_pos.get(tid)
        prev_item = index_items[pos - 1] if pos is not None and pos > 0 else None
        next_item = (
            index_items[pos + 1]
            if pos is not None and pos < len(index_items) - 1
            else None
        )
        page_content = _generate_term_page(term, bib_entries, prev_item, next_item)
        out_path = os.path.join(out_dir, f"{tid}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_content)
        print(f"  wrote {out_path}")

    index_path = os.path.join(out_dir, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(_generate_index_page(index_items))
    print(f"  wrote {index_path}")

    return len(terms)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate MkDocs wiki pages from JSON term files."
    )
    parser.add_argument(
        "--terms", nargs="+", metavar="ID", help="Term IDs to process (default: all)."
    )
    parser.add_argument(
        "--out-dir",
        default=DEFAULT_OUT_DIR,
        metavar="DIR",
        help=f"Output directory for generated pages (default: {DEFAULT_OUT_DIR}).",
    )
    args = parser.parse_args()
    generate(args.terms, args.out_dir)


if __name__ == "__main__":
    main()
