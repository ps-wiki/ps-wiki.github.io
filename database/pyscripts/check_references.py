#!/usr/bin/env python3
"""
Reference URL health scanner for PS-Wiki.

Parses assets/bibliography/papers.bib, checks every URL in the `url`, `pdf`,
and `html` fields, and writes a structured report to database/build/reference_check.json.

Usage:
    python database/pyscripts/check_references.py
    python database/pyscripts/check_references.py --recover   # also query Wayback Machine for broken NERC URLs
    python database/pyscripts/check_references.py --bib path/to/custom.bib
    python database/pyscripts/check_references.py --out path/to/output.json
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BIB = REPO_ROOT / "assets" / "bibliography" / "papers.bib"
DEFAULT_OUT = REPO_ROOT / "database" / "build" / "reference_check.json"
DEFAULT_WIKI_DIR = REPO_ROOT / "_wiki"

_DCITE_RE = re.compile(r'<d-cite\b[^>]*key="([^"]*)"')

URL_FIELDS = ("url", "pdf", "html")
NERC_DOMAIN = "nerc.com"
REQUEST_DELAY = 0.5  # seconds between requests
TIMEOUT = 12  # seconds
WAYBACK_API = "https://archive.org/wayback/available?url={url}"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; pswiki-refcheck/1.0; "
        "+https://github.com/jinningwang/pswiki)"
    )
}


# ---------------------------------------------------------------------------
# BibTeX parsing
# ---------------------------------------------------------------------------

def load_bib(bib_path: Path) -> list[dict]:
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    with open(bib_path, encoding="utf-8") as f:
        db = bibtexparser.load(f, parser=parser)
    return db.entries


def collect_urls(entries: list[dict]) -> list[dict]:
    """Return deduplicated list of {key, field, url, is_nerc}."""
    seen: set[str] = set()
    records = []
    for entry in entries:
        key = entry["ID"]
        for field in URL_FIELDS:
            url = entry.get(field, "").strip()
            if not url or url in seen:
                continue
            seen.add(url)
            records.append(
                {
                    "key": key,
                    "field": field,
                    "url": url,
                    "is_nerc": NERC_DOMAIN in url,
                }
            )
    return records


# ---------------------------------------------------------------------------
# Wiki cross-reference
# ---------------------------------------------------------------------------

def find_citing_terms(key: str, wiki_dir: Path) -> list[str]:
    """Return sorted _wiki/*.md relative paths that contain a <d-cite> for key."""
    if not wiki_dir.exists():
        return []
    matches = []
    for md_file in sorted(wiki_dir.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        for m in _DCITE_RE.finditer(text):
            if key in [k.strip() for k in m.group(1).split(",")]:
                matches.append(f"_wiki/{md_file.name}")
                break
    return matches


# ---------------------------------------------------------------------------
# HTTP checking
# ---------------------------------------------------------------------------

def _make_request(url: str, method: str = "HEAD") -> tuple[int, str]:
    """Return (status_code, final_url). Raises urllib.error.URLError on failure."""
    req = urllib.request.Request(url, headers=HEADERS, method=method)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.status, resp.url


def check_url(url: str) -> dict:
    """Check a single URL and return a status dict."""
    result = {"status_code": None, "final_url": None, "error": None, "category": None}
    try:
        code, final = _make_request(url, method="HEAD")
        if code == 405:
            code, final = _make_request(url, method="GET")
        result["status_code"] = code
        result["final_url"] = final if final != url else None
    except urllib.error.HTTPError as e:
        if e.code == 405:
            try:
                code, final = _make_request(url, method="GET")
                result["status_code"] = code
                result["final_url"] = final if final != url else None
            except urllib.error.HTTPError as e2:
                result["status_code"] = e2.code
                result["error"] = str(e2.reason)
        else:
            result["status_code"] = e.code
            result["error"] = str(e.reason)
    except urllib.error.URLError as e:
        result["error"] = str(e.reason)
    except TimeoutError:
        result["error"] = "timeout"
    except Exception as e:
        result["error"] = str(e)

    code = result["status_code"]
    if code is None:
        result["category"] = "broken"
    elif 200 <= code < 300:
        result["category"] = "ok"
    elif 300 <= code < 400:
        result["category"] = "redirect"
    elif 400 <= code < 500:
        result["category"] = "broken"
    else:
        result["category"] = "server_error"

    return result


# ---------------------------------------------------------------------------
# Wayback Machine recovery
# ---------------------------------------------------------------------------

def wayback_lookup(url: str) -> str | None:
    """Return the most recent Wayback Machine snapshot URL, or None."""
    api_url = WAYBACK_API.format(url=urllib.parse.quote(url, safe=":/?=&%"))
    try:
        req = urllib.request.Request(api_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read())
        snapshot = data.get("archived_snapshots", {}).get("closest", {})
        if snapshot.get("available"):
            return snapshot["url"]
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def scan(records: list[dict], recover: bool) -> list[dict]:
    total = len(records)
    results = []
    for i, rec in enumerate(records, 1):
        url = rec["url"]
        print(f"  [{i}/{total}] {url[:80]}", end="", flush=True)
        check = check_url(url)
        entry = {**rec, **check, "archive_url": None}

        if recover and entry["is_nerc"] and entry["category"] in ("broken", "server_error"):
            archive = wayback_lookup(url)
            entry["archive_url"] = archive
            time.sleep(REQUEST_DELAY)

        print(f"  → {entry['category'].upper()}"
              + (f" ({entry['status_code']})" if entry["status_code"] else "")
              + (f"  [archive found]" if entry.get("archive_url") else ""))

        results.append(entry)
        time.sleep(REQUEST_DELAY)

    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def build_report(
    results: list[dict], bib_path: Path, wiki_dir: Path = DEFAULT_WIKI_DIR
) -> dict:
    categories = {"ok": [], "redirect": [], "broken": [], "server_error": []}
    for r in results:
        categories.setdefault(r["category"], []).append(r)
        r["used_by"] = find_citing_terms(r["key"], wiki_dir)

    return {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "bib_file": str(bib_path),
        "summary": {cat: len(items) for cat, items in categories.items()},
        "results": results,
    }


def print_summary(report: dict) -> None:
    s = report["summary"]
    total = sum(s.values())
    print()
    print("=" * 60)
    print(f"Reference check complete — {report['scanned_at']}")
    print(f"  Total URLs scanned : {total}")
    print(f"  OK (2xx)           : {s.get('ok', 0)}")
    print(f"  Redirect (3xx)     : {s.get('redirect', 0)}")
    print(f"  Broken (4xx/conn)  : {s.get('broken', 0)}")
    print(f"  Server error (5xx) : {s.get('server_error', 0)}")
    print()

    broken = [r for r in report["results"] if r["category"] in ("broken", "server_error")]
    if not broken:
        print("No broken links found.")
        return

    nerc_broken = [r for r in broken if r["is_nerc"]]
    other_broken = [r for r in broken if not r["is_nerc"]]

    def _print_group(label: str, items: list[dict]) -> None:
        if not items:
            return
        print(f"--- {label} ({len(items)}) ---")
        for r in items:
            code_note = f" [{r['status_code']}]" if r["status_code"] else f" [{r['error']}]"
            print(f"  {r['key']} ({r['field']}){code_note}")
            print(f"    {r['url']}")
            if r.get("archive_url"):
                print(f"    archive: {r['archive_url']}")
            if r.get("used_by"):
                print(f"    used by: {', '.join(r['used_by'])}")
        print()

    _print_group("NERC broken", nerc_broken)
    _print_group("Other broken", other_broken)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Check reference URLs in papers.bib")
    parser.add_argument("--bib", type=Path, default=DEFAULT_BIB)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--wiki-dir", type=Path, default=DEFAULT_WIKI_DIR,
                        help="Path to _wiki/ directory for used-by lookup")
    parser.add_argument(
        "--recover",
        action="store_true",
        help="Query Wayback Machine for broken NERC URLs",
    )
    args = parser.parse_args()

    if not args.bib.exists():
        print(f"ERROR: bib file not found: {args.bib}", file=sys.stderr)
        sys.exit(1)

    args.out.parent.mkdir(parents=True, exist_ok=True)

    print(f"Parsing {args.bib} ...")
    entries = load_bib(args.bib)
    records = collect_urls(entries)
    print(f"Found {len(records)} unique URLs across {len(entries)} entries.\n")

    print("Scanning URLs ...")
    results = scan(records, recover=args.recover)

    report = build_report(results, args.bib, wiki_dir=args.wiki_dir)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport written to {args.out}")

    print_summary(report)

    broken_count = report["summary"].get("broken", 0) + report["summary"].get("server_error", 0)
    sys.exit(1 if broken_count else 0)


if __name__ == "__main__":
    main()
