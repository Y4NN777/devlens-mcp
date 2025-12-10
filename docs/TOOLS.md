# WebDocx MCP - Agents Documentation

This document describes how AI agents and LLMs should interact with WebDocx MCP tools.

---

## Tool Usage Guidelines

### search_web

**Purpose**: Discover relevant sources for a topic.

**When to use**:
- Starting research on a new topic
- Finding documentation URLs
- Looking for tutorials or articles
- Need region-specific results

**New features**:
- **Region support**: Search with localized results (`region="us-en"`, `"uk-en"`, etc.)
- **Quality filtering**: Automatically filters out low-quality results
- **Query normalization**: Cleans up queries for better results
- **Safe search**: Configurable content filtering

**Best practices**:
- Use specific, targeted queries
- Limit results to avoid information overload (default: 5)
- Follow up with `scrape_url` for detailed content
- Use `region` parameter for localized content
- Leverage search operators: `site:`, `"exact phrase"`, `-exclude`

**Example**:
```json
{
  "tool": "search_web",
  "args": {
    "query": "fastapi authentication middleware",
    "limit": 5,
    "region": "us-en",
    "safe_search": true
  }
}
```

---

### scrape_url

**Purpose**: Extract content from a single webpage.

**When to use**:
- Reading documentation pages
- Extracting article content
- Getting detailed information from a known URL

**New features**:
- **Retry mechanism**: Automatic retry with exponential backoff (handles slow/flaky sites)
- **Metadata extraction**: Optional word count, fetch time, line count statistics
- **Better error handling**: Graceful degradation on failures

**Best practices**:
- Verify the URL is accessible before scraping
- Use for authoritative sources (official docs, reputable sites)
- Always attribute the source in your response
- Enable `include_metadata` for analytical insights

**Example**:
```json
{
  "tool": "scrape_url",
  "args": {
    "url": "https://docs.python.org/3/library/asyncio.html",
    "include_metadata": true
  }
}
```

---

### deep_dive

**Purpose**: Comprehensive research on a topic.

**When to use**:
- User asks for thorough research
- Need to synthesize multiple sources
- Building documentation or guides

**New features**:
- **Parallel fetching**: Scrapes multiple sources concurrently for 3x faster results
- **Domain diversity**: Ensures results from different domains for broader perspective
- **Better reporting**: Shows successful vs failed fetches with progress tracking

**Best practices**:
- Set appropriate depth (1-3 for quick research, 4-5 for comprehensive)
- Review all sources for accuracy
- Synthesize, don't just concatenate
- Use `parallel=True` (default) for faster research

**Example**:
```json
{
  "tool": "deep_dive",
  "args": {
    "topic": "Python type hints best practices",
    "depth": 3,
    "parallel": true
  }
}
```

---

### crawl_docs

**Purpose**: Ingest multi-page documentation.

**When to use**:
- Learning a new framework or library
- Building a local knowledge base
- Comprehensive documentation review

**New features**:
- **Smart link filtering**: Skips login, signup, download, PDF links automatically
- **Documentation prioritization**: Prioritizes URLs with "doc", "guide", "tutorial" in path
- **Anchor-friendly TOC**: Proper markdown anchors for navigation
- **Domain restriction**: Configurable external link following

**Best practices**:
- Start with the documentation root URL
- Limit pages to avoid excessive crawling
- Use for same-domain content only (default behavior)
- Set `follow_external=False` to stay within documentation site

**Example**:
```json
{
  "tool": "crawl_docs",
  "args": {
    "root_url": "https://fastapi.tiangolo.com/",
    "max_pages": 10,
    "follow_external": false
  }
}
```

---

### summarize_page

**Purpose**: Quick overview without full content.

**When to use**:
- Triaging multiple pages
- Deciding if full scrape is needed
- Getting page structure quickly

**Best practices**:
- Use before `scrape_url` to check relevance
- Good for long articles or documentation
- Follow up with full scrape if content is relevant

**Example**:
```json
{
  "tool": "summarize_page",
  "args": {
    "url": "https://blog.example.com/long-article"
  }
}
```

---

### compare_sources

**Purpose**: Compare information across multiple sources to identify similarities and differences.

**When to use**:
- Comparing different perspectives on a topic
- Finding consensus or disagreements between sources
- Analyzing multiple implementations or approaches

**Features**:
- Identifies common topics across all sources
- Shows term frequency across sources
- Provides excerpts from each source
- Generates comparative analysis

**Best practices**:
- Use 2-5 sources for meaningful comparison
- Choose sources with different perspectives
- Review the common topics section for consensus points

**Example**:
```json
{
  "tool": "compare_sources",
  "args": {
    "topic": "Python async best practices",
    "sources": [
      "https://realpython.com/async-io-python/",
      "https://docs.python.org/3/library/asyncio.html"
    ]
  }
}
```

---

### find_related

**Purpose**: Discover pages related to a given URL.

**When to use**:
- Finding similar resources
- Exploring a topic more broadly
- Discovering alternative sources

**Features**:
- Analyzes page content to understand topic
- Searches for related resources
- Filters out the original URL
- Returns top related pages with descriptions

**Best practices**:
- Use after finding a good initial resource
- Review all recommendations for relevance
- Follow up with `scrape_url` on promising links

**Example**:
```json
{
  "tool": "find_related",
  "args": {
    "url": "https://docs.python.org/3/library/asyncio.html",
    "limit": 5
  }
}
```

---

### extract_links

**Purpose**: Extract and categorize all links from a page.

**When to use**:
- Understanding site structure
- Finding navigation patterns
- Discovering related resources
- Building a sitemap

**Features**:
- Separates internal vs external links
- Deduplicates links
- Shows link text for context
- Configurable external link filtering

**Best practices**:
- Use `filter_external=True` for internal navigation
- Review link text for relevance
- Use for site exploration before crawling

**Example**:
```json
{
  "tool": "extract_links",
  "args": {
    "url": "https://fastapi.tiangolo.com/",
    "filter_external": true
  }
}
```

---

### monitor_changes

**Purpose**: Track content changes on a webpage over time.

**When to use**:
- Monitoring documentation updates
- Tracking blog posts or news
- Detecting content modifications

**Features**:
- Generates content hash for comparison
- Detects changes from previous check
- Provides content preview
- Timestamps for change tracking

**Best practices**:
- Store returned hash for next comparison
- Check periodically for updates
- Use for critical documentation or references

**Example**:
```json
{
  "tool": "monitor_changes",
  "args": {
    "url": "https://example.com/docs",
    "previous_hash": "a1b2c3d4..."
  }
}
```

---

## Workflow Patterns

### Research Workflow
1. `search_web` — Find relevant sources
2. `summarize_page` — Triage results
3. `scrape_url` — Get full content from relevant pages
4. Synthesize and respond with attribution

### Documentation Learning Workflow
1. `crawl_docs` — Ingest documentation
2. Parse and understand structure
3. Answer questions from gathered context

### Quick Answer Workflow
1. `search_web` — Find top result
2. `scrape_url` — Get content
3. Extract answer with source citation

---

## Response Guidelines

### Always Include
- Source URLs for all cited information
- Clear attribution when quoting
- Structured Markdown formatting

### Avoid
- Presenting scraped content as your own knowledge
- Making claims without source backing
- Overloading context with unnecessary content

---

## Error Handling

| Error | Recommended Action |
|-------|-------------------|
| URL not accessible | Try alternative sources via `search_web` |
| Timeout | Retry once, then report to user |
| No results | Broaden search query or suggest alternatives |
| Rate limited | Wait and retry, or use cached content |
