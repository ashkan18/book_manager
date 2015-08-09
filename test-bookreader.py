from books import BookReader

__author__ = 'ashkan'

import unittest

class TestBookReader(unittest.TestCase):
    def setUp(self):
        self.book_reader = BookReader(file_name='pipe', order_by_year=False, reverse=True)

    def test_line_process_pipe(self):
        pipe_data = " F |L|T|D\n"
        parsed_data = self.book_reader._line_process(pipe_data)

        self.__test_parsed_data(parsed_data)

    def test_line_process_unknown_format(self):
        pipe_data = " F |L|T|D|D\n"

        with self.assertRaises(Exception):
            self.book_reader._line_process(pipe_data)

        pipe_data = " F |L|T"
        with self.assertRaises(Exception):
            self.book_reader._line_process(pipe_data)

    def test_line_process_slash(self):
        slash_data = "D/F/L/T"
        parsed_data = self.book_reader._line_process(slash_data)

        self.__test_parsed_data(parsed_data)

    def test_line_process_csv(self):
        csv_data = "T,L,F,D"
        parsed_data = self.book_reader._line_process(csv_data)

        self.__test_parsed_data(parsed_data)

    def __test_parsed_data(self, parsed_data):
        self.assertEqual(parsed_data.first_name, 'F')
        self.assertEqual(parsed_data.last_name, 'L')
        self.assertEqual(parsed_data.title, 'T')
        self.assertEqual(parsed_data.date, 'D')


    def test_get_delimiter(self):
        self.assertEqual('|', self.book_reader._get_delimiter('F|L'))

        self.book_reader.delimiter = None
        self.assertEqual('/', self.book_reader._get_delimiter('F/L'))

        self.book_reader.delimiter = None
        self.assertEqual(',', self.book_reader._get_delimiter('F,L'))

        self.book_reader.delimiter = None
        with self.assertRaises(Exception):
            self.book_reader._get_delimiter("F:L")


    def test_read_file(self):
        book_reader = BookReader(file_name='pipe')
        book_reader._read_file()
        sorted_list = book_reader._get_sorted_lines_list()

        self.assertEqual(len(sorted_list), 4)
        for index, last_name in enumerate(['Beck', 'Beck', 'Brooks', 'Fowler']):
            self.assertEqual(last_name, book_reader.data_hash[sorted_list[index]].last_name)

    def test_read_file_reverse(self):
        book_reader = BookReader(file_name='pipe', reverse=True)
        book_reader._read_file()
        sorted_list = book_reader._get_sorted_lines_list()

        self.assertEqual(len(sorted_list), 4)
        for index, last_name in enumerate(['Fowler', 'Brooks', 'Beck', 'Beck']):
            self.assertEqual(last_name, book_reader.data_hash[sorted_list[index]].last_name)

    def test_read_file_year(self):
        book_reader = BookReader(file_name='pipe', order_by_year=True)
        book_reader._read_file()
        sorted_list = book_reader._get_sorted_lines_list()

        self.assertEqual(len(sorted_list), 4)
        for index, last_name in enumerate(['Brooks', 'Fowler', 'Beck', 'Beck']):
            self.assertEqual(last_name, book_reader.data_hash[sorted_list[index]].last_name)

    def test_read_file_year_reverse(self):
        book_reader = BookReader(file_name='pipe', order_by_year=True, reverse=True)
        book_reader._read_file()
        sorted_list = book_reader._get_sorted_lines_list()

        self.assertEqual(len(sorted_list), 4)
        for index, last_name in enumerate(['Beck', 'Beck', 'Fowler', 'Brooks']):
            self.assertEqual(last_name, book_reader.data_hash[sorted_list[index]].last_name)



if __name__ == '__main__':
    unittest.main()