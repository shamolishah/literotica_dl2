from __future__ import annotations

import logging
import re
from datetime import timedelta
from enum import Enum
from pathlib import Path

import requests_cache
from fake_useragent import UserAgent

log = logging.getLogger("literotica_dl.downloader_utils")


def get_sane_filename(title: str) -> str:
    keep_characters = (" ", "_")  # Only these special chars allowed
    return "".join(c for c in title if c.isalnum() or c in keep_characters).rstrip()


def get_url_from_literotica(url: str) -> bytes:
    session = requests_cache.CachedSession("literotica_cache.sqlite", expire_after=timedelta(hours=1))

    ua = UserAgent().chrome
    header = {"User-Agent": ua}
    log.info("Fetching From Literotica: %s", url)
    page = session.get(url, headers=header, timeout=10)
    return page.content


def parse_story_series(url: str) -> str:
    series_url_matcher = re.compile(r".+series\/se\/(.+)")
    return series_url_matcher.match(url).groups()[0]


def parse_story_url(url: str) -> str:
    series_url_matcher = re.compile(r".+\/s\/(.+)")
    return series_url_matcher.match(url).groups()[0]


def save_story_pre(base_folder: str, story, extra_folder: str | None) -> Path:
    if extra_folder is not None:
        dst_path = Path(base_folder) / get_sane_filename(story.author) / get_sane_filename(extra_folder)
    else:
        dst_path = Path(base_folder) / get_sane_filename(story.author)
    dst_path.mkdir(exist_ok=True, parents=True)
    return dst_path


def save_story(base_folder: str, story, extra_folder: str | None = None, output_format: OutputFormat = "txt") -> None:
    dst_path = save_story_pre(base_folder=base_folder, story=story, extra_folder=extra_folder)
    if output_format == OutputFormat.txt:
        story_path = (dst_path / get_sane_filename(story.title)).with_suffix(".txt")
        story_path.write_text(story.text)


class OutputFormat(Enum):
    txt = "txt"
    Markdown = "md"
    HTML = "html"
