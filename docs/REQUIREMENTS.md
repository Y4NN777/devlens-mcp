# WebDocx MCP - Requirements

## Goal
An MCP server that gives LLMs real-time web access for gathering documentation or article, blog post, or any other web content without leaving your workspace: search, scrape, crawl documentation, and synthesize content with source attribution.

## Tools (12 total)

### Primitives (5)
| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `search_web` | Discover sources | query, limit, region | List of {title, url, snippet} |
| `scrape_url` | Read single page | url | Markdown with source header |
| `crawl_docs` | Ingest multi-page docs | root_url, max_pages | Combined Markdown with ToC |
| `summarize_page` | Quick overview | url | Headers + key points outline |
| `extract_links` | Categorize links | url, filter_external | Internal/external link lists |

### Composed (4)
| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `deep_dive` | Research a topic | topic, depth | Aggregated report with sources |
| `compare_sources` | Analyze differences | topic, sources | Comparison report |
| `find_related` | Discover similar pages | url, limit | Related page list |
| `monitor_changes` | Track updates | url, previous_hash | Change detection report |

### Meta (3)
| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `suggest_workflow` | Auto-recommend workflow | query, known_urls | Intent + workflow steps |
| `classify_research_intent` | Detect research goal | query | Intent classification |
| `get_server_docs` | Inline documentation | topic | Formatted docs |

## Output Contract
- Every response includes source URL(s)
- Content returned as clean Markdown
- Errors return structured messages, not crashes

## Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| **Protocol** | `mcp` (official SDK) | Standard compliance |
| **Server Framework** | `fastmcp` | Pythonic, handles JSON-RPC boilerplate |
| **Search** | `duckduckgo-search` | Free, no API key |
| **Scraping** | `crawl4ai` | AI-optimized, handles JS, outputs Markdown |
| **Fallback Scraping** | `httpx` + `beautifulsoup4` + `readability-lxml` | For simple static pages |
| **Async** | `asyncio` | Concurrent fetching |
| **Validation** | `pydantic` | Strict input/output schemas |

## V1 Scope (Current - All Completed ✅)

### Core Tools (9)
1. `search_web` - ✅ working with region support
2. `scrape_url` - ✅ working with retry + metadata
3. `deep_dive` - ✅ working with parallel fetching
4. `crawl_docs` - ✅ smart filtering + TOC
5. `summarize_page` - ✅ extract headers
6. `compare_sources` - ✅ multi-source analysis
7. `find_related` - ✅ content-based discovery
8. `extract_links` - ✅ link categorization
9. `monitor_changes` - ✅ content hashing

### Smart Orchestration (3)
10. `suggest_workflow` - ✅ smart orchestration with intent classification
11. `classify_research_intent` - ✅ 7 research patterns with confidence
12. `get_server_docs` - ✅ inline documentation system

**V1 Key Features:**
- Smart orchestration with @lru_cache for performance
- Context tracking (known_urls, failed_tools, failure_reasons)
- Dynamic workflow generation based on intent
- Parameter optimization per research goal
- Developer-first design philosophy
- Token-optimized Markdown output
- Fail-fast error handling

## Out of Scope (V2)
- PDF parsing
- Authentication/login pages
- Proxy rotation
- Real-time streaming results
