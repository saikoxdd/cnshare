# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-18

### Added

- `find_urls()` pulls URLs out of share text, stopping at whitespace, full-width spaces and full-width punctuation.
- `detect_platform()` and `PLATFORMS`: Poizon, Taobao, Tmall, JD, Pinduoduo, Xiaohongshu, 1688, Xianyu, AliExpress, Alibaba, Temu, Shein, DHgate.
- `parse()` / `parse_all()` return `ShareLink` objects with the platform and the product title found in the text.
- `ShareLink.item_id` and `ShareLink.canonical_url` for Taobao, Tmall, JD, Pinduoduo, 1688 and Poizon links.
- `cnshare` command line tool with JSON output, `--all` and `--url-only`.
- Type hints (`py.typed`), strict mypy, CI on Python 3.10-3.13.

[Unreleased]: https://github.com/saikoxdd/cnshare/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/saikoxdd/cnshare/releases/tag/v0.1.0
