# PS-Wiki Cloudflare Worker

The root `pswiki-api` Worker serves the existing read-only REST API. A separate
lightweight `pswiki-mcp` Worker serves remote MCP and calls that REST API at
`MCP_API_BASE`; it does not duplicate the PS-Wiki database.

| Surface | Production URL |
| --- | --- |
| REST API | `https://api.ps-wiki.ning.guru` |
| OpenAPI | `https://api.ps-wiki.ning.guru/openapi.json` |
| Remote MCP | `https://mcp.ps-wiki.ning.guru/mcp` |

## Development

```bash
npm ci
npm run mcp:dev
```

The REST Worker listens on `http://localhost:8787`; the MCP Worker listens on
`http://localhost:8788`. Use `http://localhost:8788/mcp` with MCP Inspector.

Checks:

```bash
npm run check
npx wrangler deploy --config wrangler.toml --dry-run
npx wrangler deploy --config wrangler-mcp.toml --dry-run
```

The root Worker tests are intentionally scoped to `tests/`; the nested
`worker/pswiki-api/` directory is an unrelated starter template and is not the
deployed API.

## Configuration

Existing REST variables remain unchanged:

- `ORIGIN_BASE` — raw term JSON base URL.
- `INDEX_URL` — generated term index URL.
- `TAGS_URL` — generated tag index URL.
- `SITE_BASE` — human-facing canonical site URL.

MCP variables are:

- `MCP_API_BASE` — REST base used by MCP tools; production uses
  `https://api.ps-wiki.ning.guru`.
- `MCP_ALLOWED_HOSTS` — comma-separated MCP Host allowlist.
- `MCP_ALLOWED_ORIGINS` — comma-separated browser Origin allowlist.
- `MCP_TIMEOUT_MS` — upstream REST timeout, bounded by the Worker code.
- `MCP_MAX_RESPONSE_BYTES` — maximum upstream JSON response size.

The initial deployment is public and read-only. It uses no OAuth, accounts, or
Durable Objects. Cloudflare’s MCP handler validates Host and present Origin
headers; non-browser clients without Origin remain supported.

## Deployment and rollback

```bash
npm run check
npx wrangler deploy
npm run deploy:mcp
```

Two GitHub Actions workflows deploy these Workers independently on approved
changes to `main`, using `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`.
The MCP config declares `mcp.ps-wiki.ning.guru` as its single Cloudflare custom
domain; the REST config declares `api.ps-wiki.ning.guru` for `pswiki-api`.
If the account requires dashboard confirmation for the first custom-domain
attachment, approve only that hostname.

Inspect or roll back versions with:

```bash
npx wrangler versions list
npx wrangler rollback <VERSION_ID>
```

After deployment, run the MCP Inspector against
`https://mcp.ps-wiki.ning.guru/mcp`, or follow the initialize/tools-list/tools-call curl
examples in [docs/mcp.md](https://ps-wiki.ning.guru/mcp/).
