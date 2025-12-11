"""WebDocx tools package."""

from devlens.tools.search import search_web
from devlens.tools.scraper import scrape_url, crawl_docs
from devlens.tools.research import deep_dive, summarize_page

__all__ = [
    "search_web",
    "scrape_url",
    "crawl_docs",
    "deep_dive",
    "summarize_page",
]
