import tempfile
from PDFReport import *


def sample_32():
    """
    Report save sample
    """

    # Init a new Report with default font-family Times and a font_size 10 points
    report = Report(font_family="Times", font_size=11.0)

    # Add text to the body, named TEXT_1
    TextFrame(report.body, "This text will NOT be printed because data provider has data for TEXT_1", frame_id="TEXT_1")

    # Add vertical distance of 2mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=2.0)

    # Add text to the body, named TEXT_2
    TextFrame(report.body, frame_id="TEXT_2")

    # Add vertical distance of 2mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=2.0)

    # Add text to the body, named TEXT_3
    TextFrame(report.body, frame_id="TEXT_3")

    # Add vertical distance of 2mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=2.0)

    # Add text to the body, named TEXT_4
    TextFrame(report.body, "This text will be printed because data provider has not data for TEXT_4", frame_id="TEXT_4")

    # Add vertical distance of 2mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=2.0)

    # Add table to the body, named TAB_1
    table = TableFrame(report.body, "TAB_1")

    # Define the columns of the table. The widths are given in mm
    TableColumn(table, "Frame type", 40.0)
    TableColumn(table, "Container type", 30.0, TextAlign.CENTER)
    TableColumn(table, "Description", 60.0)
    TableColumn(table, "Number", 20.0, TextAlign.RIGHT)

    # Create the JSON file - there is not PDF output here
    filename = tempfile.gettempdir() + "/output_32"
    report.save(filename, True)


if __name__ == '__main__':
    sample_32()
