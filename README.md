# cnshare

[![ci](https://github.com/saikoxdd/cnshare/actions/workflows/ci.yml/badge.svg)](https://github.com/saikoxdd/cnshare/actions/workflows/ci.yml)
![python](https://img.shields.io/badge/python-3.10%E2%80%933.13-c4b5fd)
![deps](https://img.shields.io/badge/dependencies-0-c4b5fd)
![license](https://img.shields.io/badge/license-MIT-c4b5fd)

Chinese marketplace apps don't share a link, they share a paragraph:

```
【得物】得物er-1W1U3T9B发现一件好物， 9 CZ0001 https://dw4.co/t/A/HnT1or9oV Champion T-trainer 牛津绿/奶白, 点击链接直接打开
```

Paste that into an `<input type="url">` and it fails; grab `\S+` and you get `奶白,` glued to the URL.
**cnshare** turns it into a clean link, the marketplace and the product title. No dependencies, no network calls.

```python
>>> from cnshare import parse
>>> link = parse("【得物】好物， https://dw4.co/t/A/HnT1or9oV Champion T-trainer 牛津绿/奶白, 点击链接直接打开")
>>> link.url
'https://dw4.co/t/A/HnT1or9oV'
>>> link.platform.name
'Poizon (得物)'
>>> link.title
'Champion T-trainer 牛津绿/奶白'

```

Built for order forms of delivery services from China, where customers paste whatever the app gave them.

## Install

```bash
pip install git+https://github.com/saikoxdd/cnshare
```

## What it understands

| Platform | Domains |
|---|---|
| Poizon / 得物 | `dewu.com`, `poizon.com`, `dw4.co` |
| Taobao / 淘宝 | `taobao.com`, `tb.cn` (`m.tb.cn`, `e.tb.cn`) |
| Tmall / 天猫 | `tmall.com` |
| JD / 京东 | `jd.com`, `3.cn` |
| Pinduoduo / 拼多多 | `pinduoduo.com`, `yangkeduo.com` |
| Xiaohongshu / 小红书 | `xiaohongshu.com`, `xhslink.com` |
| 1688, Xianyu / 闲鱼, AliExpress, Alibaba, Temu, Shein, DHgate | their main domains |

- **Links** end at whitespace or full-width punctuation (`，。「」【】…`); trailing `.,;:!?)` is stripped
- **The product link wins**: the first link of a known marketplace is returned even if another link comes first
- **`http://` → `https://`** for known marketplaces (Xiaohongshu shares http links)
- **Title**: from `「…」` (Taobao, JD) or the text right after the link up to `点击链接…`
- **Product ID and clean URL** for full links of Taobao, Tmall, JD, Pinduoduo, 1688 and Poizon

## API

```python
from cnshare import parse, parse_all, find_urls, detect_platform, item_id, canonical_url

parse(text)          # ShareLink | None - the product link
parse_all(text)      # list[ShareLink] - every link, in order
find_urls(text)      # list[str] - raw URLs only

link.url             # 'https://item.taobao.com/item.htm?id=640123456789&spm=a1z10'
link.platform        # Platform(key='taobao', name='Taobao (淘宝)', domains=(...))
link.title           # 'Nike耐克官方男子运动鞋AIR MAX' or None
link.item_id         # '640123456789' (None for short links)
link.canonical_url   # 'https://item.taobao.com/item.htm?id=640123456789'
```

Short links (`m.tb.cn`, `3.cn`, `dw4.co`, `xhslink.com`) hide the product ID behind a redirect.
cnshare never opens links, so `item_id` is `None` for them - resolve redirects yourself if you need it,
with the usual SSRF precautions.

## Command line

```bash
$ cnshare "【淘宝】 https://e.tb.cn/h.6aBcDeF?tk=AbCd1234 「Nike耐克官方男子运动鞋AIR MAX」点击链接直接打开"
{
  "url": "https://e.tb.cn/h.6aBcDeF?tk=AbCd1234",
  "platform": "taobao",
  "platform_name": "Taobao (淘宝)",
  "title": "Nike耐克官方男子运动鞋AIR MAX",
  "item_id": null,
  "canonical_url": null
}

$ pbpaste | cnshare -u        # just the URL
$ cnshare --all "…"           # every link in the text
```

## Development

```bash
pip install -e . pytest ruff mypy
pytest && ruff check . && mypy
```

## License

MIT
