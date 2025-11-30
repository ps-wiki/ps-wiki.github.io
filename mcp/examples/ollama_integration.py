"""Example of using PS-Wiki MCP server with Ollama models.

This example shows how to integrate the PS-Wiki MCP server with Ollama
for completely local, private AI-powered power systems research.

Prerequisites:
- Ollama installed (https://ollama.com)
- A model pulled (e.g., `ollama pull llama3.2`)
- pswiki-mcp installed (`pip install pswiki-mcp`)
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def query_pswiki_with_ollama():
    """
    Example: Use MCP server to get power systems data, then use Ollama to explain it.

    This demonstrates the separation of concerns:
    - MCP server provides accurate, cited data
    - Ollama provides natural language understanding and explanation
    """

    # Start PS-Wiki MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "pswiki_mcp"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("=== PS-Wiki + Ollama Integration Example ===\n")

            # Step 1: Search for terms using MCP
            print("1. Searching for 'voltage stability' terms...")
            result = await session.call_tool(
                "search_terms", arguments={"query": "voltage stability", "limit": 3}
            )

            search_data = json.loads(result.content[0].text)
            print(f"   Found {search_data['count']} terms\n")

            # Step 2: Get detailed term information
            if search_data["results"]:
                term_id = search_data["results"][0]["id"]
                print(f"2. Getting details for '{term_id}'...")

                result = await session.call_tool("get_term", arguments={"term_id": term_id})

                term_data = json.loads(result.content[0].text)
                print(f"   Title: {term_data.get('title')}")
                print(f"   Description: {term_data.get('description', '')[:100]}...\n")

                # Step 3: Get related terms
                print(f"3. Finding related terms...")
                result = await session.call_tool(
                    "get_related_terms", arguments={"term_id": term_id, "depth": 1}
                )

                related_data = json.loads(result.content[0].text)
                print(f"   Found {len(related_data.get('related_terms', []))} related terms")
                for rel in related_data.get("related_terms", [])[:3]:
                    print(f"   - {rel['title']}")

                print("\n" + "=" * 50)
                print("\nNow you could pass this data to Ollama for explanation:")
                print("\nExample Ollama prompt:")
                print(f"  'Based on this definition: {term_data.get('description', '')[:100]}...'")
                print(
                    f"  'Explain {term_data.get('title')} to a graduate student in power systems.'"
                )
                print("\nOllama would provide the explanation while PS-Wiki provides the facts!")


async def demonstrate_workflow():
    """
    Demonstrate a complete research workflow:
    1. Search for a topic
    2. Get related terms
    3. Build a knowledge graph
    """

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "pswiki_mcp"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\n=== Research Workflow Example ===\n")

            # Research topic: Understanding power system stability
            topic = "stability"

            print(f"Research Topic: Power System {topic.title()}\n")

            # Get all stability-related terms
            result = await session.call_tool("get_terms_by_tag", arguments={"tag": topic})

            data = json.loads(result.content[0].text)
            print(f"Found {data['count']} terms tagged with '{topic}':")

            for term in data["terms"][:5]:
                print(f"\n  📖 {term['title']}")
                print(f"     ID: {term['id']}")
                print(f"     Summary: {term['summary'][:80]}...")

            print("\n" + "=" * 50)
            print("\nWith Ollama, you could ask:")
            print("  'Compare and contrast these stability concepts'")
            print("  'Which stability type is most critical for renewable integration?'")
            print("  'Create a study guide for these topics'")


if __name__ == "__main__":
    print("PS-Wiki MCP Server + Ollama Integration\n")
    print("This demonstrates using MCP for data access with local AI models.\n")

    # Run examples
    asyncio.run(query_pswiki_with_ollama())
    asyncio.run(demonstrate_workflow())

    print("\n✅ Examples complete!")
    print("\nNext steps:")
    print("1. Install Continue.dev in VS Code")
    print("2. Configure it to use both Ollama and pswiki-mcp")
    print("3. Ask questions naturally and get cited answers!")
