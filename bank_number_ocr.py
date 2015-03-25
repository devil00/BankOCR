#    _  _     _  _  _  _  _  _
#  | _| _||_||_ |_   ||_||_|| |
#  ||_  _|  | _||_|  ||_| _||_| 
#

ILLEGIBLE_CHAR = "?"

class BankNumberOCR(object):
    def __init__(self):
        self.DIGITS_PER_LINE = 9 
        self.DIGIT_WIDTH = 3
        self.CELL_VALUES = {
            ' _ | ||_|': 0,
            '     |  |': 1,
            ' _  _||_ ': 2,
            ' _  _| _|': 3,
            '   |_|  |': 4,
            ' _ |_  _|': 5,
            ' _ |_ |_|': 6,
            ' _   |  |': 7,
            ' _ |_||_|': 8,
            ' _ |_| _|': 9
        }

    def parse_account_number(self, input):
        """
        Return the identified account number as a tuple.
        :param input: string representation of digit upto 3 line each having 
                      27 characters since last line is always blank.
        :type input: str
        """
        # input has 9 3x3 "cells".
        # break it up into individual cells.

        cells = self.get_cells(input)
        cell_values = []
        for cell in cells:
            cell_values.append(self.get_cell_value(cell))

        return tuple(cell_values)

    def get_cells(self, input):
        cells = []

        # copy into lines
        lines = self.get_lines(input)

        for offset in range(0, 26, 3):
            # offset, 0 will be top left of cell
            # offset + 2, 2 will be bottom right
            cell = lines[0][offset: offset+3]
            cell += lines[1][offset: offset+3]
            cell += lines[2][offset: offset+3]

            cells.append(cell)

        return cells

    def get_lines(self, input):
        # Total lines are 4 to represent a digital digit. 
        # Out of them last line is blank.
        lines = ["", "", ""]
        offset = 0

        for char in input:
            lines[offset] += char
            # Each line is 27 charactes long.
            if len(lines[offset]) == 27:
                offset += 1

        return lines

    def format_cell(self, cell):
        return "%s\n%s\n%s" % (cell[0:3], cell[3:6], cell[6:9])

    def get_cell_value(self, cell):
        return self.CELL_VALUES.get(cell, -1)

    def fetch_account_numbers_from_file(self, filename):
        """
        User Story: 1
        Returns all account numbers found in <filename>, as a list of tuples.
        :param filename: Filename which stores all the accoun numbers 
                         represented by either underscore or pipe.
        :type filename: str
        """

        account_numbers = []

        linecount = 0
        numberlines = ''
        with open(filename, 'r') as f:
            for line in f:
                linecount += 1

                if (linecount % 4) == 0:
                    account_numbers.append(self.parse_account_number(
                        numberlines))
                    numberlines = ''
                else:
                    # make sure to trim trailing newline
                    numberlines += line.rstrip('\n')

        return account_numbers

    def is_valid_account_number(self, account_number):
        """
        User Story: 2
        Calculate the checksum of an account number and if it is found to be a 
        valid checksum then return true else false since valid checksum has 
        valid account number.
        :param account_number: tuple containing digits of an account number.
        :type account_number: tuple
        :returns: bool
        """
        return sum([
            (i+1) * digit for i, digit in enumerate(
                reversed(account_number))]) % 11 == 0

    def get_result(self, input_filename, create=True):
        """
        User Story: 3
        Obtain the results for the account numbers showing the status of all 
        the account number extracted from input_file. If create flag is True
        then store result status in a file else return.
        :param input_filename: input filename where account numbers are saved.
        :type input_filename: str
        :param create: If true store status of accounts in a file else return.
                        Optional default to True.
        """
        accounts_status = {}
        # Get all the extracted account numbers.
        account_numbers = self.fetch_account_numbers_from_file(input_filename)
        for acc_no in account_numbers:
            if all([digit >= 0 for digit in acc_no]):
                if not self.is_valid_account_number(acc_no):
                    accounts_status[acc_no] = 'ERR'
                else:
                    # If checksum is valid then this is an valid account 
                    # number.
                    accounts_status[acc_no] = ''
            else:
                acc_no = tuple([
                    digit if digit >= 0 
                    else ILLEGIBLE_CHAR for digit in acc_no])
                accounts_status[acc_no] = 'ILL'

        if create is True:
            with open('accounts_status.txt', "w") as fobj:
                for acc, status in accounts_status.items():
                    fobj.write("{} {}\n".format(acc, status))
        else:
            return accounts_status


if __name__ == "__main__":
    bank_number_ocr = BankNumberOCR()
    acc_nos = bank_number_ocr.fetch_account_numbers_from_file("entries.txt")
    print "Extracted account numbers."
    print acc_nos
    print "Account number validity status"
    print [bank_number_ocr.is_valid_account_number(acc) for acc in acc_nos]
    print "Result summary of account numbers stored in {}".format(
        "account_status.txt")
    bank_number_ocr.get_result("entries.txt")
