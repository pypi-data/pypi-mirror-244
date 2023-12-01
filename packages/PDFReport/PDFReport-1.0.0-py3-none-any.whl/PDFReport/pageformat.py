from .enums import PageOrientation
from .enums import PageSize


class PageFormat:
    """
    Class to define the format of a page in the pdf report.
    The page formate defines the page size and orientation as well as the surrounding margins of all four sides.
    With these information the printable area can be calculated.
    """

    def __init__(self, page_size: PageSize = PageSize.SIZE_A4, page_orientation: PageOrientation = PageOrientation.PORTRAIT,
                 margin_left: float = 20.0, margin_top: float = 10.0,
                 margin_right: float = 10, margin_bottom: float = 10,
                 mirror_margins: bool = False):

        """
        Create a new PageFormat object

        :param page_size: Pagesize one of the enums of PageSize
        :param page_orientation: Page orientation one of the enums in PageOrientation
        :param margin_left: Left margin in mm
        :param margin_top:  Top margin in mm
        :param margin_right:  Right margin in mm
        :param margin_bottom:  Bottom margin in mm
        :param mirror_margins:  Flag if the margins should be mirrored for even and odd page numbers
        """
        self._page_size = page_size
        self._page_orientation = page_orientation
        self._margin_left = margin_left
        self._margin_top = margin_top
        self._margin_right = margin_right
        self._margin_bottom = margin_bottom
        self._mirror_margins = mirror_margins

    @property
    def page_orientation(self) -> PageOrientation:
        """
        The page orientation

        :getter: Returns the page orientation
        :setter: Sets the page orientation
        """
        return self._page_orientation

    @page_orientation.setter
    def page_orientation(self, page_orientation: PageOrientation):
        self._page_orientation = page_orientation

    @property
    def page_size(self) -> PageSize:
        """
        The page size

        :getter: Returns the page size
        :setter: Sets the page size
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size: PageSize):
        self._page_size = page_size

    @property
    def margin_top(self) -> float:
        """
        The top margin in millimeters

        :getter: Returns the top margin
        :setter: Sets the top margin
        """
        return self._margin_top

    @margin_top.setter
    def margin_top(self, margin_top: float):
        self._margin_top = margin_top

    @property
    def margin_left(self) -> float:
        """
        The left margin in millimeters

        :getter: Returns the left margin
        :setter: Sets the left margin
        """
        return self._margin_left

    @margin_left.setter
    def margin_left(self, margin_left: float):
        self._margin_left = margin_left

    @property
    def margin_right(self) -> float:
        """
        The right margin in millimeters

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
        The bottom margin in millimeters

        :getter: Returns the bottom margin
        :setter: Sets the bottom margin
        """
        return self._margin_bottom

    @margin_bottom.setter
    def margin_bottom(self, margin_bottom: float):
        self._margin_bottom = margin_bottom

    @property
    def mirror_margins(self) -> bool:
        """
        Flag to mirror the left and right margins for even and odd page number

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._mirror_margins

    @mirror_margins.setter
    def mirror_margins(self, mirror_margins: bool):
        self._mirror_margins = mirror_margins

    def to_dict(self) -> dict:
        page_format = {}

        if self.page_size != PageSize.SIZE_A4:
            page_format["page_size"] = self.page_size.value

        if self.page_orientation != PageOrientation.PORTRAIT:
            page_format["page_orientation"] = self.page_orientation.value

        if self.margin_left != 20.0:
            page_format["margin_left"] = self.margin_left

        if self.margin_top != 10.0:
            page_format["margin_top"] = self.margin_top

        if self.margin_right != 10.0:
            page_format["margin_right"] = self.margin_right

        if self.margin_bottom != 10.0:
            page_format["margin_bottom"] = self.margin_bottom

        if self.mirror_margins:
            page_format["mirror_margins"] = self.mirror_margins

        return page_format

    def from_dict(self, page_format: dict):
        if "page_size" in page_format:
            self.page_size = PageSize(page_format["page_size"])

        if "page_orientation" in page_format:
            self.page_orientation = PageOrientation(page_format["page_orientation"])

        if "margin_left" in page_format:
            self.margin_left = page_format["margin_left"]

        if "margin_top" in page_format:
            self.margin_top = page_format["margin_top"]

        if "margin_right" in page_format:
            self.margin_right = page_format["margin_right"]

        if "margin_bottom" in page_format:
            self.margin_bottom = page_format["margin_bottom"]

        if "mirror_margins" in page_format:
            self.mirror_margins = page_format["mirror_margins"]
