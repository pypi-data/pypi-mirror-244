import re

from .pen import Pen
from .rect import Rect
from .reportframe import get_rect_with_margins
from .reportframe import get_rect_with_size_and_align
from .textstyle import TextStyle
from .renderer import Renderer
from .size import Size
from .enums import TextAlign
from .enums import HAlign
from .enums import VAlign


class TableColumn:

    def __init__(self, table, title: str = "", width: float or str = 0.0, text_align: TextAlign = TextAlign.LEFT,
                 padding_right: float = 0.5, padding_left: float = 0.5, padding_top: float = 0.1, padding_bottom: float = 0.1):
        self._width_in_percent = False
        self.width = width
        self._title = title
        self._text_align = text_align
        self._padding_right = abs(padding_right)
        self._padding_left = abs(padding_left)
        self._padding_top = abs(padding_top)
        self._padding_bottom = abs(padding_bottom)

        self._width_to_use = 0.0
        self._line_break = False
        self._right_pen = Pen()

        self._table = table
        self._idx = table.add_column(self)
        self._column_id = table.frame_id + "." + str(self._idx)

    @property
    def idx(self) -> int:
        return self._idx

    @property
    def width_to_use(self) -> float:
        return self._width_to_use

    @width_to_use.setter
    def width_to_use(self, width_to_use: float):
        self._width_to_use = width_to_use

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, width: float or str):
        self._width_in_percent = False
        if isinstance(width, str):
            width = re.sub(r'[^0-9.]', '', width)
            self._width = float(width)
            self._width_in_percent = True
        else:
            self._width = width

    @property
    def width_in_percent(self) -> bool:
        return self._width_in_percent

    @width_in_percent.setter
    def width_in_percent(self, width_in_percent: bool):
        self._width_in_percent = width_in_percent

    @property
    def right_pen(self) -> Pen:
        return self._right_pen

    @right_pen.setter
    def right_pen(self, right_pen: Pen):
        self._right_pen = right_pen

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def text_align(self) -> TextAlign:
        return self._text_align

    @text_align.setter
    def text_align(self, text_align: TextAlign):
        self._text_align = text_align

    @property
    def padding_left(self) -> float:
        return self._padding_left

    @padding_left.setter
    def padding_left(self, padding_left: float):
        self._padding_left = abs(padding_left)

    @property
    def padding_right(self) -> float:
        return self._padding_right

    @padding_right.setter
    def padding_right(self, padding_right: float):
        self._padding_right = abs(padding_right)

    @property
    def padding_top(self) -> float:
        return self._padding_top

    @padding_top.setter
    def padding_top(self, padding_top: float):
        self._padding_top = abs(padding_top)

    @property
    def padding_bottom(self) -> float:
        return self._padding_bottom

    @padding_bottom.setter
    def padding_bottom(self, padding_bottom: float):
        self._padding_bottom = abs(padding_bottom)

    @property
    def line_break(self) -> bool:
        return self._line_break

    @line_break.setter
    def line_break(self, line_break: bool):
        self._line_break = line_break

    def calc_width(self, width: float):
        if self._width_in_percent:
            self._width_to_use = width * self._width / 100.0
        else:
            self._width_to_use = self._width

    def size_paint_cell(self, r: Renderer, text: str, text_style: TextStyle, x: float, y: float, width: float, max_height: float, size_only: bool) -> Size:
        rect = Rect(x, y, x + width, y + max_height)
        inner_bounds = get_rect_with_margins(rect, self._padding_top,
                                             self._padding_right + self._right_pen.extent,
                                             self._padding_bottom, self._padding_left)

        if size_only:
            string_size = r.calc_text_size(text_style, text, self._text_align, inner_bounds.get_width())

            side_margins = self._padding_left + self._padding_right + self._right_pen.extent
            top_bottom_margins = self._padding_top + self._padding_bottom

            string_size.width += side_margins
            string_size.height += top_bottom_margins

            string_size.height = min(string_size.height, max_height)
        else:
            if text_style.background_color != "#FFFFFF":
                background_rect = get_rect_with_size_and_align(rect)
                r.add_rect(background_rect, text_style.background_color)

            string_size = Size(inner_bounds.get_width(), inner_bounds.get_height())

            text_layout = get_rect_with_size_and_align(inner_bounds, string_size, HAlign.LEFT, VAlign.TOP)

            text_height = r.add_text_block(text, text_style, text_layout, self._text_align, text_style.text_color)
            text_layout.top += text_height

        return string_size

    def draw_right_line(self, r: Renderer, x: float, y: float, height: float):
        if self._right_pen.extent != 0.0:
            x -= self._right_pen.extent
            r.add_line(x, y, x, y + height, self._right_pen.extent, self._right_pen.line_style,
                       self._right_pen.color)

    def to_dict(self, data: dict, col: dict):
        """
        Fills the attribute-values to a dictionary if the attribute has no default value.
        :param data:  global dict for the whole report
        :param col: dict for the column
        """
        col["class"] = "TableColumn"
        col["parent_id"] = self._table.frame_id

        if self.width > 0.0:
            col["width"] = self.width

        if self.title != "":
            col["title"] = self.title

        if self.width_in_percent:
            col["width_in_percent"] = self.width_in_percent

        if self.text_align != TextAlign.LEFT:
            col["text_align"] = self.text_align.value

        if self.padding_right != 0.5:
            col["padding_right"] = self.padding_right

        if self.padding_left != 0.5:
            col["padding_left"] = self.padding_left

        if self.padding_top != 0.1:
            col["padding_top"] = self.padding_top

        if self.padding_bottom != 0.1:
            col["padding_bottom"] = self.padding_bottom

        p = self.right_pen.to_dict()
        if len(p) > 0:
            col["right_pen"] = p

        data[self._column_id] = col

    def from_dict(self, col: dict):
        """
        Fills the attributes based on the given dict
        :param col:
        """
        if "width" in col:
            self.width = col["width"]

        if "title" in col:
            self.title = col["title"]

        if "width_in_percent" in col:
            self.width_in_percent = col["width_in_percent"]

        if "text_align" in col:
            self.text_align = TextAlign(col["text_align"])

        if "padding_right" in col:
            self.padding_right = col["padding_right"]

        if "padding_left" in col:
            self.padding_left = col["padding_left"]

        if "padding_top" in col:
            self.padding_top = col["padding_top"]

        if "padding_bottom" in col:
            self.padding_bottom = col["padding_bottom"]

        if "right_pen" in col:
            pen = Pen()
            pen.from_dict(col["right_pen"])
            self.right_pen = pen
