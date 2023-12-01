import tempfile
from PDFReport import *


def sample_11():
    """
    Adding barcodes to a report
    """

    # Init a new Report
    report = Report()

    # Add a QR Code in a box of 50mm by 50mm
    BarcodeFrame(report.body, "adiuvaris.ch/reportlib", BarcodeType.QRCODE, 50.0, 50.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a QR Code in a box of 30mm by 40mm - it will use 30x30mm and a margin 5mm at the bottom and the top
    BarcodeFrame(report.body, "adiuvaris.ch/reportlib", BarcodeType.QRCODE, 30.0, 40.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a QR Code in a box of 100mm by 40mm - it will use 40x40mm and a margin of 30mm to the left and the right
    BarcodeFrame(report.body, "adiuvaris.ch/reportlib", BarcodeType.QRCODE, 100.0, 40.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a Code39 barcode
    BarcodeFrame(report.body, "123451234512345", BarcodeType.CODE39, 40.0, 10.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a EAN13 barcode
    BarcodeFrame(report.body, "123456789012", BarcodeType.EAN13, 40.0, 10.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a EAN8 barcode
    BarcodeFrame(report.body, "12345678", BarcodeType.EAN8, 40.0, 10.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a EAN14 barcode
    BarcodeFrame(report.body, "12345678123456", BarcodeType.EAN14, 40.0, 10.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a ISBN13 barcode
    BarcodeFrame(report.body, "979106789012", BarcodeType.ISBN13, 40.0, 10.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a ISBN10 barcode
    BarcodeFrame(report.body, "979106789", BarcodeType.ISBN10, 40.0, 10.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a ISSN barcode
    BarcodeFrame(report.body, "979106789", BarcodeType.ISSN, 40.0, 10.0)

    # Add vertical distance of 5mm
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)

    # Add a UPCA barcode
    BarcodeFrame(report.body, "97910678912", BarcodeType.UPCA, 40.0, 10.0)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_11"
    report.output(filename, True)


if __name__ == '__main__':
    sample_11()
