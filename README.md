
## 'inspector.py' and 'logparse.py' Guide
1. What are 'inspector.py' and 'logparse.py'?
'inspector.py' is a Python script designed to analyze PCAP (Packet Capture) files, commonly used to record network traffic. The script can filter packets based on IP addresses, calculate delays between packets in two different PCAP files, and provide statistical information about these delays.

'logparse.py' is a Python script designed to analyze log files by searching for patterns or severity levels. It can count occurrences of specific patterns, find the first or last log entry that matches given criteria, and filter logs based on severity levels (e.g., INFO, ERROR).

## 2. How to Use Them
Both scripts are run via the command line. Open a terminal in the directory where the scripts are located and execute them using Python.

Command Line Usage for 'inspector.py':
python inspector.py [commands and arguments]

Command Line Usage for 'logparse.py':
python logparse.py [command] [arguments]

## 3. Available Arguments and Their Usage:
A. 'inspector.py' Arguments:
file_paths (Required): Paths to one or two PCAP files.
--source (Optional): Specifies the source IP address to filter packets.
--destination (Optional): Specifies the destination IP address to filter packets.
--protocol (Optional): Filters packets based on a specific protocol (e.g., TCP, UDP).
Examples:

# 1.Analyze a Single File:
# Command:
python inspector.py file.pcap --source 192.168.1.1
Description: Analyzes packets in file.pcap with a source IP address of 192.168.1.1. Lists the destination IP addresses of these packets.

# Command:
python inspector.py file.pcap --destination 192.168.1.2
Description: Analyzes packets in file.pcap with a destination IP address of 192.168.1.2. Lists the source IP addresses of these packets.

# 2. Compare Two Files:
You can compare two PCAP files and calculate the delays between packets with specified source and destination IP addresses.

python inspector.py file1.pcap file2.pcap --source 192.168.1.1 --destination 192.168.1.2

Description: Compares 'file1.pcap' and 'file2.pcap'. Finds packets in 'file1.pcap' with source IP '192.168.1.1' and matches them with packets in 'file2.pcap' having destination IP '192.168.1.2' Calculates the delays between these packets and provides statistical data.

# B. 'logparse.py' Commands:
count: Counts occurrences of specific patterns or severities in the log file.
first: Finds the first occurrence of a log entry that matches the given pattern or severity.
last: Finds the last occurrence of a log entry that matches the given pattern or severity.
Examples:
# 1. Count Occurrences: 
# Commands: 
python logparse.py count --text User --severity INFO log_file.log
Description: Counts how many times "User" appears with severity "INFO" in log_file.log.

# 2. Find First or Last Entry:
# Commands: 
python logparse.py first --text "User" --severity ERROR log_file.log
Description: Finds the first log entry with "User" and severity "ERROR" in log_file.log.


## 4. Output Results:
# A. 'inspector.py' Results:
1.Single File Analysis:

Source IP Analysis: Provides the total number of packets with the specified source IP and lists the destination IPs.
Destination IP Analysis: Provides the total number of packets with the specified destination IP and lists the source IPs.
2.Comparison Between Two Files:

Matching Packets: Displays the number of matching packets and calculates delay statistics (min, max, avg, std. dev.).
Interval List: Lists delays in descending order with packet IDs and timestamps.
Example Output:

Total matched packets: 8
Min. delay: 5.20 ms
Max. delay: 100.45 ms
Avg. delay: 23.67 ms
Std. dev.: 15.34 ms

# B. 'logparse.py' Results:
1. Count:
Outputs the number of occurrences of the specified pattern or severity.
Example Output:

Matched logs with severity "INFO" and text "User": 3

2. First or Last :
Displays the first or last log entry that matches the specified pattern or severity.
Example Output:

First matched log: 2024-09-09 12:00:00 INFO: User logged in

## 5. Example Outputs
# A. 'inspector.py' Results:
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

# B.'logparse.py' Results:
Count Occurrences Example:

Matched logs with text "*User*": 15
Matched logs with severity "WARN": 4
Matched logs with severity "INFO" and text "User": 3


Find First Entry Example:

First matched log: 2024-09-09 12:00:00 INFO: User logged in


## 6. Notes:
A. For 'inspector.py':
When comparing two files, file_paths should be provided in order.
Use --source or --destination for single file analysis.
The --protocol option filters packets based on protocols (e.g., TCP, UDP).
B. For 'logparse.py':
Use --text for pattern matching with or without wildcards (*).
Use --severity to filter logs by severity level (INFO, WARNING, ERROR).