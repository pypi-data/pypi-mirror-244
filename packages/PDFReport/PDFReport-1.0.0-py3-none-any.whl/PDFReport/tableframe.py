from typing import List

from .enums import RowType
from .border import Border
from .pen import Pen
from .rect import Rect
from .reportframe import get_rect_with_size_and_align
from .renderer import Renderer
from .simpleframe import SimpleFrame
from .containerframe import ContainerFrame
from .size import Size
from .sizestate import SizeState
from .tablecolumn import TableColumn
from .tablerow import TableRow
from .textstyle import TextStyle
from .textstyles import TextStyles


class TableFrame(SimpleFrame):
    """
    Class for a table in a report. It is a simple frame with no sub-frames in it.
    The table has a list of columns and data rows.
    """

    HEADER_ROW_INDEX = -1

    def __init__(self, parent: ContainerFrame, frame_id: str = ""):
        """
        Creates a new TableFrame

        :param parent: Parent frame to which this frame will be added
        :param frame_id: frame id (optional)
        """

        super().__init__(parent, frame_id)

        self._column_lines = False
        self._min_header_row_height = 0.0
        self._min_detail_row_height = 0.0
        self._max_header_row_height = 100.0
        self._max_detail_row_height = 100.0
        self._margin_bottom_subtotal = 1.0
        self._inter_row_space = 0.0

        self._header_text_style = TextStyle("", base_style=TextStyle.TABLE_HEADER)
        self._detail_row_text_style = TextStyle("", base_style=TextStyle.TABLE_ROW)
        self._alternating_row_text_style = None
        self._sub_total_row_text_style = TextStyle("", base_style=TextStyle.TABLE_SUBTOTAL)
        self._total_row_text_style = TextStyle("", base_style=TextStyle.TABLE_TOTAL)

        self._border = Border()
        self._repeat_header_row = True
        self._suppress_header_row = False

        self._inner_pen_header_bottom = Pen(0.2)
        self._inner_pen_total_top = Pen(0.2)
        self._inner_pen_row = Pen()

        self._header_row_height = 0.0
        self._table_height_for_page = 0.0
        self._header_size_init = False
        self._data_rows_fit = 0
        self._min_data_rows_fit = 1
        self._row_heights = []

        self._table_data: List[TableRow] = []
        self._width = 0.0
        self._num_sub_rows = 1
        self._sub_row_height_list = {}
        self._columns: List[TableColumn] = []
        self._row_index = 0
        self.__save_y = -1

    @property
    def margin_bottom_subtotal(self) -> float:
        """
        Margin below a subtotal row

        :getter: Returns the margin
        :setter: Sets the margin
        """
        return self._margin_bottom_subtotal

    @margin_bottom_subtotal.setter
    def margin_bottom_subtotal(self, margin_bottom_subtotal: float):
        self._margin_bottom_subtotal = margin_bottom_subtotal

    @property
    def repeat_header_row(self) -> bool:
        """
        Flag if the header row will be repeated after a page break

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._repeat_header_row

    @repeat_header_row.setter
    def repeat_header_row(self, repeat_header_row: bool):
        self._repeat_header_row = repeat_header_row

    @property
    def suppress_header_row(self) -> bool:
        """
        Flag if the header row will not be repeated at all

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._suppress_header_row

    @suppress_header_row.setter
    def suppress_header_row(self, suppress_header_row: bool):
        self._suppress_header_row = suppress_header_row

    @property
    def min_header_row_height(self) -> float:
        """
        Minimal height of the header row

        :getter: Returns the min header height
        :setter: Sets the min header height
        """
        return self._min_header_row_height

    @min_header_row_height.setter
    def min_header_row_height(self, min_header_row_height: float):
        self._min_header_row_height = abs(min_header_row_height)

    @property
    def min_detail_row_height(self) -> float:
        """
        Minimal height of a row

        :getter: Returns the min height
        :setter: Sets the min height
        """
        return self._min_detail_row_height

    @min_detail_row_height.setter
    def min_detail_row_height(self, min_detail_row_height: float):
        self._min_detail_row_height = abs(min_detail_row_height)

    @property
    def max_header_row_height(self) -> float:
        """
        Maximal height of the header row

        :getter: Returns the max header height
        :setter: Sets the max header height
        """
        return self._max_header_row_height

    @max_header_row_height.setter
    def max_header_row_height(self, max_header_row_height: float):
        self._max_header_row_height = abs(max_header_row_height)

    @property
    def max_detail_row_height(self) -> float:
        """
        Maximal height of a row

        :getter: Returns the max height
        :setter: Sets the max height
        """
        return self._max_detail_row_height

    @max_detail_row_height.setter
    def max_detail_row_height(self, max_detail_row_height: float):
        self._max_detail_row_height = abs(max_detail_row_height)

    @property
    def header_text_style(self) -> TextStyle:
        """
        Text style for the header row

        :getter: Returns the text style
        :setter: Sets the text style
        """
        return self._header_text_style

    @header_text_style.setter
    def header_text_style(self, header_text_style: TextStyle or str):
        if isinstance(header_text_style, TextStyle):
            self._header_text_style = TextStyle("", base_style=header_text_style.name)
        elif header_text_style != "":
            self._header_text_style = TextStyle("", base_style=header_text_style)
        else:
            self._header_text_style = TextStyle("", base_style=TextStyle.TABLE_HEADER)

    @property
    def detail_row_text_style(self) -> TextStyle:
        """
        Text style for a row

        :getter: Returns the text style
        :setter: Sets the text style
        """
        return self._detail_row_text_style

    @detail_row_text_style.setter
    def detail_row_text_style(self, detail_row_text_style: TextStyle or str):
        if isinstance(detail_row_text_style, TextStyle):
            self._detail_row_text_style = TextStyle("", base_style=detail_row_text_style.name)
        elif detail_row_text_style != "":
            self._detail_row_text_style = TextStyle("", base_style=detail_row_text_style)
        else:
            self._detail_row_text_style = TextStyle("", base_style=TextStyle.TABLE_ROW)

    @property
    def sub_total_row_text_style(self) -> TextStyle:
        """
        Text style for a sub-total row

        :getter: Returns the text style
        :setter: Sets the text style
        """
        return self._sub_total_row_text_style

    @sub_total_row_text_style.setter
    def sub_total_row_text_style(self, sub_total_row_text_style: TextStyle or str):
        if isinstance(sub_total_row_text_style, TextStyle):
            self._sub_total_row_text_style = TextStyle("", base_style=sub_total_row_text_style.name)
        elif sub_total_row_text_style != "":
            self._sub_total_row_text_style = TextStyle("", base_style=sub_total_row_text_style)
        else:
            self._sub_total_row_text_style = TextStyle("", base_style=TextStyle.TABLE_SUBTOTAL)

    @property
    def total_row_text_style(self) -> TextStyle:
        """
        Text style for a total row

        :getter: Returns the text style
        :setter: Sets the text style
        """
        return self._total_row_text_style

    @total_row_text_style.setter
    def total_row_text_style(self, total_row_text_style: TextStyle or str):
        if isinstance(total_row_text_style, TextStyle):
            self._total_row_text_style = TextStyle("", base_style=total_row_text_style.name)
        elif total_row_text_style != "":
            self._total_row_text_style = TextStyle("", base_style=total_row_text_style)
        else:
            self._total_row_text_style = TextStyle("", base_style=TextStyle.TABLE_TOTAL)

    @property
    def alternating_row_text_style(self) -> TextStyle:
        """
        Text style for the alternating rows

        :getter: Returns the text style
        :setter: Sets the text style
        """
        return self._alternating_row_text_style

    @alternating_row_text_style.setter
    def alternating_row_text_style(self, alternating_row_text_style: TextStyle or str):
        if isinstance(alternating_row_text_style, TextStyle):
            self._alternating_row_text_style = TextStyle("", base_style=alternating_row_text_style.name)
        elif alternating_row_text_style != "":
            self._alternating_row_text_style = TextStyle("", base_style=alternating_row_text_style)
        else:
            self._alternating_row_text_style = None

    @property
    def border(self) -> Border:
        """
        Border of the table

        :getter: Returns the border
        :setter: Sets the border
        """
        return self._border

    @border.setter
    def border(self, border: Border):
        self._border = border

    @property
    def inner_pen_header_bottom(self) -> Pen:
        """
        Pen for a line below the header row

        :getter: Returns the pen
        :setter: Sets the pen
        """
        return self._inner_pen_header_bottom

    @inner_pen_header_bottom.setter
    def inner_pen_header_bottom(self, inner_pen_header_bottom: Pen):
        self._inner_pen_header_bottom = inner_pen_header_bottom

    @property
    def inner_pen_total_top(self) -> Pen:
        """
        Pen for a line above the total row

        :getter: Returns the pen
        :setter: Sets the pen
        """
        return self._inner_pen_total_top

    @inner_pen_total_top.setter
    def inner_pen_total_top(self, inner_pen_total_top: Pen):
        self._inner_pen_total_top = inner_pen_total_top

    @property
    def inner_pen_row(self) -> Pen:
        """
        Pen for a line between rows

        :getter: Returns the pen
        :setter: Sets the pen
        """
        return self._inner_pen_row

    @inner_pen_row.setter
    def inner_pen_row(self, inner_pen_row: Pen):
        self._inner_pen_row = inner_pen_row

    @property
    def inter_row_space(self) -> float:
        """
        Space between rows in millimeters

        :getter: Returns the space
        :setter: Sets the space
        """
        return self._inter_row_space

    @inter_row_space.setter
    def inter_row_space(self, inter_row_space: float):
        self._inter_row_space = abs(inter_row_space)

    @property
    def column_lines(self) -> bool:
        """
        Flag if there are vertical lines between the cells

        :getter: Returns the flag
        :setter: Sets the flag
        """
        return self._column_lines

    @column_lines.setter
    def column_lines(self, column_lines: bool):
        self._column_lines = column_lines

    def reset(self):
        super().reset()
        self._header_size_init = False

    def add_row(self, row: TableRow) -> int:
        self._table_data.append(row)
        return len(self._table_data) - 1

    def add_column(self, tc: TableColumn) -> int:
        tc.header_text_style = self._header_text_style
        tc.detail_row_text_style = self._detail_row_text_style
        tc.sub_total_row_text_style = self._sub_total_row_text_style
        tc.total_row_text_style = self._total_row_text_style
        if self._alternating_row_text_style is not None:
            tc.alternating_row_text_style = self._alternating_row_text_style

        self._columns.append(tc)

        return len(self._columns) - 1

    def _get_text(self, header_row: bool, row: TableRow or None, col_number: int) -> str:
        if header_row:
            return self._columns[col_number].title

        if row is not None:
            return row.get_text(col_number)

        return ""

    def _get_text_style(self, row: TableRow or None, col_number: int, header_row: bool, alternating_row: bool) -> TextStyle:
        if row is not None:
            ts = row.get_text_style(col_number)
            if ts is not None:
                return ts

        if row is not None and row.row_type != RowType.DETAIL:
            if row.row_type == RowType.HEADER:
                style = self._header_text_style
            elif row.row_type == RowType.SUBTOTAL:
                style = self._sub_total_row_text_style
            elif row.row_type == RowType.TOTAL:
                style = self._total_row_text_style
            else:
                style = self._detail_row_text_style
        else:

            if header_row:
                style = self._header_text_style
            else:
                if alternating_row:
                    if self._alternating_row_text_style is not None:
                        style = self._alternating_row_text_style
                    else:
                        style = self._detail_row_text_style
                else:
                    style = self._detail_row_text_style

        return style

    def _calc_header_size(self, r: Renderer, rect: Rect) -> Size:
        if not self._header_size_init:
            width = rect.get_width()
            self._resize_columns(width)
            self._header_row_height = self._size_print_row(r, TableFrame.HEADER_ROW_INDEX, rect.left, rect.top,
                                                           self._max_detail_row_height, True, True)
            self._header_size_init = True

        return Size(self._width, self._header_row_height)

    def _get_table_bounds(self, for_rect: Rect, size: Size = None) -> Rect:
        if size is None:
            size = self._border.add_border_size(self._get_header_size())
            rect = get_rect_with_size_and_align(for_rect, size, self._h_align, self._v_align)

            return Rect(rect.left, for_rect.top, rect.right, for_rect.bottom)

        rect = get_rect_with_size_and_align(for_rect, size, self._h_align, self._v_align)

        return Rect(rect.left, rect.top, rect.right, rect.bottom)

    def _get_header_size(self) -> Size:
        return Size(self._width, self._header_row_height)

    def _size_print_header(self, r: Renderer, in_rect: Rect, size_only: bool) -> bool:
        header_fits = True
        if not self._suppress_header_row and self._repeat_header_row:
            if in_rect.size_fits(self._get_header_size()):
                if not size_only:
                    self._size_print_row(r, TableFrame.HEADER_ROW_INDEX, in_rect.left, in_rect.top,
                                         self._header_row_height, False, False)

                in_rect.top += self._header_row_height
            else:
                header_fits = False

        return header_fits

    def _find_data_rows_fit(self, r: Renderer, in_rect: Rect) -> int:
        rows_that_fit = 0
        index = self._row_index
        self._row_heights = []

        while index < self._get_total_rows():
            include_row_line = index < self._get_total_rows() - 1
            row_height = self._size_print_row(r, index, in_rect.left, in_rect.top, self._max_detail_row_height, True, include_row_line)

            if in_rect.size_fits(Size(self._width, row_height)):
                self._row_heights.append(row_height)
                in_rect.top += row_height
                index += 1
                rows_that_fit += 1
            else:
                if len(self._row_heights) > 0:
                    row_height = self._size_print_row(r, index - 1, in_rect.left, in_rect.top,
                                                      self._max_detail_row_height, True, False)
                    in_rect.top -= (self._row_heights[len(self._row_heights) - 1])
                    in_rect.top += row_height
                    self._row_heights[len(self._row_heights) - 1] = row_height
                else:
                    if self.__save_y < 40 and self.__save_y == in_rect.top:
                        self._row_heights.append(in_rect.get_height())
                        in_rect.top += in_rect.get_height()
                        index += 1
                        rows_that_fit += 1
                    else:
                        self.__save_y = in_rect.top

                break

        if self._min_data_rows_fit != 0 and index < self._get_total_rows():
            if rows_that_fit < self._min_data_rows_fit:
                rows_that_fit = 0
            else:
                rows_left = self._get_total_rows() - index
                if rows_left + rows_that_fit < (2 * self._min_data_rows_fit):
                    rows_that_fit = 0
                elif self._min_data_rows_fit > rows_left:
                    rows_that_fit -= (self._min_data_rows_fit - rows_left)

        return rows_that_fit

    def _get_total_rows(self) -> int:
        return len(self._table_data)

    def _print_rows(self, r: Renderer, in_rect: Rect):
        for rowCount in range(0, self._data_rows_fit):
            height = self._row_heights[rowCount]
            self._size_print_row(r, self._row_index, in_rect.left, in_rect.top, height, False, False)
            in_rect.top += height
            self._row_index += 1

    def _check_for_sub_rows(self, width: float):
        cols_width = 0.0
        for col_number, column in enumerate(self._columns):
            column.calc_width(width)
            cols_width += column.width_to_use

            next_col_number = col_number + 1
            if next_col_number < len(self._columns):

                next_column = self._columns[next_col_number]
                next_column.calc_width(width)
                if cols_width + next_column.width_to_use > width:

                    column.line_break = True
                    self._num_sub_rows += 1

                    if cols_width > self._width:
                        self._width = cols_width

                    cols_width = 0.0

        if cols_width > self._width:
            self._width = cols_width

    def _resize_columns(self, width: float):
        self._check_for_sub_rows(width)

        if self.use_full_width:
            self._adjust_columns_to_width(width)

    def _adjust_columns_to_width(self, max_width: float):
        if len(self._columns) == 0 or max_width <= 0:
            return

        max_width -= self._margin_left
        max_width -= self._margin_right

        curr_width = 0.0
        first_col = 0
        for col_number, column in enumerate(self._columns):

            curr_width += column.width_to_use

            if column.line_break and curr_width > 0.0:

                d_delta = max_width / curr_width * 10000
                delta = int(d_delta)
                d_delta = delta / 10000.0

                for col_nr in range(first_col, col_number + 1):
                    column = self._columns[col_nr]
                    column.width_to_use = column.width_to_use * d_delta

                first_col = col_number + 1
                curr_width = 0.0

        if curr_width > 0.0:
            d_delta = max_width / curr_width * 10000
            delta = int(d_delta)
            d_delta = delta / 10000.0

            for col_nr in range(first_col, len(self._columns)):
                column = self._columns[col_nr]
                column.width_to_use = column.width_to_use * d_delta

        self._width = max_width

    def _get_valid_height(self, height: float, is_header: bool) -> float:
        if is_header:
            min_h = self._min_header_row_height
            max_h = self._max_header_row_height
        else:
            min_h = self._min_detail_row_height
            max_h = self._max_detail_row_height

        if height < min_h:
            return min_h
        elif height > max_h:
            return max_h
        else:
            return height

    def _size_print_row(self, r: Renderer, row_index: int, x: float, y: float, max_height: float, size_only: bool, show_line: bool) -> float:
        is_header = (row_index == TableFrame.HEADER_ROW_INDEX)
        alt_row = ((row_index % 2) != 0)
        row_height = 0.0
        curr_row_height = 0.0
        x_pos = x
        y_pos = y
        row = None
        if not is_header:
            row = self._table_data[row_index]

        cur_sub_row = 0

        if not size_only and self._num_sub_rows > 1:
            max_height = self._get_valid_height(self._get_sub_row_height(row_index + 1, cur_sub_row), is_header)

        for col_number, column in enumerate(self._columns):
            col_w = column.width_to_use
            if row is not None:
                if row.join_start >= 0 and row.join_end >= 0:
                    if col_number == row.join_start:

                        col_to_start = self._columns[col_number]
                        col_w = col_to_start.width

                        # Add additional column width get the total width of the joined column
                        for join_col in range(row.join_start + 1, row.join_end + 1):
                            if join_col >= len(self._columns):
                                continue

                            col_in_join = self._columns[join_col]
                            col_w += col_in_join.width

                            #  Remove text from columns in the join
                            row.set_text(join_col, "")

            text = self._get_text(is_header, row, col_number)
            text_style = self._get_text_style(row, col_number, is_header, alt_row)

            size = column.size_paint_cell(r, text, text_style, x_pos, y_pos, col_w, max_height, size_only)
            curr_row_height = max(curr_row_height, self._get_valid_height(size.height, is_header))

            x_pos += column.width_to_use

            if column.line_break:
                if size_only:
                    self._set_sub_row_height(row_index + 1, cur_sub_row, curr_row_height)
                    cur_sub_row += 1
                else:
                    cur_sub_row += 1
                    max_height = self._get_valid_height(self._get_sub_row_height(row_index + 1, cur_sub_row), is_header)

                row_height += curr_row_height

                y_pos += curr_row_height
                x_pos = x

                curr_row_height = 0.0

        row_height += curr_row_height

        if size_only and self._num_sub_rows > 1:
            self._set_sub_row_height(row_index + 1, cur_sub_row, curr_row_height)
        else:
            row_height = curr_row_height

        if show_line:
            row_height += self._row_line(r, x, y_pos + row_height, self._width, is_header, False, size_only)

        if not is_header:
            row_height += self._inter_row_space

        if row is not None and row.row_type == RowType.SUBTOTAL:
            row_height += self._row_line(r, x, y, self._width, False, True, size_only)
            row_height += self._margin_bottom_subtotal

        if row is not None and row.row_type == RowType.TOTAL:
            row_height += self._row_line(r, x, y, self._width, False, True, size_only)

        return row_height

    def _row_line(self, r: Renderer, x: float, y: float, length: float, is_header: bool, is_total: bool, size_only: bool) -> float:
        height = 0
        if is_header:
            pen = self._inner_pen_header_bottom
        elif is_total:
            pen = self._inner_pen_total_top
        else:
            pen = self._inner_pen_row

        if pen.extent != 0.0:
            if not size_only:
                y -= pen.extent / 2.0
                r.add_line(x, y, x + length, y, pen.extent, pen.line_style, pen.color)

            height = pen.extent

        return height

    def _print_all_row_lines(self, r: Renderer, rect: Rect, include_header: bool):
        x = rect.left
        y = rect.top
        row_width = rect.get_width()
        if include_header:
            self._row_line(r, x, y + self._header_row_height, row_width, True, False, False)
            y += self._header_row_height

        for rowCount in range(0, self._data_rows_fit - 1):
            height = self._row_heights[rowCount]
            self._row_line(r, x, y + height, row_width, False, False, False)
            y += height

    def _print_all_column_lines(self, r: Renderer, rect: Rect):
        if self._num_sub_rows > 1 or not self._column_lines:
            return

        x = rect.left
        y = rect.top

        for colNumber in range(0, len(self._columns)):
            #  @var TableColumn column */
            column = self._columns[colNumber]
            x += column.width_to_use

            column.draw_right_line(r, x, y, rect.get_height())

    def _get_sub_row_height(self, row: int, sub_row: int) -> float:
        height = 0.0
        if row in self._sub_row_height_list:
            if sub_row in self._sub_row_height_list[row]:
                height = self._sub_row_height_list[row][sub_row]

        return height

    def _set_sub_row_height(self, row: int, sub_row: int, height: float):
        if row in self._sub_row_height_list:
            self._sub_row_height_list[row][sub_row] = height
        else:
            self._sub_row_height_list[row] = {}
            self._sub_row_height_list[row][sub_row] = height

    def _do_calc_size(self, r: Renderer, for_rect: Rect) -> SizeState:
        size_states = SizeState()

        inside_border = self._border.get_inner_rect(for_rect)
        self._calc_header_size(r, inside_border)
        table_bounds = self._get_table_bounds(inside_border)
        original_position_y = table_bounds.top

        if self._size_print_header(r, table_bounds, True):
            self._data_rows_fit = self._find_data_rows_fit(r, table_bounds)
            self._table_height_for_page = table_bounds.top - original_position_y
            if self._get_total_rows() == 0:
                size_states.fits = True
            elif self._data_rows_fit > 0:
                size_states.fits = True
                if self._row_index + self._data_rows_fit < self._get_total_rows():
                    size_states.continued = True

            else:
                size_states.continued = True
                if self._data_rows_fit < self._min_data_rows_fit:
                    size_states.fits = False

        else:
            size_states.fits = False
            size_states.continued = True

        size_states.required_size = self._border.add_border_size(Size(self._width, self._table_height_for_page))

        return size_states

    def _do_print(self, r: Renderer, in_rect: Rect):
        table_bounds = self._get_table_bounds(in_rect, self._required_size)
        inside_borders = self._border.get_inner_rect(table_bounds)
        printing_bounds = Rect(other=inside_borders)

        self._size_print_header(r, printing_bounds, False)
        self._print_rows(r, printing_bounds)

        self._print_all_row_lines(r, inside_borders, (not self._suppress_header_row and self._repeat_header_row))
        self._print_all_column_lines(r, inside_borders)
        self._border.draw_border(r, get_rect_with_size_and_align(table_bounds))

    def _do_begin_print(self, r: Renderer):
        # If the header should not be printed, start with the first row
        if self._suppress_header_row or self._repeat_header_row:
            self._row_index = 0
        else:
            self._row_index = TableFrame.HEADER_ROW_INDEX

        self._data_rows_fit = 0

        if r.data is not None:
            r.data.on_table_data(self)

    def to_dict(self, data: dict, frame: dict):
        frame["class"] = "TableFrame"

        if self.column_lines:
            frame["column_lines"] = self.column_lines

        if self.min_header_row_height > 0.0:
            frame["min_header_row_height"] = self.min_header_row_height

        if self.min_detail_row_height > 0.0:
            frame["min_detail_row_height"] = self.min_detail_row_height

        if self.max_header_row_height != 100.0:
            frame["max_header_row_height"] = self.max_header_row_height

        if self.max_detail_row_height != 100.0:
            frame["max_detail_row_height"] = self.max_detail_row_height

        if self.margin_bottom_subtotal != 1.0:
            frame["margin_bottom_subtotal"] = self.margin_bottom_subtotal

        if self.inter_row_space > 0.0:
            frame["inter_row_space"] = self.inter_row_space

        ts = self.header_text_style.to_dict()
        if len(ts) > 0:
            frame["header_text_style"] = ts

        ts = self.detail_row_text_style.to_dict()
        if len(ts) > 0:
            frame["detail_row_text_style"] = ts

        if self.alternating_row_text_style is not None:
            ts = self.alternating_row_text_style.to_dict()
            if len(ts) > 0:
                frame["alternating_row_text_style"] = ts

        ts = self.sub_total_row_text_style.to_dict()
        if len(ts) > 0:
            frame["sub_total_row_text_style"] = ts

        ts = self.total_row_text_style.to_dict()
        if len(ts) > 0:
            frame["total_row_text_style"] = ts

        b = self.border.to_dict()
        if len(b) > 0:
            frame["border"] = b

        if not self.repeat_header_row:
            frame["repeat_header_row"] = self.repeat_header_row

        if self.suppress_header_row:
            frame["suppress_header_row"] = self.suppress_header_row

        p = self.inner_pen_row.to_dict()
        if len(p) > 0:
            frame["inner_pen_row"] = p

        if self._inner_pen_header_bottom != Pen(0.2):
            frame["inner_pen_header_bottom"] = self.inner_pen_header_bottom.to_dict()

        if self._inner_pen_total_top != Pen(0.2):
            frame["inner_pen_total_top"] = self.inner_pen_total_top.to_dict()

        data[self.frame_id] = frame
        super().to_dict(data, frame)

        for column in self._columns:
            f = {}
            column.to_dict(data, f)

        for row in self._table_data:
            f = {}
            row.to_dict(data, f)

        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        super().from_dict(frame)

        if "column_lines" in frame:
            self.column_lines = frame["column_lines"]

        if "min_header_row_height" in frame:
            self.min_header_row_height = frame["min_header_row_height"]

        if "min_detail_row_height" in frame:
            self.min_detail_row_height = frame["min_detail_row_height"]

        if "max_header_row_height" in frame:
            self.max_header_row_height = frame["max_header_row_height"]

        if "max_detail_row_height" in frame:
            self.max_detail_row_height = frame["max_detail_row_height"]

        if "margin_bottom_subtotal" in frame:
            self.margin_bottom_subtotal = frame["margin_bottom_subtotal"]

        if "inter_row_space" in frame:
            self.inter_row_space = frame["inter_row_space"]

        if "header_text_style" in frame:
            ts = TextStyle("")
            ts.from_dict(frame["header_text_style"])
            self.header_text_style = ts

        if "detail_row_text_style" in frame:
            ts = TextStyle("")
            ts.from_dict(frame["detail_row_text_style"])
            self.detail_row_text_style = ts

        if "alternating_row_text_style" in frame:
            ts = TextStyle("")
            ts.from_dict(frame["alternating_row_text_style"])
            self.alternating_row_text_style = ts

        if "sub_total_row_text_style" in frame:
            ts = TextStyle("")
            ts.from_dict(frame["sub_total_row_text_style"])
            self.sub_total_row_text_style = ts

        if "total_row_text_style" in frame:
            ts = TextStyle("")
            ts.from_dict(frame["total_row_text_style"])
            self.total_row_text_style = ts

        if "border" in frame:
            border = Border()
            border.from_dict(frame["border"])
            self.border = border

        if "repeat_header_row" in frame:
            self.repeat_header_row = frame["repeat_header_row"]

        if "suppress_header_row" in frame:
            self.suppress_header_row = frame["suppress_header_row"]

        if "inner_pen_header_bottom" in frame:
            pen = Pen()
            pen.from_dict(frame["inner_pen_header_bottom"])
            self.inner_pen_header_bottom = pen

        if "inner_pen_total_top" in frame:
            pen = Pen()
            pen.from_dict(frame["inner_pen_total_top"])
            self.inner_pen_total_top = pen

        if "inner_pen_row" in frame:
            pen = Pen()
            pen.from_dict(frame["inner_pen_row"])
            self.inner_pen_row = pen
