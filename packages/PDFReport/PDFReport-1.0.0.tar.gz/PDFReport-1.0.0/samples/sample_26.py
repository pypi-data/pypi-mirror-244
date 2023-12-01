import tempfile
from PDFReport import *

import pathlib
sample_path = str(pathlib.Path(__file__).parent)

shortText = "Gute Susanne sah im einer Augen erst der im gewesen."
text = ("Gute Susanne sah im einer Augen erst der im gewesen. Staatliche einer als für diesmal der. Ihr wie des "
        "bewegen Vorgang wieder, sagte wenn legitimen Ziel Vorsorge. Jemand man so zueinander für Schlimmste. Es "
        "wichtiger die das eine auf nicht einer eine Ziel freien. Man Netz dreinblickte verbrachte derartige neuen. "
        "Es ihm zum ihr Interesse den besass er sie ihr seine, die die in mit Spass, das Tage eine beobachtete nicht "
        "und, machte umher zu Technologien zweifelhaft.")


def sample_26():
    """
    BoxFrames using percent values as width
    This is sample 22 printed 3 times on different page sizes to show the
    flexibility of the library
    """

    # Init a new Report
    report = Report()
    body = report.body

    for i in range(0, 3):

        # Create a horizontal container frame in the body
        sf = SerialFrame(body, Direction.HORIZONTAL)

        # Add a box to the horizontal frame which uses 40% of the surrounding frame
        box = BoxFrame(sf, "40.0%")

        # Add a text to the box using the full width of the box
        TextFrame(box, text, TextStyle.NORMAL, True)

        # Add another box to the horizontal frame which uses 60% of the surrounding frame
        box = BoxFrame(sf, "60.0%")

        # Add a bold text to the box using the full width of the box
        TextFrame(box, text, TextStyle.BOLD, True)

        # Add vertical distance of 10mm
        SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

        # Create another horizontal container frame in the body
        sf = SerialFrame(body, Direction.HORIZONTAL)

        # Add a box to the horizontal frame which uses 33.3% of the surrounding frame
        # and add a padding of 2mm on the right side of the box
        box = BoxFrame(sf, "33.33%")
        box.padding_right = 2.0

        # Add justified text to the box
        TextFrame(box, text, TextStyle.NORMAL, text_align=TextAlign.JUST)

        # Add another box to the horizontal frame which uses 33.3% of the surrounding frame
        # and add a padding of 1mm left and right of the box
        box = BoxFrame(sf, "33.33%")
        box.padding_right = 1.0
        box.padding_left = 1.0

        # Add justified text to the box
        TextFrame(box, text, TextStyle.NORMAL, text_align=TextAlign.JUST)

        # Add another box to the horizontal frame which uses 33.3% of the surrounding frame
        # and add a padding of 2mm on the left side of the box
        box = BoxFrame(sf, "33.33%")
        box.padding_left = 2.0

        # Add justified text to the box
        TextFrame(box, text, TextStyle.NORMAL, text_align=TextAlign.JUST)

        # Add vertical distance of 10mm
        SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

        # Create another horizontal container frame in the body
        sf = SerialFrame(body, Direction.HORIZONTAL)

        # Add a box to the horizontal frame which uses 25% of the surrounding frame
        # and add a padding of 5mm on the right side of the box
        box = BoxFrame(sf, "25.0%")
        box.margin_right = 5.0

        # Add a barcode in the box with a max of 100mm by 100mm.
        # The output will be limited by the box width
        BarcodeFrame(box, "adiuvaris.ch/reportlib", BarcodeType.QRCODE, 100.0, 100.0)

        # Add a box to the horizontal frame which uses 40% of the surrounding frame
        box = BoxFrame(sf, "40.0%")

        # Add an image to the box with a max of 50mm by 30mm.
        # The output will be limited by the box width and the image is centered in the box
        # therefore it has some space on left and the right side of it
        ifr = ImageFrame(box, sample_path + "/image.jpg", 50.0, 30.0, True)
        ifr.h_align = HAlign.CENTER

        # Add a box to the horizontal frame which uses 45% of the surrounding frame
        box = BoxFrame(sf, "45.0%")

        # Add text to the box
        TextFrame(box, text, TextStyle.NORMAL, True)

        # Add vertical distance of 10mm
        SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

        # Create another horizontal container frame in the body
        sf = SerialFrame(body, Direction.HORIZONTAL)

        # Add a box to the horizontal frame which uses 20% of the surrounding frame
        box = BoxFrame(sf, "20.0%")

        # Add right aligned text to the box
        TextFrame(box, "Label 1: ", TextStyle.NORMAL, text_align=TextAlign.RIGHT)

        # Add text to the horizontal frame. It will be printed after the previously defined box
        TextFrame(sf, "Text for Label 1", TextStyle.BOLD)

        # Create another horizontal container frame in the body
        sf = SerialFrame(body, Direction.HORIZONTAL)

        # Add a box to the horizontal frame which uses 20% of the surrounding frame
        box = BoxFrame(sf, "20.0%")

        # Add right aligned text to the box
        TextFrame(box, "Another Label: ", TextStyle.NORMAL, text_align=TextAlign.RIGHT)

        # Add text to the horizontal frame. It will be printed after the previously defined box
        TextFrame(sf, "Text for the second label", TextStyle.BOLD)

        # After the first page change the page margins
        if i == 0:
            page_format = PageFormat(PageSize.SIZE_A4, PageOrientation.PORTRAIT, 40.0, 15.0, 30.0, 15.0)
            BreakFrame(body, page_format)

        # After the second page change the page format to landscape
        elif i == 1:
            page_format = PageFormat(PageSize.SIZE_A4, PageOrientation.LANDSCAPE, 30.0, 30.0, 20.0, 15.0)
            BreakFrame(body, page_format)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_26"
    report.output(filename, True)


if __name__ == '__main__':
    sample_26()
