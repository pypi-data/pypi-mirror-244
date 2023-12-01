import tempfile
from PDFReport import *


shortText = "Gute Susanne sah im einer Augen erst der im gewesen."
text = ("Gute Susanne sah im einer Augen erst der im gewesen. Staatliche einer als für diesmal der. Ihr wie des "
        "bewegen Vorgang wieder, sagte wenn legitimen Ziel Vorsorge. Jemand man so zueinander für Schlimmste. Es "
        "wichtiger die das eine auf nicht einer eine Ziel freien. Man Netz dreinblickte verbrachte derartige neuen. "
        "Es ihm zum ihr Interesse den besass er sie ihr seine, die die in mit Spass, das Tage eine beobachtete nicht "
        "und, machte umher zu Technologien zweifelhaft.")


def sample_28():
    """
    Exceptions
    """

    # Init a new Report
    report = Report()
    body = report.body

    # Create an endless loop
    box1 = BoxFrame(body)
    box1.add_frame(body)
    try:
        filename = tempfile.gettempdir() + "/output_28-1"
        report.output(filename, True)
    except OverflowError as error:
        print(error)
        body.clear_frames()

    # Exception because of a frame that has to be kept together but is to height for a page.
    box = BoxFrame(body)
    box.keep_together = True
    vc = SerialFrame(box, Direction.VERTICAL)
    for i in range(0, 20):
        TextFrame(vc, "Paragraph number", TextStyle.NORMAL)
        TextFrame(vc, text, TextStyle.NORMAL)
        SerialFrame(vc, Direction.VERTICAL, margin_bottom=2.0)

    try:
        filename = tempfile.gettempdir() + "/output_28-2"
        report.output(filename, True)
    except OverflowError as error:
        print(error)
        body.clear_frames()

    # No space in frame
    report = Report()
    body = report.body

    hc = SerialFrame(body, Direction.HORIZONTAL)
    TextFrame(hc, text, TextStyle.NORMAL)
    TextFrame(hc, text, TextStyle.NORMAL)

    try:
        filename = tempfile.gettempdir() + "/output_28-3"
        report.output(filename, True)
    except OverflowError as error:
        print(error)
        body.clear_frames()

    # Exception because of PositionFrame offsets outside printable area
    report = Report()
    body = report.body

    f = PositionFrame(body, 0.0, 0.0)

    hc = SerialFrame(f, Direction.HORIZONTAL)
    lf = LineFrame(hc, Direction.HORIZONTAL, 0.3, length=999.0)
    lf.use_full_width = True

    try:
        filename = tempfile.gettempdir() + "/output_28-4"
        report.output(filename, True)
    except OverflowError as error:
        print(error)
        body.clear_frames()

    # Exception because of image-file does not exist
    report = Report()
    body = report.body

    try:
        ImageFrame(body)
        filename = tempfile.gettempdir() + "/output_28-5"
        report.output(filename, True)
    except FileNotFoundError as error:
        print(error)
        body.clear_frames()


if __name__ == '__main__':
    sample_28()
