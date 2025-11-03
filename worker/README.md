# PS-Wiki API (Cloudflare Worker)

This directory contains the **Cloudflare Worker** that exposes the PS-Wiki database
as a read-only REST API, suitable for integration with **ChatGPT Actions**, other AI
agents, or web clients.


## 🌐 Overview

| Component | Description |
|------------|--------------|
| **Platform** | Cloudflare Workers (TypeScript) |
| **Purpose**  | Serve Power Systems Wiki term data as JSON |
| **Data Source** | JSON terms stored in the [`database/json/`](../database/json) directory of this repo |
| **Index Source** | [`database/build/index.json`](../database/build/index.json) & [`database/build/tags.json`](../database/build/tags.json) |
| **Schema** | [`database/schema/v1/term.schema.json`](../database/schema/v1/term.schema.json) |
| **Public Endpoint** | `https://pswiki-api.<your-account>.workers.dev` (free Cloudflare domain) |


## 🗂 Directory Structure

```
worker/
├── src/
│   └── index.ts           # Main Worker script (REST API)
├── wrangler.toml          # Worker configuration (entry point, env vars)
├── package.json           # Node project metadata
├── tsconfig.json          # TypeScript compiler settings
└── README.md              # This file
```


## ⚙️ Environment Variables (set in `wrangler.toml`)

| Name | Description |
|------|--------------|
| `ORIGIN_BASE` | Base URL of raw JSON term files in GitHub, e.g.<br>`https://raw.githubusercontent.com/ps-wiki/ps-wiki.github.io/main/database/json` |
| `INDEX_URL` | URL of `index.json` built by `build_index.py` |
| `TAGS_URL` | URL of `tags.json` built by `build_index.py` |

These variables allow the Worker to always fetch the latest data directly
from GitHub without redeploying the Worker.


## 🚀 Deployment

### One-time setup
```bash
npm install --save-dev wrangler typescript
npx wrangler login
```

### Local development
```bash
cd worker
npx wrangler dev
```

Local development server URL: <http://localhost:8787>

Example test:
```bash
curl 'http://localhost:8787/v1/terms?query=stability'
```

### Deploy to Cloudflare

Manually deploy:
```bash
npx wrangler deploy
```

Cloudflare assigns a free public URL:

```
https://pswiki-api.<your-account>.workers.dev
```


## 🔍 API Endpoints

| Endpoint | Description |
|-----------|--------------|
| `GET /v1/terms?query=&tag=&limit=&cursor=` | Search or list term summaries |
| `GET /v1/terms/{id}` | Retrieve a single term (full JSON) |
| `GET /v1/tags` | List all tags and counts |
| `GET /v1/changes?since=YYYY-MM-DD` | List terms modified since a given date |
| `GET /openapi.json` | Return OpenAPI spec for ChatGPT Actions |

All endpoints return `application/json` and include permissive CORS headers.

## 🧪 Quick Local Testing Commands

```bash
# check OpenAPI spec
curl "http://localhost:8787/openapi.json"

# List terms
curl "http://localhost:8787/v1/terms?limit=5"

# Search by keyword
curl "http://localhost:8787/v1/terms?query=stability&limit=5"

# filter by tag
curl "http://localhost:8787/v1/terms?tag=stability"

# get single term by ID
curl "http://localhost:8787/v1/terms/ambient-adjusted-ratings"

# Changes since October 2025
curl "http://localhost:8787/v1/changes?since=2025-10-01"
```


## 🧰 Troubleshooting

| Symptom | Likely Cause / Fix |
|----------|--------------------|
| `Missing entry-point` | Run `wrangler dev` *inside* the `worker` folder or add `--config worker/wrangler.toml` |
| `404 on /v1/terms/{id}` | Check `ORIGIN_BASE` path and ensure the file `<id>.json` exists in `database/json` |
| Empty results | Ensure `database/build/index.json` is committed and `INDEX_URL` matches its GitHub raw URL |
| CORS error | The Worker includes `Access-Control-Allow-Origin: *`; if you modified headers, re-add it |
| OpenAPI invalid | Hit `/openapi.json` in browser; it must return valid JSON for ChatGPT Actions |


## 🧾 License

The PS-Wiki API code follows the same license as the repository:  
**CC BY-NC 4.0** for content, and MIT-style for supporting scripts unless otherwise noted.


## 🧩 Future Enhancements

- `/v1/tags/{tag}` endpoint for direct tag lookup  
- `/v1/references` to expose citation metadata  
- Cache invalidation hooks (GitHub webhook trigger)


_Last updated: 2025-11-03_
