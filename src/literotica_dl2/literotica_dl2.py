from __future__ import annotations

import logging
from pathlib import Path

import typer

from literotica_dl2.__about__ import __version__
from literotica_dl2.author import Author
from literotica_dl2.poem import Poem
from literotica_dl2.story import Story
from literotica_dl2.story_series import StorySeries
from literotica_dl2.utils import OutputFormat, save_work

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(style="{", fmt="[{name}:{filename}] {levelname} - {message}"))

log = logging.getLogger("literotica_dl")
log.setLevel(logging.INFO)
log.addHandler(handler)

app = typer.Typer()


@app.command()
def version() -> None:
    log.info("The app Version is %s", __version__)


@app.command()
def story(story_slug: str, output: str = "output", output_format: OutputFormat = "txt") -> None:
    log.info("Trying to get %s", story_slug)
    Path(output).mkdir(exist_ok=True, parents=False)
    story = Story(story_slug)
    save_work(output, story, output_format=output_format)


@app.command()
def poetry(poem_slug: str, output: str = "output", output_format: OutputFormat = "txt") -> None:
    log.info("Trying to get %s", poem_slug)
    Path(output).mkdir(exist_ok=True, parents=False)
    poem = Poem(poem_slug)
    save_work(output, poem, output_format=output_format)


@app.command()
def author(author_slug: str, output: str = "output", output_format: OutputFormat = "txt") -> None:
    log.info("Trying to get the author: %s", author_slug)
    Path(output).mkdir(exist_ok=True, parents=False)
    author = Author(author_slug)
    for story_stub in author.individual_stories:
        story = Story(story_stub)
        save_work(output, story, extra_folder="Individual Stories", output_format=output_format)
    for series_stub in author.series:
        series = StorySeries(series_stub)
        for chapter_stub in series.stories:
            chapter = Story(chapter_stub)
            save_work(output, chapter, extra_folder=series.title, output_format=output_format)
    for poems_stub in author.poems:
        poem = Poem(poems_stub)
        save_work(output, poem, extra_folder="Poems", output_format=output_format)


if __name__ == "__main__":
    app()
