---
title: MCP Server
description: AI-native access to PS-Wiki terminology via Model Context Protocol
---

The **PS-Wiki MCP Server** provides AI assistants with direct access to power systems terminology through the [Model Context Protocol](https://modelcontextprotocol.io). This enables natural language queries with accurate, cited responses.

## Features

- Search 180+ power systems terms by keyword or concept
- Retrieve detailed definitions with equations and citations
- Explore related concepts and build knowledge graphs
- Browse by tags (stability, control, protection, market, etc.)
- Works with Claude Desktop, Ollama, and other MCP clients

## Quick Start

### Installation

```bash
# Install from source
git clone https://github.com/ps-wiki/pswiki.git
cd pswiki/mcp
pip install -e .
```

### Configuration

=== "Claude Desktop"

    Add to `claude_desktop_config.json`:

    **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
    **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

    ```json
    {
      "mcpServers": {
        "pswiki": {
          "command": "python",
          "args": ["-m", "pswiki_mcp"]
        }
      }
    }
    ```

    Restart Claude Desktop, then ask:

    - _"Search for power systems stability terms"_
    - _"Explain voltage stability in detail"_
    - _"What are related concepts to automatic generation control?"_

=== "Ollama (Continue.dev)"

    1. Install the [Continue](https://continue.dev) extension for VS Code.
    2. Configure `~/.continue/config.json`:

    ```json
    {
      "models": [
        {
          "title": "Llama 3.2",
          "provider": "ollama",
          "model": "llama3.2"
        }
      ],
      "mcpServers": {
        "pswiki": {
          "command": "python",
          "args": ["-m", "pswiki_mcp"]
        }
      }
    }
    ```

    3. Open the Continue sidebar (`⌘+L`) and start asking questions.

## Available Tools

The MCP server exposes five tools to AI assistants:

### search_terms

Search terminology by keyword, phrase, or concept.

```python
search_terms(query="frequency control", limit=10)
```

### get_term

Retrieve full details for a specific term.

```python
get_term(term_id="voltage-stability")
```

### get_related_terms

Find related concepts with configurable depth.

```python
get_related_terms(term_id="power-flow", depth=2)
```

### list_tags

List all available tags with usage counts.

```python
list_tags()
```

### get_terms_by_tag

Filter terms by category.

```python
get_terms_by_tag(tag="stability")
```

## Programmatic Usage

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["-m", "pswiki_mcp"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool(
            "search_terms",
            {"query": "stability", "limit": 5}
        )
```

## Data Source

The MCP server fetches data from the [PS-Wiki REST API](rest-api.md). All data is read-only and licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

## Resources

- **GitHub**: [ps-wiki/ps-wiki.github.io/mcp](https://github.com/ps-wiki/ps-wiki.github.io/tree/main/mcp)
- **MCP Specification**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Issues**: [GitHub Issues](https://github.com/ps-wiki/ps-wiki.github.io/issues)
