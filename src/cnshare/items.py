"""Product IDs and canonical URLs for full (non-short) marketplace links.

Short links (``m.tb.cn``, ``3.cn``, ``dw4.co`` …) hide the ID behind a redirect;
this library never follows links, so for them both functions return ``None``.
"""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlsplit

from .platforms import detect_platform

__all__ = ["canonical_url", "item_id"]

_JD_PATH = re.compile(r"^/(?:product/)?(\d{4,})\.html$")
_1688_PATH = re.compile(r"^/offer/(\d{4,})\.html$")


def _query(url: str) -> dict[str, list[str]]:
    return parse_qs(urlsplit(url).query)


def item_id(url: str) -> str | None:
    """Marketplace product ID from a full product URL.

    >>> item_id("https://item.taobao.com/item.htm?spm=a1z10&id=640123456789")
    '640123456789'
    >>> item_id("https://item.m.jd.com/product/100012043978.html")
    '100012043978'
    """
    platform = detect_platform(url)
    if platform is None:
        return None
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    q = _query(url)

    def first(*keys: str) -> str | None:
        for k in keys:
            v = q.get(k)
            if v and v[0].isdigit():
                return v[0]
        return None

    if platform.key in ("taobao", "tmall") and parts.path.endswith("item.htm"):
        return first("id")
    if platform.key == "jd" and host.endswith("jd.com"):
        m = _JD_PATH.match(parts.path)
        return m.group(1) if m else None
    if platform.key == "pinduoduo":
        return first("goods_id")
    if platform.key == "1688":
        m = _1688_PATH.match(parts.path)
        return m.group(1) if m else None
    if platform.key == "poizon":
        return first("spuId", "productId")
    return None


_CANONICAL = {
    "taobao": "https://item.taobao.com/item.htm?id={}",
    "tmall": "https://detail.tmall.com/item.htm?id={}",
    "jd": "https://item.jd.com/{}.html",
    "pinduoduo": "https://mobile.yangkeduo.com/goods.html?goods_id={}",
    "1688": "https://detail.1688.com/offer/{}.html",
}


def canonical_url(url: str) -> str | None:
    """A clean product URL without tracking parameters, when the ID is known.

    >>> canonical_url("https://detail.tmall.com/item.htm?id=1234567&spm=a220o&skuId=9")
    'https://detail.tmall.com/item.htm?id=1234567'
    """
    platform = detect_platform(url)
    pid = item_id(url)
    if platform is None or pid is None or platform.key not in _CANONICAL:
        return None
    return _CANONICAL[platform.key].format(pid)
