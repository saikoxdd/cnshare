"""A minimal aiogram 3 bot that answers a pasted share text with the parsed link.

    pip install aiogram cnshare
    BOT_TOKEN=... python examples/aiogram_bot.py

Send it something copied from Poizon or Taobao and it replies with the
platform, the clean URL and the product title.
"""

import asyncio
import os
from html import escape

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

from cnshare import parse

dp = Dispatcher()


def describe(text: str) -> str | None:
    """Turn share text into a reply, or None if there is no link."""
    link = parse(text)
    if link is None:
        return None
    lines = [f"<b>{escape(link.platform.name if link.platform else 'Unknown shop')}</b>"]
    if link.title:
        lines.append(escape(link.title))
    lines.append(escape(link.canonical_url or link.url))
    return "\n".join(lines)


@dp.message(F.text)
async def on_text(message: Message) -> None:
    reply = describe(message.text or "")
    await message.answer(reply or "No link found - paste the whole share text.")


async def main() -> None:
    bot = Bot(os.environ["BOT_TOKEN"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
