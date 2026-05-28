# /new-term — Add a new wiki term

Guide the user through creating a well-formed power systems wiki term from scratch.
Follow the steps below in order. Do not skip steps or batch them without confirmation.

---

## Philosophy

- **Quote, don't paraphrase.** Every definition block must be a direct quote from an
  authoritative source. Never synthesize or reword — the wiki's value is in the
  original language from standards, papers, and reports.
- **Cross-literature coverage.** Prefer two or more independent sources for the same
  term. Different definitions from different bodies (IEEE, NERC, CIGRE, EU regulations,
  textbooks) reveal convergence, nuance, and domain-specific usage. Each source gets
  its own section.
- **Cite precisely.** Every blockquote must be followed immediately by a `<d-cite>`
  tag. No uncited definitions.

---

## Step 1 — Clarify scope

Ask the user:
1. What is the term ID? (kebab-case, e.g., `frequency-response`)
2. What sources will be cited? (known paper keys, standards, reports — or "unknown, help me find them")
3. Any related terms already in the wiki?

---

## Step 2 — Check and add bib entries

Search `assets/bibliography/papers.bib` for existing relevant entries:

```bash
grep -i "<keyword>" assets/bibliography/papers.bib
```

Only add new entries for sources not already present. If the user's sources are
already in the bib, skip to Step 3.

### BibTeX entry format

```bibtex
@<type>{<key>,
  abbr     = {<Article|Industry|Report|Book|News>},
  author   = {<Author(s)>},
  title    = {<Full title>},
  year     = {<YYYY>},
  url      = {<URL>},
  urldate  = {<YYYY-MM-DD>},
}
```

**Entry type guidance:**
- `@article` — peer-reviewed journal or conference paper
- `@techreport` — technical report (add `institution = {}`)
- `@online` — standard, glossary, industry document, webpage
- `@book` — textbook (add `publisher = {}`, `address = {}`)

**Key naming convention:** `<firstauthor><year><oneword>` — e.g., `kundur2004stability`,
`nerc2024glossary`, `eu2017guideline`.

**URL rules:** Follow BibTeX URL conventions in `AGENTS.md` (NERC → Wayback Machine
archives; PJM → `/archive/` pinned URLs; NYISO → UUID-pinned URLs).

---

## Step 3 — Scaffold the term

```bash
python pswiki.py new <term-id>
```

This creates `_wiki/<term-id>.md` with a blank template. Open it for editing.

---

## Step 4 — Write the term

Edit `_wiki/<term-id>.md`. Structure:

### Frontmatter

```yaml
---
title: <Title Case>
description: <One sentence — the most concise definition available, or a plain-language summary.>
tags:
  - <tag1>
  - <tag2>
related:
  - <existing-term-id>
authors:
  - name: <Contributor Name>
    url: <profile URL>
date: <YYYY-MM-DD>
lastmod: <YYYY-MM-DD>
---
```

**Tag guidance:** use lowercase kebab-case. Common tags: `nerc`, `ieee`, `cigre`,
`ferc`, `nyiso`, `pjm`, `eu`, `article`, `book`, `report`, `standard`, plus
domain tags like `stability`, `reliability`, `frequency`, `voltage`.

### Body — one section per source

Use `### Section Title` (H3). The title should describe the source type and origin.
Naming patterns:

- `### Definition by NERC` / `### Definition by IEEE` / `### Definition by FERC`
- `### Definition in an Article by <Author(s) or Task Force Name>`
- `### Definition in a [European Union Regulation / NERC Standard / FERC Order]`
- `### Definition in a Textbook` / `### Definition in a Technical Report`
- `### Elaboration in an Article by ...` — for explanatory passages that are not
  strict definitions but add important context

Each section follows this pattern exactly:

```markdown
### Definition by <Source>

Source: <d-cite key="<bibkey>"></d-cite>

> "Direct quote from the source defining the term."
```

For a page-specific citation, append the page after the tag:

```markdown
Source: <d-cite key="slotine1990appliednonlinear"></d-cite> p48
```

**Cross-literature example — preferred structure for a well-covered term:**

```markdown
### Definition by NERC

Source: <d-cite key="nerc2024glossary"></d-cite>

> The ability of ...

### Definition in an Article by a Joint Task Force of IEEE and CIGRE

Source: <d-cite key="kundur2004stability"></d-cite>

> Stability of a power system refers to ...

### Definition in a European Union Regulation

Source: <d-cite key="eu2017guideline"></d-cite> p8

> 'term' means ...
```

---

## Step 5 — Process and validate

```bash
python pswiki.py process <term-id>
python pswiki.py validate <term-id>
```

Fix any validation errors before proceeding. Common issues: missing required frontmatter
fields, `<d-cite>` keys not present in `papers.bib`.

---

## Step 6 — Format

```bash
npx prettier --write .
```

CI will block the PR if prettier finds formatting issues.

---

## Step 7 — Confirm and summarize

Report to the user:
- Term ID and title
- Bib entries added (if any), with their keys
- Files changed: `_wiki/<term-id>.md`, `database/json/<term-id>.json`,
  and `assets/bibliography/papers.bib` if bib was updated
- Any validation warnings

Do not commit. The user commits when ready.
