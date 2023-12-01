import tempfile
from PDFReport import *


def sample_07():
    """
    Create new named text styles with any desired settings
    """

    # Init a new Report
    report = Report()

    # Create a text style for big red text
    ts1 = TextStyle("MyTextStyle1", font_size=36.0, text_color="#FF0000")

    # Add text with the previously defined text style using the reference to the text style
    TextFrame(report.body, "Very big red text style. Only the size and the color have been adjusted. The other attributes come from the NORMAL text style.", ts1.name)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Create a text style with a grey background
    TextStyle("MyTextStyle2", font_size=11.0, background_color="#DDDDDD")

    # Add text with the previously defined text style using its name
    TextFrame(report.body, "A text style with a grey background color. Only the background color and the size have been adjusted. The other attributes come from the NORMAL text style.", "MyTextStyle2")

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Create a text style with a grey background and blue font color, bold, italic and underlined
    ts3 = TextStyle("MyTextStyle3", font_family="Courier", font_size=16.0, text_color="#0000FF", background_color="#DDDDDD", bold=True, italic=True, underline=True)

    # Add text with the previously defined text style using the reference to the text style
    TextFrame(report.body, "A 16 point bold, italic and underlined Courier text style with a grey background and a blue font color - so all possible attributes have been adjusted.", ts3)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_07"
    report.output(filename, True)


if __name__ == '__main__':
    sample_07()
