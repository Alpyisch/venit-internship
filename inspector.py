from scapy.all import rdpcap

def calculate_inter_packet_intervals(file_path):

    packets = rdpcap(file_path)
    
    packet_times = []

    for packet in packets:
        packet_times.append(float(packet.time))

    intervals = []
    for i in range(1, len(packet_times)):
        interval = (packet_times[i] - packet_times[i - 1]) * 1000  # milisaniyeye çevirilen yer #
        intervals.append(interval)

    for i, interval in enumerate(intervals):                # intervalların yazıldığı yer #
        print(f"Paket {i+1}-{i+2}: {interval:.2f} ms")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python inspector.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    calculate_inter_packet_intervals(file_path)
