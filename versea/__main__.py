import json

import typer
from typing_extensions import Annotated

from versea.types import Book, Version
from versea.versea import Versea

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command(no_args_is_help=True)
def main(
    version: Annotated[Version, typer.Option(help="Bible version to use")],
    book: Annotated[Book, typer.Option(help="Book of the Bible")],
    chapter: Annotated[int, typer.Option(help="Chapter number", min=1)],
    verse: Annotated[int | None, typer.Option(help="Verse number", min=1)] = None,
):
    """Fetch and display a Bible verse given the book, chapter, and verse number."""
    versea = Versea()
    verses = versea.get_verse(version, book, chapter, verse)
    print(json.dumps(verses, indent=2, ensure_ascii=False))


@app.command()
def test():
    members = list(Version.__members__.keys())
    for version in members[16:]:
        # text = get_verse(version, Book.GENESIS, 1, 1)
        print(version)
        # print(text)


if __name__ == "__main__":
    app()
