"""
PyScript editor logic for PS-Wiki term editor.
"""

from pyscript import document, window
from term_processor import (
    build_term_json,
    convert_term_to_md,
    validate_term_basic,
    slugify_kebab,
)
import json


def generate_term_id():
    """Generate term ID from title."""
    title = document.getElementById("title").value
    if title:
        term_id = slugify_kebab(title)
        document.getElementById("termId").value = term_id
        return term_id
    return ""


def collect_authors():
    """Collect all authors from the form."""
    authors = []
    author_divs = document.querySelectorAll(".author-entry")
    for div in author_divs:
        name_input = div.querySelector(".author-name")
        url_input = div.querySelector(".author-url")
        if name_input and name_input.value.strip():
            author = {"name": name_input.value.strip()}
            if url_input and url_input.value.strip():
                author["url"] = url_input.value.strip()
            authors.append(author)
    return authors


def collect_sections():
    """Collect all sections from the form."""
    sections = []
    section_divs = document.querySelectorAll(".section-entry")

    for idx, div in enumerate(section_divs):
        title_input = div.querySelector(".section-title")
        type_select = div.querySelector(".section-type")
        body_textarea = div.querySelector(".section-body")
        sources_input = div.querySelector(".section-sources")
        page_input = div.querySelector(".section-page")

        if not title_input or not title_input.value.strip():
            continue

        section = {
            "order": idx + 1,
            "id": slugify_kebab(title_input.value),
            "title": title_input.value.strip(),
            "type": type_select.value if type_select else "note",
            "source_keys": [],
            "page": None,
            "body_md": (
                body_textarea.value.strip() + "\n"
                if body_textarea and body_textarea.value.strip()
                else ""
            ),
        }

        # Parse source keys
        if sources_input and sources_input.value.strip():
            source_keys = [
                s.strip() for s in sources_input.value.split(",") if s.strip()
            ]
            section["source_keys"] = source_keys

        # Add page if provided
        if page_input and page_input.value.strip():
            section["page"] = page_input.value.strip()

        sections.append(section)

    return sections


def generate_term():
    """Generate term JSON from form data."""
    # Get basic fields
    term_id = document.getElementById("termId").value.strip()
    if not term_id:
        term_id = generate_term_id()

    title = document.getElementById("title").value.strip()
    description = document.getElementById("description").value.strip()
    language = document.getElementById("language").value.strip() or "en"
    version = document.getElementById("version").value.strip() or "1.0.0"

    # Parse tags and related
    tags_input = document.getElementById("tags").value
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]

    related_input = document.getElementById("related").value
    related = [r.strip() for r in related_input.split(",") if r.strip()]

    aliases_input = document.getElementById("aliases").value
    aliases = (
        [a.strip() for a in aliases_input.split(",") if a.strip()]
        if aliases_input
        else None
    )

    # Collect authors and sections
    authors = collect_authors()
    sections = collect_sections()

    # Build term JSON
    term = build_term_json(
        term_id=term_id,
        title=title,
        description=description,
        language=language,
        tags=tags,
        related=related,
        authors=authors,
        version=version,
        sections=sections,
        aliases=aliases,
    )

    return term


def update_preview():
    """Update the preview panels."""
    try:
        term = generate_term()

        # Update JSON preview
        json_preview = document.getElementById("jsonPreview")
        json_preview.textContent = json.dumps(term, indent=2, ensure_ascii=False)

        # Update Markdown preview
        markdown = convert_term_to_md(term)
        md_preview = document.getElementById("markdownPreview")
        md_preview.textContent = markdown

        # Clear validation messages
        validation_div = document.getElementById("validationMessages")
        validation_div.innerHTML = ""
        validation_div.className = "validation-messages"

    except Exception as e:
        # Show error in validation messages
        validation_div = document.getElementById("validationMessages")
        validation_div.innerHTML = f'<div class="error-message">Error: {str(e)}</div>'
        validation_div.className = "validation-messages show"


def validate_term():
    """Validate the current term."""
    try:
        term = generate_term()
        errors = validate_term_basic(term)

        validation_div = document.getElementById("validationMessages")

        if errors:
            error_html = (
                '<div class="error-message"><strong>Validation Errors:</strong><ul>'
            )
            for error in errors:
                error_html += f"<li>{error}</li>"
            error_html += "</ul></div>"
            validation_div.innerHTML = error_html
            validation_div.className = "validation-messages show error"
        else:
            validation_div.innerHTML = '<div class="success-message">✓ Validation passed! Term is ready to download.</div>'
            validation_div.className = "validation-messages show success"

    except Exception as e:
        validation_div = document.getElementById("validationMessages")
        validation_div.innerHTML = f'<div class="error-message">Error: {str(e)}</div>'
        validation_div.className = "validation-messages show error"


def download_markdown():
    """Download the generated markdown file."""
    try:
        term = generate_term()
        markdown = convert_term_to_md(term)
        term_id = term["id"]

        # Create blob and download
        blob = window.Blob.new([markdown], {"type": "text/markdown"})
        url = window.URL.createObjectURL(blob)
        a = document.createElement("a")
        a.href = url
        a.download = f"{term_id}.md"
        a.click()
        window.URL.revokeObjectURL(url)

    except Exception as e:
        window.alert(f"Error generating markdown: {str(e)}")


def download_json():
    """Download the generated JSON file."""
    try:
        term = generate_term()
        term_id = term["id"]
        json_str = json.dumps(term, indent=2, ensure_ascii=False)

        # Create blob and download
        blob = window.Blob.new([json_str], {"type": "application/json"})
        url = window.URL.createObjectURL(blob)
        a = document.createElement("a")
        a.href = url
        a.download = f"{term_id}.json"
        a.click()
        window.URL.revokeObjectURL(url)

    except Exception as e:
        window.alert(f"Error generating JSON: {str(e)}")


def load_term_from_json(json_str):
    """Load a term from JSON string into the form."""
    try:
        term = json.loads(json_str)

        # Load basic fields
        document.getElementById("termId").value = term.get("id", "")
        document.getElementById("title").value = term.get("title", "")
        document.getElementById("description").value = term.get("description", "")
        document.getElementById("language").value = term.get("language", "en")
        document.getElementById("version").value = term.get("version", "1.0.0")

        # Load tags and related
        tags = term.get("tags", [])
        document.getElementById("tags").value = ", ".join(tags)

        related = term.get("related", [])
        document.getElementById("related").value = ", ".join(related)

        aliases = term.get("aliases", [])
        if aliases:
            document.getElementById("aliases").value = ", ".join(aliases)

        # Load authors
        authors_container = document.getElementById("authorsContainer")
        authors_container.innerHTML = ""
        for author in term.get("authors", []):
            window.addAuthor(author.get("name", ""), author.get("url", ""))

        # Load sections
        sections_container = document.getElementById("sectionsContainer")
        sections_container.innerHTML = ""
        for section in term.get("content", {}).get("sections", []):
            source_keys = section.get("source_keys", [])
            window.addSection(
                section.get("title", ""),
                section.get("type", "note"),
                section.get("body_md", ""),
                ", ".join(source_keys),
                section.get("page", ""),
            )

        # Update preview
        update_preview()

        # Close modal
        document.getElementById("loadModal").style.display = "none"

        window.alert("Term loaded successfully!")

    except Exception as e:
        window.alert(f"Error loading term: {str(e)}")


# Export functions to JavaScript
window.pyGenerateTermId = generate_term_id
window.pyUpdatePreview = update_preview
window.pyValidateTerm = validate_term
window.pyDownloadMarkdown = download_markdown
window.pyDownloadJson = download_json
window.pyLoadTermFromJson = load_term_from_json
