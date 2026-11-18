"""Guessing the product title from a share text."""

from __future__ import annotations

import re

__all__ = ["extract_title"]

# Taobao / JD / Tmall put the title in corner brackets: 「Nike Air Max」
_BRACKETS = re.compile(r"[「『]([^」』]{2,300})[」』]")
# Where the app's boilerplate starts after the title.
_TAIL = re.compile(r"[,，]?\s*(?:点击链接|點擊鏈接|复制|複製|打开|打開|【|https?://)")
_EDGES = " \t\r\n 　,，:：;；-–—|"
_HAS_WORD = re.compile(r"\w\w")


def _clean(title: str, limit: int) -> str | None:
    title = re.sub(r"\s+", " ", title).strip(_EDGES)
    title = "".join(list(title)[:limit]).rstrip(_EDGES)
    return title if _HAS_WORD.search(title) else None


def extract_title(text: str, url: str, limit: int = 300) -> str | None:
    """Product title from the text around ``url`` (as it appears in ``text``).

    Corner brackets win; otherwise the text right after the link up to the app's
    "click the link" boilerplate. ``limit`` is in characters.

    >>> extract_title("https://dw4.co/t/A/x Champion T-trainer 牛津绿, 点击链接直接打开", "https://dw4.co/t/A/x")
    'Champion T-trainer 牛津绿'
    """
    if not text:
        return None
    m = _BRACKETS.search(text)
    if m:
        return _clean(m.group(1), limit)
    pos = text.find(url)
    if pos < 0:
        return None
    after = text[pos + len(url):]
    return _clean(_TAIL.split(after, maxsplit=1)[0], limit)
