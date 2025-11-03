---
layout: about
title: about
permalink: /
subtitle: An open wiki for power systems engineers, researchers, and students.
---

<div class="button-row-container text-center mb-5">
  <div class="row justify-content-center">
    <div class="col-auto mb-3">
      <a href="/wiki/" class="btn btn-lg wiki-button" style="background-color: #007BFF; border-color: #007BFF; color: #FFFFFF;">
        <i class="fas fa-search-plus"></i> Explore Now
      </a>
    </div>
    <div class="col-auto mb-3">
      <a href="/wiki-tag/" class="btn btn-lg wiki-tags-button" style="background-color: #28A745; border-color: #28A745; color: #FFFFFF;">
        <i class="fas fa-filter"></i> Archive by Tags
      </a>
    </div>
  </div>
</div>

## Introduction

This open-access wiki is designed to help power system professionals, researchers, and students quickly find clear, concise definitions of key terms and acronyms in the industry.
Whenever a concept has multiple interpretations—whether in academic papers, technical standards, or industry reports—our goal is to present relevant definitions side by side, with citations to the original sources.

## How to Use

### Basic Usage

1. **Browse or search**: Navigate via the wiki or use the search bar to locate terms instantly.
1. **Compare definitions**: Some entries include excerpts from multiple sources—standards, peer-reviewed papers, and industry guidelines—so you can see how usage varies.
1. **Stay current**: Terminology evolves as the field advances. We update entries regularly; check back for the latest additions and revisions.
1. **Contribute**: Spot an error, omission, or new term? Please open an issue or submit a pull request on our GitHub repository.

### REST API

The [PS-Wiki REST API](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/database/openapi/pswiki.v1.yaml) provides read-only access to term data in JSON format.
It is deployed via [Cloudflare Workers](https://github.com/ps-wiki/ps-wiki.github.io/tree/main/worker) and documented using the [OpenAPI 3.1.0](https://pswiki-api.jinninggm.workers.dev/openapi.json).
Base URL: <https://pswiki-api.jinninggm.workers.dev>

No authentication is required — all endpoints are public and read-only.

#### Endpoints Overview

| Method | Endpoint         | Description                                |
| ------ | ---------------- | ------------------------------------------ |
| GET    | `/v1/terms`      | Search or list PS-Wiki terms               |
| GET    | `/v1/terms/{id}` | Retrieve a specific term by ID             |
| GET    | `/v1/tags`       | List all tags and their term counts        |
| GET    | `/v1/changes`    | List terms updated since a given timestamp |

<br>

#### Example Usage

List terms

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms?limit=5"
```

Search terms by keyword "stability"

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms?query=stability&limit=5"
```

Get a term by ID

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms/stability"
```

List all tags

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/tags"
```

Filter terms by tag "stability"

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms?tag=stability"
```

List terms updated since a date

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/changes?since=2025-07-01"
```

## Why This Wiki Exists

Language is inherently ambiguous, and power system terminologies are no exception. Inspired by an email titled “Definitions of Smart Grids a Decade Ago – What Has Changed?” on Power-Globe in 2024, I decided to compile terminologies from papers, standards, reports, and other traceable sources to build this wiki.

## Disclaimer

- **Not a primary source:** We quote and cite definitions from existing standards, papers, and reports.
- **Not exhaustive:** Some important terminologies may be missing.
- **Not rigorous:** The terminologies are not rigorously proven mathematical theories.
- **Subject to change:** As power systems evolve, definitions may be updated.
