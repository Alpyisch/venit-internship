import unittest
from os import path
from unittest.mock import patch, mock_open
from logparse import count_occurrences, find_first_or_last

class LogParseTest(unittest.TestCase):
    def setUp(self):
        self.log_file_path = path.join(path.dirname(path.abspath(__file__)), 'test.log')

    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_count_only_pattern(self, mock_file):
        count = count_occurrences(pattern="User", file_path=self.log_file_path)
        self.assertEqual(count, 0)

        count = count_occurrences(pattern="*User", file_path=self.log_file_path)
        self.assertEqual(count, 0)

        count = count_occurrences(pattern="User*", file_path=self.log_file_path)
        self.assertEqual(count, 1)

        count = count_occurrences(pattern="*User*", file_path=self.log_file_path)
        self.assertEqual(count, 1)
        
        count = count_occurrences(pattern="asdasdasd", file_path=self.log_file_path)
        self.assertEqual(count, 0)
        
        count = count_occurrences(pattern="*asdasdasd", file_path=self.log_file_path)
        self.assertEqual(count, 0)
        
        count = count_occurrences(pattern="asdasdasd*", file_path=self.log_file_path)
        self.assertEqual(count, 0)
        
        count = count_occurrences(pattern="*asdasdasd*", file_path=self.log_file_path)
        self.assertEqual(count, 0)
        
    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_count_only_severity(self, mock_file):
        count = count_occurrences(severity="INFO*", file_path=self.log_file_path)
        self.assertEqual(count, 2)

        count = count_occurrences(severity="ERROR*", file_path=self.log_file_path)
        self.assertEqual(count, 1)

        count = count_occurrences(severity="*ERROR*", file_path=self.log_file_path)
        self.assertEqual(count, 1)

        count = count_occurrences(severity="*ERROR", file_path=self.log_file_path)
        self.assertEqual(count, 1)

        count = count_occurrences(severity="DEBUG*", file_path=self.log_file_path)
        self.assertEqual(count, 0)

        count = count_occurrences(severity="DEBUG", file_path=self.log_file_path)
        self.assertEqual(count, 0)

        count = count_occurrences(severity="asdasdasd*", file_path=self.log_file_path)
        self.assertEqual(count, 0)
    
    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_count_both_pattern_and_severity(self, mock_file):
        count = count_occurrences(pattern="*System*", severity="ERROR*", file_path=self.log_file_path)
        self.assertEqual(count, 1)

        count = count_occurrences(pattern="*memory", severity="WARNING*", file_path=self.log_file_path)
        self.assertEqual(count, 1)

        count = count_occurrences(pattern="User*", severity="INFO*", file_path=self.log_file_path)
        self.assertEqual(count, 1)

        count = count_occurrences(pattern="User", severity="INFO*", file_path=self.log_file_path)
        self.assertEqual(count, 0)

        count = count_occurrences(pattern="User", file_path=self.log_file_path)
        self.assertEqual(count, 0)

    def test_count_with_real_file(self):
        result = count_occurrences(pattern="*System*", severity="ERROR*", file_path=self.log_file_path)
        self.assertEqual(result, 1)

        result = count_occurrences(pattern="*asdasda*", severity="ERROR*", file_path=self.log_file_path)
        self.assertEqual(result, 0)

        result = count_occurrences(pattern="*asdasda*", file_path=self.log_file_path)
        self.assertEqual(result, 0)

        result = count_occurrences(pattern="User*", severity="INFO", file_path=self.log_file_path)
        self.assertEqual(result, 9)

    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_first_only_pattern(self, mock_file):
        result = find_first_or_last(pattern="*System*", file_path=self.log_file_path, find_last=False)
        self.assertEqual(result, "2024-09-09 12:01:00 ERROR: System failure")

        result = find_first_or_last(pattern="ERROR*", file_path=self.log_file_path, find_last=False)
        self.assertEqual(result, None)

    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_first_only_severity(self, mock_file):
        result = find_first_or_last(severity="asdasda*", file_path=self.log_file_path, find_last=False)
        self.assertEqual(result, None)

        result = find_first_or_last(severity="INFO*", file_path=self.log_file_path, find_last=False)
        self.assertEqual(result, "2024-09-09 12:00:00 INFO: User logged in")
        
        result = find_first_or_last(severity="*INFO", file_path=self.log_file_path, find_last=False)
        self.assertEqual(result, "2024-09-09 12:00:00 INFO: User logged in")
        
        result = find_first_or_last(severity="INFO", file_path=self.log_file_path, find_last=False)
        self.assertEqual(result, "2024-09-09 12:00:00 INFO: User logged in")
        
        result = find_first_or_last(severity="*INFO*", file_path=self.log_file_path, find_last=False)
        self.assertEqual(result, "2024-09-09 12:00:00 INFO: User logged in")

    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_last_only_pattern(self, mock_file):
        result = find_first_or_last(pattern="*System*", file_path=self.log_file_path, find_last=True)
        self.assertEqual(result, "2024-09-09 12:03:00 INFO: System started")

        result = find_first_or_last(pattern="ERROR*", file_path=self.log_file_path, find_last=True)
        self.assertEqual(result, None)

    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_last_only_severity(self, mock_file):
        result = find_first_or_last(severity="asdasda*", file_path=self.log_file_path, find_last=True)
        self.assertEqual(result, None)

        result = find_first_or_last(severity="INFO*", file_path=self.log_file_path, find_last=True)
        self.assertEqual(result, "2024-09-09 12:03:00 INFO: System started")
        
        result = find_first_or_last(severity="*INFO", file_path=self.log_file_path, find_last=True)
        self.assertEqual(result, "2024-09-09 12:03:00 INFO: System started")
        
        result = find_first_or_last(severity="INFO", file_path=self.log_file_path, find_last=True)
        self.assertEqual(result, "2024-09-09 12:03:00 INFO: System started")
        
        result = find_first_or_last(severity="*INFO*", file_path=self.log_file_path, find_last=True)
        self.assertEqual(result, "2024-09-09 12:03:00 INFO: System started")

if __name__ == '__main__':
    unittest.main()