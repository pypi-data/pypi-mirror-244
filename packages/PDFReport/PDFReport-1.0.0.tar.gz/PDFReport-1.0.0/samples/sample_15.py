import tempfile
from PDFReport import *


def sample_15():
    """
    A table using more space than available - line break
    """

    # Init a new Report
    report = Report()

    # Add a table to the body of the report.
    table = TableFrame(report.body)
    table.inter_row_space = 1.5

    # Define the columns of the table.
    # The widths are given in mm and, they use more than the width of the frame width
    # It will automatically break the lines after the 3rd column
    # The 4th column is a dummy column to print the 5th column exactly below the 2nd column
    col_ft = TableColumn(table, "Frame type", 50.0)
    col_co = TableColumn(table, "Container type", 30.0)
    col_de = TableColumn(table, "Description", 80.0)
    col_du = TableColumn(table, "", 50.0)
    col_nu = TableColumn(table, "Number", 30.0)

    # Add a row to the table and fill the cells with data
    # This line shows the widths of the columns
    row = TableRow(table)
    TableCell(row, col_ft, "col 1 width 50mm")
    TableCell(row, col_co, "col 2 width 30mm")
    TableCell(row, col_de, "col 3 width 80mm")
    TableCell(row, col_du, "dummy col 4 width 50mm")
    TableCell(row, col_nu, "col 5 width 30mm")

    # Add a row to the table and fill the cells with data, no data in the dummy column
    row = TableRow(table)
    TableCell(row, col_ft, "LineFrame")
    TableCell(row, col_co, "No")
    TableCell(row, col_de, "This frame type represents a line on the report.")
    TableCell(row, col_nu, "1")

    # Add a row to the table and fill the cells with data, no data in the dummy column
    row = TableRow(table)
    TableCell(row, col_ft, "SerialFrame")
    TableCell(row, col_co, "Yes")
    TableCell(row, col_de, "This is a frame container for a series of frames which will be printed one after the other.")
    TableCell(row, col_nu, "2")

    # Add a row to the table and fill the cells with data, no data in the dummy column
    row = TableRow(table)
    TableCell(row, col_ft, "TextFrame")
    TableCell(row, col_co, "No")
    TableCell(row, col_de, "A simple frame type to print text.")
    TableCell(row, col_nu, "3")

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_15"
    report.output(filename, True)


if __name__ == '__main__':
    sample_15()
