import tempfile
from PDFReport import *


shortText = "Gute Susanne sah im einer Augen erst der im gewesen."
text = ("Gute Susanne sah im einer Augen erst der im gewesen. Staatliche einer als für diesmal der. Ihr wie des "
        "bewegen Vorgang wieder, sagte wenn legitimen Ziel Vorsorge. Jemand man so zueinander für Schlimmste. Es "
        "wichtiger die das eine auf nicht einer eine Ziel freien. Man Netz dreinblickte verbrachte derartige neuen. "
        "Es ihm zum ihr Interesse den besass er sie ihr seine, die die in mit Spass, das Tage eine beobachtete nicht "
        "und, machte umher zu Technologien zweifelhaft.")


def add_header(header: SerialFrame):

    # Add a page frame to the header which will be printed on all pages but the first
    pf = PageFrame(header, PageFrame.ON_ALL_BUT_FIRST_PAGE)

    # Add box to the page frame with a height of 15mm and using the full width.
    # It has a grey background and a padding of 1mm on all sides
    box = BoxFrame(pf)
    box.use_full_width = True
    box.set_padding(1.0)
    box.height = 15.0
    box.background = "#EEEEEE"

    # Add horizontal container frame to the box
    hf = SerialFrame(box, Direction.HORIZONTAL)

    # Add box to the horizontal frame
    TextFrame(hf, "Header for all pages but not on the first page.", TextStyle.BOLD)


def add_footer(footer: SerialFrame, on_page_nr: int, text_align: TextAlign):

    # Add a page frame to the header only on the pages defined in the parameter on_page_nr
    pf = PageFrame(footer, on_page_nr)

    # Add horizontal container frame to the page frame
    hc = SerialFrame(pf, Direction.HORIZONTAL)

    # Add a horizontal line
    lf = LineFrame(hc, Direction.HORIZONTAL, 0.3)

    # Add a box to the page frame with a height of 10mm and a margin of 5mm on top
    box = BoxFrame(pf)
    box.margin_top = 0.5
    box.use_full_width = True
    box.height = 10.0

    # Add text to the box with the given alignment
    TextFrame(box, "Page [VAR_PAGE] of [VAR_TOTAL_PAGES]", TextStyle.NORMAL, text_align=text_align)


def sample_25():
    """
    Different headers and footers via PageFrames
    """

    # Init a new Report and define that the pages should be counted before printing
    # because we want to use the variable VAR_TOTAL_PAGES
    report = Report()
    report.count_pages = True

    # Add the header a header frame (will not be printed on the first page)
    add_header(report.header)

    # Add a footer to the footer frame for odd pages
    add_footer(report.footer, PageFrame.ON_ODD_PAGES, TextAlign.RIGHT)

    # Add another footer to the footer frame for even pages
    add_footer(report.footer, PageFrame.ON_EVEN_PAGES, TextAlign.LEFT)

    # Manual page break to show that the header anf footer will be repeated on every page
    BreakFrame(report.body)

    # Manual page break to show that the header anf footer will be repeated on every page
    BreakFrame(report.body)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_25"
    report.output(filename, True)


if __name__ == '__main__':
    sample_25()
