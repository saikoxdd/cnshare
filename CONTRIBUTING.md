# Contributing

Bug reports with a real share text that parsed wrong are the most useful thing you can send. Paste the whole text (you can replace the item id with digits of the same length).

## Setup

```bash
git clone https://github.com/saikoxdd/cnshare
cd cnshare
python -m venv .venv && . .venv/bin/activate
pip install -e . pytest ruff mypy
```

## Before opening a PR

```bash
pytest -q
ruff check . && ruff format --check .
mypy
```

CI runs the same commands on Python 3.10-3.13.

## Adding a platform

1. Add a `Platform` to `PLATFORMS` in `src/cnshare/platforms.py` with every domain its links use (short-link domains too).
2. If its product URLs carry an id, teach `item_id()` and `canonical_url()` in `src/cnshare/items.py`.
3. Add a test with a real-looking share text to `tests/`.
4. Add a row to the table in `README.md` and a line under `Unreleased` in `CHANGELOG.md`.

The library has no runtime dependencies - please keep it that way.
