"""High-level API: turn a pasted share text into a product link."""

from __future__ import annotations

from dataclasses import dataclass

from .extract import find_urls
from .platforms import Platform, detect_platform
from .title import extract_title

__all__ = ["ShareLink", "parse", "parse_all"]


@dataclass(frozen=True)
class ShareLink:
    """A product link found in a share text."""

    url: str
    platform: Platform | None
    title: str | None = None

    @property
    def is_known(self) -> bool:
        return self.platform is not None


def _normalize(url: str, platform: Platform | None) -> str:
    # Xiaohongshu and some others share http:// links. For a known marketplace the
    # HTTPS form is the same page, and many forms accept only HTTPS.
    if platform is not None and url[:7].lower() == "http://":
        return "https://" + url[7:]
    return url


def parse_all(text: str) -> list[ShareLink]:
    """Every link in the text, in order, with its platform (``None`` if unknown)."""
    links = []
    for url in find_urls(text):
        platform = detect_platform(url)
        links.append(ShareLink(_normalize(url, platform), platform, extract_title(text, url)))
    return links


def parse(text: str) -> ShareLink | None:
    """The product link from a share text.

    The first link of a known marketplace wins over other links in the text;
    if none is known, the first link is returned; ``None`` if there are no links.

    >>> link = parse("【得物】好物， https://dw4.co/t/A/HnT1or9oV 球鞋, 点击链接直接打开")
    >>> link.url, link.platform.key
    ('https://dw4.co/t/A/HnT1or9oV', 'poizon')
    """
    links = parse_all(text)
    for link in links:
        if link.is_known:
            return link
    return links[0] if links else None
