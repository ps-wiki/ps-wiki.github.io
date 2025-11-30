"""Example usage of PS-Wiki MCP server programmatically."""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Example of using the MCP server programmatically."""

    # Configure server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "pswiki_mcp"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            print("=== PS-Wiki MCP Server Example ===\n")

            # Example 1: Search for terms
            print("1. Searching for 'frequency control'...")
            result = await session.call_tool(
                "search_terms", arguments={"query": "frequency control", "limit": 3}
            )
            print(f"Found {len(result.content)} results")
            print(result.content[0].text[:200] + "...\n")

            # Example 2: Get a specific term
            print("2. Getting details for 'automatic-generation-control'...")
            result = await session.call_tool(
                "get_term", arguments={"term_id": "automatic-generation-control"}
            )
            print(result.content[0].text[:200] + "...\n")

            # Example 3: List tags
            print("3. Listing all tags...")
            result = await session.call_tool("list_tags", arguments={})
            print(result.content[0].text[:200] + "...\n")

            # Example 4: Get terms by tag
            print("4. Getting terms with tag 'stability'...")
            result = await session.call_tool("get_terms_by_tag", arguments={"tag": "stability"})
            print(result.content[0].text[:200] + "...\n")

            # Example 5: Get related terms
            print("5. Getting related terms for 'voltage-stability'...")
            result = await session.call_tool(
                "get_related_terms", arguments={"term_id": "voltage-stability", "depth": 1}
            )
            print(result.content[0].text[:200] + "...\n")

            print("=== Example Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
