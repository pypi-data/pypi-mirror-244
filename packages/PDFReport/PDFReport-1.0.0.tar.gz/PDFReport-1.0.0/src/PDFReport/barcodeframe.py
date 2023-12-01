import tempfile

import qrcode
from PIL import Image

import barcode
from barcode import *
from barcode.writer import ImageWriter

from .globals import get_rect_with_size_and_align
from .enums import BarcodeType
from .size import Size
from .rect import Rect
from .sizestate import SizeState
from .renderer import Renderer
from .simpleframe import SimpleFrame
from .containerframe import ContainerFrame


class BarcodeFrame(SimpleFrame):
    """
    Class for a frame containing a barcode. It is a simple frame with no sub-frames in it.
    A barcode (e.g. "QRCODE") will be printed in a rectangle with a given width and height.
    """

    def __init__(self, parent: ContainerFrame, barcode_text: str = "", barcode_type: BarcodeType = BarcodeType.QRCODE,
                 max_width: float = 0.0, max_height: float = 0.0, frame_id: str = ""):
        """
        Creates a new BarcodeFrame object

        :param parent: The container frame to which the text frame belongs
        :param barcode_text: Text The data
        :param barcode_type: The barcode type enum BarcodeType
        :param max_width: Width of the barcode
        :param max_height: Height of the barcode
        :param frame_id:
        """
        super().__init__(parent, frame_id)

        self._barcode_text = barcode_text
        self._barcode_type = barcode_type
        self._width = abs(max_width)
        self._height = abs(max_height)

        self.max_width = max_width
        self.max_height = max_height

        self._barcode_rect = Rect()
        self._x = 0.0
        self._y = 0.0

    @property
    def barcode_text(self) -> str:
        """
        The text to be printed as barcode

        :getter: Returns the text
        :setter: Sets the text
        """
        return self._barcode_text

    @barcode_text.setter
    def barcode_text(self, barcode_text: str):
        self._barcode_text = barcode_text

    @property
    def barcode_type(self) -> BarcodeType:
        """
        The barcode type

        :getter: Returns the barcode type
        :setter: Sets the barcode type
        """
        return self._barcode_type

    @barcode_type.setter
    def barcode_type(self, barcode_type: BarcodeType):
        self._barcode_type = barcode_type

    @property
    def width(self) -> float:
        """
        The width for the barcode

        :getter: Returns the width
        :setter: Sets the width
        """
        return self._width

    @width.setter
    def width(self, width: float):
        self._width = abs(width)
        self.max_width = width

    @property
    def height(self) -> float:
        """
        The height for the barcode

        :getter: Returns the height
        :setter: Sets the height
        """
        return self._height

    @height.setter
    def height(self, height: float):
        self._height = abs(height)
        self.max_height = height

    def _set_barcode_pos(self, rect: Rect):
        self._x = rect.left
        self._y = rect.top

        bc_side = min(self._width, self._height)
        if self.barcode_type == BarcodeType.QRCODE:
            if self._height > bc_side:
                delta = self._height - bc_side
                self._y += delta / 2.0
                self._height = bc_side

            if self._width > bc_side:
                delta = self._width - bc_side
                self._x += delta / 2.0
                self._width = bc_side

    def _get_barcode_rect(self, rect: Rect) -> Rect:
        max_size = rect.get_size()
        scale_w = max_size.width / self._width
        scale_h = max_size.height / self._height
        scale = min(scale_w, scale_h)
        scale_w = scale
        scale_h = scale
        self._width = scale_w * self._width
        self._height = scale_h * self._height
        bc_size = Size(self._width, self._height)

        self._set_barcode_pos(rect)

        return get_rect_with_size_and_align(rect, bc_size, self._h_align, self._v_align)

    def _rect_changed(self, original_rect: Rect, new_rect: Rect) -> SizeState:
        self._set_barcode_pos(new_rect)
        return super()._rect_changed(original_rect, new_rect)

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        size_state = SizeState()
        self._barcode_rect = self._get_barcode_rect(for_rect)
        size_state.required_size = self._barcode_rect.get_size()
        size_state.fits = for_rect.size_fits(size_state.required_size)
        size_state.continued = False
        return size_state

    def _do_print(self, r: Renderer, in_rect: Rect):

        filename = tempfile.gettempdir() + f"/barcode_{self.frame_id}.png"

        if self._barcode_type == BarcodeType.QRCODE:
            qr = qrcode.QRCode(border=0)
            qr.add_data(self._barcode_text)
            qr.make()
            img = qr.make_image()
            img.save(filename)
            image = Image.open(filename)
            r.add_image(image, self._x, self._y, self._width, self._height)
            os.remove(filename)

        elif self._barcode_type == BarcodeType.CODE39:
            with open(filename, "wb") as f:
                barcode.Code39(self._barcode_text, writer=ImageWriter()).write(f)
                f.close()
                r.add_image(filename, self._x, self._y, self._width, self._height)
                os.remove(filename)

        elif self._barcode_type == BarcodeType.CODE128:
            with open(filename, "wb") as f:
                barcode.Code128(self._barcode_text, writer=ImageWriter()).write(f)
                f.close()
                r.add_image(filename, self._x, self._y, self._width, self._height)
                os.remove(filename)

        elif self._barcode_type == BarcodeType.EAN13:
            with open(filename, "wb") as f:
                barcode.EAN13(self._barcode_text, writer=ImageWriter()).write(f)
                f.close()
                r.add_image(filename, self._x, self._y, self._width, self._height)
                os.remove(filename)

        elif self._barcode_type == BarcodeType.EAN8:
            with open(filename, "wb") as f:
                barcode.EAN8(self._barcode_text, writer=ImageWriter()).write(f)
                f.close()
                r.add_image(filename, self._x, self._y, self._width, self._height)
                os.remove(filename)

        elif self._barcode_type == BarcodeType.EAN14:
            with open(filename, "wb") as f:
                barcode.EAN14(self._barcode_text, writer=ImageWriter()).write(f)
                f.close()
                r.add_image(filename, self._x, self._y, self._width, self._height)
                os.remove(filename)

        elif self._barcode_type == BarcodeType.ISBN13:
            with open(filename, "wb") as f:
                barcode.ISBN13(self._barcode_text, writer=ImageWriter()).write(f)
                f.close()
                r.add_image(filename, self._x, self._y, self._width, self._height)
                os.remove(filename)

        elif self._barcode_type == BarcodeType.ISBN10:
            with open(filename, "wb") as f:
                barcode.ISBN10(self._barcode_text, writer=ImageWriter()).write(f)
                f.close()
                r.add_image(filename, self._x, self._y, self._width, self._height)
                os.remove(filename)

        elif self._barcode_type == BarcodeType.ISSN:
            with open(filename, "wb") as f:
                barcode.ISSN(self._barcode_text, writer=ImageWriter()).write(f)
                f.close()
                r.add_image(filename, self._x, self._y, self._width, self._height)
                os.remove(filename)

        elif self._barcode_type == BarcodeType.UPCA:
            with open(filename, "wb") as f:
                barcode.UPCA(self._barcode_text, writer=ImageWriter()).write(f)
                f.close()
                r.add_image(filename, self._x, self._y, self._width, self._height)
                os.remove(filename)

    def _do_begin_print(self, r: Renderer):
        pass

    def reset(self):
        super().reset()

    def to_dict(self, data: dict, frame: dict):
        frame["class"] = "BarcodeFrame"
        frame["barcode_type"] = self.barcode_type.value

        if self.barcode_text != "":
            frame["barcode_text"] = self.barcode_text

        if self.width > 0.0:
            frame["width"] = self.width

        if self.height > 0.0:
            frame["height"] = self.height

        data[self.frame_id] = frame
        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        super().from_dict(frame)
        self.barcode_type = BarcodeType(frame["barcode_type"])
        if "barcode_text" in frame:
            self.barcode_text = frame["barcode_text"]

        if "width" in frame:
            self.width = frame["width"]

        if "height" in frame:
            self.height = frame["height"]
