#!/usr/bin/env python3
"""
pswiki — centralized developer CLI for the Power Systems Wiki.

Usage:
    python pswiki.py new <id>              Scaffold a new term
    python pswiki.py process [<id> ...]   Run full pipeline
    python pswiki.py validate [<id> ...]  Validate JSON against schema
    python pswiki.py serve                Build and serve site locally
    python pswiki.py build                Production build (mkdocs --strict)
    python pswiki.py check-refs           Check bibliography URLs for broken links
    python pswiki.py check-refs --recover Also query Wayback Machine for broken NERC URLs
"""

import argparse
import os
import sys
from pathlib import Path

# Make database/pyscripts importable regardless of where Python is invoked from.
_REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_REPO_ROOT / "database" / "pyscripts"))


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------


def _cmd_new(args: argparse.Namespace) -> None:
    from cli.new_cmd import cmd_new

    cmd_new(args.id)


def _cmd_process(args: argparse.Namespace) -> None:
    from bib2json import build_bib_json
    from process import build_index_files, process_term
    from utils import (
        DEFAULT_BUILD_DIR,
        DEFAULT_JSON_DIR,
        DEFAULT_SCHEMA_PATH,
        DEFAULT_WIKI_DIR,
        Colors,
    )

    wiki_dir = Path(DEFAULT_WIKI_DIR)
    json_dir = Path(DEFAULT_JSON_DIR)
    schema_path = Path(DEFAULT_SCHEMA_PATH)
    build_dir = Path(DEFAULT_BUILD_DIR)

    term_ids: list[str] = args.terms
    if term_ids:
        md_files = []
        for tid in term_ids:
            f = wiki_dir / f"{tid}.md"
            if not f.exists():
                print(f"ERROR: _wiki/{tid}.md not found.", file=sys.stderr)
                sys.exit(1)
            md_files.append(f)
    else:
        md_files = sorted(wiki_dir.glob("*.md"))

    if not md_files:
        print("No term files found.", file=sys.stderr)
        sys.exit(1)

    failed = 0
    for md_path in md_files:
        result = process_term(
            md_path,
            json_dir,
            schema_path,
            dry_run=args.dry_run,
            skip_validate=args.no_validate,
        )
        tid = md_path.stem
        if result["success"]:
            print(Colors.success(f"[{tid}] ✓"))
        else:
            print(Colors.error(f"[{tid}] ✗  {', '.join(result['errors'])}"))
            failed += 1

    if not args.dry_run:
        build_index_files(json_dir, build_dir)
        n_terms = len(md_files)
        print(f"\nRebuilt index.json + tags.json ({n_terms} terms)")

        bib_in = str(_REPO_ROOT / "assets" / "bibliography" / "papers.bib")
        bib_out = str(build_dir / "bib.json")
        n_bib = build_bib_json(bib_in, bib_out, pretty=True)
        print(f"Rebuilt bib.json ({n_bib} entries)")

    if failed:
        print(Colors.error(f"\n{failed} term(s) failed."), file=sys.stderr)
        sys.exit(1)


def _cmd_validate(args: argparse.Namespace) -> None:
    from utils import DEFAULT_JSON_DIR, DEFAULT_SCHEMA_PATH
    from validate import validate_corpus

    json_dir = Path(DEFAULT_JSON_DIR)
    schema_path = Path(DEFAULT_SCHEMA_PATH)
    term_ids: list[str] | None = args.terms or None

    errors = validate_corpus(
        json_dir,
        schema_path,
        term_ids=term_ids,
        filename_match=True,
    )

    if errors:
        for e in errors:
            print(e)
        print(f"\n{len(errors)} error(s).", file=sys.stderr)
        sys.exit(1)

    n = len(term_ids) if term_ids else len(sorted(json_dir.glob("*.json")))
    print(f"✓ {n} term(s) valid")


def _cmd_serve(args: argparse.Namespace) -> None:
    from cli.serve_cmd import cmd_serve

    cmd_serve()


def _cmd_build(args: argparse.Namespace) -> None:
    from cli.serve_cmd import cmd_build

    cmd_build()


def _cmd_check_refs(args: argparse.Namespace) -> None:
    from check_references import (
        build_report,
        collect_urls,
        load_bib,
        print_summary,
        scan,
    )

    bib_path = Path(args.bib) if args.bib else _REPO_ROOT / "assets" / "bibliography" / "papers.bib"
    out_path = Path(args.out) if args.out else _REPO_ROOT / "database" / "build" / "reference_check.json"

    print(f"Parsing {bib_path} ...")
    entries = load_bib(bib_path)
    records = collect_urls(entries)
    print(f"Found {len(records)} unique URLs across {len(entries)} entries.\n")

    print("Scanning URLs ...")
    results = scan(records, recover=args.recover)

    import json

    report = build_report(results, bib_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport written to {out_path}")

    print_summary(report)

    broken = report["summary"].get("broken", 0) + report["summary"].get("server_error", 0)
    if broken:
        sys.exit(1)


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pswiki",
        description="Power Systems Wiki — developer CLI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python pswiki.py new power-quality\n"
            "  python pswiki.py process power-quality adequacy\n"
            "  python pswiki.py process\n"
            "  python pswiki.py validate\n"
            "  python pswiki.py serve\n"
            "  python pswiki.py build\n"
            "  python pswiki.py check-refs\n"
            "  python pswiki.py check-refs --recover\n"
        ),
    )

    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # new
    p_new = sub.add_parser("new", help="Scaffold a new term in _wiki/<id>.md")
    p_new.add_argument("id", help="Term ID in kebab-case (e.g. power-quality)")
    p_new.set_defaults(func=_cmd_new)

    # process
    p_proc = sub.add_parser(
        "process",
        help="Run full pipeline: format → JSON → validate → index → bib",
    )
    p_proc.add_argument(
        "terms", nargs="*", metavar="ID", help="Term IDs to process (default: all)"
    )
    p_proc.add_argument(
        "--dry-run", action="store_true", help="Preview changes without writing files"
    )
    p_proc.add_argument(
        "--no-validate", action="store_true", help="Skip schema validation"
    )
    p_proc.set_defaults(func=_cmd_process)

    # validate
    p_val = sub.add_parser("validate", help="Validate term JSON against schema")
    p_val.add_argument(
        "terms", nargs="*", metavar="ID", help="Term IDs to validate (default: all)"
    )
    p_val.set_defaults(func=_cmd_validate)

    # serve
    p_serve = sub.add_parser(
        "serve", help="Build site and serve locally at http://localhost:8000"
    )
    p_serve.set_defaults(func=_cmd_serve)

    # build
    p_build = sub.add_parser(
        "build", help="Production build (mkdocs build --strict)"
    )
    p_build.set_defaults(func=_cmd_build)

    # check-refs
    p_chk = sub.add_parser(
        "check-refs",
        help="Check bibliography URLs for broken links",
    )
    p_chk.add_argument(
        "--recover",
        action="store_true",
        help="Query Wayback Machine for broken NERC URLs",
    )
    p_chk.add_argument("--bib", metavar="PATH", help="Path to .bib file (default: papers.bib)")
    p_chk.add_argument("--out", metavar="PATH", help="Path for JSON report (default: database/build/reference_check.json)")
    p_chk.set_defaults(func=_cmd_check_refs)

    return parser


def main() -> None:
    # Change to repo root so all relative paths in sub-scripts resolve correctly.
    os.chdir(_REPO_ROOT)
    parser = _build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
