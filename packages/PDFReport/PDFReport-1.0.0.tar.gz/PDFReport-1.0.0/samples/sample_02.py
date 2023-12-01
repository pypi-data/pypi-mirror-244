import tempfile
from PDFReport import *


def sample_02():
    """
    Simple empty report with paper format Letter in landscape mode with a margin of one inch on top and half
    an inch on the other
    """

    # Define the page format to be used in the report
    page_format = PageFormat(PageSize.SIZE_LETTER, PageOrientation.LANDSCAPE, 25.4 / 2.0, 25.4, 25.4 / 2.0, 25.4 / 2.0)

    # Init a new Report
    report = Report(page_format)

    # Add a box to show the printable area in the report
    bf = BoxFrame(report.body)
    bf.set_border_pen(Pen(0.1))

    # Create a frame that uses the full width and height
    f = SerialFrame(bf, Direction.HORIZONTAL, use_full_width=True)
    f.use_full_height = True

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_02"
    report.output(filename, True)


if __name__ == '__main__':
    sample_02()
