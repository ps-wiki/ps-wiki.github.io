---
title: REST API
description: Read-only REST API for accessing PS-Wiki terminology data
---

The **PS-Wiki REST API** provides programmatic access to 173+ power systems terminology definitions via a simple HTTP interface. Hosted on Cloudflare Workers for global low-latency access.

## Base URL

```
https://pswiki-api.jinninggm.workers.dev
```

**OpenAPI Specification**: [/openapi.json](https://pswiki-api.jinninggm.workers.dev/openapi.json)

## Quick Start

### Search for Terms

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms?query=stability&limit=5"
```

**Response**:

```json
{
  "items": [
    {
      "id": "voltage-stability",
      "title": "Voltage Stability",
      "summary": "The ability of a power system to maintain...",
      "tags": ["stability", "power-quality"],
      "updated_at": "2025-11-19"
    }
  ],
  "next_cursor": null
}
```

### Get a Specific Term

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms/voltage-stability"
```

Returns the complete term data including definition, equations, citations, and metadata.

## API Endpoints

### GET /v1/terms

Search or list term summaries.

**Query Parameters**:

- `query` (string, optional) — Free-text search across ID, title, description, and tags
- `tag` (string, optional) — Filter by exact tag (case-insensitive)
- `limit` (integer, optional) — Max results per page (1–100, default: 20)
- `cursor` (string, optional) — Pagination cursor from previous response

**Examples**:

```bash
# List all terms (paginated)
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms?limit=10"

# Search by keyword
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms?query=frequency+control"

# Filter by tag
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms?tag=stability"

# Combine search and limit
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms?query=power+flow&limit=5"
```

### GET /v1/terms/{id}

Retrieve full details for a specific term.

**Path Parameters**:

- `id` (string, required) — Term identifier (e.g., `voltage-stability`)

**Example**:

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms/automatic-generation-control"
```

**Response**: Complete term JSON including full definition and description, mathematical equations (LaTeX), citations and references, related terms, tags and metadata, and version history.

### GET /v1/tags

List all available tags with usage counts.

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/tags"
```

**Response**:

```json
{
  "tags": [
    { "tag": "stability", "count": 15 },
    { "tag": "control", "count": 23 },
    { "tag": "protection", "count": 8 }
  ]
}
```

### GET /v1/changes

Get terms updated since a specific date.

**Query Parameters**:

- `since` (string, required) — ISO 8601 date or datetime (e.g., `2025-11-01`)

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/changes?since=2025-11-01"
```

**Response**:

```json
{
  "items": [
    { "id": "voltage-stability", "updated_at": "2025-11-19" },
    { "id": "frequency-control", "updated_at": "2025-11-15" }
  ]
}
```

## Integration Examples

=== "Python"

    ```python
    import requests

    # Search for terms
    response = requests.get(
        "https://pswiki-api.jinninggm.workers.dev/v1/terms",
        params={"query": "stability", "limit": 10}
    )
    terms = response.json()

    # Get specific term
    term = requests.get(
        "https://pswiki-api.jinninggm.workers.dev/v1/terms/voltage-stability"
    ).json()

    print(f"Title: {term['title']}")
    print(f"Description: {term['description']}")
    ```

=== "JavaScript"

    ```javascript
    // Search for terms
    const response = await fetch(
      "https://pswiki-api.jinninggm.workers.dev/v1/terms?query=stability&limit=10"
    );
    const data = await response.json();

    // Get specific term
    const term = await fetch(
      "https://pswiki-api.jinninggm.workers.dev/v1/terms/voltage-stability"
    ).then((r) => r.json());

    console.log(`Title: ${term.title}`);
    console.log(`Description: ${term.description}`);
    ```

=== "curl + jq"

    ```bash
    # Pretty-print search results
    curl -s "https://pswiki-api.jinninggm.workers.dev/v1/terms?query=stability" \
      | jq '.items[] | {id, title}'

    # Extract just the description
    curl -s "https://pswiki-api.jinninggm.workers.dev/v1/terms/voltage-stability" \
      | jq -r '.description'

    # List all tags
    curl -s "https://pswiki-api.jinninggm.workers.dev/v1/tags" \
      | jq '.tags[] | "\(.tag): \(.count)"'
    ```

## Use Cases

**Researchers** — Literature review, citation management, knowledge discovery across related terms.

**Developers** — Power chatbots and AI assistants, auto-generate glossaries, build education platforms.

**Web applications** — Add term search, hover tooltips, or autocomplete to your app.

## Response Format

All endpoints return JSON with standard HTTP status codes:

| Code  | Meaning            |
| ----- | ------------------ |
| `200` | Success            |
| `400` | Invalid parameters |
| `404` | Term not found     |
| `500` | Server error       |

**CORS**: All endpoints include `Access-Control-Allow-Origin: *` for browser access.

## Rate Limits

Currently no rate limits on the free Cloudflare Workers tier. Please use responsibly.

For high-volume usage (>100k requests/day), consider caching responses locally or using the MCP server for AI integrations.

## Data Source

The API serves data from the repository's JSON database:

- **Term data**: [`database/json/`](https://github.com/ps-wiki/pswiki/tree/main/database/json)
- **Index**: [`database/build/index.json`](https://github.com/ps-wiki/pswiki/blob/main/database/build/index.json)
- **Tags**: [`database/build/tags.json`](https://github.com/ps-wiki/pswiki/blob/main/database/build/tags.json)

Data is fetched directly from GitHub, so repository updates are reflected immediately without redeploying the API.

## Self-Hosting

```bash
git clone https://github.com/ps-wiki/pswiki.git
cd pswiki/worker
npm install
# configure wrangler.toml with your settings
npx wrangler deploy
```

See [`worker/README.md`](https://github.com/ps-wiki/pswiki/blob/main/worker/README.md) for full deployment instructions.

## License

API code and data are licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Free for academic and non-commercial use.
