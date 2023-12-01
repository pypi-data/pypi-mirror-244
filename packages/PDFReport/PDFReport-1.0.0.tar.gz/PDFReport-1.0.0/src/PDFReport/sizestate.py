from .size import Size


class SizeState:
    def __init__(self):
        self.required_size = Size()
        self.fits = True
        self.continued = False
