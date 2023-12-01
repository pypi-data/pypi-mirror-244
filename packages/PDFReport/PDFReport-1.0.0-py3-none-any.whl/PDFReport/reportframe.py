from abc import ABCMeta

from .enums import HAlign
from .enums import VAlign
from .rect import Rect
from .renderer import Renderer
from .size import Size
from .sizestate import SizeState
from .globals import get_rect_with_size_and_align
from .globals import get_rect_with_margins


class ReportFrame(metaclass=ABCMeta):

    def __init__(self):
        self._frame_id = ""
        self._parent_frame = None

        self._h_align = HAlign.LEFT
        self._v_align = VAlign.TOP
        self._margin_left = 0.0
        self._margin_top = 0.0
        self._margin_right = 0.0
        self._margin_bottom = 0.0
        self._use_full_height = False
        self._use_full_width = False
        self._keep_together = False
        self._max_width = 0.0
        self._max_height = 0.0

        self._continued = False
        self._fits = True
        self._sized = False
        self._started_printing = False
        self._sizing_bounds = None
        self._size = None
        self._required_size = None

    @property
    def frame_id(self) -> str:
        """
        The frame id

        :getter: Returns the frame id
        :setter: Sets the frame id
        """
        return self._frame_id

    @frame_id.setter
    def frame_id(self, frame_id: str):
        self._frame_id = frame_id

    @property
    def parent_frame(self):
        """
        The parent frame

        :getter: Returns the parent frame
        :setter: Sets the parent frame
        """
        return self._parent_frame

    @parent_frame.setter
    def parent_frame(self, parent_frame):
        self._parent_frame = parent_frame

    @property
    def h_align(self) -> HAlign:
        """
        Horizontal alignment of the frame

        :getter: Returns the horizontal alignment of the frame
        :setter: Sets the horizontal alignment of the frame
        """
        return self._h_align

    @h_align.setter
    def h_align(self, h_align: HAlign):
        self._h_align = h_align

    @property
    def v_align(self) -> VAlign:
        """
        Vertical alignment of the frame

        :getter: Returns the vertical alignment of the frame
        :setter: Sets the vertical alignment of the frame
        """
        return self._v_align

    @v_align.setter
    def v_align(self, v_align: VAlign):
        self._v_align = v_align

    @property
    def use_full_height(self) -> bool:
        """
        Flag if the frame shall use the full possible height for the frame

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._use_full_height

    @use_full_height.setter
    def use_full_height(self, use_full_height: bool):
        self._use_full_height = use_full_height

    @property
    def use_full_width(self) -> bool:
        """
        Flag if the frame shall use the full possible width for the frame

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._use_full_width

    @use_full_width.setter
    def use_full_width(self, use_full_width: bool):
        self._use_full_width = use_full_width

    @property
    def margin_left(self) -> float:
        """
        Left margin in the frame

        :getter: Returns the left margin
        :setter: Sets the left margin
        """
        return self._margin_left

    @margin_left.setter
    def margin_left(self, margin_left: float):
        self._margin_left = margin_left

    @property
    def margin_top(self) -> float:
        """
        Top margin in the frame

        :getter: Returns the top margin
        :setter: Sets the top margin
        """
        return self._margin_top

    @margin_top.setter
    def margin_top(self, margin_top: float):
        self._margin_top = margin_top

    @property
    def margin_right(self) -> float:
        """
        Right margin in the frame

        :getter: Returns the right margin
        :setter: Sets the right margin
        """
        return self._margin_right

    @margin_right.setter
    def margin_right(self, margin_right: float):
        self._margin_right = margin_right

    @property
    def margin_bottom(self) -> float:
        """
        Bottom margin in the frame

        :getter: Returns the bottom margin
        :setter: Sets the bottom margin
        """
        return self._margin_bottom

    @margin_bottom.setter
    def margin_bottom(self, margin_bottom: float):
        self._margin_bottom = margin_bottom

    @property
    def max_width(self) -> float:
        """
        Maximal width for the frame

        :getter: Returns the maximal width
        :setter: Sets the maximal width
        """
        return self._max_width

    @max_width.setter
    def max_width(self, max_width: float):
        self._max_width = abs(max_width)

    @property
    def max_height(self) -> float:
        """
        Maximal height for the frame

        :getter: Returns the maximal height
        :setter: Sets the maximal height
        """
        return self._max_height

    @max_height.setter
    def max_height(self, max_height: float):
        self._max_height = abs(max_height)

    @property
    def keep_together(self) -> bool:
        """
        Flag if the frame shall be kept together on one page

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._keep_together

    @keep_together.setter
    def keep_together(self, keep_together: bool):
        self._keep_together = keep_together

    def set_margin(self, margin: float):
        """
        Sets the margin on all four sides to the given value

        :param margin: Margin in mm
        """
        self._margin_top = margin
        self._margin_right = margin
        self._margin_bottom = margin
        self._margin_left = margin

    @property
    def continued(self) -> bool:
        return self._continued

    @continued.setter
    def continued(self, continued: bool):
        self._continued = continued

    @property
    def fits(self) -> bool:
        return self._fits

    def get_sizing_bounds(self) -> Rect:
        if self._sizing_bounds is not None:
            return self._sizing_bounds
        return Rect()

    def get_size(self) -> Size:
        if self._size is not None:
            return self._size
        return Size()

    def reset_size(self, keep_together: bool):
        self._sized = False

    def reset(self):
        self._started_printing = False
        self._sized = False
        self._fits = False
        self._continued = False

    def begin_print(self, r: Renderer):
        if not self._started_printing:
            self._do_begin_print(r)
            self._started_printing = True

    def calc_size(self, r: Renderer, rect: Rect):
        self.begin_print(r)
        if not self._sized:
            self._sizing_bounds = self.limit_bounds(rect)
            values = self._do_calc_size(r, self._sizing_bounds)
            self.set_size(values.required_size, rect)
            if self._keep_together and values.continued:
                self._fits = False

                if r.get_page_bounds().is_equal_to(rect):

                    # There is no way to print this report.
                    raise OverflowError("Keep together frame bigger than one page!")

            else:
                self._fits = values.fits

                #  If the frame does not fit, check if there is any space at all
                if not self._fits:
                    if rect.is_empty() or rect.get_width() == 0.0:

                        #  There is no way to print this report.
                        raise OverflowError("No space left in frame for another frame!")

            self._continued = values.continued
            self._sized = True

    def print(self, r: Renderer, rect: Rect):
        printing_bounds = self.limit_bounds(rect)
        if self._sized and not printing_bounds.is_equal_to(self._sizing_bounds):
            values = self._rect_changed(self._sizing_bounds, printing_bounds)
            self.set_size(values.required_size, rect)
            self._fits = values.fits
            self._continued = values.continued

        self.calc_size(r, rect)
        if self._fits:
            self._do_print(r, printing_bounds)

        self.reset_size(self._keep_together)

    def limit_bounds(self, to_rect: Rect) -> Rect:
        rect = Rect(other=to_rect)
        if 0.0 < self._max_width < rect.get_width():
            rect = get_rect_with_size_and_align(rect, Size(self._max_width, rect.get_height()), self._h_align, self._v_align)

        if 0.0 < self._max_height < rect.get_height():
            rect = get_rect_with_size_and_align(rect, Size(rect.get_width(), self._max_height), self._h_align, self._v_align)

        margin_left = 0.0
        margin_top = 0.0
        margin_right = 0.0
        margin_bottom = 0.0

        if self._h_align == HAlign.LEFT:
            margin_left = self._margin_left
        elif self._h_align == HAlign.CENTER:
            margin_left = self._margin_left
            margin_right = self._margin_right
        elif self._h_align == HAlign.RIGHT:
            margin_right = self._margin_right

        if self._v_align == VAlign.TOP:
            margin_top = self._margin_top
        elif self._v_align == VAlign.MIDDLE:
            margin_top = self._margin_top
            margin_bottom = self._margin_bottom
        elif self._v_align == VAlign.BOTTOM:
            margin_bottom = self._margin_bottom

        return get_rect_with_margins(rect, margin_top, margin_right, margin_bottom, margin_left)

    def set_size(self, required_size: Size, rect: Rect):
        self._required_size = Size(other=required_size)
        self._size = Size()
        if self._use_full_width:
            self._size.width = rect.get_width()
        else:
            self._size.width = self._required_size.width + self._margin_left + self._margin_right

        if self._use_full_height:
            self._size.height = rect.get_height()
        else:
            self._size.height = self._required_size.height + self._margin_top + self._margin_bottom

        if self._max_width > 0.0:
            self._size.width = min(self._size.width, self._max_width)
            self._size.width = min(self._size.width, rect.get_width())

        if self._max_height > 0.0:
            self._size.height = min(self._size.height, self._max_height)
            self._size.height = min(self._size.height, rect.get_height())

    def _rect_changed(self, original_rect: Rect, new_rect: Rect) -> SizeState:
        size_state = SizeState()
        size_state.fits = self._fits
        size_state.continued = self._continued
        size_state.required_size = Size(other=self._required_size)
        return size_state

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        pass

    def _do_print(self, vr: Renderer, in_rect: Rect):
        pass

    def _do_begin_print(self, r: Renderer):
        pass

    def to_dict(self, data: dict, frame: dict):
        if self._parent_frame is not None:
            frame["parent_id"] = self._parent_frame.frame_id

        if self._h_align != HAlign.LEFT:
            frame["h_align"] = self._h_align.value

        if self._v_align != VAlign.TOP:
            frame["v_align"] = self._v_align.value

        if self._margin_left != 0.0:
            frame["margin_left"] = self._margin_left

        if self._margin_top != 0.0:
            frame["margin_top"] = self._margin_top

        if self._margin_right != 0.0:
            frame["margin_right"] = self._margin_right

        if self._margin_bottom != 0.0:
            frame["margin_bottom"] = self._margin_bottom

        if self._use_full_height:
            frame["use_full_height"] = self._use_full_height

        if self._use_full_width:
            frame["use_full_width"] = self._use_full_width

        if self._keep_together:
            frame["keep_together"] = self._keep_together

        if self._max_width > 0.0:
            frame["max_width"] = self._max_width

        if self._max_height > 0.0:
            frame["max_height"] = self._max_height

    def from_dict(self, frame: dict):
        if "h_align" in frame:
            self._h_align = HAlign(frame["h_align"])

        if "v_align" in frame:
            self._v_align = VAlign(frame["v_align"])

        if "margin_left" in frame:
            self._margin_left = frame["margin_left"]

        if "margin_top" in frame:
            self._margin_top = frame["margin_top"]

        if "margin_right" in frame:
            self._margin_right = frame["margin_right"]

        if "margin_bottom" in frame:
            self._margin_bottom = frame["margin_bottom"]

        if "use_full_height" in frame:
            self._use_full_height = frame["use_full_height"]

        if "use_full_width" in frame:
            self._use_full_width = frame["use_full_width"]

        if "keep_together" in frame:
            self._keep_together = frame["keep_together"]

        if "max_width" in frame:
            self._max_width = frame["max_width"]

        if "max_height" in frame:
            self._max_height = frame["max_height"]
