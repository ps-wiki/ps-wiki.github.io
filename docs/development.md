---
title: Development
description: How to contribute terms, run the pipeline, and build the site locally
---

## Repository Structure

| Path                                  | Purpose                                                                               |
| ------------------------------------- | ------------------------------------------------------------------------------------- |
| `_wiki/<term-id>.md`                  | **Editing interface.** One Markdown file per term — what you hand-edit.               |
| `database/json/<term-id>.json`        | **Storage.** Generated from the Markdown; do not hand-edit.                           |
| `database/build/`                     | Generated `index.json`, `tags.json`, `bib.json` — consumed by the API and site build. |
| `database/schema/v1/term.schema.json` | JSON Schema that all term files are validated against.                                |
| `assets/bibliography/papers.bib`      | BibTeX entries referenced by `<d-cite key="...">` tags.                               |
| `assets/img/pswiki/`                  | Images embedded in term definitions.                                                  |
| `docs/`                               | MkDocs source pages. `docs/wiki/` is **generated** — do not hand-edit.                |
| `mkdocs.yml`                          | MkDocs Material site configuration.                                                   |
| `worker/`                             | Cloudflare Worker REST API (TypeScript).                                              |
| `mcp/`                                | MCP server (Python).                                                                  |

## Adding or Editing a Term

### 1. Edit the Markdown file

Create or edit `_wiki/<term-id>.md`. Use `_wiki/adequacy.md` or `_wiki/stability.md` as templates.

Term IDs are **kebab-case** and must match the filename stem (e.g. `frequency-stability` → `_wiki/frequency-stability.md`).

### 2. Run the pipeline

```bash
python database/pyscripts/process.py --terms <term-id>
```

This runs format → convert → validate → rebuild the index. Omit `--terms` to process all 181 terms.

```bash
python database/pyscripts/process.py              # all terms
python database/pyscripts/process.py --index-only # rebuild index only
python database/pyscripts/process.py --dry-run --verbose  # preview, no writes
```

### 3. Preview locally

```bash
python database/pyscripts/json2mkdocs.py --terms <term-id>   # regenerate that term's page
mkdocs serve                                                   # live preview at localhost:8000
```

### 4. Commit both files

```
_wiki/<term-id>.md
database/json/<term-id>.json
```

Never commit changes to `docs/wiki/` (generated) or `database/build/` (regenerated in CI).

---

## Term Markdown Conventions

### Front matter

```yaml
---
title: Term Title
description: Brief one-sentence definition.
tags: [tag1, tag2]
related: [related-term-id-1, related-term-id-2]
authors:
  - name: Author Name
    url: https://author-url.com
version: 1.0.0
date: 2025-03-15
lastmod: 2025-11-19
---
```

`lastmod` and the `generated` comment are managed by the pipeline — don't set them manually.  
Bump `version` (semver) on meaningful content changes.

### Sections

Use `### Section Title` (H3) for sections. Start each definition with a `>` blockquote:

```markdown
### Definition by NERC

Source: <d-cite key="nerc2024glossary"></d-cite>

> The ability of the electric system to supply the aggregate demand...
```

### Citations

Cite sources inline with `<d-cite key="citation-key"></d-cite>`. The key must exist in `assets/bibliography/papers.bib` — add the BibTeX entry there before using the key.

To attribute a section to a source, add a `Source:` line before the body:

```markdown
Source: <d-cite key="nerc2024glossary"></d-cite> p42
```

For multiple sources: `Source: <d-cite key="key1"></d-cite> <d-cite key="key2"></d-cite>`

The pipeline resolves citations to footnotes in the rendered site.

### Callouts

Use kramdown block attributes for highlighted notes:

```markdown
<!-- prettier-ignore-start -->
> This term was deprecated in the 2024 revision.
{: .block-warning }
<!-- prettier-ignore-end -->
```

Available types: `block-danger`, `block-warning`, `block-tip`, `block-note`.
The `<!-- prettier-ignore -->` wrappers are required to prevent CI formatting errors.

### Figures

Store images in `assets/img/pswiki/` then reference them in the section body:

```html
<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid path="/assets/img/pswiki/your-figure.png" zoomable=true %} Caption text with optional <d-cite key="source-key"></d-cite>
  </div>
</div>
<br />
```

The pipeline extracts figures into the JSON and the site generator renders them with lightbox zoom.

---

## Pipeline Scripts

### `process.py` — main orchestrator

```bash
python database/pyscripts/process.py [--terms id1 id2] [--index-only] [--dry-run] [--no-validate] [--verbose]
```

Runs the full chain: `format.py` → `md2json.py` → `validate.py` → index rebuild.

### Individual scripts

```bash
# Markdown → JSON
python database/pyscripts/md2json.py --terms stability

# JSON → Markdown (normalise / roundtrip)
python database/pyscripts/json2md.py --terms stability

# Format (MD → JSON → MD roundtrip to normalise)
python database/pyscripts/format.py --terms stability

# Validate JSON against schema
python database/pyscripts/validate.py --terms stability

# Generate MkDocs pages from JSON
python database/pyscripts/json2mkdocs.py --terms stability
```

---

## Local Site Build

```bash
# Install dependencies (once)
pip install -r database/requirements.txt -r requirements-docs.txt

# Generate all term pages, then serve with live reload
python database/pyscripts/json2mkdocs.py
mkdocs serve

# Production build (mirrors CI)
python database/pyscripts/json2mkdocs.py
mkdocs build --strict
```

The site builds in ~1.3 s for all 181 terms.

---

## Adding a Citation

1. Add the BibTeX entry to `assets/bibliography/papers.bib`.
2. Use the key in `<d-cite key="your-key"></d-cite>` in `_wiki/<term-id>.md`.
3. Run `python database/pyscripts/process.py --terms <term-id>` to rebuild.

The pipeline's `bib2json.py` exports `papers.bib` → `database/build/bib.json` which the site generator uses to render footnotes.

---

## Formatting & CI

The CI pipeline enforces [Prettier](https://prettier.io/) formatting (print width 150, Liquid plugin). Run before pushing:

```bash
npx prettier --write .
```

Pre-commit hooks also enforce: trailing whitespace, end-of-file newline, valid YAML, no large files.

---

## JSON Schema

All term JSON files conform to `database/schema/v1/term.schema.json`. Key fields:

| Field                            | Type     | Notes                                               |
| -------------------------------- | -------- | --------------------------------------------------- |
| `id`                             | string   | Kebab-case, matches filename                        |
| `title`                          | string   | Display name                                        |
| `description`                    | string   | One-sentence summary                                |
| `tags`                           | string[] | Lowercase kebab-case                                |
| `related`                        | string[] | IDs of related terms                                |
| `version`                        | string   | Semver (bump on content change)                     |
| `content.sections`               | array    | Ordered list of definition sections                 |
| `content.sections[].source_keys` | string[] | BibTeX keys for this section                        |
| `content.sections[].body_md`     | string   | Markdown body (may contain `<d-cite>` and callouts) |

---

## Contributing

Contributions are welcome. The preferred workflow is:

1. Fork the repository and create a branch.
2. Add or edit terms following the conventions above.
3. Run the pipeline and confirm `mkdocs build --strict` passes with 0 warnings.
4. Run `npx prettier --write .` before committing.
5. Open a pull request — CI will validate, build, and check formatting automatically.

For questions or to report issues: [GitHub Issues](https://github.com/ps-wiki/pswiki/issues).

---

## License

Content is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Free for academic and non-commercial use.
