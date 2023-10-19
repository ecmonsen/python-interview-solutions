import unittest
from practice import practice1


class PracticeTests(unittest.TestCase):
    def test_format_number_success(self):
        s = practice1.format_number(1000000)
        self.assertEqual("1,000,000", s)

    def test_format_number_nosep_1digit(self):
        s = practice1.format_number(1)
        self.assertEqual("1", s)

    def test_format_number_nosep_2digit(self):
        s = practice1.format_number(46)
        self.assertEqual("46", s)

    def test_format_number_nosep_3digit(self):
        s = practice1.format_number(426)
        self.assertEqual("426", s)

    def test_sum_to_n_only_n(self):
        result = practice1.sum_to_n([8], 8)
        self.assertEqual([[8]], list(result))

    def test_sum_to_n_double(self):
        result = practice1.sum_to_n([4,2], 8)
        self.assertEqual([[2,2,2,2], [2,2,4], [4,4]], list(result))

    def test_sum_to_n_include_n(self):
        result = practice1.sum_to_n([3,4,2,9], 9)
        self.assertEqual([[2, 2, 2, 3], [2, 3, 4], [3, 3, 3],[9]], list(result))