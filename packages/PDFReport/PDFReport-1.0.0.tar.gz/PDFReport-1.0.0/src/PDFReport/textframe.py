from .textstyle import TextStyle
from .enums import TextAlign

from .rect import Rect, C_EPS
from .globals import get_rect_with_size_and_align
from .renderer import Renderer
from .simpleframe import SimpleFrame
from .containerframe import ContainerFrame
from .sizestate import SizeState


class TextFrame(SimpleFrame):
    """
    Class for a frame containing some text. It is a simple frame with no sub-frames in it.
    A block of text will be printed in a rectangle with a calculated width and height.
    """

    def __init__(self, parent: ContainerFrame, text: str = "", text_style: TextStyle or str = TextStyle.NORMAL,
                 use_full_width: bool = False, text_align: TextAlign = TextAlign.LEFT, wrap_text: bool = True, frame_id: str = ""):
        """
        Create a frame for a text

        :param parent: The container frame to which the text frame belongs
        :param text: The text to put into the frame
        :param text_style: The text-style name or instance (default TextStyle.NORMAL)
        :param use_full_width: Flag if the whole possible width should be used (default False)
        :param text_align: Text alignment (default left)
        :param wrap_text: Flag if the text may be wrapped onto multiple lines (default True)
        :param frame_id: Ident of the frame (optional)
        """
        super().__init__(parent, frame_id)

        self._text = text
        if isinstance(text_style, TextStyle):
            self._text_style = TextStyle("", base_style=text_style.name)
        else:
            self._text_style = TextStyle("", base_style=text_style)

        self._text_align = text_align
        self._wrap_text = wrap_text
        self.use_full_width = use_full_width

        self._text_to_print = ""
        self._text_layout = Rect()
        self._char_index = 0
        self._chars_fitted = 0

    @property
    def text(self) -> str:
        """
        The text to be printed in the frame

        :getter: Returns the text
        :setter: Sets the text
        """
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

    @property
    def text_style(self) -> TextStyle:
        """
        The text-style to be used

        :getter: Returns the text-style
        :setter: Sets the text-style
        """
        return self._text_style

    @text_style.setter
    def text_style(self, text_style: TextStyle or str):
        if isinstance(text_style, TextStyle):
            self._text_style = TextStyle("", base_style=text_style.name)
        elif text_style != "":
            self._text_style = TextStyle("", base_style=text_style)
        else:
            self._text_style = TextStyle("", TextStyle.NORMAL)

    @property
    def text_align(self) -> TextAlign:
        """
        The text-alignment to be used

        :getter: Returns the text-alignment
        :setter: Sets the text-alignment
        """
        return self._text_align

    @text_align.setter
    def text_align(self, text_align: TextAlign):
        self._text_align = text_align

    @property
    def wrap_text(self) -> bool:
        """
        Flag if the text may be wrapped onto multiple lines

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._wrap_text

    @wrap_text.setter
    def wrap_text(self, wrap_text: bool):
        self._wrap_text = wrap_text

    def reset(self):
        super().reset()

    def _do_begin_print(self, r: Renderer):
        self._char_index = 0
        if r.data is not None:
            r.data.on_text_data(self)

    def _get_text_to_print(self, r: Renderer) -> str:
        text = self._text[self._char_index:]
        text = r.replace_page_vars(text)
        if self._char_index > 0:
            text = text.lstrip()

        return text

    def _get_origin(self) -> int:
        origin = 0
        if self._text_align == TextAlign.CENTER:
            origin = -1
        else:
            if self._text_align == TextAlign.RIGHT:
                origin |= 1

        return origin

    def _rect_changed(self, original_rect: Rect, new_rect: Rect) -> SizeState:
        resize = True
        corner = self._get_origin()
        if corner >= 0:
            if self._get_point(original_rect, corner) == self._get_point(new_rect, corner):
                if new_rect.size_fits(self._required_size):
                    resize = False

        if resize:
            self.reset_size(self._keep_together)

        return super()._rect_changed(original_rect, new_rect)

    def _check_text_layout(self, r: Renderer) -> bool:
        font_height = r.get_font_height(self._text_style)
        fits = True

        if round(self._text_layout.get_height(), 3) < round(font_height, 3) or round(self._text_layout.get_width(), 3) < C_EPS:
            fits = False

        return fits

    def _set_text_size(self, r: Renderer, rect: Rect) -> SizeState:
        size_state = SizeState()
        size_state.fits = True
        self._chars_fitted = len(self._text_to_print)

        truncated = False

        if self._text_align == TextAlign.RIGHT or not self._wrap_text:
            required_size = r.calc_text_size(self._text_style, self._text_to_print, self._text_align)
        else:
            if self.use_full_width or self.max_width > 0.0:
                required_size = r.calc_text_size(self._text_style, self._text_to_print, self._text_align, rect.get_width())
            else:
                required_size = r.calc_text_size(self._text_style, self._text_to_print, self._text_align)

        if not rect.width_fits(required_size.width):

            text = self._text_to_print

            if not self._wrap_text and self._text_to_print.find("\n") >= 0:
                self._text_to_print = ""
                lines = text.split("\n")
                for line in lines:
                    size = r.calc_text_size(self._text_style, line, self._text_align)

                    # Cut chars form line of text to reduce the width of text to fit into the rect
                    while size.width > rect.get_width():
                        line = line[0:-1]
                        size = r.calc_text_size(self._text_style, line, self._text_align)

                    if len(self._text_to_print) > 0:
                        self._text_to_print = self._text_to_print + "\n"

                    self._text_to_print = self._text_to_print + line

                self._chars_fitted = len(self._text_to_print)
                required_size.width = r.calc_text_size(self._text_style, self._text_to_print, self._text_align, rect.get_width()).width
            else:

                text = r.trim_text(text, self._text_style, self._wrap_text, rect.get_width(), self._text_align, rect.get_height())
                self._chars_fitted = len(text)

                if self._wrap_text:
                    required_size = r.calc_text_size(self._text_style, text, self._text_align, rect.get_width())
                else:
                    required_size.width = r.calc_text_size(self._text_style, text, self._text_align, rect.get_width()).width
                    if self._chars_fitted < len(self._text_to_print):
                        truncated = True

        if not rect.height_fits(required_size.height):

            text = self._text_to_print
            text = r.trim_text(text, self._text_style, self._wrap_text, rect.get_width(), self._text_align, rect.get_height())
            self._chars_fitted = len(text)
            required_size.height = r.calc_text_size(self._text_style, text, self._text_align, rect.get_width()).height

            if self._chars_fitted < len(self._text_to_print) and not self._wrap_text:
                truncated = True

        if required_size.height == 0.0:
            required_size.height = r.get_font_height(self._text_style)

        if self._chars_fitted < len(self._text_to_print):
            if self._keep_together:
                size_state.fits = False
                self._chars_fitted = 0
                return size_state

            if not truncated:
                size_state.continued = True

        self._text_layout = get_rect_with_size_and_align(rect, required_size, self._h_align, self._v_align, self._text_align)
        size_state.required_size = self._text_layout.get_size()

        return size_state

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        size_state = SizeState()

        self._text_layout = get_rect_with_size_and_align(for_rect)
        if self._check_text_layout(r):
            self._text_to_print = self._get_text_to_print(r)
            size_state = self._set_text_size(r, for_rect)
        else:
            size_state.fits = False
            size_state.continued = True

        return size_state

    def _do_print(self, r: Renderer, in_rect: Rect):
        if self._text_style.background_color != "#FFFFFF":
            background_rect = self._text_layout
            if self.use_full_width:
                background_rect.left = in_rect.left
                background_rect.right = in_rect.get_width()

            if self.use_full_height:
                background_rect.top = in_rect.top
                background_rect.bottom = in_rect.get_height()

            r.add_rect(background_rect, self._text_style.background_color)

        r.add_text_block(self._text_to_print[0:self._chars_fitted], self._text_style, self._text_layout, self._text_align, self.text_style.text_color)

        self._char_index += self._chars_fitted

    @staticmethod
    def _get_point(rect: Rect, corner: int) -> []:
        if (corner & 1) == 0:
            x = rect.left
        else:
            x = rect.right

        if (corner & 2) == 0:
            y = rect.top
        else:
            y = rect.bottom

        point = [x, y]
        return point

    def to_dict(self, data: dict, frame: dict):
        frame["class"] = "TextFrame"
        if self.text != "":
            frame["text"] = self._text

        ts = self.text_style.to_dict()
        if len(ts) > 0:
            frame["text_style"] = ts

        if self.text_align != TextAlign.LEFT:
            frame["text_align"] = self.text_align.value

        if not self.wrap_text:
            frame["wrap_text"] = self.wrap_text

        data[self.frame_id] = frame
        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        super().from_dict(frame)
        if "text" in frame:
            self.text = frame["text"]

        if "text_style" in frame:
            ts = TextStyle("")
            ts.from_dict(frame["text_style"])
            self.text_style = ts

        if "text_align" in frame:
            self.text_align = TextAlign(frame["text_align"])

        if "wrap_text" in frame:
            self.wrap_text = frame["wrap_text"]
