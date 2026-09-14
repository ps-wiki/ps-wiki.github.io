# PS-Wiki MCP Server

This package provides the local stdio MCP server for PS-Wiki. The production
remote endpoint is hosted by the dedicated Cloudflare MCP Worker:

```text
https://mcp.ps-wiki.ning.guru/mcp
```

For the complete local/remote client guide, tool reference, deployment commands,
Inspector workflow, and verification requests, see the canonical site
documentation: [docs/mcp.md](https://ps-wiki.ning.guru/mcp/).

## Local quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pswiki-mcp
```

Claude Desktop example:

```json
{
  "mcpServers": {
    "pswiki": {
      "command": "/absolute/path/to/mcp/.venv/bin/pswiki-mcp"
    }
  }
}
```

The local server exposes five read-only tools: `search_terms`, `get_term`,
`get_related_terms`, `list_tags`, and `get_terms_by_tag`.

Run deterministic package tests with:

```bash
PYTHONPATH=src python -m pytest -q
```
