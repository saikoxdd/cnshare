"""Extract product links from Chinese marketplace share texts."""

from .core import ShareLink, parse, parse_all
from .extract import find_urls
from .items import canonical_url, item_id
from .platforms import PLATFORMS, Platform, detect_platform

__all__ = [
    "PLATFORMS",
    "Platform",
    "ShareLink",
    "canonical_url",
    "detect_platform",
    "find_urls",
    "item_id",
    "parse",
    "parse_all",
]
__version__ = "0.0.1"
