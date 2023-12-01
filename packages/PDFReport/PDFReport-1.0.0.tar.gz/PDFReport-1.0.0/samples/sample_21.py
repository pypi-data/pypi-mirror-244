import tempfile
from PDFReport import *


shortText = "Gute Susanne sah im einer Augen erst der im gewesen."
text = ("Gute Susanne sah im einer Augen erst der im gewesen. Staatliche einer als für diesmal der. Ihr wie des "
        "bewegen Vorgang wieder, sagte wenn legitimen Ziel Vorsorge. Jemand man so zueinander für Schlimmste. Es "
        "wichtiger die das eine auf nicht einer eine Ziel freien. Man Netz dreinblickte verbrachte derartige neuen. "
        "Es ihm zum ihr Interesse den besass er sie ihr seine, die die in mit Spass, das Tage eine beobachtete nicht "
        "und, machte umher zu Technologien zweifelhaft.")


def sample_21():
    """
    Use BoxFrames to place and format texts in them
    """

    # Init a new Report
    report = Report()
    body = report.body

    # Add a box to the body with a width of 50mm. The box has no border
    # so, it is just used to limit the space for the following text frame
    box = BoxFrame(body, 50.0)

    # Add text frame to the box it uses the full width of the surrounding box
    TextFrame(box, text, TextStyle.NORMAL, True)

    # Add vertical distance of 10mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

    # Add a box to the body with a width of 120mm. The box has no border
    # so, it is just used to limit the space for the following text frame
    box = BoxFrame(body, 120.0)

    # Add text frame to the box it uses the full width of the surrounding box
    TextFrame(box, text, TextStyle.BOLD, True)

    # Add vertical distance of 10mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

    # Add a box to the body with a width of 400mm. The box has no border
    # so, it is just used to limit the space for the following text frame
    box = BoxFrame(body, 40.0)

    # Add text frame to the box it uses the full width of the surrounding box
    # the text will be printed centered.
    TextFrame(box, text, TextStyle.BOLD, True, TextAlign.CENTER)

    # Add vertical distance of 10mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)

    # Add a box to the body with a width of 140mm. The box has a thin border
    # and a margin of 20mm on the left and, it uses a padding of 1mm on all sides
    # without the padding the text would stick on the line
    bf = BoxFrame(body, 140.0, border_extent=0.1)
    bf.margin_left = 20.0
    bf.set_padding(1.0)

    # Add text frame to the box it uses the full width of the surrounding box
    # the text will be printed justified.
    TextFrame(bf, text, TextStyle.NORMAL, True, TextAlign.JUST)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_21"
    report.output(filename, True)


if __name__ == '__main__':
    sample_21()
