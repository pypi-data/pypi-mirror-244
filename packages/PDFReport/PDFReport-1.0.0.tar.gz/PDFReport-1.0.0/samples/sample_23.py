import tempfile
from PDFReport import *


shortText = "Gute Susanne sah im einer Augen erst der im gewesen."
text = ("Gute Susanne sah im einer Augen erst der im gewesen. Staatliche einer als für diesmal der. Ihr wie des "
        "bewegen Vorgang wieder, sagte wenn legitimen Ziel Vorsorge. Jemand man so zueinander für Schlimmste. Es "
        "wichtiger die das eine auf nicht einer eine Ziel freien. Man Netz dreinblickte verbrachte derartige neuen. "
        "Es ihm zum ihr Interesse den besass er sie ihr seine, die die in mit Spass, das Tage eine beobachtete nicht "
        "und, machte umher zu Technologien zweifelhaft.")


def sample_23():
    """
    Use position frames to place content on an absolute position on the report
    """

    # Init a new Report
    report = Report()
    body = report.body

    # Add a position frame at x=120mm and y=50mm from the paper border
    fix = PositionFrame(body, 120.0, 50.0)

    # Add a box to show where the position frame will be printed
    # it has a thin red border and a size of 50mm by 70mm
    BoxFrame(fix, 50.0, 70.0, 0.1, "#FF0000")

    # Add vertical distance of 10mm to the body
    SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

    # Add some text to the body
    TextFrame(body, text, TextStyle.NORMAL)

    # Add a position frame at x=60mm and y=130mm from the paper border
    # Because there is already something on that spot the library will add
    # a page break (because the frame has not set the overlay flag)
    fix = PositionFrame(body, 60.0, 130.0)

    # Add a box to show where the position frame will be printed
    # it has a thin grey border and a size of 100mm by 50mm
    box = BoxFrame(fix, 100.0, 50.0, 0.1, "#CCCCCC")

    # Add vertical distance of 10mm to the body
    SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

    # Add some text to the body
    TextFrame(body, text, TextStyle.NORMAL)

    BreakFrame(body)

    # Add a position frame at x=120mm and y=50mm from the paper border
    fix = PositionFrame(body, 120.0, 50.0)

    # Add a box to show where the position frame will be printed
    # it has a thin red border and a size of 50mm by 70mm
    BoxFrame(fix, 50.0, 70.0, 0.1, "#FF0000")

    # Add vertical distance of 10mm to the body
    SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

    # Add some text to the body
    TextFrame(body, text, TextStyle.NORMAL)

    # Add a position frame at x=60mm and y=130mm from the paper border
    # Because of the overlay flag the following box will overprint the text
    fix = PositionFrame(body, 60.0, 130.0, overlay=True)

    # Add a box to show where the position frame will be printed
    # it has a thin grey border and a size of 100mm by 50mm
    box = BoxFrame(fix, 100.0, 50.0, 0.1, "#CCCCCC")

    # Add vertical distance of 10mm to the body
    SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

    # Add some text to the body
    TextFrame(body, text, TextStyle.NORMAL)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_23"
    report.output(filename, True)


if __name__ == '__main__':
    sample_23()
