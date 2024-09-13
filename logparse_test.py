import unittest
import os
from unittest.mock import patch, mock_open
from logparse import count_occurrences 

class LogParseTest(unittest.TestCase):
    def setUp(self):
        self.log_file_path = 'test_Alpi.log'
        with open(self.log_file_path, 'w') as f:
            f.write("""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
        
    def tearDown(self):
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_only_pattern(self, mock_file):
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
    def test_only_severity(self, mock_file):
        count = count_occurrences(severity="INFO*", file_path=self.log_file_path)
        self.assertEqual(count, 2)

        count = count_occurrences(severity="ERROR*", file_path=self.log_file_path)
        self.assertEqual(count, 1)

        count = count_occurrences(severity="DEBUG*", file_path=self.log_file_path)
        self.assertEqual(count, 0)
    
    @patch('builtins.open', new_callable=mock_open, read_data="""2024-09-09 12:00:00 INFO: User logged in
2024-09-09 12:01:00 ERROR: System failure
2024-09-09 12:02:00 WARNING: Low memory
2024-09-09 12:03:00 INFO: System started""")
    def test_both_pattern_and_severity(self, mock_file):
        count = count_occurrences(pattern="*System*", severity="ERROR*", file_path=self.log_file_path)
        self.assertEqual(count, 1)

        count = count_occurrences(pattern="*memory", severity="WARNING*", file_path=self.log_file_path)
        self.assertEqual(count, 1)

        count = count_occurrences(pattern="User*", severity="INFO*", file_path=self.log_file_path)
        self.assertEqual(count, 1)

    def test_real_file(self):
        try:
            with open(self.log_file_path, 'r') as f:
                log_data = f.read()

            pattern = "*System*"
            severity = "ERROR*"

            result = count_occurrences(pattern=pattern, severity=severity, file_path=self.log_file_path)

            expected_result = 1  
            self.assertEqual(result, expected_result)
        except FileNotFoundError:
            self.fail(f"file can't find: {self.log_file_path}")

if __name__ == '__main__':
    unittest.main()
