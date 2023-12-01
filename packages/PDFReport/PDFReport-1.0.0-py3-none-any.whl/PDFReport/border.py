import copy

from .pen import Pen
from .rect import Rect
from .renderer import Renderer
from .size import Size


class Border:
    """
    Class Border which represents the border of a frame.
    By default, there is no border i.e. all pens have an extent of 0.0
    """

    def __init__(self, top_pen: Pen = Pen(), left_pen: Pen = Pen(), right_pen: Pen = Pen(), bottom_pen: Pen = Pen()):
        """
        Defines a new border with the given pens. All parameters are optional.
        Default is no borderlines at all.

        :param top_pen: Pen object for the top line
        :param left_pen:  Pen object for the left line
        :param right_pen:  Pen object for the right line
        :param bottom_pen:  Pen object for the bottom line
        """
        self._top_pen = top_pen
        self._left_pen = left_pen
        self._right_pen = right_pen
        self._bottom_pen = bottom_pen

    @property
    def top_pen(self) -> Pen:
        """
        The pen object of the top borderline

        :getter: Returns the pen of the top borderline
        :setter: Sets the pen for the top borderline
        """
        return self._top_pen

    @top_pen.setter
    def top_pen(self, top_pen: Pen):
        self._top_pen = top_pen

    @property
    def left_pen(self) -> Pen:
        """
        The pen object of the left borderline

        :getter: Returns the pen of the left borderline
        :setter: Sets the pen for the left borderline
        """
        return self._left_pen

    @left_pen.setter
    def left_pen(self, left_pen: Pen):
        self._left_pen = left_pen

    @property
    def right_pen(self) -> Pen:
        """
        The pen object of the right borderline

        :getter: Returns the pen of the right borderline
        :setter: Sets the pen for the right borderline
        """
        return self._right_pen

    @right_pen.setter
    def right_pen(self, right_pen: Pen):
        self._right_pen = right_pen

    @property
    def bottom_pen(self) -> Pen:
        """
        The pen object of the bottom borderline

        :getter: Returns the pen of the bottom borderline
        :setter: Sets the pen for the bottom borderline
        """
        return self._bottom_pen

    @bottom_pen.setter
    def bottom_pen(self, bottom_pen: Pen):
        self._bottom_pen = bottom_pen

    @property
    def left_width(self) -> float:
        return self._left_pen.extent

    @property
    def top_width(self) -> float:
        return self._top_pen.extent

    @property
    def right_width(self) -> float:
        return self._right_pen.extent

    @property
    def bottom_width(self, ) -> float:
        return self._bottom_pen.extent

    def __eq__(self, other):
        if not isinstance(other, Border):
            return False

        if self.top_pen != other.top_pen:
            return False

        if self.bottom_pen != other.bottom_pen:
            return False

        if self.left_pen != other.left_pen:
            return False

        if self.right_pen != other.right_pen:
            return False

        return True

    TOP = 1
    LEFT = 2
    RIGHT = 3
    BOTTOM = 4

    def draw_border(self, r: Renderer, rect: Rect):
        self._draw_line(r, self._top_pen, rect, Border.TOP)
        self._draw_line(r, self._right_pen, rect, Border.RIGHT)
        self._draw_line(r, self._bottom_pen, rect, Border.BOTTOM)
        self._draw_line(r, self._left_pen, rect, Border.LEFT)

    def set_pen(self, pen: Pen):
        self._top_pen = copy.copy(pen)
        self._left_pen = copy.copy(pen)
        self._right_pen = copy.copy(pen)
        self._bottom_pen = copy.copy(pen)

    def add_border_size(self, to_size: Size) -> Size:
        size = Size(other=to_size)
        size.height += self._top_pen.extent
        size.width += self._right_pen.extent
        size.height += self._bottom_pen.extent
        size.width += self._left_pen.extent
        return size

    def get_inner_rect(self, for_rect: Rect) -> Rect:
        rect = Rect(other=for_rect)

        rect.top += self._top_pen.extent
        rect.right -= self._right_pen.extent
        rect.bottom -= self._bottom_pen.extent
        rect.left += self._left_pen.extent

        return rect

    @staticmethod
    def _draw_line(r: Renderer, pen: Pen, rect: Rect, edge: int):
        width = pen.extent
        half_width = width / 2.0
        color = pen.color
        line_style = pen.line_style
        x1 = 0.0
        y1 = 0.0
        x2 = 0.0
        y2 = 0.0
        if pen.extent != 0.0:
            match edge:
                case Border.TOP:
                    x1 = rect.left
                    x2 = rect.right
                    y1 = y2 = rect.top + width / 2.0
                    x1 = x1 + half_width
                    x2 = x2 - half_width

                case Border.RIGHT:
                    x1 = x2 = rect.right - width / 2.0
                    y1 = rect.top
                    y2 = rect.bottom
                    y1 = y1 + half_width
                    y2 = y2 - half_width

                case Border.BOTTOM:
                    x1 = rect.left
                    x2 = rect.right
                    y1 = y2 = rect.bottom - width / 2.0
                    x1 = x1 + half_width
                    x2 = x2 - half_width

                case Border.LEFT:
                    x1 = x2 = rect.left + width / 2.0
                    y1 = rect.top
                    y2 = rect.bottom
                    y1 = y1 + half_width
                    y2 = y2 - half_width

        r.add_line(x1, y1, x2, y2, width, line_style, color)

    def to_dict(self) -> dict:
        border = {}

        p = self.top_pen.to_dict()
        if len(p) > 0:
            border["top_pen"] = p

        p = self.left_pen.to_dict()
        if len(p) > 0:
            border["left_pen"] = p

        p = self.right_pen.to_dict()
        if len(p) > 0:
            border["right_pen"] = p

        p = self.bottom_pen.to_dict()
        if len(p) > 0:
            border["bottom_pen"] = p

        return border

    def from_dict(self, border: dict):
        if "top_pen" in border:
            self._top_pen.from_dict(border["top_pen"])

        if "left_pen" in border:
            self._left_pen.from_dict(border["left_pen"])

        if "right_pen" in border:
            self._right_pen.from_dict(border["right_pen"])

        if "bottom_pen" in border:
            self._bottom_pen.from_dict(border["bottom_pen"])
