"""Known marketplaces and their domains, including short-link services."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit

__all__ = ["Platform", "PLATFORMS", "detect_platform"]


@dataclass(frozen=True)
class Platform:
    key: str
    name: str
    domains: tuple[str, ...]


PLATFORMS: tuple[Platform, ...] = (
    Platform("poizon", "Poizon (得物)", ("dewu.com", "poizon.com", "dw4.co")),
    Platform("taobao", "Taobao (淘宝)", ("taobao.com", "tb.cn")),
    Platform("tmall", "Tmall (天猫)", ("tmall.com",)),
    Platform("jd", "JD.com (京东)", ("jd.com", "3.cn")),
    Platform("pinduoduo", "Pinduoduo (拼多多)", ("pinduoduo.com", "yangkeduo.com")),
    Platform("xiaohongshu", "Xiaohongshu (小红书)", ("xiaohongshu.com", "xhslink.com")),
    Platform("1688", "1688", ("1688.com",)),
    Platform("xianyu", "Xianyu (闲鱼)", ("goofish.com",)),
    Platform("aliexpress", "AliExpress", ("aliexpress.com",)),
    Platform("alibaba", "Alibaba", ("alibaba.com",)),
    Platform("temu", "Temu", ("temu.com",)),
    Platform("shein", "Shein", ("shein.com",)),
    Platform("dhgate", "DHgate", ("dhgate.com",)),
)

_BY_DOMAIN = {d: p for p in PLATFORMS for d in p.domains}


def _host(url: str) -> str:
    try:
        return (urlsplit(url).hostname or "").lower().rstrip(".")
    except ValueError:
        return ""


def detect_platform(url: str) -> Platform | None:
    """Return the marketplace a URL belongs to, or ``None``.

    Subdomains match only on a dot boundary: ``m.tb.cn`` is Taobao,
    ``notb.cn`` is not.

    >>> detect_platform("https://m.tb.cn/h.5abc").key
    'taobao'
    """
    host = _host(url)
    while host:
        if host in _BY_DOMAIN:
            return _BY_DOMAIN[host]
        _, _, host = host.partition(".")
    return None
