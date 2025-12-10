# DevLens MCP - Architecture

## What is this?

DevLens is an **MCP Server** - a program that implements the Model Context Protocol to give LLMs internet access. It works with any MCP-compatible client (Claude Desktop, VS Code GitHub Copilot, custom tools).

Think of it as a **developer's lens** for viewing the web - different lenses (tools) for different perspectives, with smart auto-focus (orchestration) that picks the right lens automatically.

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
|  DevLens Server      |  <-- THIS is what we're building
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

The server exposes **Tools** that the LLM can call. Each tool is just a Python function - think of them as different lenses in a camera system.

```
+------------------------------------------------------------------+
|                      DevLens MCP Server                          |
|                                                                  |
|  +--------------------+  +-----------------------------+          |
|  |   MCP Interface    |  |      Tool Registry (12)     |          |
|  |   (fastmcp)        |  |                             |          |
|  |                    |  |  Primitives (5):            |          |
|  |  Handles:          |  |  - search_web               |          |
|  |  - JSON-RPC msgs   |  |  - scrape_url               |          |
|  |  - Tool routing    |  |  - crawl_docs               |          |
|  |  - Error handling  |  |  - summarize_page           |          |
|  |                    |  |  - extract_links            |          |
|  |                    |  |                             |          |
|  |                    |  |  Composed (4):              |          |
|  |                    |  |  - deep_dive                |          |
|  |                    |  |  - compare_sources          |          |
|  |                    |  |  - find_related             |          |
|  |                    |  |  - monitor_changes          |          |
|  |                    |  |                             |          |
|  |                    |  |  Meta (3):                  |          |
|  |                    |  |  - suggest_workflow         |          |
|  |                    |  |  - classify_research_intent |          |
|  |                    |  |  - get_server_docs          |          |
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

## Lens System Metaphor

DevLens tools work like camera lenses - each optimized for a specific view:

| Lens Type | Tool | Use Case |
|-----------|------|----------|
| 🔭 Wide Angle | `search_web` | Broad discovery, finding sources |
| 🔬 Macro | `scrape_url` | Close detail on single page |
| 📷 Panoramic | `crawl_docs` | Complete view of documentation |
| 🎥 Zoom | `deep_dive` | Deep focus on topic from multiple angles |
| 🌈 Split Prism | `compare_sources` | Multiple perspectives simultaneously |
| 🔍 Finder | `find_related` | Discover what's adjacent |
| 📊 Grid | `extract_links` | Structure and navigation |
| ⏱️ Time-lapse | `monitor_changes` | Track changes over time |

**Auto-Focus System** = Smart Orchestration (suggests which lens to use)

## Smart Orchestration

DevLens includes an intelligent orchestration layer that auto-recommends workflows - like an auto-focus system that picks the right lens:

```
+------------------------------------------------------------------+
|                    Orchestration System                          |
|                   (Auto-Focus Intelligence)                      |
|                                                                  |
|  +--------------------------+  +---------------------------+     |
|  | Intent Classification    |  | Dynamic Workflow Builder  |     |
|  |                          |  |                           |     |
|  | Detects 7 patterns:      |  | Adapts based on:          |     |
|  | - quick_answer           |  | - Detected intent         |     |
|  | - deep_research          |  | - Known URLs              |     |
|  | - documentation          |  | - Failed tools            |     |
|  | - comparison             |  | - Search attempts         |     |
|  | - discovery              |  | - Failure reasons         |     |
|  | - monitoring             |  |                           |     |
|  | - validation             |  | Output:                   |     |
|  |                          |  | - Tool sequence           |     |
|  | Uses @lru_cache for      |  | - Optimized parameters    |     |
|  | performance (200 cache)  |  | - Fallback strategies     |     |
|  |                          |  | - Cost estimates          |     |
|  +--------------------------+  +---------------------------+     |
|                                                                  |
|  +----------------------------------------------------------+   |
|  |                  ResearchContext Tracking                 |   |
|  |                                                           |   |
|  |  - known_urls: Discovered sources                        |   |
|  |  - failed_tools: Tools that didn't work                  |   |
|  |  - failure_reasons: Why tools failed (NEW!)              |   |
|  |  - search_attempts: Number of searches                   |   |
|  |  - previous_results: Successful executions               |   |
|  +----------------------------------------------------------+   |
+------------------------------------------------------------------+
```

**Design Philosophy:**
- **Composability Over Complexity**: Small tools combine powerfully
- **Intelligence at Edges**: Smart orchestration, simple primitives
- **Token Optimization**: Markdown output, ~70% smaller than HTML
- **Fail Fast, Fail Clearly**: Explicit errors with actionable context
- **Context-Aware**: Workflows adapt to research state
- **Developer Velocity First**: Ship fast, iterate on real usage

## Tool Details

### Primitive Tools (The Basic Lenses)

### 1. search_web (Wide-Angle Lens)
```
Input:  query="python MCP tutorial", limit=5, region="us-en"
Output: [
  { title: "...", url: "https://...", snippet: "..." },
  ...
]
```
**Features:**
- Region support (localized results)
- Query normalization
- Quality filtering (removes low-quality results)
- Safe search configuration

Uses DDGS (DuckDuckGo Search).

---

### 2. scrape_url (Macro Lens)
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
**Features:**
- Exponential backoff retry (handles flaky networks)
- Optional metadata extraction (+41% more info)
- Crawl4ai with httpx fallback
- Clean Markdown output (token-optimized)

---

### 3. crawl_docs (Panoramic Lens)
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
**Features:**
- Smart filtering (skips login/signup/downloads)
- Documentation prioritization
- Anchor-friendly TOC generation
- Same-domain link following
- Configurable external link handling

---

### 4. summarize_page (Quick Preview)
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
Extracts structure without full content. Perfect for triage before expensive scraping.

---

### 5. extract_links (Grid View)
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

---

### Composed Tools (Multi-Lens Systems)

### 6. deep_dive (Zoom Lens)
```
Input:  topic="MCP architecture", depth=5, parallel=true
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
**Features:**
- Parallel processing (3x faster)
- Domain diversity filtering
- Progress tracking
- Successful vs failed fetch reporting

Chains: search → parallel scrape → aggregate.

---

### 7. compare_sources (Split Prism)
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
Analyzes multiple sources for similarities/differences. Generates comparative reports with common topics and source-specific content.

---

### 8. find_related (Discovery Lens)
```
Input:  url="https://example.com/article", limit=5
Output: [
  { title: "Related Article 1", url: "...", snippet: "..." },
  { title: "Related Article 2", url: "...", snippet: "..." },
  ...
]
```
Discovers related resources based on page content. Uses content analysis + search to find similar pages.

---

### 9. monitor_changes (Time-Lapse)
```
Input:  url="https://example.com/docs", previous_hash="abc123"
Output: {
  "changed": true,
  "current_hash": "def456",
  "preview": "Updated content...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```
Tracks content changes via hash comparison. Perfect for monitoring documentation updates.

---

### Meta Tools (Auto-Focus Intelligence)

### 10. suggest_workflow
```
Input:  query="How to integrate payment API?", known_urls=[]
Output: {
  "primary_intent": {
    "type": "quick_answer",
    "confidence": 0.50,
    "reasons": ["Matched: how to"],
    "keywords": ["how to"]
  },
  "workflow": [
    {
      "step": 1,
      "tool": "search_web",
      "purpose": "Find top result",
      "suggested_parameters": {"limit": 3},
      "has_fallback": true,
      "tool_details": {
        "estimated_duration": "fast",
        "resource_cost": "low"
      }
    },
    {
      "step": 2,
      "tool": "scrape_url",
      "purpose": "Get content from best result",
      "suggested_parameters": {},
      "has_fallback": true
    }
  ],
  "context_notes": {
    "has_known_urls": false,
    "failed_tools": [],
    "failure_reasons": {},
    "search_attempts": 0
  },
  "explanation": "Detected quick_answer intent with 50% confidence. Recommended 2-step workflow."
}
```
**The auto-focus system** - Auto-recommends optimal workflow based on query intent and research context.

**Features:**
- 7 intent patterns with confidence scores
- Dynamic parameter optimization (depth, limit, max_pages)
- Context-aware adaptation (skips search if URLs known)
- Fallback strategies
- Resource cost estimation
- Failure tracking with reasons

---

### 11. classify_research_intent
```
Input:  query="Compare FastAPI vs Flask"
Output: {
  "primary_intent": {
    "type": "comparison",
    "confidence": 0.65,
    "reasons": ["Matched keywords: compare, vs", "Priority level: 7/10"],
    "keywords": ["compare", "vs"]
  },
  "secondary_intents": [
    {
      "type": "deep_research",
      "confidence": 0.45,
      "reasons": ["..."]
    }
  ]
}
```
Detects research goal from 7 patterns with confidence scores. Uses LRU cache for performance.

**Intent Patterns:**
- `quick_answer` - Fast single answer
- `deep_research` - Comprehensive multi-source
- `documentation` - Full docs ingestion
- `comparison` - Multiple source analysis
- `discovery` - Find related resources
- `monitoring` - Track changes
- `validation` - URL accessibility check

---

### 12. get_server_docs
```
Input:  topic="philosophy"
Output: """# Design Philosophy & Developer Mindset

## Core Principles

### 1. Composability Over Complexity
Build small, focused tools that combine powerfully...
"""
```
Provides inline documentation about server capabilities. 

**Topics:**
- `overview` - Server capabilities and quick start
- `philosophy` - Design principles and developer mindset
- `tools` - Detailed tool reference
- `workflows` - Common usage patterns
- `orchestration` - Smart automation details
- `examples` - Real-world scenarios

---

## File Structure

```
devlens/
├── src/devlens/
│   ├── server.py       # Entry point, registers 12 tools with fastmcp
│   ├── py.typed        # PEP 561 marker
│   ├── tools/
│   │   ├── search.py   # search_web() - region support, quality filtering
│   │   ├── scraper.py  # scrape_url(), crawl_docs() - metadata, smart filtering
│   │   ├── research.py # deep_dive(), summarize_page() - parallel processing
│   │   └── advanced.py # compare_sources(), find_related(), extract_links(), monitor_changes()
│   ├── utils/
│   │   └── orchestrator.py # suggest_workflow(), classify_intent() - auto-focus system
│   ├── adapters/
│   │   ├── duckduckgo.py # DDGS search adapter
│   │   └── scraper.py    # Crawl4AI/httpx with exponential backoff retry
│   └── models/
│       ├── search.py   # SearchResult, SearchQuery
│       ├── document.py # Document, PageSummary, Section
│       └── errors.py   # WebDocxError, SearchError, ScrapingError, CrawlError
├── pyproject.toml      # Dependencies: fastmcp, crawl4ai, ddgs, httpx, pydantic
├── test_benchmark.py   # Validation tests
├── test_orchestration.py # Orchestration system tests
├── demo_orchestration.py # Live demos
├── .vscode/mcp.json    # VS Code workspace config
├── launch_mcp.sh       # MCP launcher script
└── README.md           # Updated with all features
```

## Software Architecture

### Layer Architecture

DevLens is organized in three distinct layers, following the principle of "Intelligence at Edges":

```
┌─────────────────────────────────────────────────────────────┐
│                      LAYER 3: META                          │
│                  (Intelligence & Guidance)                  │
│                                                             │
│  • suggest_workflow()      - Auto-recommends tool sequences │
│  • classify_intent()       - Detects research patterns      │
│  • get_server_docs()       - Self-documentation             │
│                                                             │
│  Location: src/devlens/utils/orchestrator.py               │
│  Dependencies: Layer 1 tools metadata                       │
│  Purpose: Smart decision-making without execution           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   LAYER 2: COMPOSED                         │
│              (Convenience Combinations)                     │
│                                                             │
│  • deep_dive()            - search + parallel scrape        │
│  • compare_sources()      - multi-scrape + analysis         │
│  • find_related()         - scrape + search + filter        │
│  • monitor_changes()      - scrape + hash comparison        │
│                                                             │
│  Location: src/devlens/tools/research.py                   │
│            src/devlens/tools/advanced.py                    │
│  Dependencies: Layer 1 primitives                           │
│  Purpose: Common workflows as single tools                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   LAYER 1: PRIMITIVES                       │
│              (Simple, Reliable, Fast)                       │
│                                                             │
│  • search_web()           - DuckDuckGo search               │
│  • scrape_url()           - Single page extraction          │
│  • crawl_docs()           - Multi-page following            │
│  • summarize_page()       - Structure extraction            │
│  • extract_links()        - Link categorization             │
│                                                             │
│  Location: src/devlens/tools/search.py                     │
│            src/devlens/tools/scraper.py                     │
│  Dependencies: Adapters only                                │
│  Purpose: Do one thing well, no intelligence                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   ADAPTERS & MODELS                         │
│                  (External Integration)                     │
│                                                             │
│  Adapters:                                                  │
│  • DDGAdapter             - DuckDuckGo API wrapper          │
│  • ScraperAdapter         - Crawl4AI + httpx fallback       │
│                                                             │
│  Models:                                                    │
│  • SearchResult           - Search response schema          │
│  • Document               - Scraped content schema          │
│  • ResearchContext        - Workflow state tracking         │
│  • WebDocxError           - Error hierarchy                 │
│                                                             │
│  Location: src/devlens/adapters/                            │
│            src/devlens/models/                              │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

**Example: User asks "Compare FastAPI vs Flask"**

```
1. MCP Client → devlens.server.py
   ↓
2. FastMCP routes to: tool_suggest_workflow()
   ↓
3. LAYER 3 (orchestrator.py):
   • classify_intent() → "comparison" (65% confidence)
   • build_dynamic_workflow() → [search_web, scrape_url×2, compare_sources]
   • suggest_parameters() → {limit: 5, parallel: true}
   ↓
4. Returns workflow to client (no execution yet)
   ↓
5. Client executes each step:
   ↓
6. LAYER 1: search_web("FastAPI vs Flask", limit=5)
   → DDGAdapter → DuckDuckGo API → [url1, url2, url3, url4, url5]
   ↓
7. LAYER 2: compare_sources(topic, [url1, url2])
   → Calls scrape_url() twice (parallel)
   → ScraperAdapter → Crawl4AI → [doc1, doc2]
   → Analyzes common terms, generates report
   ↓
8. Results flow back to MCP Client → User
```

### Data Flow Architecture

```
┌─────────────┐
│  MCP Client │ (Claude Desktop, VS Code, etc.)
└──────┬──────┘
       │ JSON-RPC over STDIO
       ↓
┌─────────────────────────────────────────────────┐
│              server.py (Entry Point)            │
│                                                 │
│  • Registers 12 tools with FastMCP              │
│  • Handles JSON-RPC protocol                    │
│  • Routes tool calls to implementations         │
│  • Returns structured responses                 │
└──────┬──────────────────────────────────────────┘
       │ Function calls
       ↓
┌─────────────────────────────────────────────────┐
│           Tool Layer (tools/*.py)               │
│                                                 │
│  • Validates input parameters (Pydantic)        │
│  • Coordinates adapter calls                    │
│  • Aggregates results                           │
│  • Formats output as Markdown                   │
└──────┬──────────────────────────────────────────┘
       │ Adapter calls
       ↓
┌─────────────────────────────────────────────────┐
│         Adapter Layer (adapters/*.py)           │
│                                                 │
│  • DDGAdapter: Rate limiting, search execution  │
│  • ScraperAdapter: Retry logic, fallback       │
│  • Converts external formats to internal models │
└──────┬──────────────────────────────────────────┘
       │ HTTP/HTTPS
       ↓
┌─────────────────────────────────────────────────┐
│            External Services                    │
│                                                 │
│  • DuckDuckGo Search API                        │
│  • Web servers (via crawl4ai/httpx)             │
└─────────────────────────────────────────────────┘
```

### State Management

DevLens is **stateless** at the server level - no database, no sessions. However, it tracks ephemeral state through `ResearchContext`:

```python
@dataclass
class ResearchContext:
    """Tracks single research session state"""
    known_urls: List[str]              # Discovered during search
    failed_tools: List[str]            # Tools that errored
    failure_reasons: Dict[str, str]    # Why they failed
    search_attempts: int               # Escalation trigger
    previous_results: Dict[str, Any]   # For multi-step workflows
```

**Flow:**
```
Initial Query
    ↓
ResearchContext() created (empty)
    ↓
suggest_workflow(query, context)
    ↓
Client executes Step 1: search_web()
    ↓
update_context_from_result(context, "search_web", results, success=True)
    → Extracts URLs from results
    → Adds to context.known_urls
    → Increments context.search_attempts
    ↓
Client executes Step 2: scrape_url(context.known_urls[0])
    ↓
If fails: update_context_from_result(context, "scrape_url", None, success=False, error="404")
    → Adds "scrape_url" to context.failed_tools
    → Records context.failure_reasons["scrape_url"] = "404"
    ↓
suggest_workflow(query, updated_context)
    → Sees scrape_url failed with 404
    → Suggests alternative workflow (try different URL or use deep_dive)
```

### Concurrency Model

DevLens uses **asyncio** for I/O-bound operations:

```python
# Primitives are async
async def search_web(query: str) -> list[dict]:
    return await _ddg.search(query)

async def scrape_url(url: str) -> str:
    doc = await _scraper.fetch(url)
    return doc.content

# Composed tools use asyncio.gather for parallelism
async def deep_dive(topic: str, depth: int, parallel: bool):
    if parallel:
        # Fetch all sources concurrently
        tasks = [fetch_source(url) for url in urls]
        results = await asyncio.gather(*tasks)
    else:
        # Sequential fetching
        results = []
        for url in urls:
            results.append(await fetch_source(url))
```

**Parallelism Strategy:**
- `parallel=True` (default): Uses `asyncio.gather()` for concurrent I/O
- `parallel=False`: Sequential execution (useful for rate-limit-sensitive sites)
- Adapter-level concurrency control via rate limiting

### Error Handling Architecture

Three-tier error handling:

```
┌─────────────────────────────────────────────────┐
│         TIER 1: Adapter Level                   │
│                                                 │
│  • Retry with exponential backoff               │
│  • Fallback mechanisms (crawl4ai → httpx)       │
│  • Rate limiting (prevent 429s)                 │
│                                                 │
│  Example: ScraperAdapter retries 3x on timeout  │
└─────────────────────────────────────────────────┘
              ↓ If all retries fail
┌─────────────────────────────────────────────────┐
│         TIER 2: Tool Level                      │
│                                                 │
│  • Catch adapter exceptions                     │
│  • Convert to structured errors (WebDocxError)  │
│  • Return error message as Markdown             │
│                                                 │
│  Example: scrape_url() returns error doc        │
└─────────────────────────────────────────────────┘
              ↓ Error propagated
┌─────────────────────────────────────────────────┐
│         TIER 3: Orchestration Level             │
│                                                 │
│  • Tracks which tools failed (ResearchContext)  │
│  • Records failure reasons                      │
│  • Suggests fallback workflows                  │
│                                                 │
│  Example: If scrape fails, suggest deep_dive    │
└─────────────────────────────────────────────────┘
```

**Error Types:**
```python
WebDocxError (base)
    ├── SearchError(query, reason)
    ├── ScrapingError(url, reason)
    └── CrawlError(root_url, reason)
```

### Caching Strategy

**Intent Classification Cache:**
```python
@lru_cache(maxsize=200)
def _classify_intent_cached(query_lower: str, has_urls: bool, search_attempts: int):
    # Cache key includes context for accuracy
    # Returns immutable tuple for cache compatibility
```

**Why these parameters in cache key?**
- `query_lower`: Same query = same intent
- `has_urls`: Changes workflow (skip search if URLs known)
- `search_attempts`: Escalation logic (attempt 3 needs different approach)

**No caching for:**
- Web requests (always fresh data)
- Tool executions (different each time)
- Context state (ephemeral by design)

### Dependency Injection Pattern

```python
# Adapters are singletons at module level
_ddg = DDGAdapter()
_scraper = ScraperAdapter()

# Tools use shared adapter instances
async def search_web(query: str):
    return await _ddg.search(query)  # Shared instance

async def scrape_url(url: str):
    return await _scraper.fetch(url)  # Shared instance
```

**Why this pattern?**
- Adapter initialization is expensive (browser setup for crawl4ai)
- Rate limiting state must be shared across calls
- Connection pooling benefits from reuse
- Simple: no complex DI framework needed

### MCP Protocol Integration

```
┌──────────────────────────────────────────────┐
│           FastMCP Framework                  │
│                                              │
│  @mcp.tool()                                 │
│  async def tool_search_web(query, limit):    │
│      return await search_web(query, limit)   │
│                                              │
│  • Generates JSON schema from signatures     │
│  • Validates input parameters                │
│  • Handles JSON-RPC over STDIO               │
│  • Serializes responses                      │
└──────────────────────────────────────────────┘
                    ↕ STDIO
┌──────────────────────────────────────────────┐
│              MCP Client                      │
│         (Claude Desktop, etc.)               │
│                                              │
│  tools/list → Get available tools            │
│  tools/call → Execute tool with params       │
│                                              │
└──────────────────────────────────────────────┘
```

**Communication:**
- Transport: STDIO (stdin/stdout)
- Protocol: JSON-RPC 2.0
- Messages: `tools/list`, `tools/call`, responses
- Format: Structured JSON with tool name + parameters

## Performance Characteristics

| Tool | Duration | Cost | Caching |
|------|----------|------|---------|
| `search_web` | Fast (1-2s) | Low | None |
| `scrape_url` | Fast (2-5s) | Low | None |
| `summarize_page` | Fast (1-3s) | Low | None |
| `extract_links` | Fast (1-3s) | Low | None |
| `crawl_docs` | Slow (10-60s) | High | None |
| `deep_dive` | Medium (5-15s) | Medium | None |
| `compare_sources` | Medium (5-20s) | Medium | None |
| `find_related` | Medium (3-8s) | Medium | None |
| `monitor_changes` | Fast (2-5s) | Low | Hash-based |
| `suggest_workflow` | Instant (<50ms) | Minimal | LRU (200 entries) |
| `classify_intent` | Instant (<50ms) | Minimal | LRU (200 entries) |
| `get_server_docs` | Instant (<1ms) | Minimal | In-memory |

## Philosophy in Action

**Example: How "Developer Velocity First" manifests:**
1. **No config files** - Works immediately after `uv sync`
2. **Sensible defaults** - `limit=5`, `depth=3` cover 80% of cases
3. **But everything's tunable** - Power users get full control
4. **Fast feedback** - Errors are immediate and actionable

**Example: How "Composability Over Complexity" manifests:**
1. **Small primitives** - `search_web` just searches
2. **Composed tools** - `deep_dive` = search + parallel scrape + aggregate
3. **User choice** - Manual control OR auto-orchestration
4. **No forced workflows** - Use tools however you want

**Example: How "Intelligence at Edges" manifests:**
1. **Dumb primitives** - `scrape_url` doesn't guess your intent
2. **Smart orchestration** - `suggest_workflow` makes decisions
3. **Reliable core** - Primitives always behave predictably
4. **Adaptive intelligence** - Orchestrator learns from context

This architecture scales from "just scrape this URL" to "research this complex topic across 50 sources" without forcing complexity on simple use cases.