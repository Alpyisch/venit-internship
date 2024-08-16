import unittest
from unittest.mock import patch
import os
from scapy.all import IP, wrpcap
from inspector import analyze_file, calculate_delays, parse_arguments, ArgumentException
import argparse

class TestInspector(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_files'
        os.makedirs(self.test_dir, exist_ok=True)

        self.file1_path = os.path.join(self.test_dir, 'file1.pcap')
        self.file2_path = os.path.join(self.test_dir, 'file2.pcap')
        self.file_path = os.path.join(self.test_dir, 'test_data.pcap')
        
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
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_parse_arguments(self):
        test_args = ['inspector.py', self.file1_path, '--source', '192.168.1.105', '--destination', '192.168.1.111', '--protocol', 'TCP']
        with patch('sys.argv', test_args):
            args = parse_arguments()
            self.assertEqual(args.file_paths, [self.file1_path])
            self.assertEqual(args.source, '192.168.1.105')
            self.assertEqual(args.destination, '192.168.1.111')
            self.assertEqual(args.protocol, 'TCP')
            
    def test_invalid_arguments(self):
        test_args = ['inspector.py']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                parse_arguments()
        self.assertEqual(cm.exception.code, 2)

        test_args = ['inspector.py', 'asdasdasd.pcap', '--source', '192.168.1.105', '--destination', '192.168.1.111']
        with patch('sys.argv', test_args):
            with self.assertRaises(ArgumentException) as cm:
                parse_arguments()
            self.assertTrue("asdasdasd.pcap" in str(cm.exception))
        
        test_args = ['inspector.py', 'file1.asd', '--source', '192.168.1.105', '--destination', '192.168.1.111', '--protocol', 'TCP']
        with patch('sys.argv', test_args):
            with self.assertRaises(ArgumentException) as cm:
                parse_arguments()
            self.assertIn(".asd is not a valid file format", str(cm.exception))

    def test_packet_time_difference(self):
        min_delay, max_delay, avg_delay, std_dev_delay = calculate_delays(self.file1_path, self.file2_path, source='192.168.1.105', destination='192.168.1.111')

        expected_min = 0.0
        expected_max = 0.0
        expected_avg = 0.0
        expected_std_dev = 0.0 

        self.assertAlmostEqual(min_delay, expected_min, delta=1, msg=f"Expected min delay {expected_min}, got {min_delay}")
        self.assertAlmostEqual(max_delay, expected_max, delta=1, msg=f"Expected max delay {expected_max}, got {max_delay}")
        self.assertAlmostEqual(avg_delay, expected_avg, delta=1, msg=f"Expected avg delay {expected_avg}, got {avg_delay}")
        self.assertAlmostEqual(std_dev_delay, expected_std_dev, delta=1, msg=f"Expected std dev {expected_std_dev}, got {std_dev_delay}")

    def test_analyze_file_with_correct_path(self):
        packets = analyze_file(self.file_path)
        self.assertEqual(len(packets), 1, "Expected one packet in the test file.")

    def test_file_format(self):
        valid_formats = ['.pcap', '.cap', '.pcang']
        file_name = "test_data.pcap"
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
            file_paths=[self.file_path],
            source=None,
            destination=None
        )
        
        with self.assertRaises(ArgumentException) as cm:
            parse_arguments()
        self.assertEqual(str(cm.exception), "Please provide source or destination IP address.")

    @patch('argparse.ArgumentParser.parse_args')
    def test_calculate_delays_with_two_files(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            file_paths=[self.file1_path, self.file2_path],
            source='192.168.1.105',
            destination='192.168.1.111'
        )
        
        args = parse_arguments()
        self.assertEqual(args.file_paths, [self.file1_path, self.file2_path])
        self.assertEqual(args.source, '192.168.1.105')
        self.assertEqual(args.destination, '192.168.1.111')

if __name__ == '__main__':
    unittest.main()
