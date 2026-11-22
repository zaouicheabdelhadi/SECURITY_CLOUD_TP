#!/usr/bin/env python3
"""
Minimal always-on TCP 'radio stream' service.

Stands in for the video-streaming server of SEED Labs TCP/IP Attack Lab
Task 3, without depending on any real external website. It just keeps a
long-lived TCP connection open and continuously pushes data to the client,
exactly the property that matters for a TCP RST attack: there is an
established connection for the attacker to disrupt.
"""
import socket
import threading
import time
import sys

PORT = 9091
HOST = "0.0.0.0"


def handle(conn, addr):
    print(f"[radio] client connected from {addr}", file=sys.stderr, flush=True)
    try:
        i = 0
        while True:
            i += 1
            line = f"NOW PLAYING: Seed FM track #{i} @ {time.strftime('%H:%M:%S')}\n"
            conn.sendall(line.encode())
            time.sleep(1)
    except (BrokenPipeError, ConnectionResetError, OSError):
        print(f"[radio] client {addr} disconnected (connection torn down)", file=sys.stderr, flush=True)
    finally:
        conn.close()


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(5)
    print(f"[radio] listening on {HOST}:{PORT}", file=sys.stderr, flush=True)
    while True:
        conn, addr = srv.accept()
        t = threading.Thread(target=handle, args=(conn, addr), daemon=True)
        t.start()


if __name__ == "__main__":
    main()
