import os
import platform
import subprocess
import json

from .globals import VAlign
from .pageformat import PageFormat
from .rect import Rect
from .globals import get_rect_with_size_and_align
from .renderer import Renderer
from .serialframe import SerialFrame
from .boxframe import BoxFrame
from .tableframe import TableFrame
from .tablecolumn import TableColumn
from .tablerow import TableRow
from .imageframe import ImageFrame
from .breakframe import BreakFrame
from .pageframe import PageFrame
from .positionframe import PositionFrame
from .barcodeframe import BarcodeFrame
from .lineframe import LineFrame
from .textframe import TextFrame
from .textstyle import TextStyle
from .textstyles import TextStyles
from .reportdata import ReportData


class Report:
    """
    This is the main class for reports in the PDFReport
    It creates some basic frames and prints them to a PDF document
    """

    def __init__(self, page_format: PageFormat = None, font_family: str = "Helvetica", font_size: float = 9.0, text_color: str = "#000000"):
        """
        Creates a new Report object.
        If no page format is passed a default page format will be used

        :param page_format: PageFormat to be used for the report or None
        """

        if page_format is None:
            page_format = PageFormat()

        self._page_format = page_format
        self._body = SerialFrame()
        self._body.frame_id = "b"

        self._header = SerialFrame()
        self._header.v_align = VAlign.TOP
        self._header.frame_id = "h"

        self._footer = SerialFrame()
        self._footer.v_align = VAlign.BOTTOM
        self._footer.frame_id = "f"

        self._header_max_height = 0.0
        self._footer_max_height = 0.0

        self._count_pages = False

        # Init text styles
        TextStyles.set_default(font_family, font_size, text_color)

    @property
    def page_format(self) -> PageFormat:
        """
        The page format to be used in the report

        :getter: Returns the page format
        :setter: Sets the page format
        """
        return self._page_format

    @page_format.setter
    def page_format(self, page_format: PageFormat):
        self._page_format = page_format

    @property
    def header(self) -> SerialFrame:
        """
        The header frame

        :getter: Returns the header frame (vertical serial frame)
        """
        return self._header

    @property
    def footer(self) -> SerialFrame:
        """
        The footer frame

        :getter: Returns the footer frame (vertical serial frame)
        """
        return self._footer

    @property
    def body(self) -> SerialFrame:
        """
        The body frame

        :getter: Returns the body frame (vertical serial frame)
        """
        return self._body

    @property
    def count_pages(self) -> bool:
        """
        Flag if the pages should be counted before the printing
        That is used if the variable for the number of pages is used

        :getter: Returns True if the pages will be counted
        :setter: Sets the count pages flag
        """
        return self._count_pages

    @count_pages.setter
    def count_pages(self, count_pages: bool):
        self._count_pages = count_pages

    def output(self, rep_file_name: str, show: bool = False, report_data: ReportData = None):
        """
        Creates the pdf file from the report structure

        :param rep_file_name: The full filename for the report without extension
        :param show: If True the created pdf will be shown (if possible)
        :param report_data: Data provider to handle callbacks to get dynamic data
        """
        if self._is_endless():
            raise OverflowError("Endless recursion loop in the report structure.")

        renderer = Renderer(self._page_format, report_data)
        self._print_report(renderer, rep_file_name + ".pdf")

        if show:
            self.show(rep_file_name + ".pdf")

    def save(self, rep_file_name: str, show: bool = False):
        """
        Save the report in a json file.

        :param rep_file_name: The full filename for the report without extension
        :param show: If True the created json file will be shown (if possible)
        """
        if self._is_endless():
            raise OverflowError("Endless recursion loop in the report structure.")

        data = {}

        report = {}
        report["class"] = "Report"
        report["count_pages"] = self._count_pages
        report["page_format"] = self._page_format.to_dict()

        data["r"] = report

        frame = {}
        self._header.to_dict(data, frame)

        frame = {}
        self._footer.to_dict(data, frame)

        frame = {}
        self._body.to_dict(data, frame)

        with open(rep_file_name + ".json", "w") as fp:
            json.dump(data, fp, sort_keys=False, indent=4)
            fp.close()
            if show:
                self.show(rep_file_name + ".json")

    def load(self, rep_file_name: str):
        """
        Loads a report from a json file.

        :param rep_file_name: The full filename for the report without extension
        """
        with open(rep_file_name + ".json", "r") as fp:
            data = json.load(fp)
            fp.close()

            frames = {}

            for frame_id, frame in data.items():
                parent = None
                if "parent_id" in frame:
                    parent = frames[frame["parent_id"]]

                if frame["class"] == "SerialFrame":

                    if frame_id == "h":
                        frames[frame_id] = self._header
                    elif frame_id == "f":
                        frames[frame_id] = self._footer
                    elif frame_id == "b":
                        frames[frame_id] = self._body
                    else:
                        frames[frame_id] = SerialFrame(parent, frame_id=frame_id)
                        frames[frame_id].from_dict(frame)

                elif frame["class"] == "BarcodeFrame":
                    frames[frame_id] = BarcodeFrame(parent, frame_id=frame_id)
                    frames[frame_id].from_dict(frame)

                elif frame["class"] == "LineFrame":
                    frames[frame_id] = LineFrame(parent, frame_id=frame_id)
                    frames[frame_id].from_dict(frame)

                elif frame["class"] == "TextFrame":
                    frames[frame_id] = TextFrame(parent, frame_id=frame_id)
                    frames[frame_id].from_dict(frame)

                elif frame["class"] == "BoxFrame":
                    frames[frame_id] = BoxFrame(parent, frame_id=frame_id)
                    frames[frame_id].from_dict(frame)

                elif frame["class"] == "ImageFrame":
                    frames[frame_id] = ImageFrame(parent, frame_id=frame_id)
                    frames[frame_id].from_dict(frame)

                elif frame["class"] == "BreakFrame":
                    frames[frame_id] = BreakFrame(parent, frame_id=frame_id)
                    frames[frame_id].from_dict(frame)

                elif frame["class"] == "PageFrame":
                    frames[frame_id] = PageFrame(parent, frame_id=frame_id)
                    frames[frame_id].from_dict(frame)

                elif frame["class"] == "PositionFrame":
                    frames[frame_id] = PositionFrame(parent, frame_id=frame_id)
                    frames[frame_id].from_dict(frame)

                elif frame["class"] == "TableFrame":
                    frames[frame_id] = TableFrame(parent, frame_id=frame_id)
                    frames[frame_id].from_dict(frame)

                elif frame["class"] == "TableColumn":
                    tc = TableColumn(parent)
                    tc.from_dict(frame)

                elif frame["class"] == "TableRow":
                    tr = TableRow(parent)
                    tr.from_dict(frame)

                elif frame["class"] == "Report":
                    self._count_pages = frame["count_pages"]
                    self._page_format = PageFormat()
                    self._page_format.from_dict(frame["page_format"])

    def _is_endless(self) -> bool:
        frames = []
        if self._header.is_endless(frames):
            return True
        if self._footer.is_endless(frames):
            return True
        return self._body.is_endless(frames)

    def _print_report(self, r: Renderer, rep_file_name: str) -> int:
        self._on_begin_print(r)
        while self._on_print_page(r):
            pass

        self._on_end_print(r, rep_file_name)

        return r.current_page

    def _on_begin_print(self, r: Renderer):
        r.create_new_pdf()
        r.pages_counted = False
        self._reset()

    def _reset(self):
        self._body.reset()
        self._header.reset()
        self._footer.reset()

    def _print_a_page(self, r: Renderer) -> bool:
        page_bounds = r.get_page_bounds()

        if self._header.get_frame_count() > 0:
            header_bounds = Rect(other=page_bounds)

            if self._header_max_height > 0:
                header_bounds.bottom = header_bounds.top + self._header_max_height

            self._header.print(r, header_bounds)
            self._header.reset()

            page_bounds.top += self._header.get_size().height

        if self._footer.get_frame_count() > 0:
            footer_bounds = Rect(other=page_bounds)

            if self._footer_max_height > 0:
                footer_bounds.top = footer_bounds.bottom + self._footer_max_height

            self._footer.calc_size(r, footer_bounds)
            footer_bounds = get_rect_with_size_and_align(footer_bounds, self._footer.get_size(),
                                                         self._footer.h_align, self._footer.v_align)

            self._footer.print(r, footer_bounds)
            self._footer.reset()

            page_bounds.bottom -= self._footer.get_size().height

        if self._body.get_frame_count() > 0:
            self._body.print(r, page_bounds)
            has_more_pages = self._body.continued
        else:
            has_more_pages = False

        return has_more_pages

    def _do_count_pages(self, r: Renderer) -> int:
        if not self._count_pages:
            return 0

        if not r.pages_counted:

            while self._print_a_page(r):
                r.add_page()

            r.pages_counted = True
            r.create_new_pdf()
            self._reset()

        return r.total_pages

    def _on_print_page(self, r: Renderer) -> bool:
        if self._count_pages and not r.pages_counted:
            self._do_count_pages(r)

        has_more_pages = self._print_a_page(r)

        if has_more_pages:
            r.add_page()

        return has_more_pages

    def _on_end_print(self, r: Renderer, rep_file_name: str):
        if len(rep_file_name) > 0:
            r.output(rep_file_name)

        self._reset()

    @staticmethod
    def show(rep_file_name: str):
        if platform.system() == 'Darwin':
            subprocess.call(('open', rep_file_name))
        elif platform.system() == 'Windows':
            os.startfile(rep_file_name)
        else:
            subprocess.call(('xdg-open', rep_file_name))
