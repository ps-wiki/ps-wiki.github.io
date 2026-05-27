# Power Systems Wiki

This wiki is an open reference designed to compile and share terminologies used in the power systems engineering.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/LICENSE)
[![Deploy site](https://github.com/ps-wiki/ps-wiki.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/ps-wiki/ps-wiki.github.io/actions/workflows/deploy.yml)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![GitHub last commit (main)](https://img.shields.io/github/last-commit/ps-wiki/ps-wiki.github.io/main?label=last%20commit%20to%20master)](https://github.com/ps-wiki/ps-wiki.github.io/commits/main/)

## Why This Wiki Exists

Language is inherently ambiguous, and power system terminologies are no exception. Inspired by an email titled “Definitions of Smart Grids a Decade Ago – What Has Changed?” on Power-Globe in 2024, I decided to compile terminologies from papers, standards, reports, and other traceable sources to build this wiki.

## Contributing

We welcome contributions from the community! If you have suggestions, corrections, or new terms to add, please open an issue or submit a pull request.

## Website Overview

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), the site is driven by a JSON term database and generated at deploy time. Key features include:

- **Metadata Display**: Last update date, tags, and related term links
- **Navigation**: Previous/Next term links for easy browsing
- **Direct Editing**: A link to edit the term directly on GitHub
- **Community Engagement**: Integrated Giscus comments

## REST API

The PS-Wiki REST API provides read-only access to term data in JSON format.
It is deployed via [Cloudflare Workers](./worker) and documented using the OpenAPI 3.1.0 specification at <https://pswiki-api.jinninggm.workers.dev/openapi.json>

### Developer Notes

- All timestamps use ISO 8601 format (YYYY-MM-DD or full date-time).
- Pagination uses opaque cursors; pass `next_cursor` to retrieve the next page.
- The `/v1/terms` and `/v1/terms/{id}` endpoints are suitable for integration with external AI clients.

## Development

All developer workflows go through the `pswiki.py` CLI at the repo root:

```bash
python pswiki.py new <term-id>        # scaffold a new term
python pswiki.py process <term-id>    # run the full pipeline for one term
python pswiki.py process              # process all terms
python pswiki.py validate             # validate all term JSON files
python pswiki.py serve                # local preview at http://localhost:8000
python pswiki.py build                # production build
```

Install Python dependencies before first use:

```bash
pip install -r database/requirements.txt -r requirements-docs.txt
```

Terms are authored in `_wiki/<term-id>.md` and stored as JSON in `database/json/`. Never hand-edit the JSON files directly — run `python pswiki.py process` to regenerate them.

## License

This project is licensed under the [CC-BY-NC 4.0](./LICENSE).
