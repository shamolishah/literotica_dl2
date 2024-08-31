import html
import logging

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

log = logging.getLogger("literotica_dl.Story")


ua = UserAgent(browsers=["chrome"], os="linux", platforms=["pc"]).random


class Story:
    def __init__(self, story_id: str) -> None:
        self.url: str = f"https://www.literotica.com/s/{story_id}"
        self.story_id = story_id
        self.first_page = None
        self.author = ""
        self._category = ""
        self.description = ""
        self.num_pages = 0
        self.text = []
        self._title = None

    def _fetch_and_parse(self) -> None:
        log.info("Getting the initial page for %s", self.story_id)
        header = {"User-Agent": ua}
        page = requests.get(self.url, headers=header, timeout=10)
        self.first_page = BeautifulSoup(page.content, features="html.parser")

        self._title = self.first_page.find("title").getText()
        self._title = html.unescape(self._title)
        self._title, self._category = self._title[:-17].rsplit(" - ", 1)

    @property
    def title(self) -> str:
        """Title of the story"""
        if self._title is None:
            self._fetch_and_parse()
        return self._title
