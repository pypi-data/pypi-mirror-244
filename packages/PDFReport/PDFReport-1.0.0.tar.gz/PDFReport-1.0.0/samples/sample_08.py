import tempfile
from PDFReport import *


def sample_08():
    """
    Adding horizontal lines with convenience functions and manually with LineFrames and Pens
    """

    # Init a new Report
    report = Report()
    body = report.body

    # Add a horizontal line 0.5mm width using the full width
    LineFrame(body, Direction.HORIZONTAL, 0.5)

    # Add vertical distance of 5mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a horizontal line 1mm width using the full width
    LineFrame(body, Direction.HORIZONTAL, 1.0)

    # Add vertical distance of 5mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a green horizontal line 0.5mm width, centered and 100mm long
    LineFrame(body, Direction.HORIZONTAL, 0.5, "#00FF00", 100.0, HAlign.CENTER)

    # Add vertical distance of 5mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a dashed red horizontal line 0.2mm width and 120mm long
    lf = LineFrame(body, Direction.HORIZONTAL, length=120.0)
    pen = Pen(0.2, "#FF0000", LineStyle.DASH)
    lf.pen = pen

    # Add vertical distance of 5mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a dotted blue horizontal line 0.2mm width and 50mm long and right aligned
    lf = LineFrame(body, Direction.HORIZONTAL, length=50.0, h_align=HAlign.RIGHT)
    pen = Pen(0.2, "#0000FF", LineStyle.DOT)
    lf.pen = pen

    # Add vertical distance of 5mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a dashed grey horizontal line 0.5mm width and using the full width of the frame
    lf = LineFrame(body, Direction.HORIZONTAL)
    pen = Pen(0.5, "#CCCCCC", LineStyle.DASH)
    lf.pen = pen

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_08"
    report.output(filename, True)


if __name__ == '__main__':
    sample_08()
