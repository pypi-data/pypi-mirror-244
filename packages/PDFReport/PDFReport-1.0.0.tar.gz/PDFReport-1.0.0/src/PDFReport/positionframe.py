from .containerframe import ContainerFrame
from .rect import Rect
from .renderer import Renderer
from .sizestate import SizeState


class PositionFrame(ContainerFrame):
    """
    This class represents a frame that has a fix position on a page
    If the position and size of this frame is free on the current page
    it will be printed on the current page. If there is already some
    output on that spot, the frame will be printed on the next page.
    This can be overwritten by defining the overlay parameter to true.
    """

    def __init__(self, parent: ContainerFrame, offset_left: float = 0.0, offset_top: float = 0.0, overlay: bool = False, frame_id: str = ""):
        """
        Creates a new PositionFrame

        :param parent: Parent frame to which this frame will be added
        :param offset_left: Left position
        :param offset_top: Top position
        :param overlay: Flag if the frame may overlay other frames
        :param frame_id: frame id (optional)
        """
        super().__init__(parent, frame_id)

        self._offset_left = offset_left
        self._offset_top = offset_top
        self._overlay = overlay

    @property
    def offset_top(self) -> float:
        """
        Offset from the top of the paper

        :getter: Returns the top offset in mm
        :setter: Sets the top offset
        """
        return self._offset_top

    @offset_top.setter
    def offset_top(self, offset_top: float):
        self._offset_top = offset_top

    @property
    def offset_left(self) -> float:
        """
        Offset from the left of the paper

        :getter: Returns the left offset in mm
        :setter: Sets the left offset
        """
        return self._offset_left

    @offset_left.setter
    def offset_left(self, offset_left: float):
        self._offset_left = offset_left

    @property
    def overlay(self) -> bool:
        """
        Flag if the frame may overlay other frames

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._overlay

    @overlay.setter
    def overlay(self, overlay: bool):
        self._overlay = overlay

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        size_state = SizeState()

        old_rect = Rect(other=for_rect)
        rect = Rect(other=for_rect)

        if self.get_frame_count() == 0:
            size_state.fits = True
        else:

            if not self._overlay:

                #  The offsets have to be inside the printable area for non overlay PositionFrames
                if self._offset_top < r.get_page_bounds().left or self._offset_left < r.get_page_bounds().top:
                    raise OverflowError("Non overlay PositionFrame is outside the printable area")

                if self._offset_top < for_rect.top or self._offset_left < for_rect.left:
                    size_state.fits = False
                    return size_state

            rect.left = self._offset_left
            rect.top = self._offset_top
            if self._overlay:
                rect.right = r.get_paper_size().width
                rect.bottom = r.get_paper_size().height

            for frame in self._frames:

                frame.calc_size(r, rect)

                size_state.required_size.height = max(size_state.required_size.height, frame.get_size().height)
                size_state.required_size.width = max(size_state.required_size.width, frame.get_size().width)
                if frame._continued:
                    if not self._overlay:
                        size_state.continued = True
                    else:
                        size_state.continued = False

                if frame._fits:
                    size_state.fits = True

        if self._offset_top + size_state.required_size.height - old_rect.top > size_state.required_size.height:
            size_state.required_size.height = self._offset_top + size_state.required_size.height - old_rect.top

        if self._offset_left + size_state.required_size.width - old_rect.left > size_state.required_size.width:
            size_state.required_size.width = self._offset_left + size_state.required_size.width - old_rect.left

        return size_state

    def _do_print(self, r: Renderer, in_rect: Rect):
        rect = Rect(other=in_rect)

        rect.left = self._offset_left
        rect.top = self._offset_top

        for frame in self._frames:

            frame.calc_size(r, rect)

            frame.print(r, rect)
            if frame._continued:
                if not self._overlay:
                    self._continued = True
                else:
                    self._continued = False

    def to_dict(self, data: dict, frame: dict):
        """
        Fills the attribute-values to a dictionary if the attribute has no default value.
        :param data:  global dict for the whole report
        :param frame: dict for the frame
        """
        frame["class"] = "PositionFrame"

        if self.offset_left != 0.0:
            frame["offset_left"] = self.offset_left

        if self.offset_top != 0.0:
            frame["offset_top"] = self.offset_top

        if self.overlay:
            frame["overlay"] = self.overlay

        data[self.frame_id] = frame
        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        """
        Fills the attributes based on the given dict
        :param frame:
        """
        super().from_dict(frame)
        if "offset_left" in frame:
            self.offset_left = frame["offset_left"]

        if "offset_top" in frame:
            self.offset_top = frame["offset_top"]

        if "overlay" in frame:
            self.overlay = frame["overlay"]
