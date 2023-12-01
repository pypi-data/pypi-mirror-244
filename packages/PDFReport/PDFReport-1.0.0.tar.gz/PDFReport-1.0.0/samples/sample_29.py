import pathlib
from datetime import datetime
import tempfile
import os
from PDFReport import *


sample_path = str(pathlib.Path(__file__).parent)


def add_header(report: Report):

    # Add vertical container frame to the header
    vc = SerialFrame(report.header, Direction.VERTICAL, margin_bottom=5.0, use_full_width=True)

    # Add box to the container with a height of 15mm and using the full width.
    box = BoxFrame(vc)
    box.use_full_width = True
    box.height = 15.0

    # Add an image to the box on the right side of the box with a max. height of 10mm and vertically in the middle
    # of the surrounding frame.
    ifr = ImageFrame(box, sample_path + "/logo2.png", 0.0, 10.0, True)
    ifr.v_align = VAlign.MIDDLE
    ifr.h_align = HAlign.RIGHT


def add_footer(report: Report):

    # Add vertical container frame to the footer
    vc = SerialFrame(report.footer, Direction.VERTICAL, margin_top=5.0, use_full_width=True)

    # Add box to the container using the full width.
    box = BoxFrame(vc)
    box.use_full_width = True

    # Add some text to the box
    TextFrame(box, "Adiuvaris    -    At the lake 901a    -    18957 Lakeside    -    100 000 00 01", TextStyle.BOLD, False, TextAlign.CENTER)


def add_title_text(report: Report):

    body = report.body

    # Add title text to the body frame
    TextFrame(body, "Project Examples", TextStyle.HEADING1)

    # Add vertical distance of 10mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

    # Add subtitle text to the body frame
    TextFrame(body, "Python library 'PDFReport'", TextStyle.HEADING2)
    TextFrame(body, "Python library for dynamic PDF reports using the FPDF library", TextStyle.BOLD)

    # Add vertical distance of 20mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=20.0)


def convert_date(timestamp) -> str:

    # Convert a timestamp to a readable date string
    d = datetime.utcfromtimestamp(timestamp)
    formatted_date = d.strftime('%d.%m.%Y')
    return formatted_date


def add_table(report: Report):
    body = report.body

    # Add a table which uses the full width
    table = TableFrame(body)
    table.use_full_width = True

    # Define the columns of the table. The widths are given in mm
    col_fn = TableColumn(table, "Filename", 40.0)
    col_nl = TableColumn(table, "Number of lines", 30.0, TextAlign.RIGHT)
    col_mo = TableColumn(table, "Last modification", 30.0, TextAlign.CENTER)
    col_si = TableColumn(table, "File-Size (Byte)", 20.0, TextAlign.RIGHT)

    # Read the list of sample files
    with os.scandir(sample_path) as entries:
        for entry in entries:

            if not entry.name.endswith(".py"):
                continue

            # Determine the number of lines in the sample
            with open(f"{sample_path}/{entry.name}", 'r') as fp:
                for count, line in enumerate(fp):
                    pass

            info = entry.stat()

            # Add a row to the table and fill the cells with the data of the file
            row = TableRow(table)
            TableCell(row, col_fn, entry.name)
            TableCell(row, col_nl, str(count + 2))
            TableCell(row, col_mo, convert_date(info.st_mtime))
            TableCell(row, col_si, str(info.st_size))


def add_source(report: Report):

    # Modify the small text style to use font family Courier
    TextStyles[TextStyle.SMALL].font_family = "Courier"

    body = report.body

    num = 0
    with os.scandir(sample_path) as entries:
        for entry in entries:

            if not entry.name.endswith(".py"):
                continue

            # Print only the content of 3 files
            num += 1
            if num > 3:
                break

            # Manually start a new page
            BreakFrame(body)

            # Title text
            TextFrame(body, f"Content of file '{entry.name}'", TextStyle.HEADING2)

            # Add a vertical frame for the lines of code
            SerialFrame(body, Direction.VERTICAL, margin_bottom=5.0)

            # Loop over all lines in the python file
            with open(f"{sample_path}/{entry.name}", 'r') as fp:
                for count, line in enumerate(fp):
                    line.strip("\n")

                    # Add a line of text
                    TextFrame(body, line, TextStyle.SMALL)


def sample_29():
    """
    Example report which uses data from the file system
    """

    # Init a new Report
    report = Report()

    # Add header
    add_header(report)

    # Add a footer
    add_footer(report)

    # Add title text
    add_title_text(report)

    # Add a table with the sample files
    add_table(report)

    # Add the text from 3 of the sample source files
    add_source(report)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_29"
    report.output(filename, True)


if __name__ == '__main__':
    sample_29()
