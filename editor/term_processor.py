"""
Browser-compatible term processing module for PS-Wiki editor.

This module provides simplified versions of md2json and json2md functionality
that work in the browser via PyScript/Pyodide.
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

# Schema URL constant
SCHEMA_URL = "https://ps-wiki.github.io/schema/v1/term.schema.json"

# Regex patterns
H3_RE = re.compile(r"^###\s+(.*)\s*$")
DCITE_RE = re.compile(r'<d-cite\s+key="([^"]+)"></d-cite>')


def slugify_kebab(s: str) -> str:
    """Convert string to kebab-case slug."""
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "untitled"


def ensure_list(v: Any) -> List[Any]:
    """Normalize value to list."""
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def build_term_json(
    term_id: str,
    title: str,
    description: str,
    language: str,
    tags: List[str],
    related: List[str],
    authors: List[Dict[str, str]],
    version: str,
    sections: List[Dict[str, Any]],
    aliases: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Build a term JSON object from components.
    
    Args:
        term_id: Kebab-case term identifier
        title: Term title
        description: Short description
        language: BCP-47 language tag (e.g., 'en')
        tags: List of topic tags
        related: List of related term IDs
        authors: List of author dicts with 'name' and optional 'url'
        version: Version string (e.g., '1.0.0')
        sections: List of section dicts
        aliases: Optional list of alternative names
    
    Returns:
        Complete term JSON object
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    term = {
        "$schema": SCHEMA_URL,
        "id": term_id,
        "title": title,
        "description": description,
        "language": language,
        "tags": tags,
        "related": related,
        "version": version,
        "breaking": False,
        "dates": {
            "created": today,
            "last_modified": today
        },
        "authors": authors,
        "content": {
            "sections": sections
        }
    }
    
    if aliases:
        # Insert aliases after related
        ordered = {}
        for key in ["$schema", "id", "title", "description", "language", "tags", "related"]:
            if key in term:
                ordered[key] = term[key]
        ordered["aliases"] = aliases
        for key in ["version", "breaking", "dates", "authors", "content"]:
            if key in term:
                ordered[key] = term[key]
        term = ordered
    
    return term


def yaml_list_block(key: str, items: List[str], indent: int = 0) -> str:
    """Render a simple YAML list block."""
    ind = " " * indent
    if not items:
        return f"{ind}{key}: []\n"
    lines = [f"{ind}{key}:"]
    for v in items:
        lines.append(f"{ind}  - {v}")
    return "\n".join(lines) + "\n"


def yaml_authors_block(authors: List[Dict[str, Any]], indent: int = 0) -> str:
    """Render authors YAML block."""
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


def render_front_matter(term: Dict[str, Any]) -> str:
    """Build the Jekyll front matter from the JSON term."""
    title = term.get("title", "")
    description = term.get("description", "")
    tags = term.get("tags", [])
    related = term.get("related", [])
    aliases = term.get("aliases", [])
    authors = term.get("authors", [])
    dates = term.get("dates", {})
    created = dates.get("created", "")
    lastmod = dates.get("last_modified", "")
    version = term.get("version", "")
    generated = datetime.now().strftime("%Y-%m-%d")

    fm = ["---"]
    fm.append(f"title: {title}")
    if aliases:
        fm.append(yaml_list_block("aliases", aliases).rstrip())
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


def render_figure_block(fig: Dict[str, Any]) -> str:
    """Render one figure include block."""
    path = fig.get("path", "")
    zoomable = fig.get("zoomable", True)
    zoom_val = "true" if zoomable else "false"
    caption = fig.get("caption_md", "")

    lines = []
    lines.append('<div class="row mt-3">')
    lines.append('    <div class="col-sm mt-3 mt-md-0">')
    lines.append("        {% include figure.liquid")
    lines.append(f'        path="{path}"')
    lines.append(f"        zoomable={zoom_val} " + "%}")
    if caption:
        lines.append(f"        {caption}")
    lines.append("    </div>")
    lines.append("</div>")
    lines.append("")
    lines.append("<br>")
    lines.append("")
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

    # Figures first
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
    # Sort by order
    sections_sorted = sorted(
        sections,
        key=lambda s: (
            s.get("order") is None,
            s.get("order", 10**9),
            s.get("title", ""),
        ),
    )

    for sec in sections_sorted:
        parts.append(render_section(sec))

    return "".join(parts).rstrip() + "\n"


def validate_term_basic(term: Dict[str, Any]) -> List[str]:
    """
    Basic validation of term structure (without full JSON schema).
    
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Required top-level fields
    required_fields = ["id", "title", "description", "language", "version", "breaking", "dates", "authors", "content"]
    for field in required_fields:
        if field not in term:
            errors.append(f"Missing required field: {field}")
    
    # Validate ID format (kebab-case)
    if "id" in term:
        term_id = term["id"]
        if not re.match(r"^[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?$", term_id):
            errors.append(f"Invalid ID format (must be kebab-case): {term_id}")
    
    # Validate language format (BCP-47)
    if "language" in term:
        lang = term["language"]
        if not re.match(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$", lang):
            errors.append(f"Invalid language format (must be BCP-47): {lang}")
    
    # Validate dates
    if "dates" in term:
        dates = term["dates"]
        if not isinstance(dates, dict):
            errors.append("dates must be an object")
        else:
            if "created" not in dates:
                errors.append("dates.created is required")
            if "last_modified" not in dates:
                errors.append("dates.last_modified is required")
    
    # Validate authors
    if "authors" in term:
        authors = term["authors"]
        if not isinstance(authors, list):
            errors.append("authors must be an array")
        elif len(authors) == 0:
            errors.append("authors must have at least one author")
        else:
            for i, author in enumerate(authors):
                if not isinstance(author, dict):
                    errors.append(f"authors[{i}] must be an object")
                elif "name" not in author:
                    errors.append(f"authors[{i}].name is required")
    
    # Validate content
    if "content" in term:
        content = term["content"]
        if not isinstance(content, dict):
            errors.append("content must be an object")
        elif "sections" not in content:
            errors.append("content.sections is required")
        elif not isinstance(content["sections"], list):
            errors.append("content.sections must be an array")
        elif len(content["sections"]) == 0:
            errors.append("content.sections must have at least one section")
    
    return errors
