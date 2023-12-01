import tempfile
from PDFReport import *


def sample_05():
    """
    Using the predefined text styles
    """

    # Init a new Report
    report = Report()
    body = report.body

    # Add text frames with all the predefined text styles
    TextFrame(body, "NORMAL (Helvetica, 9 points)", TextStyle.NORMAL)
    TextFrame(body, "BOLD is the NORMAL style but bold font face", TextStyle.BOLD)
    TextFrame(body, "ITALIC is the NORMAL style but italic", TextStyle.ITALIC)
    TextFrame(body, "UNDERLINE is the NORMAL style but underlined", TextStyle.UNDERLINE)
    TextFrame(body, "SMALL is the NORMAL style but one point smaller", TextStyle.SMALL)
    TextFrame(body, "HEADING1 is the NORMAL style but nine points taller and bold face", TextStyle.HEADING1)
    TextFrame(body, "HEADING2 is the NORMAL style but six points taller and bold face", TextStyle.HEADING2)
    TextFrame(body, "HEADING3 is the NORMAL style but three points taller and bold face and italic", TextStyle.HEADING3)
    TextFrame(body, "HEADING4 is the NORMAL style but one point taller and bold face and italic", TextStyle.HEADING4)
    TextFrame(body, "TABLE_HEADER is the NORMAL style but one point smaller and bold", TextStyle.TABLE_HEADER)
    TextFrame(body, "TABLE_ROW is the NORMAL style but one point smaller", TextStyle.TABLE_ROW)
    TextFrame(body, "TABLE_SUBTOTAL is the NORMAL style but one point smaller and italic", TextStyle.TABLE_SUBTOTAL)
    TextFrame(body, "TABLE_TOTAL is the NORMAL style but one point smaller and bold", TextStyle.TABLE_TOTAL)
    TextFrame(body, "FOOTER is the NORMAL style but one point smaller", TextStyle.FOOTER)
    TextFrame(body, "HEADER is the NORMAL style but one point smaller", TextStyle.HEADER)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_05"
    report.output(filename, True)


if __name__ == '__main__':
    sample_05()
