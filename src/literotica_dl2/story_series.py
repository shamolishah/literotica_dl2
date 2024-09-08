from __future__ import annotations

from bs4 import BeautifulSoup

from literotica_dl2.utils import get_url_from_literotica, parse_story_url


class StorySeries:
    def __init__(self, series_id: str) -> None:
        self.series_id = series_id
        self._stories = None
        self._title = None
        self.url = f"https://www.literotica.com/series/se/{series_id}"
        self.page = None

    def parse(self) -> None:
        if self.page is None:
            self.page = BeautifulSoup(get_url_from_literotica(self.url), features="html5lib")
        self._stories = []
        for link in self.page.find_all("a", class_="br_rj"):
            self.stories.append(parse_story_url(link["href"]))
        self._title = self.page.find("h1").getText()

    @property
    def stories(self):
        if self._stories is None:
            self.parse()
        return self._stories

    @property
    def title(self) -> str:
        if self._title is None:
            self.parse()
        return self._title
