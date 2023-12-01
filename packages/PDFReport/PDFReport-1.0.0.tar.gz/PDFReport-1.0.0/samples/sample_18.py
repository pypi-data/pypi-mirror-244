import tempfile
from PDFReport import *


def sample_18():
    """
    Use text styles in tables
    """

    # Init a new Report
    report = Report()

    # Modify some attributes of the default table text styles
    TextStyles[TextStyle.TABLE_HEADER].text_color = "FF0000"
    TextStyles[TextStyle.TABLE_HEADER].font_size = 11.0
    TextStyles[TextStyle.TABLE_SUBTOTAL].font_family = "Courier"
    TextStyles[TextStyle.TABLE_TOTAL].font_family = "Times"
    TextStyles[TextStyle.TABLE_ROW].text_color = "#0000FF"

    # Add a table to the body of the report.
    table = TableFrame(report.body)

    # Define the columns of the table. The widths are given in mm
    col_ft = TableColumn(table, "Frame type", 40.0)
    col_co = TableColumn(table, "Container type", 30.0, TextAlign.CENTER)
    col_de = TableColumn(table, "Description", 60.0)
    col_nu = TableColumn(table, "Number", 20.0, TextAlign.RIGHT)

    # Add a sub-total row to the table and fill the cells with data
    row = TableRow(table, RowType.SUBTOTAL)
    TableCell(row, col_ft, "width 40mm")
    TableCell(row, col_co, "width 30mm")
    TableCell(row, col_de, "width 60mm")
    TableCell(row, col_nu, "width 20mm")

    # Add a detail row to the table and fill the cells with data
    row = TableRow(table)
    TableCell(row, col_ft, "LineFrame")
    TableCell(row, col_co, "No")
    TableCell(row, col_de, "This frame type represents a line on the report.")
    TableCell(row, col_nu, "1")

    # Add a detail row to the table and fill the cells with data
    row = TableRow(table)
    TableCell(row, col_ft, "SerialFrame")
    TableCell(row, col_co, "Yes")
    TableCell(row, col_de, "This is a frame container for a series of frames which will be printed one after the other.")
    TableCell(row, col_nu, "2")

    # Add a detail row to the table and fill the cells with data
    row = TableRow(table)
    TableCell(row, col_ft, "TextFrame")
    TableCell(row, col_co, "No")
    TableCell(row, col_de, "A simple frame type to print text.")
    TableCell(row, col_nu, "3")

    # Add a sub-total row to the table and fill the cells with data
    row = TableRow(table, RowType.TOTAL)
    TableCell(row, col_ft, "Total")
    TableCell(row, col_nu, "100.00")

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_18"
    report.output(filename, True)


if __name__ == '__main__':
    sample_18()
