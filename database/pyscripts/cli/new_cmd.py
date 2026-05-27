"""new_cmd — scaffold a new term at _wiki/<id>.md."""

import re
import sys
from datetime import date
from pathlib import Path

_ID_RE = re.compile(r"^[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?$")

_TEMPLATE = """\
---
title: {title}
description: One-sentence description.
tags: []
related: []
authors:
  - name: Your Name
    url: https://
date: {today}
lastmod: {today}
---

### Definition

>
"""


def cmd_new(term_id: str) -> None:
    if not _ID_RE.match(term_id):
        print(
            f"ERROR: '{term_id}' is not a valid term ID.\n"
            "IDs must be kebab-case: lowercase letters, digits, and hyphens only\n"
            "(e.g. power-quality, agc, n-1-contingency).",
            file=sys.stderr,
        )
        sys.exit(1)

    wiki_dir = Path("_wiki")
    if not wiki_dir.exists():
        print(
            "ERROR: _wiki/ not found — run pswiki from the repo root.",
            file=sys.stderr,
        )
        sys.exit(1)

    md_path = wiki_dir / f"{term_id}.md"
    if md_path.exists():
        print(f"ERROR: {md_path} already exists.", file=sys.stderr)
        sys.exit(1)

    title = term_id.replace("-", " ").title()
    today = date.today().isoformat()
    md_path.write_text(_TEMPLATE.format(title=title, today=today), encoding="utf-8")

    print(f"Created  {md_path}")
    print(f"Next:    python pswiki.py process {term_id}")
