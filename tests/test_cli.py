import io
import json

import pytest

from cnshare.cli import main

TAOBAO = "【淘宝】 https://e.tb.cn/h.6aBcDeF?tk=AbCd1234 「Nike耐克官方男子运动鞋AIR MAX」点击链接直接打开"


def test_json(capsys):
    assert main([TAOBAO]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["url"] == "https://e.tb.cn/h.6aBcDeF?tk=AbCd1234"
    assert out["platform"] == "taobao"
    assert out["title"] == "Nike耐克官方男子运动鞋AIR MAX"


def test_url_only(capsys):
    assert main(["-u", TAOBAO]) == 0
    assert capsys.readouterr().out == "https://e.tb.cn/h.6aBcDeF?tk=AbCd1234\n"


def test_all(capsys):
    assert main(["--all", "https://3.cn/1 и https://example.com/x"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert [o["platform"] for o in out] == ["jd", None]


def test_stdin(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO(TAOBAO))
    assert main(["-u"]) == 0
    assert "e.tb.cn" in capsys.readouterr().out


def test_nothing(capsys):
    assert main(["нет ссылки"]) == 1
    assert "no link" in capsys.readouterr().err


def test_version(capsys):
    with pytest.raises(SystemExit):
        main(["--version"])
    assert "cnshare" in capsys.readouterr().out
