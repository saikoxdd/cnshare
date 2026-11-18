"""Finding URLs inside share texts.

Share texts from Chinese apps glue the link to Chinese text and full-width
punctuation, e.g. ``"…好物， https://dw4.co/t/A/xxx Название, 点击链接直接打开"``.
A link ends at whitespace or at punctuation that never occurs inside these URLs.
"""

from __future__ import annotations

import re

__all__ = ["find_urls"]

# Characters that terminate a URL inside a share text: whitespace (including the
# ideographic space U+3000 and NBSP), full-width punctuation and quotes.
_STOP = r"\s 　，。、；：！？「」【】『』（）《》“”‘’\"'<>"
_URL_RE = re.compile(rf"https?://[^{_STOP}]+", re.IGNORECASE)

# Half-width punctuation that sticks to the end of a link in normal prose.
_TRAILING = ".,;:!?)]}"


def find_urls(text: str) -> list[str]:
    """Return every http(s) URL found in ``text``, in order of appearance.

    Trailing ASCII punctuation (``.,;:!?)]}``) is stripped, duplicates are kept.

    >>> find_urls("【得物】好物， https://dw4.co/t/A/HnT1or9oV 球鞋, 点击链接直接打开")
    ['https://dw4.co/t/A/HnT1or9oV']
    """
    if not text:
        return []
    return [m.rstrip(_TRAILING) for m in _URL_RE.findall(text) if m.rstrip(_TRAILING)]
