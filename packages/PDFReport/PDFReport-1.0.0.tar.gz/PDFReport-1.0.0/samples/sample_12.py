import tempfile
from PDFReport import *


def sample_12():
    """
    Add a simple table to a report
    """

    # Init a new Report
    report = Report()

    # Add a table to the body of the report
    table = TableFrame(report.body)

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

    # Add a row to the table and fill the cells with data
    row = TableRow(table)
    TableCell(row, col_ft, "LineFrame")
    TableCell(row, col_co, "No")
    TableCell(row, col_de, "This frame type represents a line on the report.")
    TableCell(row, col_nu, "1")

    # Define a text style bold to have a grey background
    TextStyles[TextStyle.BOLD].background_color = "#CCCCCC"

    # Add a row to the table and fill the cells with data
    # Use the modified text style for one cell
    row = TableRow(table)
    TableCell(row, col_ft, "SerialFrame")
    TableCell(row, col_co, "Yes", TextStyle.BOLD)
    TableCell(row, col_de, "This is a frame container for a series of frames which will be printed one after the other.")
    TableCell(row, col_nu, "2")

    # Add a row to the table and fill the cells with data
    row = TableRow(table)
    TableCell(row, col_ft, "TextFrame")
    TableCell(row, col_co, "No")
    TableCell(row, col_de, "A simple frame type to print text.")
    TableCell(row, col_nu, "3")

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_12"
    report.output(filename, True)


if __name__ == '__main__':
    sample_12()
