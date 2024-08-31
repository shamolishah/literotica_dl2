import logging

import requests
from fake_useragent import UserAgent

log = logging.getLogger("literotica_dl.downloader_utils")


def get_sane_filename(title: str) -> str:
    keep_characters = (" ", "_")  # Only these special chars allowed
    return "".join(c for c in title if c.isalnum() or c in keep_characters).rstrip()


def get_url_from_literotica(url: str) -> bytes:
    ua = UserAgent().chrome
    header = {"User-Agent": ua}
    log.info("Fetching From Literotica: %s", url)
    page = requests.get(url, headers=header, timeout=10)
    return page.content
