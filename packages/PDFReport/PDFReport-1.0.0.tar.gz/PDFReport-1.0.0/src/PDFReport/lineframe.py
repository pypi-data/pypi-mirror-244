from .enums import HAlign
from .enums import VAlign
from .enums import Direction
from .pen import Pen
from .rect import Rect
from .renderer import Renderer
from .containerframe import ContainerFrame
from .simpleframe import SimpleFrame
from .size import Size
from .sizestate import SizeState


class LineFrame(SimpleFrame):
    """
    Class for a frame the prints a line. It is a simple frame with no sub-frames in it.
    A line will be printed with a given width or height.
    """

    def __init__(self, parent: ContainerFrame, direction: Direction = Direction.HORIZONTAL, extent: float = 0.0, color: str = "#000000",
                 length: float = 0.0, h_align: HAlign = HAlign.LEFT, v_align: VAlign = VAlign.TOP, frame_id: str = ""):
        """
        :param parent: Parent frame to which this frame will be added
        :param direction: Direction of the line vertical or horizontal
        :param extent: Extent of the pen - default 0.1mm
        :param color: Color of the line - default black
        :param length: Length of the line
        :param h_align: Horizontal alignment of the line
        :param v_align: Vertical alignment of the line
        :param frame_id: frame id (optional)
        """
        super().__init__(parent, frame_id)

        self._direction = direction
        self._pen = Pen(extent, color)
        self._length = abs(length)

        self.h_align = h_align
        self.v_align = v_align

        self._x1 = 0.0
        self._x2 = 0.0
        self._y1 = 0.0
        self._y2 = 0.0

    @property
    def pen(self) -> Pen:
        """
        Pen for the line

        :getter: Returns the pen
        :setter: Sets the pen
        """
        return self._pen

    @pen.setter
    def pen(self, pen: Pen):
        self._pen = pen

    @property
    def length(self) -> float:
        """
        Length of the line

        :getter: Returns the length
        :setter: Sets the length
        """
        return self._length

    @length.setter
    def length(self, length: float):
        self._length = abs(length)

    @property
    def direction(self) -> Direction:
        """
        Direction of the line

        :getter: Returns the direction
        :setter: Sets the direction
        """
        return self._direction

    @direction.setter
    def direction(self, direction: Direction):
        self._direction = direction

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        size_states = SizeState()
        size_states.fits = True
        size_states.continued = False
        size_states.required_size = self.get_size()

        self._set_line_points(for_rect)

        if self._direction == Direction.HORIZONTAL:
            if self._y1 != self._y2:
                size_states.fits = False

        elif self._direction == Direction.VERTICAL:
            if self._x1 != self._x2:
                size_states.fits = False

        return size_states

    def _set_line_points(self, for_rect: Rect):
        pen_width = self._pen.extent
        half_width = pen_width / 2.0
        if self._direction == Direction.HORIZONTAL:
            match self._v_align:
                case VAlign.TOP:
                    self._y1 = for_rect.top + half_width
                case VAlign.MIDDLE:
                    self._y1 = (for_rect.top + for_rect.bottom) / 2.0
                case VAlign.BOTTOM:
                    self._y1 = for_rect.bottom - half_width

            self._y2 = self._y1

            if self._length == 0:
                self._x1 = for_rect.left
                self._x2 = for_rect.right
            else:
                match self._h_align:
                    case HAlign.LEFT:
                        self._x1 = for_rect.left
                        self._x2 = self._x1 + self._length
                    case HAlign.CENTER:
                        self._x1 = for_rect.left + (for_rect.get_width() - self._length) / 2.0
                        self._x2 = self._x1 + self._length
                    case HAlign.RIGHT:
                        self._x2 = for_rect.right
                        self._x1 = self._x2 - self._length

        else:

            match self._h_align:
                case HAlign.LEFT:
                    self._x1 = for_rect.left + half_width
                case HAlign.CENTER:
                    self._x1 = (for_rect.left + for_rect.right) / 2
                case HAlign.RIGHT:
                    self._x1 = for_rect.right - half_width

            self._x2 = self._x1

            if self._length == 0:
                self._y1 = for_rect.top
                self._y2 = for_rect.bottom
            else:
                match self._v_align:
                    case VAlign.TOP:
                        self._y1 = for_rect.top
                        self._y2 = self._y1 + self._length
                    case VAlign.MIDDLE:
                        self._y1 = for_rect.top + (for_rect.get_height() - self._length) / 2
                        self._y2 = self._y1 + self._length
                    case VAlign.BOTTOM:
                        self._y2 = for_rect.bottom
                        self._y1 = self._y2 - self._length

        self._x1 = max(self._x1, for_rect.left)
        self._x2 = min(self._x2, for_rect.right)
        self._y1 = max(self._y1, for_rect.top)
        self._y2 = min(self._y2, for_rect.bottom)

    def _rect_changed(self, original_rect: Rect, new_rect: Rect) -> SizeState:
        self._set_line_points(new_rect)
        return super()._rect_changed(original_rect, new_rect)

    def _do_print(self, r: Renderer, in_rect: Rect):
        width = self._pen.extent
        color = self._pen.color
        line_style = self._pen.line_style
        r.add_line(self._x1, self._y1, self._x2, self._y2, width, line_style, color)

    def get_size(self) -> Size:
        height = self._y2 - self._y1
        width = self._x2 - self._x1

        pen_width = self._pen.extent

        match self._direction:
            case Direction.HORIZONTAL:
                height = pen_width

            case Direction.VERTICAL:
                width = pen_width

        return Size(width, height)

    def _do_begin_print(self, r: Renderer):
        pass

    def to_dict(self, data: dict, frame: dict):
        frame["class"] = "LineFrame"

        if self.direction != Direction.HORIZONTAL:
            frame["direction"] = self.direction.value

        p = self.pen.to_dict()
        if len(p) > 0:
            frame["pen"] = p

        if self.length > 0.0:
            frame["length"] = self.length

        data[self.frame_id] = frame
        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        super().from_dict(frame)
        if "direction" in frame:
            self.direction = Direction(frame["direction"])

        if "pen" in frame:
            pen = Pen()
            pen.from_dict(frame["pen"])
            self.pen = pen

        if "length" in frame:
            self.length = frame["length"]
