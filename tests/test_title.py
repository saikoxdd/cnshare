import pytest

from cnshare import parse
from cnshare.title import extract_title

POIZON = (
    "得物】得物er-1W1U3T9B发现一件好物， 9 CZ0001 å4bnv99eå  https://dw4.co/t/A/HnT1or9oV "
    "Champion T头德训鞋 Champ T-trainer 百搭潮流时尚休闲舒适 低帮 板鞋 男款 牛津绿/奶白, 点击链接直接打开"
)
TAOBAO = "【淘宝】7天无理由退货 https://e.tb.cn/h.6aBcDeF?tk=AbCd1234 CZ3457 「Nike耐克官方男子运动鞋AIR MAX」点击链接直接打开 或者 淘宝搜索直接打开"
JD = "【京东】https://3.cn/2a-BcDeF「Apple iPhone 17 Pro 256GB」点击链接直接打开"
XHS = "86 小红书 发布了一篇小红书笔记，快来看吧！ 😆 Xyz123 😆 http://xhslink.com/a/abc，复制本条信息，打开【小红书】App查看精彩内容！"


def test_poizon_title_after_link():
    assert (
        parse(POIZON).title
        == "Champion T头德训鞋 Champ T-trainer 百搭潮流时尚休闲舒适 低帮 板鞋 男款 牛津绿/奶白"
    )


def test_taobao_brackets():
    assert parse(TAOBAO).title == "Nike耐克官方男子运动鞋AIR MAX"


def test_jd_brackets():
    assert parse(JD).title == "Apple iPhone 17 Pro 256GB"


def test_xiaohongshu_has_no_title():
    assert parse(XHS).title is None


def test_plain_link_has_no_title():
    assert parse("https://item.jd.com/1.html").title is None


@pytest.mark.parametrize("limit", [5, 10])
def test_limit_counts_characters(limit):
    title = extract_title("https://a.example/x " + "德训鞋" * 50, "https://a.example/x", limit=limit)
    assert len(title) == limit


def test_url_not_in_text():
    assert extract_title("text", "https://nowhere.example") is None
