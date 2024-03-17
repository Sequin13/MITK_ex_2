import unittest
from main import hash_with_algorithm, file_hash_comparison, measure_hash_time
from unittest.mock import patch


class TestHashFunctions(unittest.TestCase):

    def test_hash_with_algorithm_string(self):
        data = "Hello, world!"
        expected_hash = "943a702d06f34599aee1f8da8ef9f7296031d699"
        self.assertEqual(hash_with_algorithm("sha1", data=data), expected_hash)

    def test_hash_with_algorithm_file(self):
        file_path = "test_file.txt"
        expected_hash = "da39a3ee5e6b4b0d3255bfef95601890afd80709"
        self.assertEqual(hash_with_algorithm("sha1", file_path=file_path), expected_hash)

    def test_file_hash_comparison(self):
        hash_result = "71be19d9245f2f10c32ba9b6165be08be4b418ca"
        known_hash = "71be19d9245f2f10c32ba9b6165be08be4b418ca"
        self.assertTrue(file_hash_comparison(hash_result, known_hash))

    @patch('main.timeit.timeit')
    def test_measure_hash_time(self, mock_timeit):
        mock_timeit.return_value = 1.0
        expected_results = {100: 1.0, 1000: 1.0, 2000: 1.0, 3000: 1.0, 4000: 1.0, 5000: 1.0,
                            6000: 1.0, 7000: 1.0, 8000: 1.0, 9000: 1.0, 10000: 1.0}
        self.assertEqual(measure_hash_time([100, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]),
                         expected_results)

if __name__ == '__main__':
    unittest.main()
