import getopt
import sys
from book_model import BookModel

__author__ = 'ashkan'

class BookReader(object):

    VALID_SEPARATORS = ['/', '|', ',']

    def __init__(self, file_name, filter=None, year=False, reverse=False):
        super(BookReader, self).__init__()

        self.file_name = file_name
        self.filter_func = (lambda x: filter in x) if filter else None
        self.order_by_year = year
        self.reverse = reverse

        self.delimiter = None
        self.last_name_hash = {}
        self.year_hash = {}
        self.data_hash = {}

    def process_file(self):
        """
            Reads the file first, then sorts the results
            and prints them
        """
        self._read_file()

        sorted_line_list = self._get_sorted_lines_list()

        self._pprint_results(sorted_line_list)

    def _read_file(self):
        """
        This method goes through each line of input file
        for each line if we have filter func, it checks if it matches the filter
        it will parse the line and based on sort it will populate year or last_name hash
        which will later be used to sort
        """
        with open(self.file_name) as f:
            for index, line in enumerate(f):
                if not self.filter_func or self.filter_func(line):
                    book_model = self._line_process(line)
                    self.data_hash[index] = book_model
                    if self.order_by_year:
                        self.year_hash.setdefault(book_model.date, []).append(index)
                    else:
                        self.last_name_hash.setdefault(book_model.last_name, []).append(index)

    def _get_delimiter(self, line):
        """
        Given a line, if we haven't already found delimiter it will find delimiter
        """
        if not self.delimiter:
            delimiter = filter(lambda x: x in line, BookReader.VALID_SEPARATORS)
            if delimiter:
                self.delimiter = delimiter[0]
            else:
                raise Exception(message="Unknown delimiter {}".format(line))
        return self.delimiter

    def _line_process(self, line):
        """
        Given a line of data, it will parse the data and return it in
        First Name, Last Name, Book Title, Book year

        input line for different delimiters is in following format

        pipe: First name | Last name | Book Title | Book Publication Date
        slash: Book Publication Date/First name/Last name/Book Title
        csv: Book Title, Last Name, First name, Book Publication Date

        """
        data = line.split(self._get_delimiter(line))
        if len(data) != 4:
            raise Exception("Unknown format: {}".format(line))

        if self.delimiter == '|':
            order = [0, 1, 2, 3]
        elif self.delimiter == '/':
            order = [1, 2, 3, 0]
        elif self.delimiter == ',':
            order = [2, 1, 0, 3]
        else:
            raise Exception(message="Data process for {} delimiter is not defined.".format(self._get_delimiter(line)))

        return BookModel([data[index].strip() for index in order])

    def _get_sorted_lines_list(self):
        """
            based on sort flag,
            returns a list of of lines based after ordering by requested order
            if order by is year,
                it will sort year_hash keys and returns all the lines in that list
            else
                it will sort last_name_hash keys and returns all the lines in that list
            sorted list is in the format of [[0,2], [1], [4]] where each item is a list of lines
            it will iterate the response with list of lines from list of list of lines
        """
        if self.order_by_year:
            sorted_list_lines = [self.year_hash[x] for x in sorted(self.year_hash.keys(), reverse=self.reverse)]
        else:
            sorted_list_lines =  [self.last_name_hash[x] for x in sorted(self.last_name_hash.keys(), reverse=self.reverse)]

        return [line for line_list in sorted_list_lines for line in line_list]

    def _pprint_results(self, line_numbers):
        """
        Given a list of line it will print the data
        """
        for line in line_numbers:
            print u'{}'.format(self.data_hash[line])


def usage():
    print 'books.py [-h] [--filter FILTER] [--year] [--reverse]'

def main(argv):
    try:
        opts, args = getopt.gnu_getopt(argv[1:], "x", ['filter=', 'year', 'reverse'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    reverse = False
    order_by_year = False
    filter = None
    file_name = argv[0]

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '--reverse':
            reverse = True
        elif opt == '--year':
            order_by_year = True
        elif opt == '--filter':
            filter = arg

    book_reader = BookReader(file_name=file_name,
                             filter=filter,
                             year=order_by_year,
                             reverse=reverse)
    book_reader.process_file()

if __name__ == '__main__':
    main(sys.argv[1:])

