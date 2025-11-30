# PS-Wiki MCP Server

MCP (Model Context Protocol) server for [PS-Wiki](https://ps-wiki.github.io) - providing AI assistants with direct access to power systems terminology and knowledge.

## Features

- 🔍 **Semantic Search**: Search across 173+ power systems terms
- 📖 **Term Lookup**: Get detailed definitions with citations
- 🔗 **Relationship Traversal**: Explore related concepts
- 🏷️ **Tag Browsing**: Filter by categories (stability, control, protection, etc.)
- 📚 **Bibliography Access**: Reference academic papers and standards

## Installation

### Prerequisites

- Python 3.10 or higher
- An MCP-compatible client:
  - [Claude Desktop](https://claude.ai/download) (commercial, easy setup)
  - [Ollama](https://ollama.com) + MCP frontend (open-source, local)
  - Or any other [MCP-compatible client](https://modelcontextprotocol.io)

### Install from PyPI

```bash
pip install pswiki-mcp
```

### Install from Source

```bash
git clone https://github.com/ps-wiki/ps-wiki.github.io.git
cd ps-wiki.github.io/mcp
pip install -e .
```

## Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

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

Or if installed globally:

```json
{
  "mcpServers": {
    "pswiki": {
      "command": "pswiki-mcp"
    }
  }
}
```

### Ollama (Open-Source Alternative)

For local, open-source AI models, you can use Ollama with MCP-compatible frontends.

#### Option 1: Using Continue.dev (VS Code Extension)

1. Install [Continue](https://continue.dev) extension in VS Code
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

#### Option 2: Using Ollama MCP Bridge

Install an Ollama MCP bridge:

```bash
# Install ollama-mcp-bridge
npm install -g @modelcontextprotocol/server-ollama

# Configure your MCP client to use both servers
```

Example configuration:

```json
{
  "mcpServers": {
    "ollama": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-ollama"]
    },
    "pswiki": {
      "command": "python",
      "args": ["-m", "pswiki_mcp"]
    }
  }
}
```

#### Option 3: Direct Integration (Advanced)

Use the programmatic API (see examples below) to integrate with your own Ollama-based application.

### Other MCP Clients

The server uses stdio transport and can be integrated with any MCP-compatible client. See [MCP documentation](https://modelcontextprotocol.io) for details.

## Available Tools

### `search_terms`

Search power systems terminology by keyword, phrase, or concept.

**Parameters:**

- `query` (string, required): Search query
- `limit` (integer, optional): Max results (default: 10, max: 50)

**Example:**

```
Search for "frequency control" → Returns terms related to AGC, governor response, inertia, etc.
```

### `get_term`

Retrieve full details for a specific term by ID.

**Parameters:**

- `term_id` (string, required): Term identifier (e.g., "automatic-generation-control")

**Example:**

```
Get term "voltage-stability" → Returns definition, equations, citations, related terms
```

### `get_related_terms`

Find terms related to a given term.

**Parameters:**

- `term_id` (string, required): Term identifier
- `depth` (integer, optional): Relationship depth (default: 1, max: 2)

**Example:**

```
Get related terms for "power-flow" → Returns load-flow, optimal-power-flow, etc.
```

### `list_tags`

List all available tags with usage counts.

**Example:**

```
List tags → Returns: stability (15), control (23), protection (8), etc.
```

### `get_terms_by_tag`

Get all terms with a specific tag.

**Parameters:**

- `tag` (string, required): Tag name (case-insensitive)

**Example:**

```
Get terms by tag "stability" → Returns all stability-related terms
```

## Available Resources

### `term:///{term_id}`

Access individual term as a resource.

### `tags://all`

List of all tags with counts.

### `index://terms`

Complete term index with metadata.

## Usage Examples

### With Claude Desktop

Once configured, you can ask Claude:

> "Explain the difference between voltage stability and frequency stability in power systems"

Claude will use the MCP server to fetch relevant terms and provide accurate, cited explanations.

> "What are the main control strategies for automatic generation control?"

Claude will retrieve the AGC term and related control concepts.

### With Ollama (Open-Source)

If using Ollama with Continue.dev or another MCP-compatible frontend:

> **User**: "Search for power systems stability terms"

> **AI**: _Uses `search_terms` tool to find stability-related terminology_

> **User**: "Explain voltage stability in detail"

> **AI**: _Uses `get_term` tool to fetch the full definition with equations and citations_

The advantage of Ollama is complete privacy - all processing happens locally on your machine.

### Programmatic Usage

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

        # Search for terms
        result = await session.call_tool("search_terms", {"query": "stability"})
        print(result)
```

## Data Source

The MCP server fetches data from the [PS-Wiki REST API](https://pswiki-api.jinninggm.workers.dev) hosted on Cloudflare Workers. All data is read-only and licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

## Development

### Setup Development Environment

```bash
cd mcp
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ tests/
ruff check src/ tests/
```

## Contributing

Contributions are welcome! Please see the [main repository](https://github.com/ps-wiki/ps-wiki.github.io) for contribution guidelines.

## License

This project is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) - see the [LICENSE](../LICENSE) file for details.

## Related Projects

- [PS-Wiki Website](https://ps-wiki.github.io) - Main terminology wiki
- [PS-Wiki REST API](https://pswiki-api.jinninggm.workers.dev) - Public API
- [MCP Specification](https://modelcontextprotocol.io) - Model Context Protocol

## Support

- 📖 [Documentation](https://ps-wiki.github.io)
- 🐛 [Issue Tracker](https://github.com/ps-wiki/ps-wiki.github.io/issues)
- 💬 [Discussions](https://github.com/ps-wiki/ps-wiki.github.io/discussions)
