"""Extract product links from Chinese marketplace share texts."""

from .core import ShareLink, parse, parse_all
from .extract import find_urls
from .platforms import PLATFORMS, Platform, detect_platform

__all__ = ["PLATFORMS", "Platform", "ShareLink", "detect_platform", "find_urls", "parse", "parse_all"]
__version__ = "0.0.1"
