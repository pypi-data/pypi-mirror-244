from typing import Dict
from .enums import RowType
from .textstyle import TextStyle
from .tablecell import TableCell
from .tablecolumn import TableColumn


class TableRow:
    """
    Class to hold the data for one row in a TableFrame
    """

    def __init__(self, table=None, row_type: RowType = RowType.DETAIL, join_start: int = -1, join_end: int = -1):
        """
        Creates a new row in the table

        :param table: Table frame to which this row will be added
        :param row_type: Row type one of the enums RowType
        :param join_start: Index of column where a span starts
        :param join_end: Index of column where a span ends
        """
        self._cells: Dict[str, TableCell] = {}
        self._row_type = row_type
        self._join_start = join_start
        self._join_end = join_end

        self._table = table
        self._idx = table.add_row(self)
        self._row_id = table.frame_id + ".r." + str(self._idx)

    @property
    def idx(self) -> int:
        """
        Number of the row

        :getter: Returns the number
        """
        return self._idx

    @property
    def row_type(self) -> RowType:
        """
        The row type

        :getter: Returns the row type
        :setter: Sets the row type
        """
        return self._row_type

    @row_type.setter
    def row_type(self, row_type: RowType):
        self._row_type = row_type

    @property
    def join_start(self) -> int:
        """
        The join start

        :getter: Returns the join star
        :setter: Sets the join start
        """
        return self._join_start

    @join_start.setter
    def join_start(self, join_start: int):
        self._join_start = join_start

    @property
    def join_end(self, ) -> int:
        """
        The join end

        :getter: Returns the join end
        :setter: Sets the join end
        """
        return self._join_end

    @join_end.setter
    def join_end(self, join_end: int):
        self._join_end = join_end

    def add_cell(self, col: TableColumn or int, table_cell: TableCell):
        col_nr = col
        if isinstance(col, TableColumn):
            col_nr = col.idx

        self._cells[col_nr] = table_cell

    def get_text_style(self, col: TableColumn or int) -> TextStyle or None:
        col_nr = col
        if isinstance(col, TableColumn):
            col_nr = col.idx

        if col_nr in self._cells:
            return self._cells[col_nr].text_style

        return None

    def get_text(self, col: TableColumn or int) -> str:
        col_nr = col
        if isinstance(col, TableColumn):
            col_nr = col.idx

        if col_nr in self._cells:
            return self._cells[col_nr].text

        return ""

    def set_text(self, col: TableColumn or int, text: str):
        col_nr = col
        if isinstance(col, TableColumn):
            col_nr = col.idx

        if col_nr in self._cells:
            self._cells[col_nr].text = text

    def to_dict(self, data: dict, row: dict):
        row["class"] = "TableRow"
        row["parent_id"] = self._table.frame_id

        if self.row_type != RowType.DETAIL:
            row["row_type"] = self.row_type.value

        if self.join_start >= 0:
            row["join_start"] = self.join_start

        if self.join_end >= 0:
            row["join_end"] = self.join_end

        cells = {}
        for col_nr, cell in self._cells.items():
            cells[str(col_nr)] = cell.to_dict()

        row["cells"] = cells

        data[self._row_id] = row

    def from_dict(self, row: dict):
        if "row_type" in row:
            self.row_type = RowType(row["row_type"])

        if "join_start" in row:
            self.join_start = row["join_start"]

        if "join_end" in row:
            self.join_start = row["join_end"]

        if "cells" in row:
            cells = row["cells"]
            for col_nr, cell in cells.items():
                ce = TableCell(self, int(col_nr))
                ce.from_dict(cell)
