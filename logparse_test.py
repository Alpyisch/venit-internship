import unittest
from unittest.mock import patch, mock_open
from logparse import count_occurrences 

class LogParseTest(unittest.TestCase):
    def setUp(self):
        self.log_file_path = r'C:\Users\alper\OneDrive\Masaüstü\Alpi.log'

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n")
    def test_count_text_only(self, mock_file):
        pattern = "User*"
        count = count_occurrences(pattern=pattern, file_path=self.log_file_path)
        self.assertEqual(count, 1)

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n2024-09-09 12:03:00 INFO: User logged out\n")
    def test_count_severity_only(self, mock_file):
        severity = "*INFO*"
        count = count_occurrences(severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 2)

    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    
    def test_count_combined(self, mock_file):
        pattern = "*User*"
        severity = "*INFO*"
        count = count_occurrences(pattern=pattern, severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 1)


    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n")
    def test_count_text_with_wildcard(self, mock_file):
        pattern = "*User*"
        count = count_occurrences(pattern=pattern, file_path=self.log_file_path)
        self.assertEqual(count, 1)

    @patch('builtins.open', new_callable=mock_open, read_data="2024-09-09 12:00:00 INFO: User logged in\n2024-09-09 12:03:00 INFO: User logged out\n")
    def test_count_severity_with_wildcard(self, mock_file):
        severity = "*INFO*"
        count = count_occurrences(severity=severity, file_path=self.log_file_path)
        self.assertEqual(count, 2)
        
def check_pattern_match(pattern, line):
    if not pattern:
        return True
    
    if pattern.startswith('*') and pattern.endswith('*'):
        pattern = pattern[1:-1]  
        return pattern in line

    if pattern.startswith('*'):
        pattern = pattern[1:]  
        return line.endswith(pattern)

    if pattern.endswith('*'):
        pattern = pattern[:-1]  
        return line.startswith(pattern)

    return pattern in line

if __name__ == '__main__':
    unittest.main()
