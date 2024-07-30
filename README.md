
## 'inspector.py' Guide
## 1. What is 'inspector.py?'
'inspector.py' is a Python script designed to analyze PCAP (Packet Capture) files. These files are commonly used to record network traffic. The script can filter packets based on IP addresses, calculate delays between packets in two different PCAP files, and provide statistical information about these delays.

## 2. How to Use It
To run the script, use the command line. Open a terminal in the directory where 'inspector.py' is located and execute the script using Python.

Command Line Usage: 
python 'inspector.py' [commands and arguments]

Arguments:
'file_paths' (Required): Paths to one or two PCAP files. Packets will be compared between these two files.
'--source' (Optional): Specifies the source IP address to filter packets.
'--destination' (Optional): Specifies the destination IP address to filter packets.
'--protocol' (Optional): Filters packets based on a specific protocol (e.g., TCP, UDP).

## 3. Available Arguments and Their Usage:
# a. Analyze a Single File:
You can analyze packets in a file on specific source or destination IP adress.

# Command:
python inspector.py file.pcap --source 192.168.1.1
Description: Analyzes packets in file.pcap with a source IP address of 192.168.1.1. Lists the destination IP addresses of these packets.

# Command:
python inspector.py file.pcap --destination 192.168.1.2
Description: Analyzes packets in file.pcap with a destination IP address of 192.168.1.2. Lists the source IP addresses of these packets.

# b. Compare Two Files:
You can compare two PCAP files and calculate the delays between packets with specified source and destination IP addresses.

python inspector.py file1.pcap file2.pcap --source 192.168.1.1 --destination 192.168.1.2

Description: Compares 'file1.pcap' and 'file2.pcap'. Finds packets in 'file1.pcap' with source IP '192.168.1.1' and matches them with packets in 'file2.pcap' having destination IP '192.168.1.2' Calculates the delays between these packets and provides statistical data.

## 4. Output Results
# a. Single File Analysis:

Source IP Analysis: Provides the total number of packets with the specified source IP and lists the destination IP addresses for these packets.

Destination IP Analysis: Provides the total number of packets with the specified destination IP and lists the source IP addresses for these packets.

# b.Comparison Between Two Files:
Matching Packets: Displays the number of matching packets and calculates the delay between each pair of packets.

Statistics: Shows the minimum, maximum, average, and standard deviation of the delay times.

Interval List: Lists the delays in descending order along with packet IDs and timestamps.

## 5. Example Outputs
Single File Analysis:

Source IP Analysis:
Total packets from source 192.168.1.1: 10
Destination addresses:
192.168.1.2
192.168.1.3

Destination IP Analysis:
Total packets to destination 192.168.1.2: 15
Source addresses:
192.168.1.1
192.168.1.4

Comparison Between Two Files:
Results for packets from file1.pcap to file2.pcap
Total matched packets: 8
Min. delay: 5.20 ms
Max. delay: 100.45 ms
Avg. delay: 23.67 ms
Std. dev.: 15.34 ms

All intervals in descending order:
Packet ID 12345: 100.45 ms - Start: 1688778240.123456, End: 1688778240.223456
Packet ID 12345: 80.30 ms - Start: 1688778250.123456, End: 1688778250.203456
...

## 6. Notes:
'file_paths' should be provided in order when comparing two files.
Use '--source' or '--destination' options for single file analysis.
'--protocol' option filters packets based on protocols (TCP, UDP, etc.).