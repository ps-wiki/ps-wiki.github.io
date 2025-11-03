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

Built upon the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme, this website introduces significant enhancements, particularly in its new wiki section.

A custom [wiki layout](./_layouts/wiki.liquid) adapted from the `distill` layout, has been developed to effectively host item-based terminologies. Key features include:

- **Metadata Display**: Last update date, tags, and related term links
- **Navigation**: Previous/Next term links for easy Browse
- **Direct Editing**: A link to edit the term directly on GitHub
- **Community Engagement**: Integrated Giscus comments

## REST API

The [PS-Wiki REST API](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/database/openapi/pswiki.v1.yaml) provides read-only access to term data in JSON format.
It is deployed via [Cloudflare Workers](./worker) and documented using the OpenAPI 3.1.0 specification at <https://pswiki-api.jinninggm.workers.dev/openapi.json>

Base URL: <https://pswiki-api.jinninggm.workers.dev>

No authentication is required — all endpoints are public and read-only.

### Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/terms` | Search or list PS-Wiki terms |
| GET | `/v1/terms/{id}` | Retrieve a specific term by ID |
| GET | `/v1/tags` | List all tags and their term counts |
| GET | `/v1/changes` | List terms updated since a given timestamp |

### Example Usage

1. List or search terms
```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms?query=stability&limit=5"
```

2. Retrieve a term by ID
```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms/stability"
```

3. List all tags
```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/tags"
```

4. List terms updated since a date
```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/changes?since=2025-07-01"
```

### Developer Notes

- All timestamps use ISO 8601 format (YYYY-MM-DD or full date-time).
- Pagination uses opaque cursors; pass `next_cursor` to retrieve the next page.
- The `/v1/terms` and `/v1/terms/{id}` endpoints are suitable for integration with external AI clients.

## Database

The folder `database` contains the source data and scripts for generating the wiki:

- Folder `database/json` contains the source JSON files for the wiki.
- Folder `database/pyscripts` contains Python scripts for processing the data.

Common commands for using the scripts are as follows:

Convert all JSON files to Markdown files in the `_wiki` folder:

```bash
python database/pyscripts/json2md_all.py --in-dir database/json --out-dir _wiki --pattern "*.json"
```

Convert a single JSON file to a Markdown file:

```bash
python database/pyscripts/json2md.py --input database/json/stability.json --output _wiki/stability.md
```

### Python scripts dependencies

Python dependencies are described in `database/requirements.txt`

## License

This project is licensed under the [CC-BY-NC 4.0](./LICENSE).
