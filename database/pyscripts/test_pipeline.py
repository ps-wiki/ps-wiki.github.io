import json
from pathlib import Path

from json2md import render_figure_block
from json2mkdocs import _generate_term_page
from md2json import parse_sections
from validate import validate_corpus


SCHEMA_PATH = Path("database/schema/v1/term.schema.json")


def _term(term_id: str, body_md: str = "", figures: list[dict] | None = None) -> dict:
    section = {
        "order": 1,
        "id": "definition",
        "title": "Definition",
        "type": "definition",
        "source_keys": [],
        "page": None,
        "body_md": body_md,
    }
    if figures:
        section["figures"] = figures

    return {
        "id": term_id,
        "title": term_id.replace("-", " ").title(),
        "description": f"Definition of {term_id}.",
        "language": "en",
        "tags": [],
        "related": [],
        "breaking": False,
        "dates": {"created": "2026-01-01", "last_modified": "2026-01-01"},
        "authors": [{"name": "Test Author"}],
        "content": {"sections": [section]},
    }


def test_standard_markdown_figure_is_extracted_with_citation_free_alt():
    body = """### Definition

Source: <d-cite key="source-main"></d-cite> p. 4

![Figure 1 (from <d-cite key="source-figure"></d-cite>)](/assets/img/figure.png)

*Figure 1 (from <d-cite key="source-figure"></d-cite>)*

> Definition body.
"""

    section = parse_sections(body)[0]

    assert section.source_keys == ["source-main"]
    assert section.page == "p. 4"
    assert section.body_md == "> Definition body.\n"
    assert len(section.figures) == 1
    assert section.figures[0].path == "/assets/img/figure.png"
    assert section.figures[0].alt == "Figure 1"
    assert section.figures[0].caption_md == (
        'Figure 1 (from <d-cite key="source-figure"></d-cite>)'
    )
    assert section.figures[0].source_keys == ["source-figure"]


def test_inline_markdown_image_remains_in_section_body():
    body = """### Note

This sentence contains ![an inline image](/assets/img/inline.png) in its body.
"""

    section = parse_sections(body)[0]

    assert section.figures == []
    assert "![an inline image]" in section.body_md


def test_json_to_markdown_renders_modern_figure_syntax():
    rendered = render_figure_block(
        {
            "path": "/assets/img/figure.png",
            "alt": "Figure 1",
            "caption_md": 'Figure 1 (from <d-cite key="source"></d-cite>)',
            "zoomable": True,
        }
    )

    assert rendered.startswith("![Figure 1](/assets/img/figure.png)\n")
    assert '*Figure 1 (from <d-cite key="source"></d-cite>)*' in rendered
    assert "figure.liquid" not in rendered
    assert "<br>" not in rendered


def test_mkdocs_generation_normalizes_links_and_keeps_citations_out_of_alt():
    term = _term(
        "alpha",
        body_md=(
            "See [Beta](/wiki/beta) and "
            '<img src="/assets/img/inline.png" alt="Inline">.\n'
        ),
        figures=[
            {
                "path": "/assets/img/figure.png",
                "alt": 'Figure 1 <d-cite key="source"></d-cite>',
                "caption_md": 'Figure 1 (from <d-cite key="source"></d-cite>)',
                "zoomable": True,
                "source_keys": ["source"],
            }
        ],
    )
    bib = {
        "source": {
            "fields": {
                "author": "A. Author",
                "year": "2026",
                "title": "Source",
                "url": "https://example.com/source",
            }
        }
    }

    rendered = _generate_term_page(term, bib, None, None)

    assert "![Figure 1](../assets/img/figure.png)" in rendered
    assert "*Figure 1 (from [^source])*" in rendered
    assert "![Figure 1 [^source]]" not in rendered
    assert "[Beta](beta.md)" in rendered
    assert 'src="../assets/img/inline.png"' in rendered
    assert "](/wiki/" not in rendered
    assert "](/assets/" not in rendered


def test_corpus_validation_reports_broken_content_references(tmp_path: Path):
    json_dir = tmp_path / "database" / "json"
    assets_dir = tmp_path / "assets"
    json_dir.mkdir(parents=True)
    assets_dir.mkdir()

    alpha = _term(
        "alpha",
        body_md=(
            "See [Missing](/wiki/missing).\n\n"
            "![Bad alt <d-cite key=\"source\"></d-cite>]"
            "(/assets/img/missing.png)\n"
        ),
    )
    beta = _term("beta", body_md="> Valid body.\n")
    (json_dir / "alpha.json").write_text(json.dumps(alpha), encoding="utf-8")
    (json_dir / "beta.json").write_text(json.dumps(beta), encoding="utf-8")

    errors = validate_corpus(
        json_dir,
        SCHEMA_PATH,
        assets_dir=assets_dir,
    )

    assert any("wiki target 'missing' not found" in error for error in errors)
    assert any("asset '/assets/img/missing.png' not found" in error for error in errors)
    assert any("image alt text must not contain <d-cite>" in error for error in errors)
