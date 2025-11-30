"""MCP server implementation for PS-Wiki."""

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from .api_client import APIClient
from .tools import (
    search_terms_tool,
    get_term_tool,
    get_related_terms_tool,
    list_tags_tool,
    get_terms_by_tag_tool,
)


# Initialize server
app = Server("pswiki-mcp")

# Global API client (initialized in main)
api_client: APIClient | None = None


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="tags://all",
            name="All Tags",
            mimeType="application/json",
            description="List of all tags with usage counts",
        ),
        Resource(
            uri="index://terms",
            name="Term Index",
            mimeType="application/json",
            description="Complete index of all power systems terms",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI."""
    if not api_client:
        raise RuntimeError("API client not initialized")

    if uri == "tags://all":
        tags = await api_client.list_tags()
        return json.dumps({"tags": tags}, indent=2)

    elif uri == "index://terms":
        # Get all terms (paginate if needed)
        terms = await api_client.search_terms(limit=100)
        return json.dumps(
            {"terms": [term.model_dump() for term in terms], "count": len(terms)}, indent=2
        )

    elif uri.startswith("term:///"):
        # Individual term resource: term:///voltage-stability
        term_id = uri.replace("term:///", "")
        term = await api_client.get_term(term_id)
        return json.dumps(term, indent=2)

    else:
        raise ValueError(f"Unknown resource URI: {uri}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_terms",
            description="Search power systems terminology by keyword, phrase, or concept. "
            "Searches across term IDs, titles, descriptions, and tags.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'frequency control', 'stability')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10, max: 50)",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_term",
            description="Retrieve full details for a specific power systems term by its ID. "
            "Returns definition, equations, citations, related terms, and metadata.",
            inputSchema={
                "type": "object",
                "properties": {
                    "term_id": {
                        "type": "string",
                        "description": "Term identifier (e.g., 'voltage-stability', 'automatic-generation-control')",
                    }
                },
                "required": ["term_id"],
            },
        ),
        Tool(
            name="get_related_terms",
            description="Find terms related to a given term. Useful for exploring connected concepts "
            "and building knowledge graphs.",
            inputSchema={
                "type": "object",
                "properties": {
                    "term_id": {
                        "type": "string",
                        "description": "Term identifier to find related terms for",
                    },
                    "depth": {
                        "type": "integer",
                        "description": "Relationship depth (1=direct, 2=includes related-to-related)",
                        "minimum": 1,
                        "maximum": 2,
                        "default": 1,
                    },
                },
                "required": ["term_id"],
            },
        ),
        Tool(
            name="list_tags",
            description="List all available tags with usage counts. "
            "Tags categorize terms (e.g., stability, control, protection, market).",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_terms_by_tag",
            description="Get all terms with a specific tag. "
            "Useful for browsing terms by category.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tag": {
                        "type": "string",
                        "description": "Tag name (case-insensitive, e.g., 'stability', 'control')",
                    }
                },
                "required": ["tag"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    if not api_client:
        raise RuntimeError("API client not initialized")

    # Route to appropriate tool handler
    if name == "search_terms":
        result = await search_terms_tool(api_client, arguments)
    elif name == "get_term":
        result = await get_term_tool(api_client, arguments)
    elif name == "get_related_terms":
        result = await get_related_terms_tool(api_client, arguments)
    elif name == "list_tags":
        result = await list_tags_tool(api_client, arguments)
    elif name == "get_terms_by_tag":
        result = await get_terms_by_tag_tool(api_client, arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def run_server():
    """Run the MCP server."""
    global api_client

    # Initialize API client
    api_client = APIClient()

    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    finally:
        # Cleanup
        if api_client:
            await api_client.close()


def main():
    """Main entry point."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
