import tempfile

from PDFReport import *


def sample_19():
    """
    Tables that spread over more than one page
    """

    # Init a new Report
    report = Report()

    # Create a red text style to use it in the table
    ts_red = TextStyle("Red", text_color="#FF0000")

    # Add a table to the body of the report. Add 1mm space between rows.
    table = TableFrame(report.body)
    table.inter_row_space = 1.0

    # Define the columns of the table. The widths are given in mm
    col_ft = TableColumn(table, "Frame type", 40.0)
    col_co = TableColumn(table, "Container type", 30.0, TextAlign.CENTER)
    col_de = TableColumn(table, "Description", 60.0)
    col_nu = TableColumn(table, "Number", 20.0, TextAlign.RIGHT)

    # Add a row to the table and fill the cells with data
    row = TableRow(table)
    TableCell(row, col_ft, "width 40mm")
    TableCell(row, col_co, "width 30mm")
    TableCell(row, col_de, "width 60mm")
    TableCell(row, col_nu, "width 20mm")

    # Add 60 rows
    for i in range(0, 60):

        # Add a row to the table and fill the cells with data
        # All columns will use a different text styles
        row = TableRow(table)
        TableCell(row, col_ft, "LineFrame", TextStyle.ITALIC)
        TableCell(row, col_co, "No", TextStyle.BOLD)
        TableCell(row, col_de, "This frame type represents a line on the report.")
        TableCell(row, col_nu, str(i + 1), ts_red)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_19"
    report.output(filename, True)


if __name__ == '__main__':
    sample_19()
