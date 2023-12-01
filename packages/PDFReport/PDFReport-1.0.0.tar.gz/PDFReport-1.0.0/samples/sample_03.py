import tempfile
from PDFReport import *

text = ("Gute Susanne sah im einer Augen erst der im gewesen. Staatliche einer als für diesmal der. Ihr wie des "
        "bewegen Vorgang wieder, sagte wenn legitimen Ziel Vorsorge. Jemand man so zueinander für Schlimmste. Es "
        "wichtiger die das eine auf nicht einer eine Ziel freien. Man Netz dreinblickte verbrachte derartige neuen. "
        "Es ihm zum ihr Interesse den besass er sie ihr seine, die die in mit Spass, das Tage eine beobachtete nicht "
        "und, machte umher zu Technologien zweifelhaft.")


def sample_03():
    """
    Report with default format and three paragraphs of text on it
    """

    # Init a new Report
    report = Report()

    # Add 3 text frames to the body frame of the report
    TextFrame(report.body, text)
    TextFrame(report.body, text)
    TextFrame(report.body, text)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_03"
    report.output(filename, True)


if __name__ == '__main__':
    sample_03()
