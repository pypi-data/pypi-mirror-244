import tempfile
from PIL import ImageColor
from PDFReport import *


def sample_06():
    """
    Adjust the predefined text styles to use other font families or sizes and colors
    """

    # Init a new Report
    # Define that the font family should be Times and the default size to be 11 points
    # This will be used for all predefined text styles (if not changed later)
    report = Report(font_family="Times", font_size=11.0)
    body = report.body

    # Change the font family for some text styles to Courier
    TextStyles[TextStyle.TABLE_HEADER].font_family = "Courier"
    TextStyles[TextStyle.TABLE_ROW].font_family = "Courier"
    TextStyles[TextStyle.TABLE_TOTAL].font_family = "Courier"
    TextStyles[TextStyle.TABLE_SUBTOTAL].font_family = "Courier"

    # Change the text color for Header and Footer text style
    TextStyles[TextStyle.FOOTER].text_color = "#CCCCCC"
    TextStyles[TextStyle.HEADER].text_color = ImageColor.colormap["lime"]

    # Add text frames with all the predefined but adjusted text styles
    TextFrame(body, "NORMAL (Times, 11 points)", TextStyle.NORMAL)
    TextFrame(body, "BOLD is the NORMAL style but bold font face", TextStyle.BOLD)
    TextFrame(body, "ITALIC is the NORMAL style but italic", TextStyle.ITALIC)
    TextFrame(body, "UNDERLINE is the NORMAL style but underlined", TextStyle.UNDERLINE)
    TextFrame(body, "SMALL is the NORMAL style but one point smaller", TextStyle.SMALL)
    TextFrame(body, "HEADING1 is the NORMAL style but nine points taller and bold face", TextStyle.HEADING1)
    TextFrame(body, "HEADING2 is the NORMAL style but six points taller and bold face", TextStyle.HEADING2)
    TextFrame(body, "HEADING3 is the NORMAL style but three points taller and bold face and italic", TextStyle.HEADING3)
    TextFrame(body, "HEADING4 is the NORMAL style but one point taller and bold face and italic", TextStyle.HEADING4)
    TextFrame(body, "TABLE_HEADER is the NORMAL style but one point smaller and bold (courier!)", TextStyle.TABLE_HEADER)
    TextFrame(body, "TABLE_ROW is the NORMAL style but one point smaller (courier!)", TextStyle.TABLE_ROW)
    TextFrame(body, "TABLE_SUBTOTAL is the NORMAL style but one point smaller and italic (courier!)", TextStyle.TABLE_SUBTOTAL)
    TextFrame(body, "TABLE_TOTAL is the NORMAL style but one point smaller and bold (courier!)", TextStyle.TABLE_TOTAL)
    TextFrame(body, "FOOTER is the NORMAL style but one point smaller (grey!)", TextStyle.FOOTER)
    TextFrame(body, "HEADER is the NORMAL style but one point smaller (green!)", TextStyle.HEADER)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_06"
    report.output(filename, True)


if __name__ == '__main__':
    sample_06()
