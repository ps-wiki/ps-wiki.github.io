#!/usr/bin/env python3
"""
Quick test script for PS-Wiki MCP + Ollama integration.
This is the simplest way to see your MCP server working with local AI.
"""

import asyncio
import json
import subprocess
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def demo_mcp_ollama(topic: str = "voltage stability"):
    """Demonstrate MCP server fetching data for Ollama to explain."""

    print(f"\n{'='*70}")
    print(f"  PS-Wiki MCP + Ollama Demo")
    print(f"{'='*70}\n")

    # Start MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "pswiki_mcp"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print(f"🔍 Step 1: Searching PS-Wiki for '{topic}'...")

            # Search for terms
            result = await session.call_tool("search_terms", arguments={"query": topic, "limit": 3})

            data = json.loads(result.content[0].text)
            print(f"   ✓ Found {data['count']} results\n")

            if not data["results"]:
                print("   No results found. Try a different topic.")
                return

            # Show search results
            print("   Search Results:")
            for i, term in enumerate(data["results"], 1):
                print(f"   {i}. {term['title']} ({term['id']})")

            # Get first term details
            term_id = data["results"][0]["id"]
            print(f"\n📖 Step 2: Fetching full details for '{term_id}'...")

            result = await session.call_tool("get_term", arguments={"term_id": term_id})

            term = json.loads(result.content[0].text)
            print(f"   ✓ Retrieved term data\n")

            # Display term info
            print(f"{'='*70}")
            print(f"  {term['title']}")
            print(f"{'='*70}\n")

            description = term.get("description", "No description available")
            print(f"Description:\n{description[:300]}...")

            if term.get("tags"):
                print(f"\nTags: {', '.join(term['tags'][:5])}")

            if term.get("related"):
                print(f"Related: {', '.join(term['related'][:5])}")

            # Now call Ollama
            print(f"\n{'='*70}")
            print(f"🤖 Step 3: Asking Ollama to explain (using llama3.2)...")
            print(f"{'='*70}\n")

            prompt = f"""Based on this technical definition from PS-Wiki:

"{description}"

Please explain "{term['title']}" in simple terms for a graduate student in power systems engineering. Keep it concise (2-3 paragraphs)."""

            try:
                # Call Ollama CLI
                result = subprocess.run(
                    ["ollama", "run", "llama3.2", prompt],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                if result.returncode == 0:
                    print("Ollama's Explanation:")
                    print("-" * 70)
                    print(result.stdout)
                    print("-" * 70)
                else:
                    print(f"Error calling Ollama: {result.stderr}")
                    print("\nTo use Ollama:")
                    print("1. Make sure Ollama is running")
                    print("2. Pull a model: ollama pull llama3.2")
                    print("3. Run this script again")

            except FileNotFoundError:
                print("⚠️  Ollama CLI not found!")
                print("\nYou can still use the data above. To enable Ollama:")
                print("1. Install Ollama from https://ollama.com")
                print("2. Run: ollama pull llama3.2")
                print("3. Run this script again")

            except subprocess.TimeoutExpired:
                print("⚠️  Ollama took too long to respond (>60s)")
                print("Try a smaller model or increase timeout")

            except Exception as e:
                print(f"⚠️  Error: {e}")
                print("\nManual workflow:")
                print(f"1. Run: ollama run llama3.2")
                print(f"2. Paste: Explain '{term['title']}' based on: {description[:100]}...")


if __name__ == "__main__":
    import sys

    # Get topic from command line or use default
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "voltage stability"

    print("\nPS-Wiki MCP Server + Ollama Integration Demo")
    print("=" * 70)
    print(f"Topic: {topic}")

    try:
        asyncio.run(demo_mcp_ollama(topic))

        print(f"\n{'='*70}")
        print("✅ Demo complete!")
        print(f"{'='*70}\n")
        print("Try other topics:")
        print("  python quick_test.py 'frequency control'")
        print("  python quick_test.py 'renewable energy'")
        print("  python quick_test.py 'power flow'")
        print()

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the mcp/ directory")
        print("2. Install the package: pip install -e .")
        print("3. Check Ollama is running: ollama list")
