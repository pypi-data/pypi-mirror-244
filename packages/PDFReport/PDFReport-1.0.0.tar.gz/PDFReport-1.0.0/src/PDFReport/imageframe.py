import os
from PIL import Image

from .rect import Rect
from .globals import get_rect_with_size_and_align
from .renderer import Renderer
from .simpleframe import SimpleFrame
from .containerframe import ContainerFrame
from .size import Size
from .sizestate import SizeState


class ImageFrame(SimpleFrame):
    """
    Class for a frame containing an image. It is a simple frame with no sub-frames in it.
    An image (jpeg, png) will be printed in a rectangle with a given width and height.
    """

    def __init__(self, parent: ContainerFrame, filename: str = "", max_width: float = 0.0, max_height: float = 0.0, keep_aspect_ratio: bool = True, frame_id: str = ""):
        """
        Creates a new ImageFrame object

        :param parent: Parent frame to which this frame will be added
        :param filename: Image file
        :param max_width: max width of the image in the printed report
        :param max_height: max height of the image in the printed report
        :param keep_aspect_ratio: Flag if the image may be stretched or not
        :param frame_id: frame id (optional)
        """
        super().__init__(parent, frame_id)

        self._image = None
        self._filename = ""
        self._keep_aspect_ratio = keep_aspect_ratio
        if filename != "":
            self.filename = filename

        self.max_width = max_width
        self.max_height = max_height

        self._width = 0.0
        self._height = 0.0
        self._imageRect = Rect()

    @property
    def filename(self) -> str:
        """
        Image filename

        :getter: Returns the filename
        :setter: Sets the filename
        """
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        self._filename = filename

    @property
    def keep_aspect_ratio(self) -> bool:
        """
        Flag if the aspect ratio should be kept

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._keep_aspect_ratio

    @keep_aspect_ratio.setter
    def keep_aspect_ratio(self, preserve_aspect_ratio: bool):
        self._keep_aspect_ratio = preserve_aspect_ratio

    def _get_image_rect(self, rect: Rect) -> Rect:
        max_size = rect.get_size()
        scale_w = max_size.width / self._width
        scale_h = max_size.height / self._height
        if self._keep_aspect_ratio:
            scale = min(scale_w, scale_h)
            scale_w = scale
            scale_h = scale

        width = scale_w * self._width
        height = scale_h * self._height
        img_size = Size(width, height)

        return get_rect_with_size_and_align(rect, img_size, self._h_align, self._v_align)

    def _rect_changed(self, original_rect: Rect, new_rect: Rect) -> SizeState:
        self._imageRect = self._get_image_rect(new_rect)

        size_state = SizeState()
        size_state.required_size = self._imageRect.get_size()
        size_state.fits = new_rect.size_fits(size_state.required_size)
        size_state.continued = False
        return size_state

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        size_state = SizeState()
        self._imageRect = self._get_image_rect(for_rect)
        size_state.required_size = self._imageRect.get_size()
        size_state.fits = for_rect.size_fits(size_state.required_size)
        size_state.continued = False
        return size_state

    def _do_print(self, r: Renderer, in_rect: Rect):
        if self._image is not None:
            r.add_image(self._image, self._imageRect.left, self._imageRect.top, self._imageRect.get_width(), self._imageRect.get_height())

    def _do_begin_print(self, r: Renderer):
        self._width = 1
        self._height = 1
        self._image = None

        if os.path.exists(self.filename):
            self._image = Image.open(self.filename)
        else:
            raise FileNotFoundError("Image file does not exist: ")

        self._width, self._height = self._image.size

    def reset(self):
        super().reset()

    def to_dict(self, data: dict, frame: dict):
        frame["class"] = "ImageFrame"

        if self.filename != "":
            frame["filename"] = self.filename

        if not self.keep_aspect_ratio:
            frame["keep_aspect_ratio"] = self.keep_aspect_ratio

        data[self.frame_id] = frame
        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        super().from_dict(frame)
        if "filename" in frame:
            self.filename = frame["filename"]

        if "keep_aspect_ratio" in frame:
            self.keep_aspect_ratio = frame["keep_aspect_ratio"]
