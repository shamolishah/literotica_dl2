import logging
import re
from datetime import timedelta

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
