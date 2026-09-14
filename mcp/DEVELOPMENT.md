# MCP development

The Python package is the local stdio compatibility layer. The public remote
MCP endpoint is implemented by the dedicated `pswiki-mcp` Worker in `worker/`
and calls the existing `api.ps-wiki.ning.guru` REST API; it is not deployed from this
directory.

## Setup and tests

```bash
cd mcp
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
PYTHONPATH=src python -m pytest -q
ruff check src tests
python -m py_compile src/pswiki_mcp/*.py
```

The API-client tests use `httpx.MockTransport` and do not contact production.
The explicit live stdio smoke test is:

```bash
python tests/test_server_manual.py
```

## Remote Worker development

```bash
cd worker
npm ci
npm run mcp:dev
```

The local remote endpoint is `http://localhost:8788/mcp`. Run `npm run check`
for type checking and protocol tests. Use MCP Inspector for interactive calls.

## Remote deployment

From `worker/`, after review:

```bash
npm run check
npx wrangler deploy --config wrangler-mcp.toml --dry-run
npm run deploy:mcp
```

The Worker’s MCP configuration is in `worker/wrangler-mcp.toml`. It contains no
secrets. `MCP_API_BASE`, `MCP_ALLOWED_HOSTS`, `MCP_ALLOWED_ORIGINS`,
`MCP_TIMEOUT_MS`, and `MCP_MAX_RESPONSE_BYTES` are configurable variables.

See [the site MCP documentation](https://ps-wiki.ning.guru/mcp/) for client
configuration, curl verification, rollback, and Cloudflare follow-up.
