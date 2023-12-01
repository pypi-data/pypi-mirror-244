
# Dict with the defined text styles
text_styles = {}


class TextStyle:
    """
    Class TextStyle to define a font with its size, color and other attributes.
    """

    # Names of the predefined text styles
    NORMAL = "NORMAL"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    UNDERLINE = "UNDERLINE"
    SMALL = "SMALL"
    HEADING1 = "HEADING1"
    HEADING2 = "HEADING2"
    HEADING3 = "HEADING3"
    HEADING4 = "HEADING4"
    FOOTER = "FOOTER"
    HEADER = "HEADER"
    TABLE_HEADER = "TABLE_HEADER"
    TABLE_ROW = "TABLE_ROW"
    TABLE_SUBTOTAL = "TABLE_SUBTOTAL"
    TABLE_TOTAL = "TABLE_TOTAL"

    def __init__(self, name: str, font_family: str = "", font_size: float = 0.0, bold=None, italic=None, underline=None,
                 text_color: str = "", background_color: str = "", base_style=NORMAL):
        """
        Set the attributes for a text style. Default is Helvetica with size 9 points, black text on white background
        If a base_style is passed its attributes are used and modified by the other passed attributes

        :param name: name for access in text_styles
        :param font_family: font family
        :param font_size: size of the font in points
        :param bold: bold flag
        :param italic: italic flag
        :param underline:  underline flag
        :param text_color: text color
        :param background_color: background color
        :param base_style: base style
        """

        if name != "" and name in text_styles:
            # The text style exists - error
            raise ValueError(f"TextStyle {name} already exists.")

        self._name = name
        self._font_family = ""
        self._font_size = 0.0
        self._bold = False
        self._italic = False
        self._underline = False
        self._text_color = ""
        self._background_color = ""

        if base_style != "" and base_style in text_styles:
            ts = text_styles[base_style]
            self._font_family = ts.font_family
            self._font_size = ts.font_size
            self._text_color = ts.text_color
            self._background_color = ts.background_color
            self._bold = ts.bold
            self._italic = ts.italic
            self._underline = ts.underline

        if font_family != "":
            self._font_family = font_family

        if font_size > 0.0:
            self._font_size = font_size

        if text_color != "":
            self._text_color = text_color

        if background_color != "":
            self._background_color = background_color

        if bold is not None:
            self._bold = bold

        if italic is not None:
            self._italic = italic

        if underline is not None:
            self._underline = underline

        if self._font_family == "":
            self._font_family = "Helvetica"

        if self._font_size == 0.0:
            self._font_size = 9.0

        if self._text_color == "":
            self._text_color = "#000000"

        if self._background_color == "":
            self._background_color = "#FFFFFF"

        if name != "":
            text_styles[name] = self

    @property
    def name(self) -> str:
        """
        The name of the text style

        :getter: Returns the name of the text style
        """
        return self._name

    @property
    def font_family(self) -> str:
        """
        Font family of the text style

        :getter: Returns the font family
        :setter: Sets the font family
        """
        return self._font_family

    @font_family.setter
    def font_family(self, font_family: str):
        self._font_family = font_family

    @property
    def font_size(self) -> float:
        """
        Size of the text style in points

        :getter: Returns the size
        :setter: Sets the size
        """
        return self._font_size

    @font_size.setter
    def font_size(self, font_size: float):
        self._font_size = font_size

    @property
    def bold(self) -> bool:
        """
        Bold flag for the text style

        :getter: Returns the bold flag
        :setter: Sets the bold flag
        """
        return self._bold

    @bold.setter
    def bold(self, bold: bool):
        self._bold = bold

    @property
    def italic(self) -> bool:
        """
        Italic flag for the text style

        :getter: Returns the italic flag
        :setter: Sets the italic flag
        """
        return self._italic

    @italic.setter
    def italic(self, italic: bool):
        self._italic = italic

    @property
    def underline(self) -> bool:
        """
        Underline flag for the text style

        :getter: Returns the underline flag
        :setter: Sets the underline flag
        """
        return self._underline

    @underline.setter
    def underline(self, underline: bool):
        self._underline = underline

    @property
    def text_color(self) -> str:
        """
        Text color of the text style

        :getter: Returns the text color
        :setter: Sets the text color
        """
        return self._text_color

    @text_color.setter
    def text_color(self, text_color: str):
        self._text_color = text_color

    @property
    def background_color(self) -> str:
        """
        Background color of the text style

        :getter: Returns the background color
        :setter: Sets the background color
        """
        return self._background_color

    @background_color.setter
    def background_color(self, background_color: str):
        self._background_color = background_color

    def to_dict(self) -> dict:
        ts = {}

        if self._font_family != "Helvetica":
            ts["font_family"] = self._font_family

        if self._font_size != 9.0:
            ts["font_size"] = self._font_size

        if self._bold:
            ts["bold"] = self._bold

        if self._italic:
            ts["italic"] = self._italic

        if self._underline:
            ts["underline"] = self._underline

        if self._text_color != "#000000":
            ts["text_color"] = self._text_color

        if self._background_color != "#FFFFFF":
            ts["background_color"] = self._background_color

        return ts

    def from_dict(self, ts: dict):
        if "font_family" in ts:
            self._font_family = ts["font_family"]

        if "font_size" in ts:
            self._font_size = ts["font_size"]

        if "bold" in ts:
            self._bold = ts["bold"]

        if "italic" in ts:
            self._italic = ts["italic"]

        if "underline" in ts:
            self._underline = ts["underline"]

        if "text_color" in ts:
            self._text_color = ts["text_color"]

        if "background_color" in ts:
            self._background_color = ts["background_color"]
