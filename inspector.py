import argparse
from scapy.all import rdpcap
import numpy as np

def calculate_inter_packet_intervals(file_path, source=None, destination=None, protocol=None):
    packets = rdpcap(file_path)

    packet_times = []
    source_ips = []
    destination_ips = []

    for packet in packets:
        if packet.haslayer('IP'):
            if source and packet['IP'].src != source:
                continue
            if destination and packet['IP'].dst != destination:
                continue
            if protocol and not packet.haslayer(protocol):
                continue
            packet_times.append(float(packet.time))
            source_ips.append(packet['IP'].src)
            destination_ips.append(packet['IP'].dst)

    if not packet_times:
        print(f"No packets match the specified criteria in {file_path}.")
        return

    intervals = []
    for i in range(1, len(packet_times)):
        interval = (packet_times[i] - packet_times[i - 1]) * 1000  
        intervals.append(interval)

    if not intervals:
        print(f"Not enough packets to calculate intervals in {file_path}.")
        return

    unique_sources = set(source_ips)
    unique_destinations = set(destination_ips)
    min_time = np.min(intervals)
    max_time = np.max(intervals)
    avg_time = np.mean(intervals)
    std_dev = np.std(intervals)

    min_time_source = source_ips[intervals.index(min_time)]
    max_time_source = source_ips[intervals.index(max_time)]
    
    print(f"\nResults for file: {file_path}")
    if source:
        print(f"Source address: {source}")
    if destination:
        print(f"Destination address: {destination}")
    print(f"Total packets: {len(packet_times)}")
    print(f"Min. time: {min_time:.2f} ms (source {min_time_source})")
    print(f"Max. time: {max_time:.2f} ms (source {max_time_source})")
    print(f"Avg. time: {avg_time:.2f} ms")
    print(f"Std. dev.: {std_dev:.2f} ms")

    if destination and not source:
        print("Sources:")
        for src in unique_sources:
            print(src)
    elif source and not destination:
        print("Destinations:")
        for dst in unique_destinations:
            print(dst)
    elif not source and not destination:
        print("Sources:")
        for src in unique_sources:
            print(src)
        print("Destinations:")
        for dst in unique_destinations:
            print(dst)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate inter-packet intervals from one or two PCAP files.")
    parser.add_argument("file_paths", nargs='*', help="Path to the PCAP file(s)")
    parser.add_argument("--source", help="Source IP address to filter packets")
    parser.add_argument("--destination", help="Destination IP address to filter packets")
    parser.add_argument("--protocol", help="Protocol to filter packets (e.g., TCP, UDP)")

    args = parser.parse_args()

    if len(args.file_paths) == 0:
        print("No PCAP files provided.")
    elif len(args.file_paths) == 1:
        print(f"Analyzing single file: {args.file_paths[0]}")
        calculate_inter_packet_intervals(args.file_paths[0], args.source, args.destination, args.protocol)
    elif len(args.file_paths) == 2:
        print(f"Analyzing file1: {args.file_paths[0]}")
        calculate_inter_packet_intervals(args.file_paths[0], args.source, args.destination, args.protocol)
        print(f"Analyzing file2: {args.file_paths[1]}")
        calculate_inter_packet_intervals(args.file_paths[1], args.source, args.destination, args.protocol)
    else:
        print("Please provide one or two PCAP files.")
