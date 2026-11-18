"""Command line: ``cnshare "share text"`` or ``pbpaste | cnshare``."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from . import __version__
from .core import ShareLink, parse, parse_all


def _as_dict(link: ShareLink) -> dict[str, str | None]:
    return {
        "url": link.url,
        "platform": link.platform.key if link.platform else None,
        "platform_name": link.platform.name if link.platform else None,
        "title": link.title,
        "item_id": link.item_id,
        "canonical_url": link.canonical_url,
    }


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="cnshare",
        description="Extract the product link from a Chinese marketplace share text.",
    )
    ap.add_argument("text", nargs="*", help="share text; read from stdin when omitted")
    ap.add_argument("-a", "--all", action="store_true", help="print every link, not only the product")
    ap.add_argument("-u", "--url-only", action="store_true", help="print just the URL(s)")
    ap.add_argument("-V", "--version", action="version", version=f"cnshare {__version__}")
    args = ap.parse_args(argv)

    text = " ".join(args.text) if args.text else sys.stdin.read()
    if args.all:
        links = parse_all(text)
    else:
        link = parse(text)
        links = [link] if link else []
    if not links:
        print("no link found", file=sys.stderr)
        return 1

    if args.url_only:
        for link in links:
            print(link.url)
    else:
        data = [_as_dict(link) for link in links]
        print(json.dumps(data if args.all else data[0], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
