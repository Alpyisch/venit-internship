import unittest
from unittest.mock import patch, mock_open
from logparse import count_occurrences 

class LogParseTest(unittest.TestCase):
    def setUp(self):
        self.log_file_path = r'C:\Users\alper\OneDrive\Masaüstü\Alpi.log'

    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_count_user_info_with_wildcards(self, mock_file):
        pattern = "*User*"
        severity = "*INFO*"
        count = count_occurrences(pattern=pattern, severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 1)
    
    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_count_user_info_no_end_wildcard(self, mock_file):
        pattern = "User*"
        severity = "INFO*"
        count = count_occurrences(pattern=pattern, severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 1)

    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_count_user_info_no_severity_wildcard(self, mock_file):
        pattern = "*User"
        severity = "INFO"
        count = count_occurrences(pattern=pattern, severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 0)

    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_count_user_exact_match(self, mock_file):
        pattern = "User"
        severity = "INFO"
        count = count_occurrences(pattern=pattern, severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 0)
    

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n")
    def test_count_user_exact_pattern_only(self, mock_file):
        pattern = "User"
        count = count_occurrences(pattern=pattern, file_path=self.log_file_path)
        self.assertEqual(count, 0)

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n")
    def test_count_user_pattern_wildcard(self, mock_file):
        pattern = "*User*"
        count = count_occurrences(pattern=pattern, file_path=self.log_file_path)
        self.assertEqual(count, 1)

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n")
    def test_count_user_no_wildcard(self, mock_file):
        pattern = "*User"
        count = count_occurrences(pattern=pattern, file_path=self.log_file_path)
        self.assertEqual(count, 0)

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n")
    def test_count_user_starting_wildcard(self, mock_file):
        pattern = "User*"
        count = count_occurrences(pattern=pattern, file_path=self.log_file_path)
        self.assertEqual(count, 1)


    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n2024-09-09 12:03:00 INFO: User logged out\n")
    def test_count_severity_info_only(self, mock_file):
        severity = "INFO"
        count = count_occurrences(severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 2)

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n2024-09-09 12:03:00 INFO: User logged out\n")
    def test_count_severity_info_wildcard(self, mock_file):
        severity = "*INFO*"
        count = count_occurrences(severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 2)

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n2024-09-09 12:03:00 INFO: User logged out\n")
    def test_count_severity_starting_info_wildcard(self, mock_file):
        severity = "INFO*"
        count = count_occurrences(severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 2)

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n2024-09-09 12:03:00 INFO: User logged out\n")
    def test_count_severity_ending_info_wildcard(self, mock_file):
        severity = "*INFO"
        count = count_occurrences(severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 2)


    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:02:00 WARNING: Low memory\n")
    def test_count_pattern_not_found(self, mock_file):
        pattern = "asd"
        count = count_occurrences(pattern=pattern, file_path=self.log_file_path)
        self.assertEqual(count, 0)

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n")
    def test_count_pattern_not_found_with_wildcard(self, mock_file):
        pattern = "asd*"
        count = count_occurrences(pattern=pattern, file_path=self.log_file_path)
        self.assertEqual(count, 0)
    
    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:03:00 INFO: System started\n")
    def test_count_pattern_no_match(self, mock_file):
        pattern = "*asdasd*"
        count = count_occurrences(pattern=pattern, file_path=self.log_file_path)
        self.assertEqual(count, 0)
        
if __name__ == '__main__':
    unittest.main()
