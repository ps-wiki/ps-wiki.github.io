# Development Guide

This document provides guidance for developing and maintaining the PS-Wiki MCP server.

## Project Structure

```
mcp/
├── pyproject.toml              # Package configuration
├── README.md                   # User documentation
├── DEVELOPMENT.md              # This file
├── .gitignore
├── src/
│   └── pswiki_mcp/
│       ├── __init__.py         # Package exports
│       ├── __main__.py         # Module entry point
│       ├── server.py           # MCP server implementation
│       ├── api_client.py       # REST API wrapper
│       └── tools.py            # Tool implementations
├── tests/
│   ├── test_api_client.py      # API client tests
│   └── test_server_manual.py   # Manual server test
└── examples/
    ├── claude_desktop_config.json
    └── usage_example.py
```

## Development Setup

### 1. Install in Development Mode

```bash
cd mcp
pip install -e ".[dev]"
```

This installs the package in editable mode with development dependencies:
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `black` - Code formatter
- `ruff` - Linter

### 2. Verify Installation

```bash
# Run tests
pytest tests/ -v

# Test server manually
python tests/test_server_manual.py

# Check if command works
pswiki-mcp --help  # Should show error (no --help implemented yet)
```

## Testing

### Unit Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api_client.py

# Run with coverage
pytest --cov=pswiki_mcp tests/
```

### Manual Server Testing

```bash
# Test server initialization and basic functionality
python tests/test_server_manual.py
```

### Integration Testing with Claude Desktop

1. Install the package:
   ```bash
   pip install -e .
   ```

2. Configure Claude Desktop (see `examples/claude_desktop_config.json`):
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

3. Restart Claude Desktop

4. Test by asking Claude:
   - "Search for power systems stability terms"
   - "What is automatic generation control?"
   - "Show me terms related to voltage stability"

## Code Quality

### Formatting

```bash
# Format code with black
black src/ tests/

# Check formatting without changes
black --check src/ tests/
```

### Linting

```bash
# Run ruff linter
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### Type Checking (Optional)

```bash
# Install mypy
pip install mypy

# Run type checker
mypy src/pswiki_mcp
```

## Making Changes

### Adding a New Tool

1. Define the tool in `server.py` (`list_tools()` method)
2. Implement the handler in `tools.py`
3. Register the handler in `server.py` (`call_tool()` method)
4. Add tests in `tests/`
5. Update `README.md` documentation

Example:
```python
# In tools.py
async def my_new_tool(client: APIClient, args: dict[str, Any]) -> dict[str, Any]:
    """Implementation of new tool."""
    # ... implementation
    return result

# In server.py list_tools()
Tool(
    name="my_new_tool",
    description="Description of what it does",
    inputSchema={...}
)

# In server.py call_tool()
elif name == "my_new_tool":
    result = await my_new_tool(api_client, arguments)
```

### Adding a New Resource

1. Define the resource in `server.py` (`list_resources()` method)
2. Handle reading in `read_resource()` method
3. Add tests
4. Update documentation

### Modifying API Client

1. Update methods in `api_client.py`
2. Update `TermSummary` model if needed
3. Add/update tests in `test_api_client.py`

## Building and Publishing

### Build Package

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# This creates:
# - dist/pswiki_mcp-0.1.0-py3-none-any.whl
# - dist/pswiki_mcp-0.1.0.tar.gz
```

### Test Package Locally

```bash
# Install from wheel
pip install dist/pswiki_mcp-0.1.0-py3-none-any.whl

# Test it works
pswiki-mcp  # Should start server
python -m pswiki_mcp  # Alternative way
```

### Publish to PyPI

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Install from TestPyPI to verify
pip install --index-url https://test.pypi.org/simple/ pswiki-mcp

# Publish to real PyPI
twine upload dist/*
```

### Version Bumping

1. Update version in `pyproject.toml`
2. Update version in `src/pswiki_mcp/__init__.py`
3. Commit changes
4. Tag release: `git tag mcp-v0.2.0`
5. Push tag: `git push origin mcp-v0.2.0`

## Debugging

### Enable Debug Logging

```python
# In server.py, add at the top
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test with MCP Inspector

The MCP project provides an inspector tool:

```bash
# Install MCP inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector
mcp-inspector python -m pswiki_mcp
```

### Common Issues

**Server won't start:**
- Check Python version (requires 3.10+)
- Verify dependencies: `pip list | grep mcp`
- Check for syntax errors: `python -m py_compile src/pswiki_mcp/*.py`

**API calls failing:**
- Verify API is accessible: `curl https://pswiki-api.jinninggm.workers.dev/v1/terms`
- Check network connectivity
- Look for rate limiting issues

**Claude Desktop not seeing server:**
- Verify config file location
- Check JSON syntax in config
- Restart Claude Desktop completely
- Check Claude Desktop logs (Help → View Logs)

## CI/CD

### GitHub Actions Workflow

Create `.github/workflows/test-mcp.yml`:

```yaml
name: Test MCP Server

on:
  push:
    paths:
      - 'mcp/**'
  pull_request:
    paths:
      - 'mcp/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        working-directory: ./mcp
        run: |
          pip install -e ".[dev]"
      - name: Run tests
        working-directory: ./mcp
        run: pytest -v
      - name: Check formatting
        working-directory: ./mcp
        run: black --check src/ tests/
      - name: Run linter
        working-directory: ./mcp
        run: ruff check src/ tests/
```

### Publishing Workflow

Create `.github/workflows/publish-mcp.yml`:

```yaml
name: Publish MCP to PyPI

on:
  push:
    tags:
      - 'mcp-v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install build tools
        run: pip install build twine
      - name: Build package
        working-directory: ./mcp
        run: python -m build
      - name: Publish to PyPI
        working-directory: ./mcp
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: twine upload dist/*
```

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [PS-Wiki REST API](https://pswiki-api.jinninggm.workers.dev/openapi.json)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)
