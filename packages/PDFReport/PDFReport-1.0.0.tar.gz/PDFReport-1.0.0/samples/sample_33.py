import tempfile
from PDFReport import *


class DataProvider(ReportData):
    """
    This class is the data provider for the report saved in the previous sample.
    """
    def __init__(self):
        pass

    def on_text_data(self, text_frame: TextFrame):
        """
        Will be called for text frames to get the content of the frame.

        :param text_frame: The text frame
        """
        if text_frame.frame_id == "TEXT_1":
            text_frame.text = "Text 1"
        elif text_frame.frame_id == "TEXT_2":
            text_frame.text = "Text 2, text 2"
        elif text_frame.frame_id == "TEXT_3":
            text_frame.text = "Text 3 row 1\nText 3 row 2"

    def on_table_data(self, table_frame: TableFrame):
        """
        Will be called by table frames to get the content of the table

        :param table_frame: The table frame
        """
        if table_frame.frame_id == "TAB_1":

            # Add a row to the table and fill the cells with data
            row = TableRow(table_frame)
            TableCell(row, 0, "width 40mm")
            TableCell(row, 1, "width 30mm")
            TableCell(row, 2, "width 60mm")
            TableCell(row, 3, "width 20mm")

            # Add a row to the table and fill the cells with data
            row = TableRow(table_frame)
            TableCell(row, 0, "TextFrame")
            TableCell(row, 1, "No")
            TableCell(row, 2, "A simple frame type to print text.")
            TableCell(row, 3, "3")


def sample_33():
    """
    Print saved report with 'dynamic' data
    """

    # Init a new Report
    report = Report()

    # Load the save JSON file from sample 32
    filename = tempfile.gettempdir() + "/output_32"
    report.load(filename)

    # Create the data provider object
    data = DataProvider()

    # Create the PDF - the data provider may define the content in the report
    filename = tempfile.gettempdir() + "/output_33"
    report.output(filename, True, data)


if __name__ == '__main__':
    sample_33()
