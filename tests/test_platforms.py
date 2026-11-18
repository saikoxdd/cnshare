import pytest

from cnshare.platforms import PLATFORMS, detect_platform


@pytest.mark.parametrize(
    "url, key",
    [
        ("https://dw4.co/t/A/HnT1or9oV", "poizon"),
        ("https://m.dewu.com/router/product/ProductDetail?spuId=1", "poizon"),
        ("https://m.tb.cn/h.5abc?tk=Xy12", "taobao"),
        ("https://e.tb.cn/h.6aBc", "taobao"),
        ("https://item.taobao.com/item.htm?id=123", "taobao"),
        ("https://detail.tmall.com/item.htm?id=456", "tmall"),
        ("https://item.jd.com/100012043978.html", "jd"),
        ("https://3.cn/2a-BcD", "jd"),
        ("https://mobile.yangkeduo.com/goods.html?goods_id=1", "pinduoduo"),
        ("http://xhslink.com/a/abc", "xiaohongshu"),
        ("https://detail.1688.com/offer/1.html", "1688"),
        ("https://www.goofish.com/item?id=1", "xianyu"),
        ("HTTPS://WWW.TAOBAO.COM./item", "taobao"),
    ],
)
def test_detect(url, key):
    assert detect_platform(url).key == key


@pytest.mark.parametrize(
    "url",
    [
        "https://notb.cn/x",
        "https://taobao.com.evil.example/x",
        "https://example.com",
        "not a url",
        "",
        "http://[::1",
    ],
)
def test_unknown(url):
    assert detect_platform(url) is None


def test_domains_are_unique():
    domains = [d for p in PLATFORMS for d in p.domains]
    assert len(domains) == len(set(domains))
