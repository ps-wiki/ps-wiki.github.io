#!/usr/bin/env python3
"""
Render the GitHub issue body for the [CI] Reference Health Tracker issue.

Called by the check-references CI workflow after a scan; outputs markdown to stdout.

Usage:
    python database/pyscripts/render_ref_issue.py \
        --report database/build/reference_check.json \
        --artifact-url <url> \
        --sha <sha> \
        --trigger <schedule|push|workflow_dispatch> \
        --run-url <url>
"""

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def _domain(r: dict) -> str:
    if r.get("is_nerc"):
        return "NERC"
    key = r["key"].lower()
    for name in ("nyiso", "pjm", "ieee", "ferc", "cigre"):
        if name in key:
            return name.upper()
    return "Other"


def render_issue_body(
    report: dict,
    artifact_url: str,
    sha: str,
    trigger: str,
    run_url: str,
) -> str:
    scan_iso = report["scanned_at"]
    scan_date = scan_iso[:10]
    scan_dt = datetime.fromisoformat(scan_iso.replace("Z", "+00:00"))
    expiry = (scan_dt + timedelta(days=90)).strftime("%Y-%m-%d")

    summary = report["summary"]
    total = sum(summary.values())
    all_results = report["results"]

    broken_results = [r for r in all_results if r["category"] in ("broken", "server_error")]
    recoverable = sorted(
        [r for r in broken_results if r.get("archive_url")],
        key=lambda r: (not r.get("used_by"), r["key"]),
    )
    temporary = sorted(
        [r for r in broken_results if not r.get("archive_url") and r["category"] == "server_error"],
        key=lambda r: (not r.get("used_by"), r["key"]),
    )
    needs_review = sorted(
        [r for r in broken_results if not r.get("archive_url") and r["category"] == "broken"],
        key=lambda r: (not r.get("used_by"), r["key"]),
    )

    broken_count = len(broken_results)
    status = "✅ All references OK" if broken_count == 0 else f"⚠️ {broken_count} broken link(s) detected"

    trigger_label = {
        "schedule": "quarterly schedule",
        "push": "`papers.bib` push",
        "workflow_dispatch": "manual trigger",
    }.get(trigger, trigger)
    sha_short = sha[:7] if sha else "unknown"

    L = []  # output lines

    L += [
        f"## Reference Health — {scan_date}",
        "",
        f"> **{status}** · {total} URLs checked · triggered by {trigger_label} · commit `{sha_short}`",
        "",
    ]
    if artifact_url:
        L.append(f"**Artifact**: [reference_check.json]({artifact_url}) _(expires {expiry})_")
    else:
        L.append("**Artifact**: not available")
    L += ["", "---", ""]

    if not broken_results:
        L.append("No broken references found. 🎉")
    else:
        L.append("### Broken references")
        L.append("")

        if recoverable:
            L += [
                "#### Recoverable — Wayback Machine snapshot found",
                "",
                "| Key | Field | Error | Involved terms | Suggested URL |",
                "|-----|-------|-------|----------------|---------------|",
            ]
            for r in recoverable:
                terms = ", ".join(f"`{t}`" for t in r.get("used_by", [])) or "—"
                error = str(r.get("status_code") or r.get("error", ""))
                L.append(f"| `{r['key']}` | `{r['field']}` | {error} | {terms} | `{r['archive_url']}` |")
            L.append("")

        if needs_review:
            L += [
                "#### Needs manual review",
                "",
                "| Key | Field | Error | Domain | Involved terms | Notes |",
                "|-----|-------|-------|--------|----------------|-------|",
            ]
            for r in needs_review:
                terms = ", ".join(f"`{t}`" for t in r.get("used_by", [])) or "—"
                error = str(r.get("status_code") or r.get("error", ""))
                L.append(f"| `{r['key']}` | `{r['field']}` | {error} | {_domain(r)} | {terms} | No archive found. |")
            L.append("")

        if temporary:
            L += [
                "#### Possibly temporary (5xx / 403 / timeout — recheck before acting)",
                "",
                "| Key | Field | Error | Involved terms |",
                "|-----|-------|-------|----------------|",
            ]
            for r in temporary:
                terms = ", ".join(f"`{t}`" for t in r.get("used_by", [])) or "—"
                error = str(r.get("status_code") or r.get("error", ""))
                L.append(f"| `{r['key']}` | `{r['field']}` | {error} | {terms} |")
            L.append("")

    L += [
        "---",
        "",
        "### Fix guidance",
        "",
        "See [BibTeX URL conventions](.claude/AGENT.md#bibtex-url-conventions) in AGENT.md for",
        "domain-specific strategies (NERC, NYISO, PJM, general).",
        "",
        "To apply fixes with agent assistance, run the `/fix-broken-refs` skill in Claude Code.",
        "",
        "---",
        "",
    ]

    agent_data = {
        "scan_date": scan_date,
        "artifact_url": artifact_url or "",
        "run_url": run_url or "",
        "summary": {
            "total_urls": total,
            "broken": len(needs_review),
            "recoverable": len(recoverable),
            "temporary": len(temporary),
        },
        "broken": [
            {
                "key": r["key"],
                "field": r["field"],
                "current_url": r["url"],
                "error": str(r.get("status_code") or r.get("error", "")),
                "domain": _domain(r).lower(),
                "wayback_url": r.get("archive_url"),
                "used_by": r.get("used_by", []),
            }
            for r in recoverable + needs_review
        ],
        "temporary": [
            {
                "key": r["key"],
                "field": r["field"],
                "current_url": r["url"],
                "error": str(r.get("status_code") or r.get("error", "")),
                "used_by": r.get("used_by", []),
            }
            for r in temporary
        ],
    }

    L += [
        "<details>",
        "<summary>Agent instructions (JSON)</summary>",
        "",
        "```json",
        json.dumps(agent_data, indent=2),
        "```",
        "",
        "</details>",
    ]

    return "\n".join(L)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render issue body for reference health tracker")
    parser.add_argument("--report", type=Path, required=True, help="Path to reference_check.json")
    parser.add_argument("--artifact-url", default="", metavar="URL")
    parser.add_argument("--sha", default="", metavar="SHA")
    parser.add_argument("--trigger", default="", metavar="EVENT")
    parser.add_argument("--run-url", default="", metavar="URL")
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    print(render_issue_body(report, args.artifact_url, args.sha, args.trigger, args.run_url))


if __name__ == "__main__":
    main()
