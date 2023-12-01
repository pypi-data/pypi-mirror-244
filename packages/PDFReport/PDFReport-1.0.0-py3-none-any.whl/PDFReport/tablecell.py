from .textstyle import TextStyle


class TableCell:
    """
    Class representing the content and the text style of a cell in a table
    """

    def __init__(self, table_row, table_col, text: str = "", text_style: TextStyle or str = ""):
        """
        Creates a new TableCell object.
        If there is no text style the default text style from the TableFrame will be used
        based on the row type

        :param table_row: Table row to which this cell will be added
        :param table_col: Column number or object
        :param text: Text in the cell
        :param text_style: Text style for the cell
        """
        self._text = text
        self._text_style = None
        if text_style is not None:
            if isinstance(text_style, TextStyle):
                self._text_style = TextStyle("", base_style=text_style.name)
            elif text_style != "":
                self._text_style = TextStyle("", base_style=text_style)

        table_row.add_cell(table_col, self)

    @property
    def text(self) -> str:
        """
        The text to be printed in the cell

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
        The text style

        :getter: Returns the text style (can be None)
        :setter: Sets the text style
        """
        return self._text_style

    @text_style.setter
    def text_style(self, text_style: TextStyle or str):
        self._text_style = None
        if text_style is not None:
            if isinstance(text_style, TextStyle):
                self._text_style = TextStyle("", base_style=text_style.name)
            elif text_style != "":
                self._text_style = TextStyle("", base_style=text_style)

    def to_dict(self) -> dict:
        """
        Fills the attribute-values to a dictionary if the attribute has no default value.
        :return: dict with attributes
        """
        cell = {}

        if self.text != "":
            cell["text"] = self.text

        if self.text_style is not None:
            ts = self.text_style.to_dict()
            if len(ts) > 0:
                cell["text_style"] = ts

        return cell

    def from_dict(self, cell: dict):
        """
        Fills the attributes based on the given dict
        :param cell:
        """
        if "text" in cell:
            self.text = cell["text"]

        if "text_style" in cell:
            ts = TextStyle("")
            ts.from_dict(cell["text_style"])
            self.text_style = ts
