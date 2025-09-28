from dataclasses import dataclass
from enum import StrEnum


class Version(StrEnum):
    KJV = "KJV"
    NKJV = "NKJV"
    NLT = "NLT"
    NIV = "NIV"
    ESV = "ESV"
    CSB = "CSB"
    NASB20 = "NASB2020"
    NASB95 = "NASB95"
    LSB = "LSB"
    AMP = "AMP"
    YLT = "YLT"
    DBY = "DBY"
    WEB = "WEB"
    HNV = "HNV"
    VUL = "VUL"
    NAV = "NAV"
    WLC = "WLC"
    LXX = "LXX"
    SVD = "SVD"
    BES = "BES"
    RVR09 = "RVR09"
    RVR60 = "RVR60"
    BBE = "BBE"
    CHT = "CHT"
    EM = "EM"

    # MGNT = "MGNT"
    # TR = "TR"


class Book(StrEnum):
    # List of all books of the Bible
    GENESIS = "Genesis"
    EXODUS = "Exodus"
    LEVITICUS = "Leviticus"
    NUMBERS = "Numbers"
    DEUTERONOMY = "Deuteronomy"
    JOSHUA = "Joshua"
    JUDGES = "Judges"
    RUTH = "Ruth"
    FIRST_SAMUEL = "1 Samuel"
    SECOND_SAMUEL = "2 Samuel"
    FIRST_KINGS = "1 Kings"
    SECOND_KINGS = "2 Kings"
    FIRST_CHRONICLES = "1 Chronicles"
    SECOND_CHRONICLES = "2 Chronicles"
    EZRA = "Ezra"
    NEHEMIAH = "Nehemiah"
    ESTHER = "Esther"
    JOB = "Job"
    PSALMS = "Psalms"
    PROVERBS = "Proverbs"
    ECCLESIASTES = "Ecclesiastes"
    SONG_OF_SONGS = "Song of Songs"
    ISAIAH = "Isaiah"
    JEREMIAH = "Jeremiah"
    LAMENTATIONS = "Lamentations"
    EZEKIEL = "Ezekiel"
    DANIEL = "Daniel"
    HOSEA = "Hosea"
    JOEL = "Joel"
    AMOS = "Amos"
    OBADIAH = "Obadiah"
    JONAH = "Jonah"
    MICAH = "Micah"
    NAHUM = "Nahum"
    HABAKKUK = "Habakkuk"
    ZEPHANIAH = "Zephaniah"
    HAGGAI = "Haggai"
    ZECHARIAH = "Zechariah"
    MALACHI = "Malachi"
    MATTHEW = "Matthew"
    MARK = "Mark"
    LUKE = "Luke"
    JOHN = "John"
    ACTS = "Acts"
    ROMANS = "Romans"
    FIRST_CORINTHIANS = "1 Corinthians"
    SECOND_CORINTHIANS = "2 Corinthians"
    GALATIANS = "Galatians"
    EPHESIANS = "Ephesians"
    PHILIPPIANS = "Philippians"
    COLOSSIANS = "Colossians"
    FIRST_THESSALONIANS = "1 Thessalonians"
    SECOND_THESSALONIANS = "2 Thessalonians"
    FIRST_TIMOTHY = "1 Timothy"
    SECOND_TIMOTHY = "2 Timothy"
    TITUS = "Titus"
    PHILEMON = "Philemon"
    HEBREWS = "Hebrews"
    JAMES = "James"
    FIRST_PETER = "1 Peter"
    SECOND_PETER = "2 Peter"
    FIRST_JOHN = "1 John"
    SECOND_JOHN = "2 John"
    THIRD_JOHN = "3 John"
    JUDE = "Jude"
    REVELATION = "Revelation"


@dataclass
class Reference:
    book: Book
    chapter: int
    verse: int

    def __str__(self) -> str:
        return f"{self.book} {self.chapter}:{self.verse}"


@dataclass
class ReferenceRange:
    """A contiguous range of 1 or more verses. May span multiple chapters but not multiple books.

    Examples:
        - Valid: Ephesians 1:20-23
        - Valid: Ephesians 1:20-2:3
        - Valid: Ephesians 1-2
        - Invalid: Ephesians 6-Philipians 1 (spans multiple books)
    """

    start_ref: Reference
    end_ref: Reference | None = None

    def __str__(self) -> str:
        if self.end_ref:
            if self.start_ref.book == self.end_ref.book:
                if self.start_ref.chapter == self.end_ref.chapter:
                    return f"{self.start_ref.book} {self.start_ref.chapter}:{self.start_ref.verse}-{self.end_ref.verse}"
                else:
                    return f"{self.start_ref.book} {self.start_ref.chapter}:{self.start_ref.verse}-{self.end_ref.chapter}:{self.end_ref.verse}"
            else:
                return f"{self.start_ref.book} {self.start_ref.chapter}:{self.start_ref.verse}-{self.end_ref.book} {self.end_ref.chapter}:{self.end_ref.verse}"
        else:
            return str(self.start_ref)
