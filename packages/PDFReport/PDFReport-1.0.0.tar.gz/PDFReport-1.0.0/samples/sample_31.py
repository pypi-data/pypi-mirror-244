import tempfile
import sqlite3

from PDFReport import *


def add_sqlite_table(body: SerialFrame, db_file: str, fields: [str], widths: [float], tab: str, where: str):

    # Add a table to the body
    tf = TableFrame(body)

    tc = []

    # Add the columns to the table based on the fields list
    # and create the sql statement
    con = sqlite3.connect(db_file)
    sql = "SELECT "
    for idx, f in enumerate(fields):
        tc.append(TableColumn(tf, f, widths[idx]))
        sql = sql + f
        sql = sql + ", "

    sql = sql.rstrip(", ")
    sql = sql + " FROM " + tab + " WHERE " + where
    cur = con.cursor()

    # Execute the sql statement anf fill the table with the read data
    for row in cur.execute(sql):

        # Add a row to the table and fill the cells with data
        r = TableRow(tf)
        for idx, f in enumerate(fields):
            TableCell(r, tc[idx], str(row[idx]))

    con.close()

    # Add vertical distance of 10mm
    SerialFrame(body, Direction.VERTICAL, margin_bottom=10.0)


def create_db(db_file: str):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS frames")
    cur.execute("CREATE TABLE frames(number, frame_type, container, description)")

    data = [
        (1, "LineFrame", 0, "This frame type represents a line on the report."),
        (2, "SerialFrame", 1, "This is a container for a series of frames which will be printed one after the other."),
        (3, "TextFrame", 0, "A simple frame type to print text."),
    ]
    cur.executemany("INSERT INTO frames VALUES(?, ?, ?, ?)", data)
    con.commit()
    con.close()


def sample_31():
    """
    Report based on a sqlite database
    """

    # Create a database with some data
    db_file = str(tempfile.gettempdir()) + "/data31.db"
    create_db(db_file)

    # Init a new Report
    report = Report()

    # Add a table to the body with some data from sqlite database
    add_sqlite_table(report.body, db_file, ["number", "frame_type", "container", "description"], [20.0, 30.0, 20.0, 90.0], "frames", "number > 1")

    # Add a table to the body with some other data from sqlite database
    add_sqlite_table(report.body, db_file, ["number", "frame_type", "description"], [20.0, 30.0, 110.0], "frames", "number = 1")

    # Create the PDF
    filename = str(tempfile.gettempdir()) + "/output_31"
    report.output(filename, True)


if __name__ == '__main__':
    sample_31()
