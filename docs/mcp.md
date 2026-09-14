---
title: MCP Server
description: Local and remote AI-agent access to PS-Wiki terminology
---

# PS-Wiki MCP Server

PS-Wiki exposes the same read-only terminology through two MCP transports:

- **Local MCP:** a Python package launched over stdio.
- **Remote MCP:** a dedicated Cloudflare Worker endpoint at `https://mcp.ps-wiki.ning.guru/mcp`.

The REST API remains the canonical programmatic data interface. MCP is a thin,
agent-facing semantic adapter:

```text
LLM / AI agent
      ↓
PS-Wiki MCP
      ↓
PS-Wiki REST API
      ↓
PS-Wiki data
```

All tools are read-only. Responses include concise structured JSON and, where
available, canonical PS-Wiki URLs and attribution metadata.

## Local MCP (stdio)

Install from source:

```bash
git clone https://github.com/ps-wiki/ps-wiki.github.io.git
cd ps-wiki.github.io/mcp
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run the server directly:

```bash
pswiki-mcp
# equivalent:
python -m pswiki_mcp
```

For a live smoke test against the REST API:

```bash
python tests/test_server_manual.py
```

Example Claude Desktop configuration:

```json
{
  "mcpServers": {
    "pswiki": {
      "command": "/absolute/path/to/ps-wiki.github.io/mcp/.venv/bin/pswiki-mcp"
    }
  }
}
```

The same stdio configuration shape works for other local MCP clients that
launch a child process. The automated Python tests use mocked HTTP responses:

```bash
cd mcp
PYTHONPATH=src python -m pytest -q
```

## Remote MCP (Streamable HTTP)

No installation is required for a client that supports remote MCP:

```text
https://mcp.ps-wiki.ning.guru/mcp
```

The endpoint is stateless, public, and read-only. It supports MCP initialization,
tool discovery, and tool calls over the current Streamable HTTP handler, with
compatibility for ordinary stateless 2025-era clients. Clients should send
`Accept: application/json, text/event-stream` and `Content-Type: application/json`.

Generic client configuration:

```json
{
  "mcpServers": {
    "pswiki": {
      "url": "https://mcp.ps-wiki.ning.guru/mcp"
    }
  }
}
```

Claude Desktop versions that do not accept a remote URL directly can use the
standard local proxy:

```json
{
  "mcpServers": {
    "pswiki": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.ps-wiki.ning.guru/mcp"]
    }
  }
}
```

### ChatGPT and the OpenAI API

For a current ChatGPT workspace, an administrator or owner can create a custom
MCP app in Developer Mode, scan the tools, and publish the app to the
workspace. Full MCP app support is currently available on ChatGPT Business and
Enterprise/Edu web workspaces; availability and permissions can change as the
feature evolves. Use the [official ChatGPT MCP app
instructions](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt)
for the current UI flow.

For the OpenAI Responses API, the protocol-level shape is:

```python
response = client.responses.create(
    model="gpt-6-astra",
    input="Explain voltage stability using PS-Wiki.",
    tools=[{
        "type": "mcp",
        "server_label": "pswiki",
        "server_description": "Read-only power-systems terminology from PS-Wiki.",
        "server_url": "https://mcp.ps-wiki.ning.guru/mcp",
        "allowed_tools": [
            "search_terms",
            "get_term",
            "get_related_terms",
            "list_tags",
            "get_terms_by_tag",
        ],
        "require_approval": "never",
    }],
)
```

The current OpenAI API uses an array of tool names for `allowed_tools`. Replace
the example model with one currently available to your account. `never` is
appropriate here because all five PS-Wiki tools are read-only; use approvals
if write-capable tools are added later.

### Claude

Claude users can add the public endpoint as a custom connector:

1. On an individual Pro or Max plan, open **Customize → Connectors**, choose
   **Add custom connector**, and enter `https://mcp.ps-wiki.ning.guru/mcp`.
2. On Team or Enterprise, an Owner adds it under **Organization settings →
   Connectors → Add → Custom → Web**; members then connect it from
   **Customize → Connectors**.
3. Enable the connector for the conversation from the **+** menu.

See [Claude's current remote MCP connector
instructions](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
Claude connects to remote connectors from Anthropic's infrastructure, so the
server must remain publicly reachable.

### Directory listings

Direct custom connections do not require a directory listing. A public listing
is a separate, optional distribution step:

- [OpenAI plugin submission](https://developers.openai.com/plugins/deploy/submission)
  accepts a universal public MCP URL, but requires publisher identity
  verification, domain verification, and public website, support, privacy, and
  terms URLs.
- Anthropic's [Connectors Directory](https://support.anthropic.com/en/articles/11596036-anthropic-mcp-directory-faq)
  is curated and requires a review submission; inclusion is not guaranteed.

PS-Wiki is prepared for these paths, but directory submission still requires
the project owner's account, identity verification, and any reviewer-domain
challenge.

## Tools

### `search_terms`

Search by keyword, phrase, or concept. Use this to discover candidate terms;
results are bounded summaries with IDs, tags, update times, and canonical URLs.

Arguments: `query` (required string), `limit` (optional integer, 1–50,
default 10).

### `get_term`

Retrieve the complete definition for a known term ID, including description,
equations, citations, related terms, canonical URL, and attribution.

Argument: `term_id` (required kebab-case string, for example
`voltage-stability`).

### `get_related_terms`

Explore direct relationships for a known term. Use `depth: 1` for direct
relationships or `depth: 2` for a bounded second-level exploration.

Arguments: `term_id` (required string), `depth` (optional integer, 1–2,
default 1).

### `list_tags`

List the PS-Wiki taxonomy and usage counts. Use this to browse categories.

### `get_terms_by_tag`

List terms in a specific category/tag. Use this for taxonomy-based browsing
rather than free-text concept search.

Argument: `tag` (required string, case-insensitive).

## Local development and verification

Run the remote Worker locally:

```bash
cd worker
npm ci
npm run mcp:dev
# endpoint: http://localhost:8788/mcp
```

Run deterministic checks:

```bash
npm run check
npx wrangler deploy --config wrangler-mcp.toml --dry-run
```

For interactive verification, start the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
npx @modelcontextprotocol/inspector@latest
```

Connect it to `http://localhost:8788/mcp`, select **List Tools**, and invoke
`search_terms` with `{"query":"stability","limit":3}`.

## Deployment and rollback

From the Worker directory:

```bash
cd worker
npm ci
npm run check
npm run deploy:mcp
```

The MCP Worker deployment uses the Cloudflare account configured in
Wrangler or the repository’s `CLOUDFLARE_API_TOKEN` and
`CLOUDFLARE_ACCOUNT_ID` Actions secrets. No new secret, OAuth provider,
or Durable Object is required.

After deployment, verify the endpoint with MCP Inspector or by sending the
following JSON-RPC requests:

```bash
MCP_URL=https://mcp.ps-wiki.ning.guru/mcp
curl -sS "$MCP_URL" \
  -X POST \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}}}'

curl -sS "$MCP_URL" \
  -X POST \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

curl -sS "$MCP_URL" \
  -X POST \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_terms","arguments":{"query":"stability","limit":3}}}'
```

### Operational telemetry

The remote Worker has Cloudflare Workers Logs enabled for short-term diagnosis.
Each top-level tool call emits one structured event with the tool name,
upstream REST status information, a bounded error class, and elapsed time in
milliseconds. Tool arguments, prompts, query text, response bodies, IP
addresses, and session identifiers are not logged. A tool that makes multiple
REST requests records the bounded list of observed upstream statuses.

The R2 traffic log stores one JSON object per request with the worker, method,
origin/path, status, duration, request ID, and selected Cloudflare location
metadata. Query strings are intentionally omitted so REST search text is not
written to durable traffic logs. See the [privacy policy](privacy.md) and
[service terms](terms.md) for the current data-handling and usage details.

Workers Logs are diagnostic rather than durable usage analytics; retention is
limited by the Cloudflare plan. The separate monitoring repository stores
aggregated request data for longer-term reporting.

For a failed deployment, inspect `npx wrangler versions list` and use
`npx wrangler rollback <VERSION_ID>` from `worker/` after confirming the
target version. The existing REST routes should be probed after rollback.

The MCP Worker config declares the dedicated `pswiki-mcp` Worker at the
`mcp.ps-wiki.ning.guru` custom hostname. If Cloudflare asks for dashboard
confirmation on the first deployment, approve only that hostname. The REST
Worker uses `api.ps-wiki.ning.guru`. A rate-limit rule scoped to `/mcp` can be
added later if traffic warrants it. Do not change nameservers or unrelated DNS
records.

## Resources and attribution

The local stdio server also retains its existing read-only resources:
`tags://all`, `index://terms`, and `term:///<term-id>`.

PS-Wiki content is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
The remote MCP layer delegates data retrieval to the [PS-Wiki REST API](rest-api.md).
For data handling and support, see the [privacy policy](privacy.md) and
[service terms](terms.md).
