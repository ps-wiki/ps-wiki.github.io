import pytest
from render import cite_to_footnotes, callouts_to_admonitions

ADEQUACY_SECTION1 = (
    "> The ability of the electric system to supply the aggregate electrical demand and energy requirements of the end-use customers at all times, "
    "taking into account scheduled and reasonably expected unscheduled outages of system elements.\n"
    "\n"
    "<!-- prettier-ignore-start -->\n"
    '> The previous reference <d-cite key="nerc2013terminology"></d-cite> is no longer available.\n'
    "{: .block-danger }\n"
    "<!-- prettier-ignore-end -->\n"
)

REAL_BIB_ENTRIES = {
    "nerc2013terminology": {
        "fields": {
            "author": "North American Electric Reliability Corporation (NERC)",
            "title": "Reliability Terminology",
            "year": "2013",
            "month": "August",
            "url": "https://www.nerc.com/AboutNERC/Documents/Terms%20AUG13.pdf",
        }
    }
}


# --- cite_to_footnotes ---


def test_cite_known_key_reference_inserted():
    bib = {
        "smith2020": {
            "fields": {
                "author": "J. Smith",
                "year": "2020",
                "title": "Power Systems",
                "url": "https://example.com",
            }
        }
    }
    body = 'See <d-cite key="smith2020"></d-cite> for details.'
    out, defs = cite_to_footnotes(body, bib)
    assert "[^smith2020]" in out
    assert "<d-cite" not in out
    assert len(defs) == 1
    assert defs[0] == "[^smith2020]: J. Smith (2020). *Power Systems*. [https://example.com](https://example.com)"


def test_cite_missing_key_fallback():
    body = 'See <d-cite key="ghost2099"></d-cite>.'
    out, defs = cite_to_footnotes(body, {})
    assert "[^ghost2099]" in out
    assert len(defs) == 1
    assert defs[0] == "[^ghost2099]: [ghost2099]"


def test_cite_prettier_ignore_stripped():
    body = (
        "<!-- prettier-ignore-start -->\n"
        'Some text <d-cite key="k1"></d-cite>.\n'
        "<!-- prettier-ignore-end -->\n"
    )
    out, _ = cite_to_footnotes(body, {})
    assert "<!-- prettier-ignore-start -->" not in out
    assert "<!-- prettier-ignore-end -->" not in out


def test_cite_deduplication():
    body = (
        'First <d-cite key="dup"></d-cite> and second <d-cite key="dup"></d-cite>.'
    )
    out, defs = cite_to_footnotes(body, {})
    assert out.count("[^dup]") == 2
    assert len(defs) == 1


def test_cite_partial_fields_no_url():
    bib = {
        "nourl": {
            "fields": {
                "author": "A. Author",
                "year": "2021",
                "title": "Some Title",
            }
        }
    }
    body = '<d-cite key="nourl"></d-cite>'
    out, defs = cite_to_footnotes(body, bib)
    assert len(defs) == 1
    assert "https" not in defs[0]
    assert "*Some Title*" in defs[0]


# --- callouts_to_admonitions ---


def test_callout_block_danger_real_excerpt():
    body = (
        "<!-- prettier-ignore-start -->\n"
        "> The previous reference is no longer available.\n"
        "{: .block-danger }\n"
        "<!-- prettier-ignore-end -->\n"
    )
    out = callouts_to_admonitions(body)
    assert "!!! danger" in out
    assert "    The previous reference is no longer available." in out
    assert "{: .block-danger }" not in out
    assert "<!-- prettier-ignore" not in out


def test_callout_block_tip():
    body = (
        "<!-- prettier-ignore-start -->\n"
        "> This is a tip.\n"
        "{: .block-tip }\n"
        "<!-- prettier-ignore-end -->\n"
    )
    out = callouts_to_admonitions(body)
    assert "!!! tip" in out
    assert "    This is a tip." in out
    assert "{: .block-tip }" not in out


def test_callout_block_warning():
    body = (
        "<!-- prettier-ignore-start -->\n"
        "> Be careful here.\n"
        "{: .block-warning }\n"
        "<!-- prettier-ignore-end -->\n"
    )
    out = callouts_to_admonitions(body)
    assert "!!! warning" in out
    assert "    Be careful here." in out
    assert "{: .block-warning }" not in out


def test_plain_blockquote_unchanged():
    body = "> This is a plain blockquote with no callout marker.\n"
    out = callouts_to_admonitions(body)
    assert out == body


def test_multiple_callouts_both_transformed():
    body = (
        "<!-- prettier-ignore-start -->\n"
        "> First callout.\n"
        "{: .block-tip }\n"
        "<!-- prettier-ignore-end -->\n"
        "\n"
        "Some prose.\n"
        "\n"
        "<!-- prettier-ignore-start -->\n"
        "> Second callout.\n"
        "{: .block-warning }\n"
        "<!-- prettier-ignore-end -->\n"
    )
    out = callouts_to_admonitions(body)
    assert "!!! tip" in out
    assert "!!! warning" in out
    assert "{: .block-tip }" not in out
    assert "{: .block-warning }" not in out


# --- Composition ---


def test_composition_adequacy_section1():
    step1 = callouts_to_admonitions(ADEQUACY_SECTION1)
    step2, defs = cite_to_footnotes(step1, REAL_BIB_ENTRIES)

    assert "<d-cite" not in step2
    assert "{: .block-" not in step2
    assert "!!! danger" in step2
    assert "[^nerc2013terminology]" in step2
    assert len(defs) == 1
    assert "Reliability Terminology" in defs[0]
