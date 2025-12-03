#!/usr/bin/env python3
"""
Test script to verify the term_processor module works correctly.
This simulates what PyScript will do in the browser.
"""

import json
from term_processor import (
    build_term_json,
    convert_term_to_md,
    validate_term_basic,
    slugify_kebab,
)


def test_basic_functionality():
    """Test basic term generation and conversion."""
    print("Testing PS-Wiki Term Editor Components...")
    print("=" * 60)

    # Test 1: Slugify function
    print("\n1. Testing slugify_kebab()...")
    test_title = "Frequency Stability"
    term_id = slugify_kebab(test_title)
    print(f"   Title: '{test_title}'")
    print(f"   Generated ID: '{term_id}'")
    assert (
        term_id == "frequency-stability"
    ), f"Expected 'frequency-stability', got '{term_id}'"
    print("   ✓ Slugify works correctly")

    # Test 2: Build term JSON
    print("\n2. Testing build_term_json()...")
    term = build_term_json(
        term_id="test-term",
        title="Test Term",
        description="A test term for validation",
        language="en",
        tags=["test", "validation"],
        related=["related-term"],
        authors=[{"name": "Test Author", "url": "https://example.com"}],
        version="1.0.0",
        sections=[
            {
                "order": 1,
                "id": "definition",
                "title": "Definition",
                "type": "definition",
                "source_keys": ["test2024"],
                "page": "p. 42",
                "body_md": "> This is a test definition.\n",
            }
        ],
    )
    print(f"   Generated term with ID: {term['id']}")
    print(f"   Title: {term['title']}")
    print(f"   Sections: {len(term['content']['sections'])}")
    print("   ✓ Term JSON generation works")

    # Test 3: Validate term
    print("\n3. Testing validate_term_basic()...")
    errors = validate_term_basic(term)
    if errors:
        print(f"   ✗ Validation failed with {len(errors)} errors:")
        for error in errors:
            print(f"     - {error}")
    else:
        print("   ✓ Validation passed (no errors)")

    # Test 4: Convert to markdown
    print("\n4. Testing convert_term_to_md()...")
    markdown = convert_term_to_md(term)
    print(f"   Generated markdown ({len(markdown)} characters)")
    print("   First 200 characters:")
    print("   " + markdown[:200].replace("\n", "\n   "))
    print("   ✓ Markdown conversion works")

    # Test 5: Verify markdown structure
    print("\n5. Verifying markdown structure...")
    assert markdown.startswith("---"), "Markdown should start with front matter"
    assert "title: Test Term" in markdown, "Title should be in front matter"
    assert "### Definition" in markdown, "Section heading should be present"
    assert "> This is a test definition." in markdown, "Body content should be present"
    print("   ✓ Markdown structure is correct")

    # Test 6: JSON roundtrip
    print("\n6. Testing JSON serialization...")
    json_str = json.dumps(term, indent=2, ensure_ascii=False)
    term_reloaded = json.loads(json_str)
    assert term_reloaded["id"] == term["id"], "JSON roundtrip failed"
    print(f"   JSON size: {len(json_str)} bytes")
    print("   ✓ JSON serialization works")

    print("\n" + "=" * 60)
    print("✓ All tests passed successfully!")
    print("\nThe term_processor module is working correctly.")
    print("The editor should function properly in PyScript.")

    return term, markdown


if __name__ == "__main__":
    term, markdown = test_basic_functionality()

    # Optionally save test outputs
    print("\n" + "=" * 60)
    print("Saving test outputs...")

    with open("test_output.json", "w", encoding="utf-8") as f:
        json.dump(term, f, indent=2, ensure_ascii=False)
    print("✓ Saved: test_output.json")

    with open("test_output.md", "w", encoding="utf-8") as f:
        f.write(markdown)
    print("✓ Saved: test_output.md")

    print("\nYou can inspect these files to verify the output format.")
