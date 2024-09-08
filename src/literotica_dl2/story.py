import html
import logging

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

from literotica_dl2.utils import get_url_from_literotica

log = logging.getLogger("literotica_dl.Story")


# Create shorthand method for conversion
def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


class Story:
    def __init__(self, story_id: str) -> None:
        self.url: str = f"https://www.literotica.com/s/{story_id}"
        self.story_id: str = story_id
        self.first_page = None
        self._author: str = None
        self._category: str = None
        self._description: str = None
        self._pages: int = None
        self._text = None
        self._title = None
        self._md = None

    def _fetch_and_parse(self) -> None:
        if self.first_page is not None:
            return
        log.info("Getting the initial page for %s", self.story_id)

        page = get_url_from_literotica(self.url)
        self.first_page = BeautifulSoup(page, features="html5lib")

        self._title = self.first_page.find("title").getText()
        self._title = html.unescape(self._title)
        self._title, self._category = self._title[:-17].rsplit(" - ", 1)

        # Author link class name is y_eU . If the CSS changes update here.
        self._author = self.first_page.find("a", class_="y_eU").getText()

        # Description dive class name is bn_B.
        self._description = self.first_page.find("div", class_="bn_B").getText()

        # Pages link class = l_bJ
        try:
            self._pages = int(self.first_page.find_all("a", class_="l_bJ")[-1].getText())
        except IndexError:
            self._pages = 1
        except Exception:
            log.exception("Error Getting page numbers")

    @property
    def title(self) -> str:
        """Title of the story"""
        if self._title is None:
            self._fetch_and_parse()
        return self._title

    @property
    def author(self) -> str:
        """Author of the story"""
        if self._author is None:
            self._fetch_and_parse()
        return self._author

    @property
    def category(self) -> str:
        """Category of the story"""
        if self._category is None:
            self._fetch_and_parse()
        return self._category

    @property
    def description(self) -> str:
        """Description of the story"""
        if self._description is None:
            self._fetch_and_parse()
        return self._description

    @property
    def pages(self) -> int:
        """Pages of the story"""
        if self._pages is None:
            self._fetch_and_parse()
        return self._pages

    def populate_full_story(self) -> None:
        if self._pages is None:
            self._fetch_and_parse()
        # the page css for the story text is aa_ht
        # since we already have first page no need to get it again.
        # https://www.literotica.com/s/hot-neighbor-noelle?page=3

        page_soups = [self.first_page]
        if self._pages > 1:
            for pg_no in range(2, self._pages + 1):
                page_url = f"{self.url}?page={pg_no}"
                page_soups.append(BeautifulSoup(get_url_from_literotica(page_url), features="html5lib"))
        story_soups = [x.find("div", class_="aa_ht") for x in page_soups]
        pages = [x.getText("\n\n") for x in story_soups]

        self._text = "\n".join([str(x) for x in pages])
        self._md = "\n".join([md(x) for x in story_soups])

    @property
    def text(self) -> str:
        """The full story"""
        if self._text is None:
            self.populate_full_story()
        return self._text

    @property
    def markdown(self) -> str:
        """The full story in markdown"""
        if self._md is None:
            self.populate_full_story()
        return self._md
