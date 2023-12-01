# PDFReport

*Python Report Library*

* **category**    Library
* **author**      Michael Hodel <info@adiuvaris.ch>
* **version**     1.0.0
* **copyright**   2023-2023 Michael Hodel - Adiuvaris
* **license**     http://www.gnu.org/copyleft/lesser.html GNU-LGPL v3 (see LICENSE.TXT)
* **link**        https://github.com/adiuvaris/PDFReport
* **source**      https://github.com/adiuvaris/PDFReport


## Description

Python library to generate dynamic PDF reports using the FPDF2 library to create the PDF documents. 
The library works with nested rectangle regions on the paper where the sizes can be defined in millimeters 
or in percent of the surrounding rectangle or the library calculates them by the content.

### Main Features:
* all standard page formats (from FPDF), custom page margins;
* different page formats in one report;
* management of text styles;
* images, 2D barcodes (e.g. QR);
* page header and footer management;
* automatic page break, line break and text alignments;
* automatic page numbering;
* support for tables with a lot of features (e.g. automatic repeat the table header row after page break)
* nested structure of rectangles to create the report structure


## Install

Via PyPi

``` bash
$ pip install PDFReport
```

## Samples

``` python
python -m PDFReport <sample number>
```
Sample number can be any number from 1 to 34, e.g.

``` python
python -m PDFReport 26
```

## Usage

See the documentation https://docs.adiuvaris.ch/index.html


## License

GNU LESSER GENERAL PUBLIC LICENSE. Please see [License File](LICENSE) for more information.

