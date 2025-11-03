#!/usr/bin/env python3
"""
Build lightweight artifacts for the API:
- index.json: term summaries for fast listing/search
- tags.json : tag counts
Usage:
  python ./database/pyscripts/build_index.py
"""

import json, sys
from pathlib import Path
from collections import Counter
from datetime import datetime

TERMS_DIR = Path("./database/json") 
OUT_DIR   = Path("./database/build")
OUT_DIR.mkdir(parents=True, exist_ok=True)

items = []
tags_counter = Counter()

for fp in sorted(TERMS_DIR.glob("*.json")):
    with fp.open("r", encoding="utf-8") as f:
        t = json.load(f)
    item = {
        "id": t["id"],
        "title": t["title"],
        "summary": t["description"],  # we use description as snippet
        "tags": t.get("tags", []),
        "updated_at": t["dates"]["last_modified"],  # ISO date
    }
    items.append(item)
    tags_counter.update(item["tags"])

index = {
    "items": items,
    "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
}

tags = {
    "tags": [{"tag": k, "count": v} for k, v in sorted(tags_counter.items(), key=lambda kv: (-kv[1], kv[0]))]
}

with (OUT_DIR / "index.json").open("w", encoding="utf-8") as f:
    json.dump(index, f, indent=2, ensure_ascii=False)
    f.write("\n")

with (OUT_DIR / "tags.json").open("w", encoding="utf-8") as f:
    json.dump(tags, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Built {OUT_DIR/'index.json'} and {OUT_DIR/'tags.json'}")
