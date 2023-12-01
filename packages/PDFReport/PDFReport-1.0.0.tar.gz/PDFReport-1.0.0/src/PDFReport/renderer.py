from PIL import Image
from fpdf import FPDF, enums

from .enums import TextAlign
from .enums import PageOrientation
from .enums import PageSize
from .enums import LineStyle
from .rect import Rect
from .size import Size
from .pageformat import PageFormat
from .textstyle import TextStyle
from .reportdata import ReportData

CELL_HEIGHT_RATIO = 1.25


class Renderer:

    def __init__(self, page_format: PageFormat, report_data: ReportData):
        self._pdf = None

        self._current_page = 0
        self._total_pages = 0
        self._pages_counted = False
        self._page_formats = {0: page_format}

        self._data = report_data

    @property
    def data(self) -> ReportData:
        return self._data

    @property
    def current_page(self) -> int:
        return self._current_page

    @property
    def total_pages(self) -> int:
        return self._total_pages

    @property
    def pages_counted(self) -> bool:
        return self._pages_counted

    @pages_counted.setter
    def pages_counted(self, pages_counted: bool):
        self._pages_counted = pages_counted

    def get_page_format(self, page_nr: int) -> PageFormat:
        while page_nr not in self._page_formats:
            page_nr -= 1
        if page_nr in self._page_formats:
            return self._page_formats[page_nr]
        return self._page_formats[0]

    def get_page_bounds(self, page_nr: int = 0) -> Rect:
        if page_nr == 0:
            page_nr = self.current_page

        page_format = self.get_page_format(page_nr)
        paper_size = self.get_paper_size(page_nr)

        if page_format.mirror_margins:
            if page_nr % 2 == 0:
                page_bounds = Rect(page_format.margin_right, page_format.margin_top,
                                   paper_size.width - page_format.margin_left,
                                   paper_size.height - page_format.margin_bottom)
            else:
                page_bounds = Rect(page_format.margin_left, page_format.margin_top,
                                   paper_size.width - page_format.margin_right,
                                   paper_size.height - page_format.margin_bottom)
        else:
            page_bounds = Rect(page_format.margin_left, page_format.margin_top,
                               paper_size.width - page_format.margin_right,
                               paper_size.height - page_format.margin_bottom)

        return page_bounds

    def get_paper_size(self, page_nr: int = 0) -> Size:
        if page_nr == 0:
            page_nr = self.current_page

        page_format = self.get_page_format(page_nr)

        w = 210.0
        h = 297.0

        if page_format.page_size == PageSize.SIZE_A3:
            w = 297.0
            h = 420.0
        elif page_format.page_size == PageSize.SIZE_A5:
            w = 148.0
            h = 210.0

        elif page_format.page_size == PageSize.SIZE_LETTER:
            w = 215.9
            h = 279.4

        elif page_format.page_size == PageSize.SIZE_LEGAL:
            w = 215.9
            h = 355.6

        if page_format.page_orientation == PageOrientation.PORTRAIT:
            paper_size = Size(round(w, 2), round(h, 2))
        else:
            paper_size = Size(round(h, 2), round(w, 2))
        return paper_size

    def get_printable_width(self, page_nr: int = 0) -> float:
        return self.get_page_bounds(page_nr).get_width()

    def get_printable_height(self, page_nr: int = 0) -> float:
        return self.get_page_bounds(page_nr).get_height()

    def set_page_format(self, from_page: int, page_format: PageFormat):
        self._page_formats[from_page] = page_format

    def create_new_pdf(self):
        self._pdf = FPDF()
        self._pdf.set_auto_page_break(False)
        self._pdf.set_margin(0.0)
        self._pdf.c_margin = 0.0

        self._current_page = 0
        if not self._pages_counted:
            self._total_pages = 0

        self.add_page()

    def add_page(self):
        self._current_page += 1
        if not self._pages_counted:
            self._total_pages += 1

        page_format = self.get_page_format(self._current_page)
        self._pdf.add_page(page_format.page_orientation.value, page_format.page_size.value)

    def replace_page_vars(self, var_text: str) -> str:
        if var_text.find("[VAR_PAGE]"):
            var_text = var_text.replace("[VAR_PAGE]", str(self._current_page))

        if var_text.find("[VAR_TOTAL_PAGES]"):
            var_text = var_text.replace("[VAR_TOTAL_PAGES]", str(self._total_pages))

        return var_text

    def output(self, filename: str):
        self._pdf.output(filename)

    def add_line(self, x1: float, y1: float, x2: float, y2: float, width: float, line_style: LineStyle, color: str):
        self._pdf.set_draw_color(self.get_color_array(color))
        self._pdf.set_line_width(width)

        if line_style == LineStyle.SOLID:
            self._pdf.set_dash_pattern()
        elif line_style == LineStyle.DASH:
            self._pdf.set_dash_pattern(12 * width, 4 * width)
        elif line_style == LineStyle.DOT:
            self._pdf.set_dash_pattern(width, 4 * width)

        self._pdf.line(x1, y1, x2, y2)
        self._pdf.set_draw_color(self.get_color_array(color))
        self._pdf.set_dash_pattern()

    def add_rect(self, rect: Rect, fill_color: str = "#C0C0C0"):
        self._pdf.set_fill_color(self.get_color_array(fill_color))
        rect_style = 'F'
        self._pdf.rect(rect.left, rect.top, rect.get_width(), rect.get_height(), rect_style)

    def get_font_height(self, text_style: TextStyle) -> float:
        font_style = self.get_style(text_style)
        self._pdf.set_font(text_style.font_family, font_style, text_style.font_size)
        return self._pdf.font_size * CELL_HEIGHT_RATIO

    def calc_text_size(self, text_style: TextStyle, text_to_print: str, text_align: TextAlign = TextAlign.LEFT, max_width: float = 0.0) -> Size:
        size = Size()
        font_height = self.get_font_height(text_style)

        if max_width != 0.0:
            align = self.get_align(text_align)
            lns = self._pdf.multi_cell(max_width, None, text_to_print, 0, align, False, dry_run=True, output=enums.MethodReturnValue.LINES)
            size.height = len(lns) * font_height
            size.width = max_width
        else:
            ls = text_to_print.split("\n")
            max_width = 0.0
            for line in ls:
                w = self._pdf.get_string_width(line)
                if w > max_width:
                    max_width = w

            size.width = max_width * 1.01
            align = self.get_align(text_align)
            lns = self._pdf.multi_cell(self.get_printable_width(), None, text_to_print, 0, align, False, dry_run=True, output=enums.MethodReturnValue.LINES)
            size.height = len(lns) * font_height
        return size

    def trim_text(self, text_to_print: str, text_style: TextStyle, wrap_text: bool, width: float,
                  text_align: TextAlign = TextAlign.LEFT, height: float = 0.0) -> str:

        font_style = self.get_style(text_style)
        self._pdf.set_font(text_style.font_family, font_style, text_style.font_size)

        start_len = len(text_to_print)
        if start_len == 0 or not wrap_text:
            return text_to_print

        if height < 0.0:
            return ""
        elif height == 0.0:
            text_width = self._pdf.get_string_width(text_to_print)

            if round(text_width, 2) > round(width, 2):
                text_len = len(text_to_print)
                factor = 0.5
                correction = 0.5
                last_text = text_to_print

                while True:
                    correction /= 2.0

                    check_text = text_to_print[0:int(text_len * factor)]
                    text_width = self._pdf.get_string_width(check_text)

                    if round(text_width, 2) <= round(width, 2):
                        if len(check_text) == len(last_text):
                            text_to_print = check_text
                            break

                        last_text = check_text
                        factor = factor + correction
                    else:
                        factor = factor - correction

        else:

            text_height = self.calc_text_size(text_style, text_to_print, text_align, width)
            if round(text_height.height, 2) > round(height, 2):
                text_len = len(text_to_print)
                factor = 0.5
                correction = 0.5
                last_text = text_to_print
                while True:
                    correction /= 2.0

                    check_text = text_to_print[0:int(text_len * factor)]
                    text_height = self.calc_text_size(text_style, check_text, text_align, width)

                    if round(text_height.height, 2) <= round(height, 2):
                        if len(check_text) == len(last_text):
                            text_to_print = check_text
                            break

                        last_text = check_text
                        factor = factor + correction
                    else:
                        factor = factor - correction

        if len(text_to_print) != start_len:
            save_text = text_to_print

            search = " .:;,=|�+-/*@#[]{}<>()$\\%&?!\r\n\t"
            while len(text_to_print) > 0:
                last_char = text_to_print[-1]

                if search.find(last_char) >= 0:
                    text_to_print = text_to_print.strip(last_char)
                    break

                text_to_print = text_to_print[:-1]

                if len(text_to_print) == 0:
                    text_to_print = save_text

        return text_to_print

    def add_text_block(self, text_to_print: str, text_style: TextStyle, text_layout: Rect, text_align: TextAlign = TextAlign.LEFT, text_color: str = "#000000") -> float:
        font_height = self.get_font_height(text_style)
        self._pdf.set_text_color(self.get_color_array(text_color))

        self._pdf.set_y(text_layout.top)
        self._pdf.set_x(text_layout.left)
        align = self.get_align(text_align)

        height = self._pdf.multi_cell(text_layout.get_width(), font_height, text_to_print, 0, align, False, output=enums.MethodReturnValue.HEIGHT, max_line_height=font_height)

        return height

    def add_image(self, img: Image, x: float, y: float, w: float, h: float):
        self._pdf.image(img, x, y, w, h)

    @staticmethod
    def get_align(align: TextAlign) -> enums.Align:
        match align:
            case TextAlign.LEFT:
                return enums.Align.L
            case TextAlign.RIGHT:
                return enums.Align.R
            case TextAlign.CENTER:
                return enums.Align.C
            case TextAlign.JUST:
                return enums.Align.J

    @staticmethod
    def get_style(text_style: TextStyle) -> str:
        font_style = ''
        if text_style.bold:
            font_style += 'B'

        if text_style.underline:
            font_style += 'U'

        if text_style.italic:
            font_style += 'I'

        return font_style

    @staticmethod
    def get_color_array(color: str) -> []:
        if len(color) == 6:
            color = '#' + color

        if len(color) != 7:
            return [0, 0, 0]

        r = max(0, min(255, int(color[1:3], 16)))
        g = max(0, min(255, int(color[3:5], 16)))
        b = max(0, min(255, int(color[5:7], 16)))

        return [r, g, b]
