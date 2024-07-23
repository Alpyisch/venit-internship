import argparse
from scapy.all import rdpcap
import numpy as np

def calculate_inter_packet_intervals(file_path, source=None, destination=None):
    packets = rdpcap(file_path)
    
    packet_times = []
    source_ips = []

    for packet in packets:
        if packet.haslayer('IP'):
            if source and packet['IP'].src != source:
                continue
            if destination and packet['IP'].dst != destination:
                continue
            packet_times.append(float(packet.time))
            source_ips.append(packet['IP'].src)

    if not packet_times:
        print("No packets match the specified criteria.")
        return

    intervals = []
    for i in range(1, len(packet_times)):
        interval = (packet_times[i] - packet_times[i - 1]) * 1000  
        intervals.append(interval)

    if not intervals:
        print("Not enough packets to calculate intervals.")
        return

    min_time = np.min(intervals)
    max_time = np.max(intervals)
    avg_time = np.mean(intervals)
    std_dev = np.std(intervals)

    min_time_source = source_ips[intervals.index(min(intervals))]
    max_time_source = source_ips[intervals.index(max(intervals))]

    print(f"Destination address: {destination}")
    print(f"Min. time: {min_time:.2f} ms (source {min_time_source})")
    print(f"Max. time: {max_time:.2f} ms (source {max_time_source})")
    print(f"Avg. time: {avg_time:.2f} ms")
    print(f"Std. dev.: {std_dev:.2f} ms")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate inter-packet intervals from a PCAP file.")
    parser.add_argument("file_path", help="Path to the PCAP file")
    parser.add_argument("--source", help="Source IP address to filter packets")
    parser.add_argument("--destination", help="Destination IP address to filter packets")

    args = parser.parse_args()

    calculate_inter_packet_intervals(args.file_path, args.source, args.destination)
