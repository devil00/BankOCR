import unittest
from bank_number_ocr import BankNumberOCR

class TestReadEntries(unittest.TestCase):
    def setUp(self):
        self.bno = BankNumberOCR()

    def test_read_zeroes(self):
        input = " _  _  _  _  _  _  _  _  _ "\
                "| || || || || || || || || |"\
                "|_||_||_||_||_||_||_||_||_|"

        account_number = self.bno.parse_account_number(input)
        self.assertEquals(account_number, (0,0,0,0,0,0,0,0,0))

    def test_read_ones(self):
        input = "                           "\
                "  |  |  |  |  |  |  |  |  |"\
                "  |  |  |  |  |  |  |  |  |"

        account_number = self.bno.parse_account_number(input)
        self.assertEquals(account_number, (1,1,1,1,1,1,1,1,1))

    def test_get_lines(self):
        input = "                           "\
                "  |  |  |  |  |  |  |  |  |"\
                "  |  |  |  |  |  |  |  |  |"

        lines = self.bno.get_lines(input)
        self.assertEquals(lines[0][0], ' ')
        self.assertEquals(lines[1][1], ' ')
        self.assertEquals(lines[2][2], '|')

    def test_get_cells(self):
        input = " _  _  _  _  _  _  _  _  _ "\
                "| || || || || || || || || |"\
                "|_||_||_||_||_||_||_||_||_|"

        cells = self.bno.get_cells(input)

        self.assertEquals(self.bno.format_cell(cells[0]), " _ \n| |\n|_|")

    def test_fetch_account_numbers_from_file(self):
        filename = 'entries.txt'
        account_numbers = self.bno.fetch_account_numbers_from_file(filename)
        self.assertEquals(account_numbers[10], (1,2,3,4,5,6,7,8,9))

    def test_account_status(self):
        filename = 'entries.txt'
        results = self.bno.get_result(filename, False)
        self.assertEquals(results[(0, 0, 0, 0, 0, 0, 0, 0, 0)], '')
        self.assertEquals(results[1, 1, 1, 1, 1, 1, 1, 1, 1], 'ERR')

    def test_account_validity(self):
        is_valid = self.bno.is_valid_account_number((3, 4, 5, 8, 8, 2, 8,
                                                     6, 5))
        self.assertEquals(is_valid, True)

if __name__ == '__main__':
    unittest.main()

