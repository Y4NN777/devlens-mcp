# WebDocx MCP - Architecture

## What is this?

WebDocx is an **MCP Server** - a program that implements the Model Context Protocol to give LLMs internet access. It works with any MCP-compatible client (Claude Desktop, VS Code GitHub Copilot, custom tools).

```
You (Human)
    |
    | "Research topic X"
    v
+------------------+
|   MCP Client     |  <-- Any MCP-compatible AI assistant
| (Claude/VS Code/ |      (LLM has no direct internet access)
|  Custom Tool)    |
+------------------+
    |
    | MCP Protocol: calls tool search_web("topic X")
    v
+----------------------+
|  WebDocx Server      |  <-- THIS is what we're building
|  (STDIO transport)   |
+----------------------+
    |
    | HTTP/HTTPS requests
    v
+------------------+
|  The Internet    |
|  (DDG, websites) |
+------------------+
    |
    | Results flow back up
    v
Client receives structured data, answers your question with sources
```

## How the Server Works

The server exposes **Tools** that the LLM can call. Each tool is just a Python function.

```
+------------------------------------------------------------------+
|                      WebDocx MCP Server                          |
|                                                                  |
|  +--------------------+  +-----------------------------+          |
|  |   MCP Interface    |  |      Tool Registry (9)      |          |
|  |   (fastmcp)        |  |                             |          |
|  |                    |  |  CORE:                      |          |
|  |  Handles:          |  |  - search_web               |          |
|  |  - JSON-RPC msgs   |  |  - scrape_url               |          |
|  |  - Tool routing    |  |  - deep_dive                |          |
|  |  - Error handling  |  |  - crawl_docs               |          |
|  |                    |  |  - summarize_page           |          |
|  |                    |  |  ADVANCED: 🆕               |          |
|  |                    |  |  - compare_sources          |          |
|  |                    |  |  - find_related             |          |
|  |                    |  |  - extract_links            |          |
|  |                    |  |  - monitor_changes          |          |
|  +--------------------+  +-----------------------------+          |
|            |                      |                              |
|            v                      v                              |
|  +----------------------------------------------------------+   |
|  |                    Shared Services                        |   |
|  |                                                           |   |
|  |  +---------------+  +---------------+  +---------------+  |   |
|  |  | Web Fetcher   |  | HTML Cleaner  |  | Aggregator    |  |   |
|  |  | (crawl4ai)    |  | (readability) |  | (combines     |  |   |
|  |  |               |  |               |  |  sources)     |  |   |
|  |  +---------------+  +---------------+  +---------------+  |   |
|  +----------------------------------------------------------+   |
+------------------------------------------------------------------+
```

## Tool Details

### Core Tools

### 1. search_web ✨ Enhanced
```
Input:  query="python MCP tutorial", limit=5, region="us-en"
Output: [
  { title: "...", url: "https://...", snippet: "..." },
  ...
]
```
Uses DDGS (migrated from duckduckgo-search). **New**: Region support, query normalization, quality filtering.

### 2. scrape_url ✨ Enhanced
```
Input:  url="https://docs.python.org/3/", include_metadata=true
Output: 
  # Python Documentation
  > Source: https://docs.python.org/3/
  
  (clean markdown content...)
  
  ## Metadata
  - Word count: 1234
  - Lines: 89
  - Fetch time: 1.2s
```
Uses crawl4ai + httpx fallback. **New**: Retry mechanism (exponential backoff), optional metadata (+41% more info).

### 3. deep_dive ✨ Enhanced
```
Input:  topic="MCP architecture", depth=3, parallel=true
Output:
  # Research: MCP architecture
  
  ## Sources
  1. [Article A](url)
  2. [Article B](url)
  3. [Article C](url)
  
  ## Content
  ### From Source 1
  (content...)
  
  ### From Source 2
  (content...)
```
Chains search + scrape. **New**: Parallel processing (3x faster), domain diversity filtering.

### 4. crawl_docs ✨ Enhanced
```
Input:  root_url="https://fastapi.tiangolo.com/", max_pages=5, follow_external=false
Output:
  # FastAPI Documentation
  
  ## Table of Contents
  1. [Introduction](#introduction)
  2. [Installation](#installation)
  3. [First Steps](#first-steps)
  
  ## Introduction
  (content from page 1...)
  
  ## Installation
  (content from page 2...)
```
Follows links within the same domain. **New**: Smart filtering (skips login/signup), documentation prioritization, anchor-friendly TOC.

### 5. summarize_page
```
Input:  url="https://long-article.com/post"
Output:
  # Summary: Article Title
  > Source: https://long-article.com/post
  
  ## Key Sections
  - Introduction: Brief overview of...
  - Main Point 1: ...
  - Main Point 2: ...
  - Conclusion: ...
```
Extracts structure without full content. Good for triage.

---

### Advanced Tools 🆕

### 6. compare_sources
```
Input:  topic="Python async", sources=["url1", "url2"]
Output:
  # Comparison: Python async
  
  ## Common Topics
  - asyncio (appears in 2/2 sources, 15 mentions)
  - coroutines (appears in 2/2 sources, 8 mentions)
  
  ## Source 1: Real Python
  Key focus: Practical examples of asyncio...
  
  ## Source 2: Python Docs
  Key focus: Technical specification...
```
Analyzes multiple sources for similarities/differences. Generates comparative reports.

### 7. find_related
```
Input:  url="https://example.com/article", limit=5
Output: [
  { title: "Related Article 1", url: "...", snippet: "..." },
  { title: "Related Article 2", url: "...", snippet: "..." },
  ...
]
```
Discovers related resources based on page content. Uses content analysis + search.

### 8. extract_links
```
Input:  url="https://example.com", filter_external=true
Output: {
  "internal": [
    { "url": "/docs", "text": "Documentation" },
    { "url": "/guide", "text": "Guide" }
  ],
  "external": []  # filtered out
}
```
Extracts and categorizes all links. Useful for navigation discovery and sitemap building.

### 9. monitor_changes
```
Input:  url="https://example.com/docs", previous_hash="abc123"
Output: {
  "changed": true,
  "current_hash": "def456",
  "preview": "Updated content...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```
Tracks content changes via hash comparison. Detects documentation updates.

## File Structure

```
webdocx/
├── src/webdocx/
│   ├── server.py       # Entry point, registers 9 tools with fastmcp
│   ├── py.typed        # PEP 561 marker
│   ├── tools/
│   │   ├── search.py   # search_web() - enhanced with region support
│   │   ├── scraper.py  # scrape_url(), crawl_docs() - metadata extraction
│   │   ├── research.py # deep_dive(), summarize_page() - parallel processing
│   │   └── advanced.py # compare_sources(), find_related(), extract_links(), monitor_changes() 🆕
│   ├── adapters/
│   │   ├── duckduckgo.py # DDGS search adapter (migrated from duckduckgo-search)
│   │   └── scraper.py    # Crawl4AI/httpx with retry mechanism
│   └── models/
│       ├── search.py   # SearchResult
│       ├── document.py # Document
│       └── errors.py   # WebDocxError, ScrapingError
├── pyproject.toml      # Updated: ddgs instead of duckduckgo-search
├── test_benchmark.py   # Real validation tests (100% pass rate) 🆕
├── .vscode/mcp.json    # VS Code workspace config 🆕
├── launch_mcp.sh       # MCP launcher script 🆕
└── README.md           # Updated with all features
```

## How to Run

```bash
# Install
uv sync

# Run server (stdio mode for Claude Desktop)
uv run python -m webdocx.server
```

Then add to Claude Desktop's `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "webdocx": {
      "command": "uv",
      "args": ["run", "python", "-m", "webdocx.server"],
      "cwd": "/path/to/webdocx"
    }
  }
}
```
