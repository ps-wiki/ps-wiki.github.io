"""serve_cmd — build and serve the MkDocs site."""

import subprocess
import sys

_BIB_INPUT = "assets/bibliography/papers.bib"
_BIB_OUTPUT = "database/build/bib.json"


def _prebuild() -> None:
    """Regenerate bib.json and docs/wiki/ before serving or building."""
    from bib2json import build_bib_json

    n = build_bib_json(_BIB_INPUT, _BIB_OUTPUT, pretty=True)
    print(f"Built bib.json ({n} entries)")

    from json2mkdocs import generate

    count = generate()
    print(f"Generated {count} term pages")


def cmd_serve() -> None:
    _prebuild()
    print(
        "\nServing at http://localhost:8000\n"
        "Tip: run 'python pswiki.py process <id>' in another terminal to update a term.\n"
    )
    subprocess.run(["mkdocs", "serve"], check=True)


def cmd_build() -> None:
    _prebuild()
    result = subprocess.run(["mkdocs", "build", "--strict"])
    sys.exit(result.returncode)
