import html
import logging

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

from literotica_dl2.utils import get_url_from_literotica

log = logging.getLogger("literotica_dl.Poem")


# Create shorthand method for conversion
def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


class Poem:
    def __init__(self, poem_id: str) -> None:
        self.url: str = f"https://www.literotica.com/p/{poem_id}"
        self.poem_id: str = poem_id
        self.first_page = None
        self._title: str = None
        self._text: str = None
        self._category: str = None
        self._md: str = None
        self._author: str = None

    def _fetch_and_parse(self) -> None:
        if self.first_page is not None:
            return
        log.info("Getting the initial page for %s", self.poem_id)
        self.first_page = BeautifulSoup(get_url_from_literotica(self.url), features="html5lib")

        self._title = self.first_page.find("title").getText()
        self._title = html.unescape(self._title)
        self._title, self._category = self._title[:-17].rsplit(" - ", 1)
        self._author = self.first_page.find("a", class_="y_eU").getText()
        poem_div = self.first_page.find("div", class_="aa_ht")
        self._text = poem_div.get_text("\n")
        self._md = md(poem_div)

    @property
    def title(self) -> str:
        """Title of the poem"""
        if self._title is None:
            self._fetch_and_parse()
        return self._title

    @property
    def author(self) -> str:
        """Author of the poem"""
        if self._author is None:
            self._fetch_and_parse()
        return self._author

    @property
    def text(self) -> str:
        """The full poem"""
        if self._text is None:
            self._fetch_and_parse()
        return self._text

    @property
    def markdown(self) -> str:
        """The full poem in markdown"""
        if self._md is None:
            self._fetch_and_parse()
        return self._md
