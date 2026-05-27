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

---

## Developer CLI

All workflows go through `pswiki.py` at the repo root:

```bash
python pswiki.py new <term-id>        # scaffold a new term
python pswiki.py process <term-id>    # run the full pipeline for one term
python pswiki.py process              # process all terms
python pswiki.py validate             # validate all term JSON files
python pswiki.py serve                # local preview at http://localhost:8000
python pswiki.py build                # production build (mkdocs --strict)
```

Install Python dependencies before first use:

```bash
pip install -r database/requirements.txt -r requirements-docs.txt
```

---

## Adding or Editing a Term

### 1. Scaffold or create the Markdown file

For a new term, scaffold it:

```bash
python pswiki.py new <term-id>
```

This creates `_wiki/<term-id>.md` with all required front matter pre-filled. For an existing term, edit `_wiki/<term-id>.md` directly.

Term IDs are **kebab-case** and must match the filename stem (e.g. `frequency-stability` → `_wiki/frequency-stability.md`).

### 2. Run the pipeline

```bash
python pswiki.py process <term-id>
```

This runs format → convert → validate → rebuild the index and `bib.json`. Omit the ID to process all terms.

```bash
python pswiki.py process              # all terms
python pswiki.py process --dry-run    # preview without writing
python pswiki.py process --no-validate  # skip schema validation (faster, for drafting)
```

### 3. Preview locally

```bash
python pswiki.py serve
```

Builds the full site and starts a live-reload server at <http://localhost:8000>. To pick up edits to a term while the server is running, run `python pswiki.py process <term-id>` in a second terminal — mkdocs detects the regenerated page and reloads.

### 4. Commit both files

```
_wiki/<term-id>.md
database/json/<term-id>.json
```

Never commit `docs/wiki/` (generated) or `database/build/` (regenerated at build time).

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
date: 2025-03-15
lastmod: 2025-11-19
---
```

`lastmod` and `generated` are managed by the pipeline — do not set them manually.

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

The pipeline resolves citations to footnotes in the rendered site. If a BibTeX entry has a `doi` field, the footnote links to `https://doi.org/{doi}`; otherwise it uses the `url` field.

### Callouts

Use kramdown block attributes for highlighted notes:

```markdown
<!-- prettier-ignore-start -->
> This term was deprecated in the 2024 revision.
{: .block-warning }
<!-- prettier-ignore-end -->
```

Available types: `block-danger`, `block-warning`, `block-tip`, `block-note`. The pipeline converts these to MkDocs admonitions at build time. The `<!-- prettier-ignore -->` wrappers are required to prevent CI formatting errors.

### Figures

Store images in `assets/img/pswiki/` then embed them with standard Markdown:

```markdown
![Caption text (from <d-cite key="source-key"></d-cite>)](/assets/img/pswiki/your-figure.png)
```

The pipeline extracts figures into the JSON and the site generator renders them with lightbox zoom.

---

## Adding a Citation

1. Add the BibTeX entry to `assets/bibliography/papers.bib`.
2. Use the key in `<d-cite key="your-key"></d-cite>` in `_wiki/<term-id>.md`.
3. Run `python pswiki.py process <term-id>` to rebuild.

---

## Formatting & CI

The CI pipeline enforces [Prettier](https://prettier.io/) formatting (print width 150). Run before pushing:

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
| `content.sections`               | array    | Ordered list of definition sections                 |
| `content.sections[].source_keys` | string[] | BibTeX keys for this section                        |
| `content.sections[].body_md`     | string   | Markdown body (may contain `<d-cite>` and callouts) |

---

## Contributing

Contributions are welcome. The preferred workflow is:

1. Fork the repository and create a branch.
2. Add or edit terms following the conventions above.
3. Run the pipeline and confirm `python pswiki.py build` passes with 0 warnings.
4. Run `npx prettier --write .` before committing.
5. Open a pull request — CI will validate, build, and check formatting automatically.

For questions or to report issues: [GitHub Issues](https://github.com/ps-wiki/pswiki/issues).

---

## License

Content is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Free for academic and non-commercial use.
