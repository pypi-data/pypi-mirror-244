import pathlib
import tempfile
from PDFReport import *


sample_path = str(pathlib.Path(__file__).parent)


def sample_10():
    """
    Adding images to a report
    """

    # Init a new Report
    report = Report()

    # Add image in a box of max. 100mm x 100mm - will use the full 100mm width
    # but the height will be adjusted to keep the aspect ratio
    ImageFrame(report.body, sample_path + "/image.jpg", 100.0, 100.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add image in a box of max. 100mm x 30mm - will shrink the width of the image
    # because the height is max 30mm and the aspect ratio will be kept
    ImageFrame(report.body, sample_path + "/image.jpg", 100.0, 30.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add image in a box of max. 20mm x 40mm - ignore aspect ratio
    # So it will use a box of 20mm width and 40mm height
    ImageFrame(report.body, sample_path + "/image.jpg", 20.0, 40.0, False)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_10"
    report.output(filename, True)


if __name__ == '__main__':
    sample_10()
