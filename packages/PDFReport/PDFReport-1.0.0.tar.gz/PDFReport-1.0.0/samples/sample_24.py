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


def add_header(header: SerialFrame):

    # Add vertical container frame to the header
    vc = SerialFrame(header, Direction.VERTICAL, margin_bottom=5.0, use_full_width=True)

    # Add box to the container with a height of 15mm and using the full width.
    # It has a grey background and a padding of 1mm on all sides
    box = BoxFrame(vc)
    box.use_full_width = True
    box.set_padding(1.0)
    box.height = 15.0
    box.background = "#EEEEEE"

    # Add a horizontal container frame to the box which uses full height and width
    hc = SerialFrame(box, Direction.HORIZONTAL)
    hc.use_full_width = True
    hc.use_full_height = True

    # Add an image to the horizontal container with a max. height of 10mm vertically in the middle
    # of the surrounding frame.
    ifr = ImageFrame(hc, sample_path + "/logo.png", 0.0, 10.0, True)
    ifr.v_align = VAlign.MIDDLE

    # Add a two line text on the right side of the horizontal container using bold text style
    TextFrame(hc, "Fancy report\nwith a header and a footer", TextStyle.BOLD, text_align=TextAlign.RIGHT)

    # Add a horizontal container frame to the vertical frame and add a green line to it
    hc = SerialFrame(vc, Direction.HORIZONTAL)
    lf = LineFrame(hc, Direction.HORIZONTAL, 0.3, "#00FF00")


def add_footer(footer: SerialFrame):

    # Add vertical container frame to the footer
    vc = SerialFrame(footer, Direction.VERTICAL, margin_top=5.0, use_full_width=True)

    # Add a horizontal container frame to the vertical frame and add a black line to it 0.3mm thick
    hc = SerialFrame(vc, Direction.HORIZONTAL)
    lf = LineFrame(hc, Direction.HORIZONTAL, 0.3)

    # Add box to the vertical container with a height of 10mm and using the full width.
    # It has a margin on top of 5mm (the body can not come nearer than 5mm to the footer)
    box = BoxFrame(vc)
    box.use_full_width = True
    box.height = 10.0
    box.margin_top = 0.5

    # Add a text on the right side of the box. It uses variables that will be filled by the library.
    # The variables ar for the number of the current page and the total number of pages.
    TextFrame(box, "Page [VAR_PAGE] of [VAR_TOTAL_PAGES]", TextStyle.NORMAL, text_align=TextAlign.RIGHT)


def sample_24():
    """
    Header and footer
    """

    # Init a new Report and define that the pages should be counted before printing
    # because we want to use the variable VAR_TOTAL_PAGES
    report = Report()
    report.count_pages = True

    # Add the header a header frame
    add_header(report.header)

    # Add a footer to the footer frame
    add_footer(report.footer)

    # Manual page break to show that the header anf footer will be repeated on every page
    BreakFrame(report.body)

    # Manual page break to show that the header anf footer will be repeated on every page
    BreakFrame(report.body)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_24"
    report.output(filename, True)


if __name__ == '__main__':
    sample_24()
