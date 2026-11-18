"""Inputs that should never crash the parser."""

import random
import string

import pytest

from cnshare import find_urls, parse, parse_all

WEIRD = [
    "",
    " ",
    "\n\n\t",
    "http://",
    "https://",
    "https:// space",
    "【】",
    "「",
    "』",
    "https://" + "a" * 5000,
    "点击链接" * 200,
    "\x00\x01\x02",
    "https://dw4.co/t/A/" + "　",
    "😀" * 100 + " https://m.tb.cn/h.abc 😀",
]


@pytest.mark.parametrize("text", WEIRD)
def test_weird_input_does_not_crash(text: str) -> None:
    links = parse_all(text)
    assert isinstance(links, list)
    first = parse(text)
    assert first is None or first.url.startswith("https://") or first.url.startswith("http://")


def test_random_noise_does_not_crash() -> None:
    rng = random.Random(1234)
    alphabet = string.printable + "得物淘宝【】「」，。！？：　 "
    for _ in range(500):
        text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 200)))
        for link in parse_all(text):
            assert link.url in text or link.url.replace("https://", "http://", 1) in text
            _ = link.item_id, link.canonical_url, link.title


def test_urls_never_contain_whitespace() -> None:
    rng = random.Random(42)
    for _ in range(200):
        pad = "".join(rng.choice(" \t\n　 ，。") for _ in range(3))
        text = f"x{pad}https://item.taobao.com/item.htm?id={rng.randint(1, 10**12)}{pad}y"
        (url,) = find_urls(text)
        assert not any(ch.isspace() for ch in url)
        assert "，" not in url and "。" not in url
