from .size import Size


C_EPS = 0.001


class Rect:

    def __init__(self, left: float = 0.0, top: float = 0.0, right: float = 0.0, bottom: float = 0.0, other=None):
        if other is not None:
            self.left = other.left
            self.top = other.top
            self.right = other.right
            self.bottom = other.bottom
        else:
            self.left = left
            self.top = top
            self.right = right
            self.bottom = bottom

    def get_width(self) -> float:
        return self.right - self.left

    def get_height(self) -> float:
        return self.bottom - self.top

    def get_size(self) -> Size:
        return Size(self.get_width(), self.get_height())

    def is_empty(self) -> bool:
        return (self.get_width() <= C_EPS) and (self.get_height() <= C_EPS)

    def size_fits(self, size: Size) -> bool:
        h = size.height - self.get_height()
        w = size.width - self.get_width()
        return not (h > C_EPS or w > C_EPS)

    def width_fits(self, width: float) -> bool:
        w = width - self.get_width()
        return not (w > C_EPS)

    def height_fits(self, height: float) -> bool:
        h = height - self.get_height()
        return not (h > C_EPS)

    def is_equal_to(self, rect) -> bool:
        return (self.coord_equal(self.left, rect.left) and self.coord_equal(self.top, rect.top) and
                self.coord_equal(self.right, rect.right) and self.coord_equal(self.bottom, rect.bottom))

    @staticmethod
    def coord_equal(a: float, b: float) -> bool:
        if a > b:
            return (a - b) < C_EPS
        else:
            return (b - a) < C_EPS
