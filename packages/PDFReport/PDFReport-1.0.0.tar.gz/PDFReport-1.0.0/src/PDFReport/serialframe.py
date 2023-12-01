from .enums import Direction
from .enums import HAlign
from .containerframe import ContainerFrame
from .rect import Rect
from .renderer import Renderer
from .size import Size
from .sizestate import SizeState


class SerialFrame(ContainerFrame):
    """
    Container class to group other frames vertically or horizontally
    This is a frame container for a series of frames that will be printed
    one after the other.
    """

    def __init__(self, parent: ContainerFrame = None, direction: Direction = Direction.VERTICAL, margin_bottom: float = 0.0, margin_right: float = 0.0,
                 margin_top: float = 0.0, margin_left: float = 0.0, use_full_width: bool = False, frame_id: str = ""):
        """
        Creates a new container for horizontally or vertically grouped frames

        :param parent: Parent frame to which this frame will be added
        :param direction: One of the Direction enums
        :param margin_bottom: Bottom margin (inherited from ReportFrame)
        :param margin_right: Right margin (inherited from ReportFrame)
        :param margin_top: top margin (inherited from ReportFrame)
        :param margin_left: left margin (inherited from ReportFrame)
        :param use_full_width: flag if the full width will be used (inherited from ReportFrame)
        :param frame_id: frame id (optional)
        """
        super().__init__(parent, frame_id)
        self._direction = direction

        self.margin_bottom = margin_bottom
        self.margin_right = margin_right
        self.margin_left = margin_left
        self.margin_top = margin_top
        self.use_full_width = use_full_width

    @property
    def direction(self) -> Direction:
        """
        Direction of the frame

        :getter: Returns the direction
        :setter: Sets the direction
        """
        return self._direction

    @direction.setter
    def direction(self, direction: Direction):
        self._direction = direction

    def _advance_pointers(self, size: Size, rect: Rect, required_size: Size):
        match self._direction:
            case Direction.VERTICAL:
                rect.top += size.height
                required_size.height += size.height
                required_size.width = max(required_size.width, size.width)

            case Direction.HORIZONTAL:
                rect.left += size.width
                required_size.width += size.width
                required_size.height = max(required_size.height, size.height)

    def _size_print_frames(self, r: Renderer, in_rect: Rect, size_only: bool, advance_section_index: bool) -> SizeState:
        rect = Rect(other=in_rect)
        size_states = SizeState()
        size_states.fits = False

        saved_frame_index = self._currentFrameIndex

        save_idx = -1
        while self._currentFrameIndex < self.get_frame_count():
            delta = 0.0

            if self._direction == Direction.HORIZONTAL and self._get_current_frame()._h_align == HAlign.RIGHT:

                curr_idx = self._currentFrameIndex
                self._currentFrameIndex += 1
                while self._currentFrameIndex < self.get_frame_count():
                    self._get_current_frame().calc_size(r, rect)
                    delta += self._get_current_frame().get_size().width
                    self._currentFrameIndex += 1

                self._currentFrameIndex = curr_idx
                rect.right -= delta

            self._get_current_frame().calc_size(r, rect)
            if self._get_current_frame()._fits:
                size_states.fits = True

                if not size_only:
                    self._get_current_frame().print(r, rect)

                self._advance_pointers(self._get_current_frame().get_size(), rect, size_states.required_size)
                if self._get_current_frame()._continued and (
                        self._direction != Direction.HORIZONTAL or self._currentFrameIndex >= self.get_frame_count() - 1):

                    if save_idx >= 0:
                        self._currentFrameIndex = save_idx

                    break
                else:

                    if self._get_current_frame()._continued and save_idx < 0:
                        save_idx = self._currentFrameIndex

                    self._currentFrameIndex += 1
                    rect.right += delta

            else:
                self._get_current_frame().reset_size(self._get_current_frame()._keep_together)
                break

        if save_idx >= 0:
            size_states.continued = save_idx < self.get_frame_count()
            self._currentFrameIndex = save_idx
        else:
            size_states.continued = self._currentFrameIndex < self.get_frame_count()

        if self._currentFrameIndex == saved_frame_index and not size_states.continued:
            size_states.fits = True

        if not advance_section_index:
            self._currentFrameIndex = saved_frame_index

        return size_states

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        return self._size_print_frames(r, for_rect, True, False)

    def _do_print(self, r: Renderer, in_rect: Rect):
        rect = Rect(other=in_rect)
        if not self.use_full_width:
            rect.right = rect.left + self._required_size.width

        if not self.use_full_height:
            rect.bottom = rect.top + self._required_size.height

        self._size_print_frames(r, rect, False, True)

    def _do_begin_print(self, r: Renderer):
        super()._do_begin_print(r)
        self._currentFrameIndex = 0

    def to_dict(self, data: dict, frame: dict):
        """
        Fills the attribute-values to a dictionary if the attribute has no default value.
        :param data:  global dict for the whole report
        :param frame: dict for the frame
        """
        frame["class"] = "SerialFrame"

        if self.direction != Direction.VERTICAL:
            frame["direction"] = self.direction.value

        data[self.frame_id] = frame
        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        """
        Fills the attributes based on the given dict
        :param frame:
        """
        if "direction" in frame:
            self.direction = Direction(frame["direction"])

        super().from_dict(frame)
