# Using PS-Wiki MCP Server with Ollama on Mac

Complete step-by-step guide to use your PS-Wiki MCP server with Ollama for local, private AI-powered power systems research.

## Prerequisites

✅ You have:
- Mac with Ollama installed
- PS-Wiki MCP server installed (`cd mcp && pip install -e .`)

## Step 1: Start Ollama

### 1.1 Check if Ollama is Running

```bash
# Check if Ollama service is running
ollama list
```

If you see a list of models (or "No models found"), Ollama is running. If you get an error, start it:

```bash
# Ollama should auto-start on Mac, but if not:
# Just run any ollama command and it will start automatically
ollama --version
```

### 1.2 Pull a Model (if you haven't already)

```bash
# Pull a good model for technical content (recommended)
ollama pull llama3.2

# Or try a larger model for better quality (if you have RAM)
ollama pull llama3.1:8b

# Or a smaller, faster model
ollama pull phi3
```

**Recommended**: `llama3.2` (good balance of speed and quality)

### 1.3 Test Ollama

```bash
# Quick test
ollama run llama3.2 "What is voltage stability?"
```

Press `Ctrl+D` or type `/bye` to exit the chat.

## Step 2: Choose Your MCP Client

You have **3 options** to use MCP with Ollama:

### Option A: Continue.dev in VS Code (Easiest) ⭐ **RECOMMENDED**

### Option B: Direct Python Script (Most Flexible)

### Option C: Custom Integration (Advanced)

---

## Option A: Continue.dev (Easiest Setup)

### A.1 Install Continue Extension

1. Open VS Code
2. Go to Extensions (⌘+Shift+X)
3. Search for "Continue"
4. Click Install

### A.2 Configure Continue

1. Open Command Palette (⌘+Shift+P)
2. Type "Continue: Open config.json"
3. Replace contents with:

```json
{
  "models": [
    {
      "title": "Llama 3.2 (Local)",
      "provider": "ollama",
      "model": "llama3.2",
      "apiBase": "http://localhost:11434"
    }
  ],
  "mcpServers": {
    "pswiki": {
      "command": "python",
      "args": ["-m", "pswiki_mcp"]
    }
  },
  "tabAutocompleteModel": {
    "title": "Starcoder",
    "provider": "ollama",
    "model": "starcoder2:3b"
  }
}
```

### A.3 Restart VS Code

Close and reopen VS Code for changes to take effect.

### A.4 Test It!

1. Open Continue sidebar (click Continue icon or ⌘+L)
2. Ask: **"Search for power systems stability terms"**
3. Continue will use your MCP server to search PS-Wiki!
4. Ask: **"Explain voltage stability in detail"**
5. It will fetch the term and explain it!

**Example conversation:**
```
You: "What is automatic generation control?"

Continue: [Uses get_term tool]
Based on PS-Wiki, Automatic Generation Control (AGC) is...
[Provides detailed explanation with citations]

You: "What are related concepts?"

Continue: [Uses get_related_terms tool]
Related concepts include:
- Load Frequency Control
- Governor Response
- Area Control Error
...
```

---

## Option B: Direct Python Script (Most Flexible)

This gives you full control and doesn't require VS Code.

### B.1 Create a Test Script

Create `test_ollama_mcp.py`:

```python
#!/usr/bin/env python3
"""
Simple script to test PS-Wiki MCP server with Ollama.
This demonstrates the data flow without needing a full MCP client.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def search_and_explain(topic: str):
    """Search PS-Wiki and get data for Ollama to explain."""
    
    # Start MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "pswiki_mcp"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print(f"\n🔍 Searching PS-Wiki for: {topic}")
            
            # Search for terms
            result = await session.call_tool(
                "search_terms",
                arguments={"query": topic, "limit": 3}
            )
            
            data = json.loads(result.content[0].text)
            
            if not data['results']:
                print("No results found!")
                return
            
            # Get first term details
            term_id = data['results'][0]['id']
            print(f"\n📖 Fetching details for: {term_id}")
            
            result = await session.call_tool(
                "get_term",
                arguments={"term_id": term_id}
            )
            
            term = json.loads(result.content[0].text)
            
            print(f"\n{'='*60}")
            print(f"Term: {term['title']}")
            print(f"{'='*60}")
            print(f"\nDescription:\n{term.get('description', 'N/A')}")
            
            if term.get('related'):
                print(f"\nRelated terms: {', '.join(term['related'][:5])}")
            
            # Now you can pass this to Ollama
            print(f"\n{'='*60}")
            print("Now calling Ollama to explain this...")
            print(f"{'='*60}\n")
            
            # Call Ollama (requires ollama Python package)
            try:
                import subprocess
                prompt = f"Based on this definition: {term.get('description', '')}\n\nExplain '{term['title']}' to a graduate student in power systems engineering."
                
                result = subprocess.run(
                    ["ollama", "run", "llama3.2", prompt],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                print("Ollama's Explanation:")
                print(result.stdout)
                
            except Exception as e:
                print(f"Note: Install ollama CLI to see AI explanation")
                print(f"You can manually ask Ollama: 'Explain {term['title']}'")


if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "voltage stability"
    asyncio.run(search_and_explain(topic))
```

### B.2 Run It

```bash
cd /Users/jinningwang/work/pswiki/mcp

# Search for voltage stability
python test_ollama_mcp.py "voltage stability"

# Search for frequency control
python test_ollama_mcp.py "frequency control"

# Search for any topic
python test_ollama_mcp.py "renewable energy integration"
```

This will:
1. Search PS-Wiki via MCP
2. Get the term definition
3. Pass it to Ollama for explanation

---

## Option C: Interactive Chat (Advanced)

For a more interactive experience, you can use the MCP Inspector:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector with your server
npx @modelcontextprotocol/inspector python -m pswiki_mcp
```

This opens a web UI where you can:
- See all available tools
- Call tools manually
- Inspect responses
- Test your MCP server

---

## Quick Test Commands

### Test 1: Search Terms
```bash
cd /Users/jinningwang/work/pswiki/mcp
python examples/ollama_integration.py
```

### Test 2: Manual Ollama + MCP Workflow

```bash
# Terminal 1: Get data from PS-Wiki
cd /Users/jinningwang/work/pswiki/mcp
python -c "
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def search():
    params = StdioServerParameters(command='python', args=['-m', 'pswiki_mcp'])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            result = await s.call_tool('search_terms', {'query': 'stability', 'limit': 3})
            print(json.loads(result.content[0].text))

asyncio.run(search())
"

# Terminal 2: Ask Ollama to explain
ollama run llama3.2
# Then paste the term description and ask for explanation
```

---

## Troubleshooting

### Issue: "command not found: ollama"
**Solution**: Ollama not in PATH. Try:
```bash
/Applications/Ollama.app/Contents/MacOS/ollama list
```

### Issue: "Connection refused" from Ollama
**Solution**: Start Ollama:
```bash
# Open Ollama app from Applications
# Or run: ollama serve
```

### Issue: MCP server not found
**Solution**: Make sure you're in the right environment:
```bash
cd /Users/jinningwang/work/pswiki/mcp
pip install -e .
python -m pswiki_mcp  # Should start without error
```

### Issue: Tests failing
**Solution**: Install pytest-asyncio:
```bash
pip install pytest-asyncio
pytest tests/ -v
```

---

## Recommended Workflow

1. **Start with Option B** (Python script) to understand the flow
2. **Move to Option A** (Continue.dev) for daily use
3. **Use Option C** (Inspector) for debugging

---

## Example Research Session

```bash
# 1. Start VS Code with Continue
code /Users/jinningwang/work/pswiki

# 2. Open Continue (⌘+L)

# 3. Ask questions:
"Search for terms related to power system stability"
"Explain the difference between voltage and frequency stability"
"What are the main challenges in renewable energy integration?"
"Show me terms related to automatic generation control"

# Continue will:
# - Use your MCP server to fetch accurate data from PS-Wiki
# - Use Ollama to provide natural language explanations
# - All processing happens locally on your Mac!
```

---

## Benefits of This Setup

✅ **Complete Privacy**: All data stays on your Mac
✅ **No API Costs**: Free to use, no rate limits
✅ **Accurate Data**: PS-Wiki provides cited definitions
✅ **Natural Language**: Ollama makes it conversational
✅ **Offline Capable**: Works without internet (after models are downloaded)

---

## Next Steps

1. Try Option B script first to see it working
2. Install Continue.dev for better UX
3. Experiment with different Ollama models
4. Customize the prompts for your research needs

Enjoy your local AI-powered power systems research assistant! 🎉
