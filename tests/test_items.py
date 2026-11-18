import pytest

from cnshare import parse
from cnshare.items import canonical_url, item_id


@pytest.mark.parametrize(
    "url, pid",
    [
        ("https://item.taobao.com/item.htm?spm=a1z10&id=640123456789", "640123456789"),
        ("https://detail.tmall.com/item.htm?id=1234567&skuId=9", "1234567"),
        ("https://item.jd.com/100012043978.html", "100012043978"),
        ("https://item.m.jd.com/product/100012043978.html?wxa_abtest=o", "100012043978"),
        ("https://mobile.yangkeduo.com/goods.html?goods_id=987654&page_from=23", "987654"),
        ("https://detail.1688.com/offer/612345678901.html?spm=a26352", "612345678901"),
        ("https://m.dewu.com/router/product/ProductDetail?spuId=1234567", "1234567"),
    ],
)
def test_item_id(url, pid):
    assert item_id(url) == pid


@pytest.mark.parametrize(
    "url",
    [
        "https://m.tb.cn/h.5abc?tk=Xy12",  # short link: id is behind a redirect
        "https://3.cn/2a-BcD",
        "https://dw4.co/t/A/HnT1or9oV",
        "https://item.taobao.com/item.htm?id=abc",  # not numeric
        "https://shop123.taobao.com/",
        "https://example.com/item.htm?id=1",
    ],
)
def test_no_item_id(url):
    assert item_id(url) is None


def test_canonical_strips_tracking():
    assert canonical_url("https://item.jd.com/100012043978.html?cu=true&utm_source=x") == (
        "https://item.jd.com/100012043978.html"
    )
    assert canonical_url("https://mobile.yangkeduo.com/goods.html?goods_id=987654&refer_page=x") == (
        "https://mobile.yangkeduo.com/goods.html?goods_id=987654"
    )


def test_canonical_none_for_short_links():
    assert canonical_url("https://m.tb.cn/h.5abc") is None


def test_sharelink_properties():
    link = parse("看看这个 https://item.taobao.com/item.htm?id=640123456789&spm=x 好物")
    assert link.item_id == "640123456789"
    assert link.canonical_url == "https://item.taobao.com/item.htm?id=640123456789"
