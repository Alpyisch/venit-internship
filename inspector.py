import argparse
from scapy.all import rdpcap

def calculate_inter_packet_intervals(file_path, source=None, destination=None):
    packets = rdpcap(file_path)
    
    packet_times = []

    for packet in packets:
        if packet.haslayer('IP'):
            if source and packet['IP'].src != source:
                continue
            if destination and packet['IP'].dst != destination:
                continue
            packet_times.append(float(packet.time))

    if not packet_times:
        print("No packets match the specified criteria.")
        return

    intervals = []
    for i in range(1, len(packet_times)):
        interval = (packet_times[i] - packet_times[i - 1]) * 1000  
        intervals.append(interval)

    for i, interval in enumerate(intervals):
        print(f"Paket {i+1}-{i+2}: {interval:.2f} ms")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate inter-packet intervals from a PCAP file.")
    parser.add_argument("file_path", help="Path to the PCAP file")
    parser.add_argument("--source", help="Source IP address to filter packets")
    parser.add_argument("--destination", help="Destination IP address to filter packets")

    args = parser.parse_args()

    calculate_inter_packet_intervals(args.file_path, args.source, args.destination)
