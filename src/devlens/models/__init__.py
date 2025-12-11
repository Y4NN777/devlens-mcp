"""WebDocx models package."""

from devlens.models.search import SearchResult, SearchQuery
from devlens.models.document import Document, PageSummary, Section
from devlens.models.errors import WebDocxError, SearchError, ScrapingError, CrawlError

__all__ = [
    "SearchResult",
    "SearchQuery",
    "Document",
    "PageSummary",
    "Section",
    "WebDocxError",
    "SearchError",
    "ScrapingError",
    "CrawlError",
]
