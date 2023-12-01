import tempfile

from PDFReport import *


def sample_01():
    """
    Simple empty report with paper format A4 in portrait mode with default margins, showing the printable area
    """

    # Init a new Report
    report = Report()

    # Add a box to show the printable area in the report
    bf = BoxFrame(report.body)
    bf.set_border_pen(Pen(0.1))

    # Create a frame that uses the full width and height
    f = SerialFrame(bf, Direction.HORIZONTAL, use_full_width=True)
    f.use_full_height = True

    # Create the PDF
    filename = str(tempfile.gettempdir()) + "/output_01"
    report.output(filename, True)


if __name__ == '__main__':
    sample_01()
