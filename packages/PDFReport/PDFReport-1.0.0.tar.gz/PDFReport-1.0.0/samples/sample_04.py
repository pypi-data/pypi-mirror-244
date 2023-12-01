import tempfile
from PDFReport import *


shortText = "Gute Susanne sah im einer Augen erst der im gewesen."
text = ("Gute Susanne sah im einer Augen erst der im gewesen. Staatliche einer als für diesmal der. Ihr wie des "
        "bewegen Vorgang wieder, sagte wenn legitimen Ziel Vorsorge. Jemand man so zueinander für Schlimmste. Es "
        "wichtiger die das eine auf nicht einer eine Ziel freien. Man Netz dreinblickte verbrachte derartige neuen. "
        "Es ihm zum ihr Interesse den besass er sie ihr seine, die die in mit Spass, das Tage eine beobachtete nicht "
        "und, machte umher zu Technologien zweifelhaft.")


def sample_04():
    """
    Report with text paragraphs showing different formatting possibilities
    """

    # Init a new Report
    report = Report()

    # Add text frame with NORMAL text style, default left aligned
    TextFrame(report.body, text)

    # Add vertical distance of 10mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=10.0)

    # Add text frame with NORMAL text style, right aligned
    TextFrame(report.body, text, text_align=TextAlign.RIGHT)

    # Add vertical distance of 10mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=10.0)

    # Add text frame with NORMAL text style, justify aligned
    TextFrame(report.body, text, text_align=TextAlign.JUST)

    # Add vertical distance of 10mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=10.0)

    # Add text frame with NORMAL text style, centered
    # Use full width of the frame so the centering can take effect
    TextFrame(report.body, shortText, use_full_width=True, text_align=TextAlign.CENTER)

    # Add vertical distance of 10mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=10.0)

    # Add text frame with NORMAL text style, centered, red text color
    # Use full width of the frame so the centering can take effect
    te = TextFrame(report.body, shortText, use_full_width=True, text_align=TextAlign.CENTER)
    te.text_style.text_color = "#FF0000"

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_04"
    report.output(filename, True)


if __name__ == '__main__':
    sample_04()
