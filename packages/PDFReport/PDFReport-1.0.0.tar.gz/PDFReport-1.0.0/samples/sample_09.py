import tempfile
from PDFReport import *


shortText = "Gute Susanne sah im einer Augen erst der im gewesen."
text = ("Gute Susanne sah im einer Augen erst der im gewesen. Staatliche einer als für diesmal der. Ihr wie des "
        "bewegen Vorgang wieder, sagte wenn legitimen Ziel Vorsorge. Jemand man so zueinander für Schlimmste. Es "
        "wichtiger die das eine auf nicht einer eine Ziel freien. Man Netz dreinblickte verbrachte derartige neuen. "
        "Es ihm zum ihr Interesse den besass er sie ihr seine, die die in mit Spass, das Tage eine beobachtete nicht "
        "und, machte umher zu Technologien zweifelhaft.")


def sample_09():
    """
    Automatic and manual page breaks and changes of the page formats and margins
    """

    # Init a new Report
    report = Report()
    body = report.body

    # Add 20 times text to the body using the default page format
    # It will break automatically to a second page
    for i in range(0, 20):
        TextFrame(body, "Paragraph number " + str(i + 1), TextStyle.NORMAL)
        TextFrame(body, text, TextStyle.NORMAL)

        # Add vertical distance of 2mm between the text frames
        SerialFrame(body, Direction.VERTICAL, margin_bottom=2.0)

    # Add a manual page break
    BreakFrame(body)

    # Add text to the body (on the 3. page)
    TextFrame(body, text, TextStyle.NORMAL)

    # Add a manual page break and use a different page format from now on
    page_format = PageFormat(PageSize.SIZE_A4, PageOrientation.LANDSCAPE, 30.0, 20.0, 30.0)
    BreakFrame(body, page_format)

    # Add 12 times text to the body using the new page format
    # It will start on the 4. page and breaks automatically to a 5. page
    for i in range(0, 12):
        TextFrame(body, "Paragraph number " + str(i + 1), TextStyle.NORMAL)
        TextFrame(body, text, TextStyle.NORMAL)

        # Add vertical distance of 3mm between the text frames
        SerialFrame(body, Direction.VERTICAL, margin_bottom=3.0)

    # Add a manual page break and use a different page format from now on (A5)
    page_format = PageFormat(PageSize.SIZE_A5, PageOrientation.LANDSCAPE)
    BreakFrame(body, page_format)

    # Add text to the body (on the 6. page)
    TextFrame(body, text, TextStyle.NORMAL)

    # Add a manual page break and use a different page format from now on (A5 landscape)
    page_format = PageFormat(PageSize.SIZE_A5, PageOrientation.PORTRAIT, 20.0, 10.0, 10.0, 10.0, True)
    BreakFrame(body, page_format)

    # Add 10 times text to the body using the new page format
    # It will start on the 7. page and breaks automatically to a 8. page
    for i in range(0, 10):
        TextFrame(body, "Paragraph number " + str(i + 1), TextStyle.NORMAL)
        TextFrame(body, text, TextStyle.NORMAL)

        # Add vertical distance of 3mm between the text frames
        SerialFrame(body, Direction.VERTICAL, margin_bottom=3.0)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_09"
    report.output(filename, True)


if __name__ == '__main__':
    sample_09()
