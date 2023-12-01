from .enums import LineStyle


class Pen:

    def __init__(self, extent: float = 0.0, line_color: str = "#000000", line_style: LineStyle = LineStyle.SOLID):
        """
        Define a new pen with a given extend, color and line style

        :param extent: Width in mm
        :param line_color: Color hex string
        :param line_style: One of the LineStyle enums
        """
        self._extent = extent
        self._color = line_color
        self._line_style = line_style

    @property
    def extent(self) -> float:
        """
        The extent of the line in millimeters

        :getter: Returns the extent
        :setter: Sets the extent
        """
        return self._extent

    @extent.setter
    def extent(self, extent: float):
        self._extent = extent

    @property
    def color(self) -> str:
        """
        The color of the line

        :getter: Returns the color
        :setter: Sets the color
        """
        return self._color

    @color.setter
    def color(self, color: str):
        self._color = color

    @property
    def line_style(self) -> LineStyle:
        """
        The line style of the line

        :getter: Returns the line style
        :setter: Sets the line style
        """
        return self._line_style

    @line_style.setter
    def line_style(self, line_style: LineStyle):
        self._line_style = line_style

    def __eq__(self, other):
        if not isinstance(other, Pen):
            return False

        if self.extent != other.extent:
            return False

        if self.color != other.color:
            return False

        if self.line_style != other.line_style:
            return False

        return True

    def to_dict(self) -> dict:
        pen = {}

        if self.extent > 0.0:
            pen["extent"] = self.extent
        if self.color != "#000000":
            pen["color"] = self.color
        if self.line_style != LineStyle.SOLID:
            pen["line_style"] = self.line_style.value

        return pen

    def from_dict(self, pen: dict):
        if "extent" in pen:
            self.extent = pen["extent"]

        if "color" in pen:
            self.color = pen["color"]

        if "line_style" in pen:
            self.line_style = LineStyle(pen["line_style"])
