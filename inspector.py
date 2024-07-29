import argparse
from scapy.all import rdpcap
import numpy as np

def analyze_file(file_path, source=None, destination=None, protocol=None):
    try:
        packets = rdpcap(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

    packet_info = []
    for packet in packets:
        if packet.haslayer('IP'):
            if source and packet['IP'].src != source:
                continue
            if destination and packet['IP'].dst != destination:
                continue
            if protocol and not packet.haslayer(protocol):
                continue
            packet_info.append(packet)

    return packet_info

def calculate_delays(file1_path, file2_path, source, destination, protocol=None):
    packets1 = analyze_file(file1_path, source, destination, protocol)
    packets2 = analyze_file(file2_path, source, destination, protocol)

    if not packets1 or not packets2:
        print("No matching packets found in the specified criteria.")
        return

    packet_times1 = {float(packet.time): packet for packet in packets1}
    packet_times2 = {float(packet.time): packet for packet in packets2}

    intervals = []
    for time1 in sorted(packet_times1.keys()):
        matching_times = [time2 for time2 in sorted(packet_times2.keys()) if time2 > time1]
        if matching_times:
            time2 = min(matching_times)
            interval = (time2 - time1) * 1000  
            intervals.append(interval)

    if not intervals:
        print("Not enough packets to calculate intervals.")
        return

    intervals.sort(reverse=True)  

    min_time = np.min(intervals)
    max_time = np.max(intervals)
    avg_time = np.mean(intervals)
    std_dev = np.std(intervals)

    print(f"\nResults for packets from {file1_path} to {file2_path}")
    print(f"Total matched packets: {len(intervals)}")
    print(f"Min. delay: {min_time:.2f} ms")
    print(f"Max. delay: {max_time:.2f} ms")
    print(f"Avg. delay: {avg_time:.2f} ms")
    print(f"Std. dev.: {std_dev:.2f} ms")
    
    print("\nAll intervals in desc order:")
    for i, interval in enumerate(intervals, 1):
        print(f"Packet {i}: {interval:.2f} ms")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze PCAP files and calculate packet delays.")
    parser.add_argument("file_paths", nargs='+', help="Path to the PCAP file(s)")
    parser.add_argument("--source", help="Source IP address to filter packets")
    parser.add_argument("--destination", help="Destination IP address to filter packets")
    parser.add_argument("--protocol", help="Protocol to filter packets (e.g., TCP, UDP)")

    args = parser.parse_args()

    if not args.source and not args.destination:
        print("Please provide source or destination IP address.")
    elif len(args.file_paths) == 1:
        file_path = args.file_paths[0]
        if args.source:
            packets = analyze_file(file_path, source=args.source, protocol=args.protocol)
            destinations = {packet['IP'].dst for packet in packets}
            print(f"Total packets from source {args.source}: {len(packets)}")
            print("Destination addresses:")
            for dst in destinations:
                print(dst)
        elif args.destination:
            packets = analyze_file(file_path, destination=args.destination, protocol=args.protocol)
            sources = {packet['IP'].src for packet in packets}
            print(f"Total packets to destination {args.destination}: {len(packets)}")
            print("Source addresses:")
            for src in sources:
                print(src)
    elif len(args.file_paths) == 2 and args.source and args.destination:
        file1_path = args.file_paths[0]
        file2_path = args.file_paths[1]
        calculate_delays(file1_path, file2_path, args.source, args.destination, args.protocol)
    else:
        print("Please provide one or two PCAP files along with the necessary parameters.")