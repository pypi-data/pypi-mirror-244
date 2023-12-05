from pathlib import Path
import unittest
from ..src.workbook import Workbook, QUITTING, PATH_ERROR, WORKBOOK_ERROR

ANSI_COLOR_RED = "\x1b[31m"
ANSI_COLOR_RESET = "\x1b[0m"
ANSI_COLOR_RED = ""
ANSI_COLOR_RESET = ""


class TestWorkbookyOpen(unittest.TestCase):
    def test_open_valid(self):
        path = Path('tests', 'test_data', 'valid_workbook.xlsx')
        workbook = Workbook(path)
        self.assertEqual(len(workbook.worksheets), 1)

    def test_workbook_missing(self):
        path = Path('tests', 'test_data', 'missing_workbook.xlsx')
        err_msg = f'{QUITTING} {PATH_ERROR}'

        with self.assertRaises(SystemExit) as cm:
            Workbook(path)
        self.assertEqual(cm.exception.code, err_msg)

    def test_open_invalid(self):
        path = Path('tests', 'test_data', 'invalid_workbook.xlsx')
        err_msg = f'{QUITTING} {WORKBOOK_ERROR}'

        with self.assertRaises(SystemExit) as cm:
            Workbook(path)
        self.assertEqual(cm.exception.code, err_msg)


class TestWorkbookyRead(unittest.TestCase):
    def setUp(self):
        """ Executed before every test case """
        path = Path('tests', 'test_data', 'valid_workbook.xlsx')
        self.workbook = Workbook(path)
        print(self.workbook.worksheets)

    def test_rows_from_worksheet_use_first_row(self):
        rows = self.workbook.rows_from_worksheet('valid_sheet_name', False)
        self.assertEqual(len(rows), 14)

    def test_rows_from_worksheet_ignore_first_row(self):
        rows = self.workbook.rows_from_worksheet('valid_sheet_name')
        self.assertEqual(len(rows), 13)

    def test_row_value(self):
        rows = self.workbook.rows_from_worksheet('valid_sheet_name')
        self.assertEqual(rows[12][1], 12)
        self.assertEqual(len(rows[1]), 2)
