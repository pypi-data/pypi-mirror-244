import pathlib
import tempfile

from PDFReport import *


sample_path = str(pathlib.Path(__file__).parent)


def add_header(report: Report):
    vc = SerialFrame(report.header, Direction.VERTICAL, margin_bottom=5.0, use_full_width=True)

    box = BoxFrame(vc, height=15.0)
    box.use_full_width = True

    ifr = ImageFrame(box, sample_path + "/logo2.png", 0.0, 10.0, True)
    ifr.v_align = VAlign.MIDDLE
    ifr.h_align = HAlign.RIGHT


def add_footer(report: Report):

    # Footer will only be printed on first page
    pf = PageFrame(report.footer, 1)
    pf.margin_top = 5.0

    vc = SerialFrame(pf, Direction.VERTICAL, margin_top=5.0, use_full_width=True)

    box = BoxFrame(vc)
    box.use_full_width = True

    TextFrame(box, "Adiuvaris    -    At the lake 901a    -    18957 Lakeside    -    100 000 00 01", TextStyle.BOLD, False, TextAlign.CENTER)


def print_address(report: Report):
    b = PositionFrame(report.body, 120.0, 50.0)

    adr = "Jane Doe\nSample Street 11b\n009900 Somewhere"

    frame = SerialFrame(b, Direction.VERTICAL, use_full_width=True)

    te = TextFrame(frame, adr, TextStyle.NORMAL)
    te.margin_bottom = 20.0


def print_project_object(report: Report):
    v_frame = SerialFrame(report.body, Direction.VERTICAL, use_full_width=True)
    h_frame = SerialFrame(v_frame, Direction.HORIZONTAL)

    box = BoxFrame(h_frame, 35.0)
    TextFrame(box, "Project", TextStyle.NORMAL, True)

    TextFrame(h_frame, "Test Building", TextStyle.BOLD)

    h_frame = SerialFrame(v_frame, Direction.HORIZONTAL)

    box = BoxFrame(h_frame, 35.0)
    TextFrame(box, "", TextStyle.NORMAL, True)

    title = "Example structure near the woods\n"
    TextFrame(h_frame, title, TextStyle.NORMAL)

    h_frame = SerialFrame(v_frame, Direction.HORIZONTAL)
    box = BoxFrame(h_frame, 35.0)
    TextFrame(box, "", TextStyle.NORMAL, True)
    desc = "Apartment 45"

    TextFrame(h_frame, desc, TextStyle.NORMAL)

    object_name = "Apartment\nGarage"

    SerialFrame(v_frame, Direction.VERTICAL, margin_bottom=2.0)
    h_frame = SerialFrame(v_frame, Direction.HORIZONTAL)
    box = BoxFrame(h_frame, 35.0)
    TextFrame(box, "Object", TextStyle.NORMAL, True)
    TextFrame(h_frame, object_name, TextStyle.BOLD)

    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)


def print_invoice_data(report: Report):
    v_frame = SerialFrame(report.body, Direction.VERTICAL, use_full_width=True)

    h_frame = SerialFrame(v_frame, Direction.HORIZONTAL)

    box = BoxFrame(h_frame, 35.0)
    TextFrame(box, "Invoice number", TextStyle.NORMAL, True)

    TextFrame(h_frame, "2023-09-123456", TextStyle.ITALIC)

    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=2.0)

    v_frame = SerialFrame(report.body, Direction.VERTICAL, use_full_width=True)
    h_frame = SerialFrame(v_frame, Direction.HORIZONTAL)
    box = BoxFrame(h_frame, 35.0)
    TextFrame(box, "Tax number", TextStyle.NORMAL, True)

    TextFrame(h_frame, "YYY-000-111-222", TextStyle.ITALIC)

    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)


def print_title(report: Report):
    f = SerialFrame(report.body, Direction.HORIZONTAL)
    TextFrame(f, "Final Certificate", TextStyle.HEADING1)
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)


def print_invoice_text(report: Report):
    f = SerialFrame(report.body, Direction.HORIZONTAL)
    TextFrame(f, "According to the contract we allow ourselves to invoice as follows", TextStyle.NORMAL)
    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=5.0)


def print_values(report: Report):
    tab = TableFrame(report.body)

    tab.set_margin(0.5)
    tab.inter_row_space = 0.5
    tab.inner_pen_total_top = Pen(0.0)
    tab.suppress_header_row = True
    tab.margin_bottom_subtotal = 1.2
    tab.use_full_width = True

    col_de = TableColumn(tab, "Description", 70.0)
    col_ba = TableColumn(tab, "Base", 28, TextAlign.RIGHT, 2.0)
    col_fa = TableColumn(tab, "Factor", 20.0)
    col_cu = TableColumn(tab, "Currency", 10.0)
    col_va = TableColumn(tab, "Amount", 30.0, TextAlign.RIGHT)

    row = TableRow(tab, RowType.TOTAL)
    TableCell(row, col_de, "Apartment 45 & Garage")
    TableCell(row, col_cu, "CHF")
    TableCell(row, col_va, "350'000.00")

    row = TableRow(tab)
    TableCell(row, col_de, "  ./. On Account")
    TableCell(row, col_cu, "CHF")
    TableCell(row, col_va, "-100'000.00")

    row = TableRow(tab, RowType.TOTAL)
    TableCell(row, col_de, "Pre-tax")
    TableCell(row, col_cu, "CHF")
    TableCell(row, col_va, "250'000.00")

    row = TableRow(tab)
    TableCell(row, col_de, "Tax")
    TableCell(row, col_fa, "10.0%")
    TableCell(row, col_cu, "CHF")
    TableCell(row, col_va, "25'000.00")

    row = TableRow(tab, RowType.TOTAL)
    TableCell(row, col_de, "Total")
    TableCell(row, col_cu, "CHF")
    TableCell(row, col_va, "275'000.00")

    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=8.0)


def print_payable(report: Report):
    f = SerialFrame(report.body, Direction.HORIZONTAL)
    box = BoxFrame(f, 35.0)
    TextFrame(box, "payable until", TextStyle.NORMAL, True)

    TextFrame(f, "01.01.2024", TextStyle.BOLD)

    SerialFrame(report.body, Direction.VERTICAL, margin_bottom=1.0)


def print_text_end(report: Report):
    f = SerialFrame(report.body, Direction.HORIZONTAL)
    TextFrame(f, "We thank you in advance for the transfer to our account.", TextStyle.NORMAL)


def print_greetings(report: Report):
    f = SerialFrame(report.body, Direction.VERTICAL, use_full_width=True)
    f.margin_left = 100.0
    SerialFrame(f, Direction.VERTICAL, margin_bottom=30.0)

    TextFrame(f, "Kind regards", TextStyle.NORMAL)

    SerialFrame(f, Direction.VERTICAL, margin_bottom=10.0)

    TextFrame(f, "Michael Hodel", TextStyle.ITALIC)

    TextFrame(f, "Vice President", TextStyle.NORMAL)


def add_qr_code_z(report: Report):
    qr_top_offset = 297.0 - 105.0
    f = PositionFrame(report.body, 67.0, qr_top_offset + 17.0, True)
    BarcodeFrame(f, "CH0011112222333344448\nApartment 45\n275000\n01.01.2024\nJane Doe", BarcodeType.QRCODE, 46.0, 46.0)


def convert_pt_to_mm(pt: float) -> float:
    return pt * 25.4 / 72.0


def add_qr_text(report: Report, text: str, x: float, y: float, w: float, ts: str, font_size: float, text_align: TextAlign = TextAlign.LEFT) -> float:
    qr_top_offset = 297.0 - 105.0
    f = PositionFrame(report.body, x, qr_top_offset + y, True)

    box = BoxFrame(f, w)
    TextFrame(box, text, ts, True, text_align)

    return y + convert_pt_to_mm(font_size)


def add_qr_title_e(report: Report):
    add_qr_text(report, "Empfangsschein", 5.0, 5.0, 52.0, "TitleE", 0.0)


def add_qr_data_e(report: Report):
    next_y = add_qr_text(report, "Konto / Zahlbar an", 5.0, 12.0, 52.0, "CaptionE", 9.0)
    next_y = add_qr_text(report, "CH00 1111 2222 3333 4444 8", 5.0, next_y, 52.0, "ValueE", 9.0)
    next_y = add_qr_text(report, "Adiuvaris", 5.0, next_y, 52.0, "ValueE", 9.0)
    next_y = add_qr_text(report, "At the lake 901a", 5.0, next_y, 52.0, "ValueE", 9.0)
    next_y = add_qr_text(report, "00100 Lakeside", 5.0, next_y, 52.0, "ValueE", 9.0)
    next_y = add_qr_text(report, "", 5.0, next_y, 52.0, "ValueE", 9.0)

    next_y = add_qr_text(report, "Zahlbar durch", 5.0, next_y, 52.0, "CaptionE", 9.0)
    next_y = add_qr_text(report, "Jane Doe", 5.0, next_y, 52.0, "ValueE", 9.0)
    next_y = add_qr_text(report, "Sample Street 11b", 5.0, next_y, 52.0, "ValueE", 9.0)
    add_qr_text(report, "009900 Somewhere", 5.0, next_y, 52.0, "ValueE", 9.0)


def add_qr_value_e(report: Report):
    next_y = add_qr_text(report, "Währung", 5.0, 68.0, 15.0, "CaptionE", 9.0)
    add_qr_text(report, "Betrag", 20.0, 68.0, 35.0, "CaptionE", 9.0)

    add_qr_text(report, "CHF", 5.0, next_y, 35.0, "ValueE", 11.0)
    add_qr_text(report, "275 000.00", 20.0, next_y, 35.0, "ValueE", 11.0)


def add_qre(report: Report):
    add_qr_text(report, "Annahmestelle", 5.0, 82.0, 52.0, "CaptionE", 8.0, TextAlign.RIGHT)


def add_qr_title_z(report: Report):
    add_qr_text(report, "Zahlteil", 67.0, 5.0, 51.0, "TitleZ", 0.0)


def add_qr_data_z(report: Report):
    next_y = add_qr_text(report, "Konto / Zahlbar an", 118.0, 5.0, 92.0, "CaptionZ", 11.0)
    next_y = add_qr_text(report, "CH00 1111 2222 3333 4444 8", 118.0, next_y, 92.0, "ValueZ", 11.0)
    next_y = add_qr_text(report, "Adiuvaris", 118.0, next_y, 92.0, "ValueZ", 11.0)
    next_y = add_qr_text(report, "At the lake 901a", 118.0, next_y, 92.0, "ValueZ", 11.0)
    next_y = add_qr_text(report, "00100 Lakeside", 118.0, next_y, 92.0, "ValueZ", 11.0)
    next_y = add_qr_text(report, "", 118.0, next_y, 92.0, "ValueZ", 11.0)

    next_y = add_qr_text(report, "Zusätzliche Informationen", 118.0, next_y, 92.0, "CaptionZ", 11.0)
    next_y = add_qr_text(report, "Apartment 45/275000/01.01.2024", 118.0, next_y, 92.0, "ValueZ", 11.0)
    next_y = add_qr_text(report, "", 118.0, next_y, 92.0, "ValueZ", 11.0)

    next_y = add_qr_text(report, "Zahlbar durch", 118.0, next_y, 92.0, "CaptionZ", 9.0)
    next_y = add_qr_text(report, "Jane Doe", 118.0, next_y, 92.0, "ValueZ", 9.0)
    next_y = add_qr_text(report, "Sample Street 11b", 118.0, next_y, 92.0, "ValueZ", 9.0)
    add_qr_text(report, "009900 Somewhere", 118.0, next_y, 92.0, "ValueZ", 9.0)


def add_qr_value_z(report: Report):
    next_y = add_qr_text(report, "Währung", 67.0, 68.0, 15.0, "CaptionZ", 11.0)
    add_qr_text(report, "Betrag", 82.0, 68.0, 35.0, "CaptionZ", 9.0)

    add_qr_text(report, "CHF", 67.0, next_y, 34.0, "ValueZ", 11.0)

    add_qr_text(report, "275 000.00", 82.0, next_y, 34.0, "ValueZ", 11.0)


def add_qr_lines(report: Report):
    qr_top_offset = 297.0 - 105.0
    add_qr_text(report, "Hier abtrennen", 0.0, -3.5, 210.0, "CaptionZ", 0.0, TextAlign.CENTER)

    f = PositionFrame(report.body, 0.0, qr_top_offset, True)

    hc = SerialFrame(f, Direction.HORIZONTAL)
    lf = LineFrame(hc, Direction.HORIZONTAL, 0.3, length=999.0)
    lf.use_full_width = True

    f = PositionFrame(report.body, 62.0, qr_top_offset, True)

    hc = SerialFrame(f, Direction.HORIZONTAL)
    lf = LineFrame(hc, Direction.VERTICAL)
    lf.use_full_height = True


def print_qr_slip(report: Report):

    BreakFrame(report.body)

    add_qr_code_z(report)
    add_qr_title_e(report)
    add_qr_data_e(report)
    add_qr_value_e(report)
    add_qre(report)
    add_qr_title_z(report)
    add_qr_data_z(report)
    add_qr_value_z(report)
    add_qr_lines(report)


def sample_30():
    """
    More complex example report
    """

    # Init a new Report
    report = Report()

    TextStyles[TextStyle.ITALIC].bold = True
    TextStyle("CaptionE", font_size=6.0, bold=True)
    TextStyle("ValueE", font_size=8.0)
    TextStyle("TitleE", font_size=11.0, bold=True)
    TextStyle("TitleZ", font_size=11.0, bold=True)
    TextStyle("CaptionZ", font_size=8.0, bold=True)
    TextStyle("ValueZ", font_size=10.0)

    add_header(report)
    add_footer(report)

    print_address(report)
    print_project_object(report)
    print_invoice_data(report)
    print_title(report)
    print_invoice_text(report)
    print_values(report)
    print_payable(report)
    print_text_end(report)
    print_greetings(report)
    print_qr_slip(report)

    # Create the PDF
    filename = tempfile.gettempdir() + "/output_30"
    report.output(filename, True)


if __name__ == '__main__':
    sample_30()
