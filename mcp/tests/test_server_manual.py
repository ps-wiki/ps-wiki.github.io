#!/usr/bin/env python3
"""Quick test to verify the MCP server can start and respond."""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_server():
    """Test basic server functionality."""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "pswiki_mcp"],
    )

    print("Starting MCP server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            print("Initializing session...")
            await session.initialize()
            print("✓ Server initialized successfully")

            # List tools
            print("\nListing available tools...")
            tools_result = await session.list_tools()
            print(f"✓ Found {len(tools_result.tools)} tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description[:60]}...")

            # List resources
            print("\nListing available resources...")
            resources_result = await session.list_resources()
            print(f"✓ Found {len(resources_result.resources)} resources:")
            for resource in resources_result.resources:
                print(f"  - {resource.name} ({resource.uri})")

            # Test a simple tool call
            print("\nTesting search_terms tool...")
            result = await session.call_tool(
                "search_terms", arguments={"query": "stability", "limit": 3}
            )
            data = json.loads(result.content[0].text)
            print(f"✓ Search returned {data['count']} results")
            if data["results"]:
                print(f"  First result: {data['results'][0]['title']}")

            print("\n✅ All tests passed! MCP server is working correctly.")


if __name__ == "__main__":
    asyncio.run(test_server())
