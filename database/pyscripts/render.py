import re


_CALLOUT_TYPE_MAP = {
    "block-danger": "danger",
    "block-warning": "warning",
    "block-tip": "tip",
    "block-note": "note",
}

_PRETTIER_IGNORE_RE = re.compile(r"<!--\s*prettier-ignore-(start|end)\s*-->\n?")
_DCITE_RE = re.compile(r'<d-cite key="([^"]+)"></d-cite>')


def cite_to_footnotes(body_md: str, bib_entries: dict) -> tuple[str, list[str]]:
    body_md = _PRETTIER_IGNORE_RE.sub("", body_md)

    seen_keys: list[str] = []
    seen_set: set[str] = set()

    def _replace(m: re.Match) -> str:
        key = m.group(1)
        if key not in seen_set:
            seen_set.add(key)
            seen_keys.append(key)
        return f"[^{key}]"

    transformed = _DCITE_RE.sub(_replace, body_md)

    footnote_defs: list[str] = []
    for key in seen_keys:
        entry = bib_entries.get(key)
        if entry is None:
            footnote_defs.append(f"[^{key}]: [{key}]")
            continue

        fields = entry.get("fields", entry)
        author = fields.get("author", "")
        year = fields.get("year", "")
        title = fields.get("title", "")
        url = fields.get("url", "")

        parts: list[str] = []
        if author and year:
            parts.append(f"{author} ({year}).")
        elif author:
            parts.append(f"{author}.")
        elif year:
            parts.append(f"({year}).")

        if title:
            parts.append(f"*{title}*.")

        if url:
            parts.append(f"[{url}]({url})")

        body = " ".join(parts) if parts else f"[{key}]"
        footnote_defs.append(f"[^{key}]: {body}")

    return transformed, footnote_defs


_CALLOUT_PATTERN = re.compile(
    r"(?:<!--\s*prettier-ignore-start\s*-->\n?)?"
    r"((?:^>.*\n)+)"
    r"(?:\n)?"
    r"\{: \.([^\s}]+) \}\n?"
    r"(?:<!--\s*prettier-ignore-end\s*-->\n?)?",
    re.MULTILINE,
)


def callouts_to_admonitions(body_md: str) -> str:
    def _replace(m: re.Match) -> str:
        quote_block = m.group(1)
        css_class = m.group(2)
        admonition_type = _CALLOUT_TYPE_MAP.get(css_class, "note")

        lines = quote_block.splitlines()
        content_lines: list[str] = []
        for line in lines:
            if line.startswith("> "):
                content_lines.append("    " + line[2:])
            elif line == ">":
                content_lines.append("    ")
            else:
                content_lines.append("    " + line)

        content = "\n".join(content_lines)
        return f"!!! {admonition_type}\n{content}\n"

    return _CALLOUT_PATTERN.sub(_replace, body_md)
