"""Extract product links from Chinese marketplace share texts."""

from .core import ShareLink, parse, parse_all
from .extract import find_urls
from .platforms import PLATFORMS, Platform, detect_platform

__all__ = ["ShareLink", "parse", "parse_all", "find_urls", "Platform", "PLATFORMS", "detect_platform"]
__version__ = "0.0.1"
