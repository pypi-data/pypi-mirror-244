from .textstyle import TextStyle, text_styles


class TextStylesMeta(type):
    """
    Metaclass for TextStyles to enable []-access to text styles
    """
    def __getitem__(self, item) -> TextStyle:
        if len(text_styles) == 0:
            TextStyles.init_text_styles()

        if item in text_styles:
            return text_styles[item]

        return TextStyle(item)


class TextStyles(metaclass=TextStylesMeta):
    font_family: str = "Helvetica"
    font_size: float = 9.0
    text_color: str = "#000000"

    @staticmethod
    def set_default(font_family: str = "Helvetica", font_size: float = 9.0, text_color: str = "#000000"):
        text_styles.clear()
        TextStyles.font_family = font_family
        TextStyles.font_size = font_size
        TextStyles.text_color = text_color
        TextStyles.init_text_styles()

    @staticmethod
    def init_text_styles():
        ts_normal = TextStyle(TextStyle.NORMAL, font_family=TextStyles.font_family, font_size=TextStyles.font_size, text_color=TextStyles.text_color)
        TextStyle(TextStyle.BOLD, bold=True)
        TextStyle(TextStyle.ITALIC, italic=True)
        TextStyle(TextStyle.UNDERLINE, underline=True)
        TextStyle(TextStyle.SMALL, font_size=ts_normal.font_size - 1)
        TextStyle(TextStyle.HEADING1, bold=True, font_size=ts_normal.font_size + 9.0)
        TextStyle(TextStyle.HEADING2, bold=True, font_size=ts_normal.font_size + 6.0)
        TextStyle(TextStyle.HEADING3, bold=True, italic=True, font_size=ts_normal.font_size + 3.0)
        TextStyle(TextStyle.HEADING4, bold=True, italic=True, font_size=ts_normal.font_size + 1.0)
        TextStyle(TextStyle.FOOTER, font_size=ts_normal.font_size - 1.0)
        TextStyle(TextStyle.HEADER, font_size=ts_normal.font_size - 1.0)
        TextStyle(TextStyle.TABLE_HEADER, bold=True, font_size=ts_normal.font_size - 1.0)
        TextStyle(TextStyle.TABLE_ROW, font_size=ts_normal.font_size - 1.0)
        TextStyle(TextStyle.TABLE_SUBTOTAL, italic=True, font_size=ts_normal.font_size - 1.0)
        TextStyle(TextStyle.TABLE_TOTAL, bold=True, font_size=ts_normal.font_size - 1.0)
