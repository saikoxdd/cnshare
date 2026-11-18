from cnshare import ShareLink, parse, parse_all

POIZON = (
    "得物】得物er-1W1U3T9B发现一件好物， 9 CZ0001 å4bnv99eå  https://dw4.co/t/A/HnT1or9oV "
    "Champion T头德训鞋 Champ T-trainer 百搭潮流时尚休闲舒适 低帮 板鞋 男款 牛津绿/奶白, 点击链接直接打开"
)
XHS = "86 小红书 发布了一篇小红书笔记，快来看吧！ 😆 Xyz123 😆 http://xhslink.com/a/abc，复制本条信息，打开【小红书】App查看精彩内容！"


def test_poizon():
    link = parse(POIZON)
    assert isinstance(link, ShareLink)
    assert link.url == "https://dw4.co/t/A/HnT1or9oV"
    assert link.platform.key == "poizon"


def test_http_upgraded_for_known_shop():
    link = parse(XHS)
    assert link.url == "https://xhslink.com/a/abc"
    assert link.platform.key == "xiaohongshu"


def test_http_kept_for_unknown_site():
    assert parse("see http://example.com/x").url == "http://example.com/x"


def test_known_shop_wins_over_earlier_link():
    text = "guide https://bit.ly/x then https://item.jd.com/1.html"
    assert parse(text).url == "https://item.jd.com/1.html"


def test_unknown_only():
    link = parse("https://example.com/a")
    assert link.url == "https://example.com/a" and not link.is_known


def test_no_links():
    assert parse("нет ссылки") is None
    assert parse_all("") == []


def test_parse_all_keeps_order():
    links = parse_all("https://m.tb.cn/h.1 и https://3.cn/2")
    assert [l.platform.key for l in links] == ["taobao", "jd"]
