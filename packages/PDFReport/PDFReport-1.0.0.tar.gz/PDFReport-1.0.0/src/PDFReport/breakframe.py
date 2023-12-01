from .pageformat import PageFormat
from .rect import Rect
from .renderer import Renderer
from .simpleframe import SimpleFrame
from .containerframe import ContainerFrame
from .sizestate import SizeState


class BreakFrame(SimpleFrame):
    """
    Class for a forced page break in a report. It is a simple frame with no sub-frames in it.
    After this frame a new page will be started in the report.
    It is possible to change the page format, orientation and margins from the next page on.
    """

    def __init__(self, parent: ContainerFrame, page_format: PageFormat = None, frame_id: str = ""):
        """
        Creates a new BreakFrame object

        :param parent: Parent frame to which this frame will be added
        :param page_format: Page format information for the next section or null if the format should not be changed
        :param frame_id: frame id (optional)
        """
        super().__init__(parent, frame_id)

        self._page_format = page_format

        self._page_number = 0
        self._first_time_called = False

    @property
    def page_format(self) -> PageFormat:
        """
        Page format used for the pages after the page break

        :getter: Returns the page format
        :setter: Sets the page format
        """
        return self._page_format

    @page_format.setter
    def page_format(self, page_format: PageFormat):
        self._page_format = page_format

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        size_state = SizeState()
        size_state.fits = True
        page = r.current_page

        if self._first_time_called:
            self._first_time_called = False

            self._page_number = page
            if self._page_format is not None:
                r.set_page_format(page + 1, self._page_format)

            size_state.continued = True
            size_state.required_size = for_rect.get_size()

        else:
            if page == self._page_number:
                size_state.continued = True
                size_state.required_size = for_rect.get_size()
            else:

                size_state.continued = False
                size_state.required_size.set_size(0, 0)

        return size_state

    def _do_print(self, r: Renderer, in_rect: Rect):
        pass

    def _do_begin_print(self, r: Renderer):
        self._first_time_called = True

    def to_dict(self, data: dict, frame: dict):
        frame["class"] = "BreakFrame"
        if self._page_format is not None:
            pf = self.page_format.to_dict()
            if len(pf) > 0:
                frame["page_format"] = pf

        data[self.frame_id] = frame
        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        super().from_dict(frame)
        if "page_format" in frame:
            page_format = PageFormat()
            page_format.from_dict(frame["page_format"])
            self.page_format = page_format
