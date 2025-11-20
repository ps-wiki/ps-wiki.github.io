---
layout: page
title: add new term
permalink: /add-new/
description:
nav: false
horizontal: false
---

The PS-Wiki uses **Markdown files as the editing interface** and **JSON files for storage**. You should always edit Markdown files; the conversion to JSON happens automatically.

# Quick Start

## Adding a New Term

1. **Create a Markdown file** in `_wiki/<term-id>.md` using [stability.md](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/_wiki/stability.md) as a template
2. **Edit the content** following the conventions below
3. **Run the processing script**:
   ```bash
   python database/pyscripts/process_all_terms.py
   ```
4. **Commit both files**: `_wiki/<term-id>.md` and `database/json/<term-id>.json`

## Editing an Existing Term

1. **Edit the Markdown file** in `_wiki/<term-id>.md`
2. **Run the processing script**:
   ```bash
   python database/pyscripts/process_all_terms.py
   ```
3. **Commit the updated files**

# Markdown File Conventions

When creating or editing term Markdown files, follow these conventions:

## Front Matter

The YAML front matter should include:

```yaml
---
title: Term Title
description: Brief description of the term
tags: [tag1, tag2, tag3]
related: [related-term-1, related-term-2]
authors:
  - name: Author Name
    url: https://author-url.com
version: 1.0.0
date: 2025-03-15
lastmod: 2025-11-19
---
```

## Content Structure

- Use `### Section Title` (H3) for section headings
- Start definition sections with `>` (blockquote) for proper formatting
- Include figures using Jekyll's figure.liquid include
- Add citations using `<d-cite key="citation-key"></d-cite>` tags
- Reference bibliography entries from `assets/bibliography/papers.bib`

## Figures

Figures should use this format:

{% raw %}
```html
<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid
        path="/assets/img/pswiki/example-figure.png"
        zoomable=true %}
        Caption with <d-cite key="source-key"></d-cite>
    </div>
</div>

<br>
```
{% endraw %}


**Figure Guidelines:**
- Store figures in `assets/img/pswiki/` directory
- Use relative paths starting with `/assets/img/pswiki/`
- Include concise captions in Markdown format
- Set `zoomable=true` for click-to-zoom functionality
- Reference sources using `<d-cite>` tags in captions

## Citations

Add source citations at the end of each section:

```markdown
Source: <d-cite key="citation-key"></d-cite> p42
```

The citation keys must correspond to entries in `assets/bibliography/papers.bib`.

# Processing Script Options

The `process_all_terms.py` script provides several options:

```bash
# Process all terms (recommended)
python database/pyscripts/process_all_terms.py

# Process only specific terms
python database/pyscripts/process_all_terms.py --only stability frequency-control

# Dry-run mode (see what would be done)
python database/pyscripts/process_all_terms.py --dry-run

# Verbose output
python database/pyscripts/process_all_terms.py --verbose

# Skip validation (not recommended)
python database/pyscripts/process_all_terms.py --no-validate
```

# Advanced: Working with JSON Directly

While **editing JSON files directly is not recommended**, you may need to work with JSON for:

- Schema migrations
- Bulk updates
- Automated processing

## JSON File Structure

Each term is stored as `database/json/<term-id>.json` with this structure:

```json
{
  "$schema": "https://ps-wiki.github.io/schema/v1/term.schema.json",
  "id": "term-id",
  "title": "Term Title",
  "description": "Brief description",
  "language": "en",
  "tags": ["tag1", "tag2"],
  "related": ["related-term-1"],
  "version": "1.0.0",
  "breaking": false,
  "dates": {
    "created": "2025-03-15",
    "last_modified": "2025-11-19"
  },
  "authors": [
    {
      "name": "Author Name",
      "url": "https://author-url.com"
    }
  ],
  "content": {
    "sections": [
      {
        "order": 1,
        "id": "section-id",
        "title": "Section Title",
        "type": "definition",
        "source_keys": ["citation-key"],
        "page": "p42",
        "body_md": "Section content in Markdown...\n"
      }
    ]
  }
}
```

## Regenerating Markdown from JSON

If you need to regenerate Markdown files from JSON (e.g., after a schema migration):

```bash
# Regenerate all Markdown files
python database/pyscripts/json2md_all.py --in-dir database/json --out-dir _wiki --overwrite

# Regenerate a single file
python database/pyscripts/json2md.py --input database/json/stability.json --output _wiki/stability.md --overwrite
```

# Troubleshooting

## Validation Errors

If you encounter validation errors:

1. Check the error message for the specific issue
2. Verify all required fields are present in the front matter
3. Ensure citation keys exist in `assets/bibliography/papers.bib`
4. Verify figure paths are correct
5. Check that related term IDs exist

## Formatting Issues

To format a Markdown file:

```bash
python database/pyscripts/md_format.py -i _wiki/<term-id>.md
```

This performs a roundtrip conversion (MD → JSON → MD) to normalize formatting.

## Schema Reference Missing

The processing script automatically adds the `$schema` field to JSON files. If needed manually:

```bash
python database/pyscripts/add_schema_reference.py
```

# Deployment

During website deployment, JSON files are automatically converted back to Markdown for rendering. The JSON files serve as the canonical source of truth for the data.

**Note:** There may be minor formatting differences between your original Markdown and the deployed version due to the conversion process. This is normal and ensures consistency across all terms.

