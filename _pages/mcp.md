---
layout: page
title: mcp
permalink: /mcp/
description: AI-native access to PS-Wiki terminology via Model Context Protocol
nav: false
horizontal: false
---

The **PS-Wiki MCP Server** provides AI assistants with direct access to power systems terminology through the [Model Context Protocol](https://modelcontextprotocol.io). This enables natural language queries with accurate, cited responses.

# Features

- 🔍 **Search** 173+ power systems terms by keyword or concept
- 📖 **Retrieve** detailed definitions with equations and citations
- 🔗 **Explore** related concepts and build knowledge graphs
- 🏷️ **Browse** by tags (stability, control, protection, market, etc.)
- 🤖 **Works with** Claude Desktop, Ollama, and other MCP clients

# Quick Start

## Installation

```bash
# Install from PyPI (when published)
pip install pswiki-mcp

# Or install from source
git clone https://github.com/ps-wiki/ps-wiki.github.io.git
cd ps-wiki.github.io/mcp
pip install -e .
```

## Configuration

### Option 1: Claude Desktop (Easiest)

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

### Option 2: Ollama (Open-Source)

For local, private AI using Ollama:

#### Using Continue.dev (VS Code)

1. Install [Continue](https://continue.dev) extension
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

3. Open Continue sidebar (⌘+L) and start asking questions!

#### Quick Test Script

```bash
cd ps-wiki.github.io/mcp

# Make sure Ollama is running
ollama pull llama3.2

# Run demo
python quick_test.py "voltage stability"
```

This demonstrates the complete workflow: MCP fetches data, Ollama explains it.

# Available Tools

The MCP server provides 5 tools for AI assistants:

## search_terms

Search terminology by keyword, phrase, or concept.

**Example**: `search_terms(query="frequency control", limit=10)`

## get_term

Retrieve full details for a specific term.

**Example**: `get_term(term_id="voltage-stability")`

## get_related_terms

Find related concepts with configurable depth.

**Example**: `get_related_terms(term_id="power-flow", depth=2)`

## list_tags

List all available tags with usage counts.

**Example**: `list_tags()`

## get_terms_by_tag

Filter terms by category.

**Example**: `get_terms_by_tag(tag="stability")`

# Usage Examples

## With Claude Desktop

> **You**: "Explain the difference between voltage stability and frequency stability"

> **Claude**: _[Uses `search_terms` and `get_term` tools to fetch PS-Wiki data, then provides accurate explanation with citations]_

## With Ollama

> **You**: "What is automatic generation control?"

> **AI**: _[Fetches AGC definition from PS-Wiki via MCP, explains using local Llama model]_

**Advantage**: Complete privacy - all processing happens on your machine.

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

# Data Source

The MCP server fetches data from the [PS-Wiki REST API](https://pswiki-api.jinninggm.workers.dev) hosted on Cloudflare Workers. All data is read-only and licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

# Benefits

✅ **AI-Native**: Natural language access to technical terminology  
✅ **Accurate**: Cited definitions from standards and papers  
✅ **Private**: Use with Ollama for complete local processing  
✅ **Free**: No API costs, no rate limits  
✅ **Extensible**: Works with any MCP-compatible client

# Resources

- **GitHub**: [ps-wiki/ps-wiki.github.io/mcp](https://github.com/ps-wiki/ps-wiki.github.io/tree/main/mcp)
- **Documentation**: [README](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/mcp/README.md)
- **Ollama Guide**: [OLLAMA_GUIDE.md](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/mcp/OLLAMA_GUIDE.md)
- **MCP Specification**: [modelcontextprotocol.io](https://modelcontextprotocol.io)

# Support

- 🐛 [Issue Tracker](https://github.com/ps-wiki/ps-wiki.github.io/issues)
- 💬 [Discussions](https://github.com/ps-wiki/ps-wiki.github.io/discussions)
