class Size:
    def __init__(self, width: float = 0.0, height: float = 0.0, other=None):
        if other is not None:
            self.width = other.width
            self.height = other.height
        else:
            self.width = width
            self.height = height

    def set_size(self, width: float = 0.0, height: float = 0.0):
        self.width = width
        self.height = height
