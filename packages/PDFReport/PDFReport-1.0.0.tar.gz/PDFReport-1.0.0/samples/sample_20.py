import tempfile
from PDFReport import *


def sample_20():
    """
    How to use BoxFrames with borders
    """

    # Init a new Report
    report = Report()

    # Add a box 70mm by 50mm with a thin red border around it
    BoxFrame(report.body, 70.0, 50.0, 0.1, "#FF0000")

    # Add vertical distance of 10mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=10.0)

    # Add a box 150mm by 20mm with a red border around it
    # the left and right lines are 5mm width.
    box = BoxFrame(report.body, 150.0, 20.0, 0.1, "#FF0000")
    box.border.left_pen.extent = 5.0
    box.border.right_pen.extent = 5.0

    # Add vertical distance of 10mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=10.0)

    # Add a box 10mm height using the full width. It has different pens for the lines
    box = BoxFrame(report.body, 0.0, 10.0, 0.1, "#0000FF")
    box.use_full_width = True
    box.border.top_pen.extent = 1.0
    box.border.left_pen.extent = 2.0
    box.border.bottom_pen.extent = 3.0
    box.border.bottom_pen.color = "#FF00FF"
    box.border.right_pen.extent = 4.0
    box.border.right_pen.color = "#FF00FF"

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_20"
    report.output(filename, True)


if __name__ == '__main__':
    sample_20()
