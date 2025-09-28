import re

import requests
from bs4 import BeautifulSoup

from versea.types import Book, Version


class InvalidVersesError(Exception):
    """Raised when a format is invalid."""

    pass


class Versea:
    def _valid_verse_range(self, v: str):
        if not bool(re.fullmatch(r"(\d+)(-\d+)?", v)):
            raise InvalidVersesError(f"Invalid verse range: {v}")

    def parse_bible_text(self, d: dict, text: str) -> dict:
        # Extract the reference in curly brackets
        ref_match = re.match(r"\{([^\}]+)\}", text)
        if not ref_match:
            raise ValueError("No reference found")
        reference = ref_match.group(1)

        # Remove the reference part from the text
        verses_text = text[ref_match.end() :].strip()

        # Split into verses using the square bracket numbering
        verse_pattern = re.compile(r"\[(\d+)\]\s*(.*?)\s*(?=(\[\d+\]|$))", re.DOTALL)

        verses = {}
        for match in verse_pattern.finditer(verses_text):
            verse_number = int(match.group(1))
            verse_text = match.group(2).strip()
            verses[verse_number] = verse_text

        return {"reference": reference, "verses": verses}

    def get_verse(
        self, version: Version, book: Book, chapter: int, verse: int | None
    ) -> dict:
        """
        Fetch and display a Bible verse given the book, chapter, and verse number.

        Args:
            version (Version): Bible version to use.
            book (Book): Book of the Bible.
            chapter (int): Chapter number (must be >= 1).
            verse (int | None): Verse number (must be >= 1 if provided).

        Returns:
            str: The fetched Bible verse text.
        """

        url = "https://www.blueletterbible.org/tools/MultiVerse.cfm"
        mvText = f"{book} {chapter}"

        if verse:
            mvText += f":{verse}"

        data = {
            "t": version,
            "mvText": mvText,
            "refDelim": "2",
            "refFormat": "2",
            "numDelim": "2",
            "abbrev": "1",
        }
        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise Exception(f"Error fetching verse: {response.status_code}")

        # use beautifulsoup to parse the text from a div with id="multiResults"
        soup = BeautifulSoup(response.text, "html.parser")
        elem = soup.find("div", {"id": "multiResults"})
        if not elem:
            with open("error.html", "w") as f:
                f.write(response.text)
        text = elem.get_text()

        # Extract the reference in curly brackets
        ref_match = re.match(r"\{([^\}]+)\}", text)
        if not ref_match:
            raise ValueError("No reference found")
        # reference = ref_match.group(1)

        # Remove the reference part from the text
        verses_text = text[ref_match.end() :].strip()

        # Split into verses using the square bracket numbering
        verse_pattern = re.compile(r"\[(\d+)\]\s*(.*?)\s*(?=(\[\d+\]|$))", re.DOTALL)

        verses = {}
        for match in verse_pattern.finditer(verses_text):
            verse_number = int(match.group(1))
            verse_text = match.group(2).strip()
            verses[verse_number] = verse_text

        return self.parse_bible_text(verse_text)
