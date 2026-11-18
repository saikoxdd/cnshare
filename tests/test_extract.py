import pytest

from cnshare.extract import find_urls

POIZON = (
    "得物】得物er-1W1U3T9B发现一件好物， 9 CZ0001 å4bnv99eå  https://dw4.co/t/A/HnT1or9oV "
    "Champion T头德训鞋 Champ T-trainer 百搭潮流时尚休闲舒适 低帮 板鞋 男款 牛津绿/奶白, 点击链接直接打开"
)


def test_poizon_share_text():
    assert find_urls(POIZON) == ["https://dw4.co/t/A/HnT1or9oV"]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("https://item.jd.com/100012043978.html", ["https://item.jd.com/100012043978.html"]),
        ("看看 https://m.tb.cn/h.5abc?tk=Xy12，复制本条", ["https://m.tb.cn/h.5abc?tk=Xy12"]),
        ("链接：https://e.tb.cn/h.6aBc「标题」", ["https://e.tb.cn/h.6aBc"]),
        ("ideographic　space https://3.cn/2a-BcD　next", ["https://3.cn/2a-BcD"]),
        ("prose (https://example.com/a).", ["https://example.com/a"]),
        ("http://xhslink.com/a/abc，复制本条信息", ["http://xhslink.com/a/abc"]),
        ("HTTPS://WWW.TAOBAO.COM/item", ["HTTPS://WWW.TAOBAO.COM/item"]),
    ],
)
def test_boundaries(text, expected):
    assert find_urls(text) == expected


def test_several_links_keep_order():
    text = "first https://a.example/1 then https://b.example/2!"
    assert find_urls(text) == ["https://a.example/1", "https://b.example/2"]


@pytest.mark.parametrize("text", ["", "просто текст", "ftp://example.com", "https://"])
def test_nothing_found(text):
    assert find_urls(text) == []
