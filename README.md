# WebDocx MCP

Model Context Protocol (MCP) server providing real-time web access for LLMs and AI agents. Search, scrape, and crawl documentation—all from your workspace.

## Why?

Stop copy-pasting URLs and manually feeding web content to your AI assistant. WebDocx gives any MCP-compatible client (Claude Desktop, VS Code Copilot, custom tools) direct web access through a standardized protocol.


## Tools

### Core Tools
| Tool | What it does |
|------|-------------|
| `search_web` | Search with DuckDuckGo (region/filter support) |
| `scrape_url` | Grab content from a URL as Markdown (w/ metadata) |
| `crawl_docs` | Crawl multi-page docs (smart link filtering) |
| `deep_dive` | Research a topic (parallel scraping) |
| `summarize_page` | Quick page overview |

### Advanced Tools
| Tool | What it does |
|------|-------------|
| `compare_sources` | Compare info across multiple sources |
| `find_related` | Discover related pages |
| `extract_links` | Extract and categorize all links |
| `monitor_changes` | Track page changes over time |

## Setup

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/Y4NN777/webdocx-mcp.git
cd webdocx-mcp

# Install dependencies
uv sync

# Run the server (STDIO mode)
uv run python -m webdocx.server

# Test locally
uv run python test_benchmark.py
```

### MCP Client Configuration

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` or `~/.config/claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "webdocx": {
      "command": "uv",
      "args": ["run", "python", "-m", "webdocx.server"],
      "cwd": "/path/to/webdocx-mcp"
    }
  }
}
```

**VS Code Copilot** (`.vscode/mcp.json` in workspace):
```json
{
  "servers": {
    "webdocx": {
      "command": "/path/to/webdocx-mcp/launch_mcp.sh"
    }
  }
}
```

**Other MCP Clients**: Use STDIO transport with `uv run python -m webdocx.server`

## Stack

- `fastmcp` — MCP server framework
- `crawl4ai` — Web scraping with JavaScript support
- `ddgs` — Search (DuckDuckGo)
- `httpx` — HTTP client with fallback
- `pydantic` — Validation

## Features

**v0.2.0 Enhanced** (80% Validated)
- Metadata extraction (+41% information)
- Retry mechanism (handles network delays)
- Source comparison (analytical insights)
- Region-specific search (localized results)
- Parallel research (faster processing)
- Link extraction & analysis
- Change monitoring

[See Benchmark Results →](docs/VALIDATED_IMPROVEMENTS.md)

## Documentation

- [Validated Improvements](docs/VALIDATED_IMPROVEMENTS.md) - Benchmarked results
- [Enhanced Features](docs/ENHANCED_FEATURES.md)
- [Requirements](docs/REQUIREMENTS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Tools Reference](docs/TOOLS.md)

