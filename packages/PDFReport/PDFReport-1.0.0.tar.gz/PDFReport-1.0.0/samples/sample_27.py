import tempfile
from PDFReport import *


def sample_27():
    """
    Table rows with joined columns
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
    # On this row the columns 0 to 3 will be joined and only the text from the first
    # of the joined columns will be printed (using the full width of the joined columns).
    row = TableRow(table, RowType.TOTAL)
    TableCell(row, col_ft, "On this row there is a join from the first to the last column of the table.")
    TableCell(row, col_co, "Not printed")
    TableCell(row, col_co, "Not printed")
    row.join_start = 0
    row.join_end = 3

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
    filename = tempfile.gettempdir() + "/output_27"
    report.output(filename, True)


if __name__ == '__main__':
    sample_27()
