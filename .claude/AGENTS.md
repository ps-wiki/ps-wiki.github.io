# PS-Wiki — Agent Guide

Single source of truth for AI assistants (Claude Code & Codex) working in this repo.
Root `CLAUDE.md` and `AGENTS.md` are thin pointers to this file.

## What this project is

The **Power Systems Wiki** — an open reference compiling power-systems engineering
terminology from papers, standards, and reports. It is a [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
static site driven by a JSON database, plus a REST API and an MCP server.

Stack: **Python/MkDocs** (site + data pipeline) + **Node/TypeScript** (Cloudflare Worker API & MCP).

## Repository map

| Path | Purpose |
|------|---------|
| `_wiki/<term-id>.md` | **Editing interface.** One markdown file per term — what you hand-edit. |
| `database/json/<term-id>.json` | **Storage.** Generated from the markdown; do not hand-edit. |
| `database/pyscripts/` | Python pipeline: `process.py` (orchestrator), `md2json.py`, `json2md.py`, `json2mkdocs.py`, `render.py`, `format.py`, `bib2json.py`, `validate.py`, `utils.py`. |
| `database/build/` | Generated `index.json`, `tags.json`, `bib.json` consumed by the API and site build. |
| `database/schema/` | JSON schema terms are validated against. |
| `assets/bibliography/papers.bib` | BibTeX entries referenced by `<d-cite key="...">` tags. |
| `assets/img/pswiki/` | Images embedded in term definitions. |
| `docs/` | MkDocs source: `index.md`, `tags.md`, `javascripts/`, hand-authored pages. `docs/wiki/` is generated — do not hand-edit. |
| `mkdocs.yml` | MkDocs Material configuration. |
| `worker/` | Cloudflare Worker REST API (TypeScript, `wrangler`). |
| `mcp/` | MCP server exposing the wiki (Python). |
| `_pages/` | Legacy al-folio pages (about, rest-api, mcp, changelog) — pending port to MkDocs. |

## Core workflow: editing a term

1. Edit (or create) `_wiki/<term-id>.md`.
2. Run the pipeline to regenerate JSON + indexes:
   ```bash
   python pswiki.py process <term-id>
   ```
   (omit the ID to process all; `--dry-run` previews without writing.)
3. Commit **both** `_wiki/<term-id>.md` and `database/json/<term-id>.json`.

### Term markdown conventions

- Front matter: `title`, `description`, `tags`, `related`, `authors`, `date`, `lastmod` (see `_wiki/stability.md` or `_wiki/adequacy.md` as templates). `lastmod` is managed by the pipeline.
- Use `### Section Title` (H3) for sections; start each definition with a `>` blockquote.
- Cite sources with `<d-cite key="citation-key"></d-cite>`; the key must exist in `assets/bibliography/papers.bib`.

## Build & dev commands

```bash
# Scaffold a new term
python pswiki.py new <term-id>

# Data pipeline (run after editing a term)
python pswiki.py process <term-id>   # process one term
python pswiki.py process             # process all terms
python pswiki.py process --dry-run   # preview without writing

# Validation
python pswiki.py validate            # validate all term JSON files
python pswiki.py validate <term-id>  # validate specific term

# Site dev & build
python pswiki.py serve               # local preview at http://localhost:8000
python pswiki.py build               # production build (mkdocs --strict)

# Reference URL health check
python pswiki.py check-refs          # scan papers.bib for broken URLs; report → database/build/reference_check.json
python pswiki.py check-refs --recover  # also query Wayback Machine for broken NERC URLs

# Formatting (required by CI)
npx prettier --write .
```

- Python deps: `pip install -r requirements-dev.txt -r requirements-docs.txt`
- Pre-commit hooks: trailing-whitespace, end-of-file-fixer, check-yaml, large-file check.
- CI enforces **prettier**; run it before pushing. Deploy is via `.github/workflows/deploy.yml` (GitHub Pages, `gh-pages` branch).
- `docs/wiki/` is **generated** — never hand-edit files there. Edit `_wiki/<id>.md` → run pipeline → run generator.

## Development process — plan first, then code

For any non-trivial change, **write a plan before writing code**:

1. **Plan.** Create a markdown plan in `.claude/projects/<project-name>/plan.md` (copy `.claude/projects/_template/plan.md`). Capture goal, approach, affected files, steps, and risks. This is the tracking artifact — keep it updated as work progresses.
2. **Review.** Confirm the plan with the user before implementing anything with meaningful surface area.
3. **Code.** Implement against the plan, checking off steps as you go.
4. **Verify.** Run the relevant build/pipeline/format commands and note results in the plan.

Trivial fixes (a typo, a single term edit) don't need a project folder — use judgment.

## Project history & locked decisions

Key decisions already made — don't re-open these without a strong reason.

### Rendering stack migration (completed 2026-05-27, PR #36)

The site migrated from **al-folio/Jekyll** to **MkDocs Material**. Live at https://ps-wiki.github.io/.

Locked decisions:
- **Renderer:** MkDocs Material — lowest effort, Python-only, reuses the existing `json→md` pipeline.
- **Hosting:** GitHub Pages (unchanged).
- **§5-first rule:** Decouple citation and callout rendering into the Python pipeline *before* the SSG touches it — `<d-cite>` tags become Markdown footnotes (built from `bib.json`); kramdown `{: .block-* }` callouts become Material admonitions. Keeps the renderer dumb and swappable.
- **Keep:** MathJax, dark/light toggle, figure zoom/lightbox (glightbox).
- **Drop:** Giscus comments.
- **Don't build yet, don't foreclose:** versioned terms.
- `_pages/` directory is legacy al-folio content — pending port to MkDocs; don't delete yet.

The JSON database, schema, REST API (Cloudflare Worker), and MCP server are renderer-agnostic and unchanged.
Full plan and evaluation: `.claude/projects/rendering-stack-migration/`.

### Reference health (completed 2026-05-27, branch fix/broken-references)

Broken URL scanner added at `database/pyscripts/check_references.py`. Fixed 7 broken bib entries
(5 NERC → Wayback Machine archives; 1 IEEE → archive; 2 PJM floating → pinned to archive/ URLs).
2 entries annotated with `note` fields (no archive found). CI workflow pending.
See `.claude/projects/fix-broken-references/plan.md`.

## Conventions & guardrails

- Never hand-edit `database/json/*.json` or `database/build/*` — regenerate via `python pswiki.py process`.
- Citations require a matching `papers.bib` entry; add the entry before the `<d-cite>`.
- Run prettier before committing site/markdown changes (CI blocks otherwise).
- Term IDs are kebab-case and match the filename stem in both `_wiki/` and `database/json/`.
- Commit only when asked; branch off `main` for PRs.

### BibTeX URL conventions

ISO/RTO manuals are updated regularly. Use stable, version-pinned URLs:

- **PJM manuals:** Always use the `/archive/` URL with version number and date in the filename
  (e.g. `archive/m03/m03v69-transmission-operations-11-20-2025.pdf`), never the floating
  `manuals/m03.pdf`. The archive path is permanent; the floating path tracks the current version.
- **NYISO documents:** The document portal assigns a UUID per revision; include the UUID in the
  URL (e.g. `.../ancserv.pdf/df83ac75-...`). When NYISO publishes a new version the old UUID
  eventually expires — the CI reference scanner detects this. Fix: create a new bib entry with
  the updated UUID and update the wiki term's `<d-cite>` key.
- **NERC documents:** URLs are fragile due to ongoing site migrations. Prefer archiving to
  Wayback Machine when a NERC URL breaks; run `check_references.py --recover` to find snapshots.
- **General:** When a document is updated and the old citation still applies, keep the pinned
  URL. When the content you're referencing has changed in the new version, create a new bib entry
  (new key) and update the term.
