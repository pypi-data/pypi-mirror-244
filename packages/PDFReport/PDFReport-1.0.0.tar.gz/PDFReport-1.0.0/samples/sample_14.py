import tempfile
from PDFReport import *


def sample_14():
    """
    A table using percent values for the widths of the columns.
    """

    # Init a new Report
    report = Report()

    # Add a table to the body of the report.
    table = TableFrame(report.body)

    # Define the columns of the table.
    # The widths are given in percents of the full width of the frame
    # The sum must be 100 or less.
    col_ft = TableColumn(table, "Frame type", "15%")
    col_co = TableColumn(table, "Container type", "15%", TextAlign.CENTER)
    col_de = TableColumn(table, "Description", "40%")
    col_nu = TableColumn(table, "Number", "10%", TextAlign.RIGHT)

    # Add a row to the table and fill the cells with data
    row = TableRow(table)
    TableCell(row, col_ft, "width 15%")
    TableCell(row, col_co, "width 15%")
    TableCell(row, col_de, "width 40%")
    TableCell(row, col_nu, "width 10%")

    # Add a row to the table and fill the cells with data
    row = TableRow(table)
    TableCell(row, col_ft, "LineFrame")
    TableCell(row, col_co, "No")
    TableCell(row, col_de, "This frame type represents a line on the report.")
    TableCell(row, col_nu, "1")

    # Add a row to the table and fill the cells with data
    row = TableRow(table)
    TableCell(row, col_ft, "SerialFrame")
    TableCell(row, col_co, "Yes")
    TableCell(row, col_de, "This is a frame container for a series of frames which will be printed one after the other.")
    TableCell(row, col_nu, "2")

    # Add a row to the table and fill the cells with data
    row = TableRow(table)
    TableCell(row, col_ft, "TextFrame")
    TableCell(row, col_co, "No")
    TableCell(row, col_de, "A simple frame type to print text.")
    TableCell(row, col_nu, "3")

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_14"
    report.output(filename, True)


if __name__ == '__main__':
    sample_14()
