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

The PS-Wiki REST API provides read-only access to term data in JSON format.
It is deployed via [Cloudflare Workers](./worker) and documented using the OpenAPI 3.1.0 specification at <https://pswiki-api.jinninggm.workers.dev/openapi.json>

### Developer Notes

- All timestamps use ISO 8601 format (YYYY-MM-DD or full date-time).
- Pagination uses opaque cursors; pass `next_cursor` to retrieve the next page.
- The `/v1/terms` and `/v1/terms/{id}` endpoints are suitable for integration with external AI clients.

## Database

The folder `database` contains the source data and scripts for generating the wiki:

- Folder `database/json` contains the source JSON files for the wiki.
- Folder `database/pyscripts` contains Python scripts for processing the data.

### Python scripts

Python dependencies are described in `database/requirements.txt`

Check page [_pages/add-new.md](./_pages/add-new.md) for instructions on how to edit or add new terms.

## License

This project is licensed under the [CC-BY-NC 4.0](./LICENSE).
