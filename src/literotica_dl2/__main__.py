import argparse
import logging
from pathlib import Path

from literotica_dl2.__about__ import __version__
from literotica_dl2.story import Story
from literotica_dl2.utils import get_sane_filename


handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(style="{", fmt="[{name}:{filename}] {levelname} - {message}"))

log = logging.getLogger("literotica_dl")
log.setLevel(logging.INFO)
log.addHandler(handler)


def main():
    # Handle Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument(
        "-s",
        "--story",
        default=None,
        help="The story to download. pass in the part after the /s/*",
    )
    parser.add_argument("-a", "--author", default=None, help="The author to mirror.")
    parser.add_argument(
        "-o",
        "--output",
        default="output",
        help="The directory to write files. default: %(default)s",
    )
    args = parser.parse_args()

    # argument checking
    if args.author is None and args.story is None:
        msg = "One of (-a / -s) flags must be specified"
        log.error(msg)
        raise RuntimeError(msg)

    Path(args.output).mkdir(exist_ok=True, parents=False)

    if args.story:
        log.info("Trying to get %s", args.story)
        story = Story(args.story)
        dst_path = Path(args.output) / get_sane_filename(story.author)
        dst_path.mkdir(exist_ok=True,parents=True)
        story_path = (dst_path / get_sane_filename(story.title)).with_suffix(".txt")
        story_path.write_text(story.text)



if __name__ == "__main__":
    main()
