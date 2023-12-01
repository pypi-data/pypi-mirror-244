import re

from .border import Border
from .containerframe import ContainerFrame
from .pen import Pen
from .rect import Rect
from .globals import get_rect_with_margins
from .globals import get_rect_with_size_and_align
from .renderer import Renderer
from .reportframe import ReportFrame
from .size import Size
from .sizestate import SizeState


class BoxFrame(ContainerFrame):
    """
    Class representing a box with a fix width or height in a report.
    A box frame can have a border around the whole frame and a colored background.
    It is a special container frame, because it can only contain one frame.
    But that frame can be any kind of frame, i.e. it can ba another container frame,
    so a box can be filled with any content.
    """

    def __init__(self, parent: ContainerFrame, width: float or str = 0.0, height: float or str = 0.0,
                 border_extent: float = 0.0, border_color: str = "#000000", background_color: str = "#FFFFFF", keep_together: bool = False, frame_id: str = ""):
        """
        Creates a new BoxFrame object.
        The default values of the params will create an empty box with no border and white background

        :param parent: Parent frame to which this frame will be added
        :param width: Width of the box in mm or % - float->mm, string->"%"
        :param height: Height of the box in mm or % - float->mm, string->"%"
        :param border_extent: Extent for the borderline
        :param border_color: Color for the borderline
        :param background_color: Background color for the box
        :param keep_together: flag if the box should be kept together on one page (inherited from ReportFrame)
        :param frame_id: frame id (optional)
        """

        super().__init__(parent, frame_id)

        self._width_in_percent = False
        self._width = 0.0
        self._height_in_percent = False
        self._height = 0.0

        self.width = width
        self.height = height
        self.keep_together = keep_together

        self._padding_left = 0.0
        self._padding_top = 0.0
        self._padding_right = 0.0
        self._padding_bottom = 0.0

        self._border = Border()
        self.set_border_pen(Pen(border_extent, border_color))

        self._background = background_color

        self._width_to_use = 0.0
        self._height_to_use = 0.0
        self._border_rect = Rect()
        self._padding_rect = Rect()
        self._content_rect = Rect()

    @property
    def border(self) -> Border:
        """
        The border of the box frame

        :getter: Returns the border object
        :setter: Sets the border
        """
        return self._border

    @border.setter
    def border(self, border: Border):
        self._border = border

    @property
    def width(self):
        """
        The width of the boy

        :getter: Returns the width
        :setter: Sets the width
        """
        return self._width

    @width.setter
    def width(self, width: float or str):
        self._width_in_percent = False
        if isinstance(width, str):
            width = re.sub(r'[^0-9.]', '', width)
            self._width = abs(float(width))
            self._width_in_percent = True
        else:
            self._width = abs(width)

    @property
    def height(self):
        """
        The height of the box

        :getter: Returns the height
        :setter: Sets the height
        """
        return self._height

    @height.setter
    def height(self, height: float or str):
        self._height_in_percent = False
        if isinstance(height, str):
            height = re.sub(r'[^0-9.]', '', height)
            self._height_in_percent = True
            self._height = abs(float(height))
        else:
            self._height = abs(height)

    @property
    def width_in_percent(self) -> bool:
        """
        Flag if the width is given in percent or as absolute value in millimeters

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._width_in_percent

    @width_in_percent.setter
    def width_in_percent(self, width_in_percent: bool):
        self._width_in_percent = width_in_percent

    @property
    def height_in_percent(self) -> bool:
        """
        Flag if the height is given in percent or as absolute value in millimeters

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._height_in_percent

    @height_in_percent.setter
    def height_in_percent(self, height_in_percent: bool):
        self._height_in_percent = height_in_percent

    @property
    def padding_top(self) -> float:
        """
        Padding on top of the box

        :getter: Returns the top padding
        :setter: Sets the top padding
        """
        return self._padding_top

    @padding_top.setter
    def padding_top(self, padding_top: float):
        self._padding_top = padding_top

    @property
    def padding_right(self) -> float:
        """
        Padding on right of the box

        :getter: Returns the right padding
        :setter: Sets the right padding
        """
        return self._padding_right

    @padding_right.setter
    def padding_right(self, padding_right: float):
        self._padding_right = padding_right

    @property
    def padding_bottom(self) -> float:
        """
        Padding on bottom of the box

        :getter: Returns the bottom padding
        :setter: Sets the bottom padding
        """
        return self._padding_bottom

    @padding_bottom.setter
    def padding_bottom(self, padding_bottom: float):
        self._padding_bottom = padding_bottom

    @property
    def padding_left(self) -> float:
        """
        Padding on left of the box

        :getter: Returns the left padding
        :setter: Sets the left padding
        """
        return self._padding_left

    @padding_left.setter
    def padding_left(self, padding_left: float):
        self._padding_left = padding_left

    @property
    def background(self) -> str:
        """
        Background color of the box

        :getter: Returns the background color
        :setter: Sets the background color
        """
        return self._background

    @background.setter
    def background(self, background: str):
        self._background = background

    def set_border_pen(self, pen: Pen):
        """
        Sets the pen for all four sides

        :param pen: Pen to be used
        """
        self._border.set_pen(pen)

    def set_padding(self, val: float):
        """
        Sets the padding on all four sides
        :param val: Padding in mm
        """
        self._padding_top = val
        self._padding_right = val
        self._padding_bottom = val
        self._padding_left = val

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        size_state = SizeState()
        rect = Rect(other=for_rect)

        size_state.fits = True
        size_state.continued = False

        content_size = Size()
        if self._is_current_frame_valid():
            self._get_current_frame().calc_size(r, self._get_max_content_rect(rect))
            content_size = self._get_current_frame().get_size()

            size_state.fits = self._get_current_frame()._fits
            size_state.continued = self._get_current_frame()._continued

        self._border_rect = self._get_border_rect(rect, content_size, True)
        self._padding_rect = self._border.get_inner_rect(self._border_rect)
        self._content_rect = get_rect_with_margins(self._padding_rect, self._padding_top, self._padding_right,
                                                   self._padding_bottom, self._padding_left)

        size_state.required_size = self._border_rect.get_size()

        if self._border_rect.get_height() > for_rect.get_height():
            size_state.fits = False
            size_state.continued = True

        if self.keep_together and not self._size_to_contents_height():
            if self._border_rect.get_height() < self._height:
                size_state.fits = False
                size_state.continued = True

        return size_state

    def _get_max_content_rect(self, from_rect: Rect) -> Rect:
        rect = Rect(other=from_rect)

        rect.left += self._border.left_width + self._padding_left
        rect.top += self._border.top_width + self._padding_top
        if self._width > 0:
            if self._width_in_percent:
                if self._parent_frame is None:
                    frame_width = rect.get_width()
                else:
                    frame_width = self._parent_frame.get_sizing_bounds().get_width()

                content_width = ((frame_width * self._width / 100.0) -
                                 self._margin_left - self._margin_right - self._border.left_width - self._border.right_width - self._padding_left - self._padding_right)

                rect.right = rect.left + content_width
            else:
                content_width = self._width - self._margin_left - self._margin_right - self._border.left_width - self._border.right_width - self._padding_left - self._padding_right

                rect.right = rect.left + content_width

        else:
            rect.right -= self._border.right_width + self._padding_right

        if self._height > 0:
            if self._width_in_percent:
                if self._parent_frame is None:
                    frame_height = rect.get_height()
                else:
                    frame_height = self._parent_frame.get_sizing_bounds().get_height()

                content_height = ((frame_height * self._height / 100.0) -
                                  self._margin_top - self._margin_bottom - self._border.top_width - self._border.bottom_width - self._padding_top - self._padding_bottom)

                rect.bottom = rect.top + content_height
            else:
                content_height = self._height - self._margin_top - self._margin_bottom - self._border.top_width - self._border.bottom_width - self._padding_top - self._padding_bottom

                rect.bottom = rect.top + content_height

        else:
            rect.bottom -= self._border.bottom_width + self._padding_bottom

        return rect

    def _rect_changed(self, original_rect: Rect, new_rect: Rect) -> SizeState:
        content_size = self.get_size()

        self._border_rect = self._get_border_rect(new_rect, content_size, False)
        self._padding_rect = self._border.get_inner_rect(self._border_rect)
        self._content_rect = get_rect_with_margins(self._padding_rect, self._padding_top, self._padding_right,
                                                   self._padding_bottom, self._padding_left)

        return super()._rect_changed(original_rect, new_rect)

    def _size_to_contents_width(self) -> bool:
        return self._width == 0.0

    def _size_to_contents_height(self) -> bool:
        return self._height == 0.0

    def _get_border_rect(self, rect: Rect, content_size: Size, calc_size: bool) -> Rect:
        border_size = rect.get_size()
        if self._size_to_contents_width():
            if self.use_full_width:
                border_size.width = rect.get_width()
            else:
                if calc_size:
                    border_size.width = content_size.width + self._padding_left + self._padding_right + self._border.left_width + self._border.right_width
                else:
                    border_size.width = content_size.width
        else:
            if self._width_to_use == 0.0:
                self._width_to_use = self._width
                if self._width_in_percent:
                    if self._parent_frame is None:
                        frame_width = rect.get_width()
                    else:
                        frame_width = self._parent_frame.get_sizing_bounds().get_width()

                    self._width_to_use = frame_width * (self._width / 100.0)

            border_size.width = self._width_to_use - self._margin_left - self._margin_right

        if self._size_to_contents_height():
            if self.use_full_height:
                border_size.height = rect.get_height()
            else:
                if calc_size:
                    border_size.height = content_size.height + self._padding_top + self._padding_bottom + self._border.top_width + self._border.bottom_width
                else:
                    border_size.height = content_size.height
        else:
            if self._height_to_use == 0.0:
                self._height_to_use = self._height
                if self._height_in_percent:
                    if self._parent_frame is None:
                        frame_height = rect.get_height()
                    else:
                        frame_height = self._parent_frame.get_sizing_bounds().get_height()

                    self._height_to_use = frame_height * (self._height / 100.0)

            border_size.height = self._height_to_use - self._margin_top - self._margin_bottom

        self._border_rect = get_rect_with_size_and_align(rect, border_size, self._h_align, self._v_align)

        return self._border_rect

    def _do_print(self, r: Renderer, in_rect: Rect):
        self._border.draw_border(r, get_rect_with_size_and_align(self._border_rect))

        if self._background != "#FFFFFF":
            r.add_rect(get_rect_with_size_and_align(self._padding_rect), self._background)

        if self._is_current_frame_valid():
            self._get_current_frame().print(r, self._content_rect)

    def add_frame(self, frame: ReportFrame) -> int:
        if self.get_frame_count() > 0:
            self.clear_frames()

        self._frames.append(frame)
        return len(self._frames) - 1

    def to_dict(self, data: dict, frame: dict):
        frame["class"] = "BoxFrame"

        if self.width > 0.0:
            frame["width"] = self.width

        if self.height > 0.0:
            frame["height"] = self.height

        if self.width_in_percent:
            frame["width_in_percent"] = self.width_in_percent

        if self.height_in_percent:
            frame["height_in_percent"] = self.height_in_percent

        if self.padding_left != 0.0:
            frame["padding_left"] = self.padding_left

        if self.padding_top != 0.0:
            frame["padding_top"] = self.padding_top

        if self.padding_right != 0.0:
            frame["padding_right"] = self.padding_right

        if self.padding_bottom != 0.0:
            frame["padding_bottom"] = self.padding_bottom

        b = self.border.to_dict()
        if len(b) > 0:
            frame["border"] = b

        if self.background != "#FFFFFF":
            frame["background"] = self.background

        data[self.frame_id] = frame
        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        super().from_dict(frame)

        if "width" in frame:
            self.width = frame["width"]
        if "height" in frame:
            self.height = frame["height"]
        if "width_in_percent" in frame:
            self.width_in_percent = frame["width_in_percent"]
        if "height_in_percent" in frame:
            self.height_in_percent = frame["height_in_percent"]
        if "padding_left" in frame:
            self.padding_left = frame["padding_left"]
        if "padding_top" in frame:
            self.padding_top = frame["padding_top"]
        if "padding_right" in frame:
            self.padding_right = frame["padding_right"]
        if "padding_bottom" in frame:
            self.padding_bottom = frame["padding_bottom"]

        if "border" in frame:
            border = Border()
            border.from_dict(frame["border"])
            self.border = border

        if "background" in frame:
            self.background = frame["background"]
