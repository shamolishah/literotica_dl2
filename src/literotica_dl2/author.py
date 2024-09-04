from __future__ import annotations

from logging import getLogger

from bs4 import BeautifulSoup

from literotica_dl2.utils import (
    get_url_from_literotica,
    parse_story_series,
    parse_story_url,
)

log = getLogger("literotica.author")


class Author:
    def __init__(self, author_slug: str):
        self.slug: str = author_slug
        self.stories_page = None
        self.stories_url: str = f"https://www.literotica.com/authors/{author_slug}/works/stories/all"
        self._authorname: str = None
        self._series: list[str] = None
        self._individual_works: list[str] = None

    def _fetch_and_parse(self) -> None:
        if self.stories_page is not None:
            return
        self.stories_page = BeautifulSoup(get_url_from_literotica(self.stories_url), "html5lib")
        self._authorname = self.stories_page.find("p", class_="_header_title_1jjo0_57").getText()

        # get all the "series"
        self._series = []
        self._individual_works = []
        for work in self.stories_page.find_all("div", "_works_item__series_expanded_header_card_14spp_15"):
            try:
                log.info("Series Title %s", work.getText()[:100])
                self._series.append(parse_story_series(work.find("a")["href"]))
            except AttributeError:
                log.exception(work.get_text())
        for work in self.stories_page.find_all("div", class_="_series_parts__item__series_part_card_14spp_275"):
            if work.css.closest("._series_parts__wrapper_14spp_257"):
                continue
            log.info("Individual Title: %s", work.getText()[:100])
            self._individual_works.append(parse_story_url(work.find("a")["href"]))

        # _works_item_14spp_5 # this is all stories
        # _series_parts__item__series_part_card_14spp_275 : individual stories that are not in a series
        # _works_item__series_expanded_header_card_14spp_15
        # _series_parts__wrapper_14spp_257 : wrapper to group

    @property
    def author_name(self) -> str:
        if self._authorname is None:
            self._fetch_and_parse()
        return self._authorname

    @property
    def series(self) -> list[str | None]:
        if self._series is None:
            self._fetch_and_parse()
        return self._series

    @property
    def individual_stories(self) -> list[str | None]:
        if self._individual_works is None:
            self._fetch_and_parse()
        return self._individual_works
