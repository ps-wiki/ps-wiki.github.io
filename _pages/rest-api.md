---
layout: page
title: rest api
permalink: /rest-api/
description: Read-only REST API for accessing PS-Wiki terminology data
nav: false
horizontal: false
---

The **PS-Wiki REST API** provides programmatic access to 173+ power systems terminology definitions via a simple HTTP interface. Hosted on Cloudflare Workers for global low-latency access.

# Base URL

```
https://pswiki-api.jinninggm.workers.dev
```

**OpenAPI Specification**: [/openapi.json](https://pswiki-api.jinninggm.workers.dev/openapi.json)

# Quick Start

## Search for Terms

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

## Get a Specific Term

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms/voltage-stability"
```

Returns the complete term data including definition, equations, citations, and metadata.

# API Endpoints

## GET /v1/terms

Search or list term summaries.

**Query Parameters**:

- `query` (string, optional) - Free-text search across ID, title, description, and tags
- `tag` (string, optional) - Filter by exact tag (case-insensitive)
- `limit` (integer, optional) - Max results per page (1-100, default: 20)
- `cursor` (string, optional) - Pagination cursor from previous response

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

## GET /v1/terms/{id}

Retrieve full details for a specific term.

**Path Parameters**:

- `id` (string, required) - Term identifier (e.g., `voltage-stability`)

**Example**:

```bash
curl "https://pswiki-api.jinninggm.workers.dev/v1/terms/automatic-generation-control"
```

**Response**: Complete term JSON including:

- Full definition and description
- Mathematical equations (LaTeX)
- Citations and references
- Related terms
- Tags and metadata
- Version history

## GET /v1/tags

List all available tags with usage counts.

**Example**:

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

## GET /v1/changes

Get terms updated since a specific date.

**Query Parameters**:

- `since` (string, required) - ISO 8601 date or datetime (e.g., `2025-11-01` or `2025-11-01T00:00:00Z`)

**Example**:

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

# Integration Examples

## Python

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

## JavaScript

```javascript
// Search for terms
const response = await fetch("https://pswiki-api.jinninggm.workers.dev/v1/terms?query=stability&limit=10");
const data = await response.json();

// Get specific term
const term = await fetch("https://pswiki-api.jinninggm.workers.dev/v1/terms/voltage-stability").then((r) => r.json());

console.log(`Title: ${term.title}`);
console.log(`Description: ${term.description}`);
```

## curl with jq

```bash
# Pretty-print search results
curl -s "https://pswiki-api.jinninggm.workers.dev/v1/terms?query=stability" | jq '.items[] | {id, title}'

# Extract just the description
curl -s "https://pswiki-api.jinninggm.workers.dev/v1/terms/voltage-stability" | jq -r '.description'

# List all tags
curl -s "https://pswiki-api.jinninggm.workers.dev/v1/tags" | jq '.tags[] | "\(.tag): \(.count)"'
```

# Use Cases

## For Researchers

- **Literature Review**: Search for relevant power systems concepts
- **Citation Management**: Get standardized definitions with references
- **Knowledge Discovery**: Explore related terms and build concept maps

## For Developers

- **AI Integration**: Power chatbots and AI assistants with accurate data
- **Documentation**: Auto-generate glossaries for technical documents
- **Education Platforms**: Build interactive learning tools

## For Web Applications

- **Search Functionality**: Add power systems term search to your app
- **Tooltips**: Display definitions on hover
- **Autocomplete**: Suggest terms as users type

# Response Format

All endpoints return JSON with appropriate HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Term not found
- `500 Internal Server Error` - Server error

**CORS**: All endpoints include `Access-Control-Allow-Origin: *` for browser access.

**Content-Type**: `application/json; charset=utf-8`

# Rate Limits

Currently **no rate limits** on the free Cloudflare Workers tier. Please use responsibly.

For high-volume usage (>100k requests/day), consider:

- Caching responses locally
- Using the [MCP server](/mcp/) for AI integrations
- Hosting your own instance (see [GitHub](https://github.com/ps-wiki/ps-wiki.github.io/tree/main/worker))

# Data Source

The API serves data from:

- **Term Data**: [`database/json/`](https://github.com/ps-wiki/ps-wiki.github.io/tree/main/database/json)
- **Index**: [`database/build/index.json`](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/database/build/index.json)
- **Tags**: [`database/build/tags.json`](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/database/build/tags.json)

Data is fetched directly from GitHub, so updates to the repository are reflected immediately without redeploying the API.

# Schema

All term data conforms to the JSON schema:  
[`database/schema/v1/term.schema.json`](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/database/schema/v1/term.schema.json)

# Self-Hosting

To deploy your own instance:

```bash
# Clone repository
git clone https://github.com/ps-wiki/ps-wiki.github.io.git
cd ps-wiki.github.io/worker

# Install dependencies
npm install

# Configure wrangler.toml with your settings

# Deploy to Cloudflare
npx wrangler deploy
```

See [`worker/README.md`](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/worker/README.md) for detailed deployment instructions.

# Support

- 📖 **OpenAPI Spec**: [/openapi.json](https://pswiki-api.jinninggm.workers.dev/openapi.json)
- 🐛 **Issues**: [GitHub Issues](https://github.com/ps-wiki/ps-wiki.github.io/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/ps-wiki/ps-wiki.github.io/discussions)
- 🔧 **Source Code**: [worker/](https://github.com/ps-wiki/ps-wiki.github.io/tree/main/worker)

# License

API code and data are licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).  
Free for academic and non-commercial use.
