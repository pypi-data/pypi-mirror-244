import tempfile
from PDFReport import *


def sample_34():
    """
    How to use BoxFrames with borders
    """

    # Init a new Report
    report = Report()

    # Add 5 boxes with a fix height of 80mm
    # Creates an implicit page break after 3 boxes because there is no space for the 4th box
    for i in range(0, 5):

        # Add a box with 80mm height and a thin red border around it
        # The box will be printed on one page, if no space left the box starts on the next page
        box = BoxFrame(report.body, 0.0, 80.0, 0.1, "#FF0000", keep_together=True)
        box.use_full_width = True

        # Add vertical distance of 3mm after the box
        SerialFrame(report.body, Direction.VERTICAL, margin_bottom=3.0)

    # Add 3 more boxes with 10 lines of text each.
    # After 1 box an implicit page break will be added
    for i in range(0, 3):

        # Add a box with a thin red border around it. The size is defined by its content
        # It has the flag to keep the box together on one page.
        box = BoxFrame(report.body, border_extent=0.1, border_color="#FF0000", keep_together=True)
        box.set_padding(2.0)

        # Add a vertical container frame to the box to fill it with some content
        sf = SerialFrame(box, Direction.VERTICAL)

        # Add 10 lines of text
        for j in range(0, 10):
            # Add a text frame
            TextFrame(sf, "This is some text with a border line around the box.")

            # Add vertical distance of 2mm after a line of text.
            # But not after the last row of text.
            if j < 9:
                SerialFrame(sf, Direction.VERTICAL, margin_bottom=2.0)

        # Add vertical distance of 10mm after the box
        SerialFrame(report.body, Direction.VERTICAL, margin_bottom=10.0)

    # Add vertical containers with keep together flag active
    for i in range(0, 5):

        # Add a vertical container frame to the body and fill it with some lines of text
        sf = SerialFrame(report.body, Direction.VERTICAL)
        sf.keep_together = True

        # Add 5 lines of text
        for j in range(0, 5):
            # Add a text frame
            TextFrame(sf, "This is some text without a border line around the box.")
            SerialFrame(sf, Direction.VERTICAL, margin_bottom=2.0)

        # Add vertical distance of 10mm after the vertical container
        SerialFrame(report.body, Direction.VERTICAL, margin_bottom=10.0)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_34"
    report.output(filename, True)


if __name__ == '__main__':
    sample_34()
