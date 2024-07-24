import argparse
from scapy.all import rdpcap

def calculate_inter_packet_intervals(file_path, source=None, destination=None):
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
            packet_times.append(float(packet.time))
            source_ips.append(packet['IP'].src)
            destination_ips.append(packet['IP'].dst)

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

    unique_sources = set(source_ips)
    unique_destinations = set(destination_ips)
    
    print(f"Destination address: {destination}")
    print(f"Source address: {source}")
    print(f"Total packets: {len(packet_times)}")

    if destination:
        print("Sources:")
        for src in unique_sources:
            print(src)
    elif source:
        print("Destinations:")
        for dst in unique_destinations:
            print(dst)
    else:
        print("Sources:")
        for src in unique_sources:
            print(src)
        print("Destinations:")
        for dst in unique_destinations:
            print(dst)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate inter-packet intervals from a PCAP file.")
    parser.add_argument("file_path", help="Path to the PCAP file")
    parser.add_argument("--source", help="Source IP address to filter packets")
    parser.add_argument("--destination", help="Destination IP address to filter packets")

    args = parser.parse_args()

    calculate_inter_packet_intervals(args.file_path, args.source, args.destination)
