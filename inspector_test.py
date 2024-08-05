import unittest
from unittest.mock import patch
import os
from scapy.all import IP, wrpcap
from inspector import analyze_file, calculate_delays, parse_arguments, ArgumentException
import argparse

class TestInspector(unittest.TestCase):

    def setUp(self):
        self.file1_path = 'file1.pcap'
        self.file2_path = 'file2.pcap'
        self.file_path = 'test_data.pcap'
        
        packets = [
            IP(src="192.168.1.105", dst="192.168.1.111")/b"data"
        ]
        wrpcap(self.file_path, packets)
        wrpcap(self.file1_path, packets)
        wrpcap(self.file2_path, packets)

    def tearDown(self):
        for path in [self.file1_path, self.file2_path, self.file_path]:
            if os.path.exists(path):
                os.remove(path)

    def test_parse_arguments(self):
        test_args = ['inspector.py', 'file1.pcap', '--source', '192.168.1.105', '--destination', '192.168.1.111', '--protocol', 'TCP']
        with patch('sys.argv', test_args):
            args = parse_arguments()
            self.assertEqual(args.file_paths, ['file1.pcap'])
            self.assertEqual(args.source, '192.168.1.105')
            self.assertEqual(args.destination, '192.168.1.111')
            self.assertEqual(args.protocol, 'TCP')

    def test_file_exists(self):
        required_files = [self.file1_path, self.file2_path]
        for file in required_files:
            self.assertTrue(os.path.exists(file), f"File does not exist: {file}")

    def test_analyze_file_with_correct_path(self):
        packets = analyze_file(self.file_path)
        self.assertEqual(len(packets), 1, "Expected one packet in the test file.")

    def test_file_format(self):
        valid_formats = ['.pcap', '.cap', '.pcang']
        file_name = "test_file.pcap"
        self.assertTrue(any(file_name.endswith(fmt) for fmt in valid_formats), 
                        f"File format should be one of {valid_formats}")

    def test_analyze_file_data(self):
        packets = analyze_file(self.file_path, source="192.168.1.105", destination="192.168.1.111")
        self.assertEqual(len(packets), 1, "Expected to find one packet.")
        self.assertEqual(packets[0]['IP'].src, "192.168.1.105")
        self.assertEqual(packets[0]['IP'].dst, "192.168.1.111")

    @patch('argparse.ArgumentParser.parse_args')
    def test_calculate_delays_with_one_file(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            file_paths=['file.pcap'],
            source=None,
            destination=None
        )
        
        with self.assertRaises(ArgumentException) as cm:
            parse_arguments()
        self.assertEqual(str(cm.exception), "Please provide source or destination IP address.")

    @patch('argparse.ArgumentParser.parse_args')
    def test_calculate_delays_with_two_files(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            file_paths=['file1.pcap', 'file2.pcap'],
            source='192.168.1.105',
            destination='192.168.1.111'
        )
        
        args = parse_arguments()
        self.assertEqual(args.file_paths, ['file1.pcap', 'file2.pcap'])
        self.assertEqual(args.source, '192.168.1.105')
        self.assertEqual(args.destination, '192.168.1.111')

if __name__ == '__main__':
    unittest.main()
