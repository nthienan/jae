import unittest
from src import utility


class UtilityTest(unittest.TestCase):

    def test_str_to_megabytes_bytes(self):
        actual_value = utility.str_to_megabytes("103.1 bytes")
        self.assertEqual(actual_value, 103.1/1000000)

    def test_str_to_megabytes_kb(self):
        actual_value = utility.str_to_megabytes("10.12 KB")
        self.assertEqual(actual_value, 10.12/1000)

    def test_str_to_megabytes_mb(self):
        actual_value = utility.str_to_megabytes("5.5 MB")
        self.assertEqual(actual_value, 5.5)

    def test_str_to_megabytes_gb(self):
        actual_value = utility.str_to_megabytes("1.212 GB")
        self.assertEqual(actual_value, 1.212 * 1000)

    def test_str_to_megabytes_tb(self):
        actual_value = utility.str_to_megabytes("1.52 TB")
        self.assertEqual(actual_value, 1.52 * 1000000)

    @unittest.skip("demonstare skipped test case")
    def test_str_to_megabytes_failed_case(self):
        actual_value = utility.str_to_megabytes("1.52 TB")
        self.assertEqual(actual_value, 1.521 * 1000000)

    @unittest.skip("demonstare skipped test case")
    def test_str_to_megabytes_skipped_case(self):
        actual_value = utility.str_to_megabytes("1.52 TB")
        self.assertEqual(actual_value, 1.52 * 1000000)
