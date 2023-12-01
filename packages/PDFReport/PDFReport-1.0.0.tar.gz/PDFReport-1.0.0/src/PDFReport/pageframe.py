from .containerframe import ContainerFrame
from .rect import Rect
from .renderer import Renderer
from .sizestate import SizeState


class PageFrame(ContainerFrame):
    """
    Container frame for content that should be printed on several pages (e.g. header/footer)
    The frame can be printed on all pages, on odd or on even pages, or an all but the first page
    """

    ON_ALL_PAGES = 0
    ON_ODD_PAGES = -1
    ON_EVEN_PAGES = -2
    ON_ALL_BUT_FIRST_PAGE = -3

    def __init__(self, parent: ContainerFrame, on_page_nr: int = 0, use_full_width: bool = True, frame_id: str = ""):
        """
        Creates a new PageFrame object

        :param parent: Parent frame to which this frame will be added
        :param on_page_nr: Definition on which page this frame will be printed
        :param use_full_width: Flag if the frame may use the full width
        :param frame_id: frame id (optional)
        """
        super().__init__(parent, frame_id)

        self._on_page_nr = on_page_nr
        self.use_full_width = use_full_width

    @property
    def on_page_nr(self) -> int:
        """
        On which page the frame will be printed

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._on_page_nr

    @on_page_nr.setter
    def on_page_nr(self, on_page_nr: int):
        self._on_page_nr = on_page_nr

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        size_state = SizeState()
        rect = Rect(other=for_rect)

        if self.get_frame_count() == 0:
            size_state.fits = True
        else:

            if not self.print_on_page(r):
                return size_state

            for frame in self._frames:
                frame.calc_size(r, rect)

                size_state.required_size.height = max(size_state.required_size.height, frame.get_size().height)
                size_state.required_size.width = max(size_state.required_size.width, frame.get_size().width)
                if frame._continued:
                    size_state.continued = True

                if frame._fits:
                    size_state.fits = True

        return size_state

    def _do_print(self, r: Renderer, in_rect: Rect):
        rect = Rect(other=in_rect)

        if not self.print_on_page(r):
            return

        if not self.use_full_width:
            rect.right = rect.left + self._required_size.width

        for frame in self._frames:
            frame.print(r, rect)
            if frame._continued:
                self.continued = True

    def print_on_page(self, r: Renderer) -> bool:
        page = r.current_page

        if self._on_page_nr > 0:
            if page != self._on_page_nr:
                return False

        elif self._on_page_nr == PageFrame.ON_ODD_PAGES:
            if (page % 2) == 0:
                return False

        elif self._on_page_nr == PageFrame.ON_EVEN_PAGES:
            if (page % 2) == 1:
                return False

        elif self._on_page_nr == PageFrame.ON_ALL_BUT_FIRST_PAGE:
            if page == 1:
                return False

        return True

    def _do_begin_print(self, r: Renderer):
        pass

    def to_dict(self, data: dict, frame: dict):
        frame["class"] = "PageFrame"

        if self.on_page_nr != 0:
            frame["on_page_nr"] = self.on_page_nr

        data[self.frame_id] = frame
        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        super().from_dict(frame)
        if "on_page_nr" in frame:
            self.on_page_nr = frame["on_page_nr"]
