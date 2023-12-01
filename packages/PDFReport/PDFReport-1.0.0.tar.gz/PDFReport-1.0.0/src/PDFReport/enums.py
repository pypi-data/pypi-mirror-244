from enum import Enum


class PageOrientation(Enum):
    PORTRAIT = 'P'
    LANDSCAPE = 'L'


class PageSize(Enum):
    SIZE_A3 = 'A3'
    SIZE_A4 = 'A4'
    SIZE_A5 = 'A5'
    SIZE_LETTER = 'Letter'
    SIZE_LEGAL = 'Legal'


class HAlign(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2


class VAlign(Enum):
    TOP = 0
    BOTTOM = 1
    MIDDLE = 2


class TextAlign(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2
    JUST = 3


class Direction(Enum):
    VERTICAL = 'V'
    HORIZONTAL = 'H'


class LineStyle(Enum):
    SOLID = 0
    DASH = 1
    DOT = 2


class BarcodeType(Enum):
    QRCODE = 1
    CODE39 = 2
    CODE128 = 3
    EAN13 = 4
    EAN8 = 5
    ISBN13 = 6
    ISBN10 = 7
    ISSN = 8
    UPCA = 9
    EAN14 = 10


class RowType(Enum):
    DETAIL = 'D'
    HEADER = 'H'
    SUBTOTAL = 'S'
    TOTAL = 'T'
