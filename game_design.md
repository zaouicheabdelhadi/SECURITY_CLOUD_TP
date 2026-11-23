# TCP/IP Attack Lab

Training based on the **SEED Labs TCP/IP Attack Lab** (Wenliang Du, Syracuse University), adapted for the CyberRangeCZ Platform with a dedicated topology (attacker/server/client all on one LAN, as the original lab requires) and values changed from the PDF handout so students cannot copy/paste answers.

## Disclaimer

This game is for educational purposes only, performed inside an isolated, authorized sandbox. Unauthorized use of the tools and techniques covered here against systems you do not own or have explicit permission to test is illegal. The story is fictitious.

## Scoring

Total: **20 points**, spread across 9 training levels. Each hint opened costs between **0.5 and 2 points**, deducted from that level's own score.

| # | Level | Max score |
|---|-------|-----------|
| 2 | Mapping the LAN | 2 |
| 3 | Diagnostic access & reading the SYN backlog | 1.5 |
| 4 | SYN Flooding Attack | 3 |
| 5 | Turning on SYN cookies | 1.5 |
| 6 | TCP RST Attack - telnet | 2.5 |
| 7 | TCP RST Attack - SSH | 2 |
| 8 | TCP RST Attack - radio stream | 1.5 |
| 9 | TCP Session Hijacking | 3.5 |
| 10 | Reverse Shell via TCP Session Hijacking | 2.5 |
| | **Total** | **20** |

## Topology summary

| Host | Image | Flavor |
|------|-------|--------|
| attacker | seed | m1.medium |
| server | seed | m1.medium |
| client | seed | m1.medium |
| router | debian-12-x86_64 | m1.medium |

`attacker`, `server` and `client` are all on the **same LAN** (`10.1.26.0/24`), because the SEED Labs TCP/IP Attack Lab explicitly assumes the attacker can sniff the client<->server traffic to read sequence numbers, ack numbers and source ports.

## Environment facts (deliberately different from the PDF handout)

* Telnet service on server: port **2323** (not 23), account `victim` / `VictimPass2025` (not given to students - only its session matters).
* Radio-stream demo service (stand-in for the SEED Lab's video-streaming task): port **9091**.
* `net.ipv4.tcp_max_syn_backlog` on server: **8** (non-default, and deliberately small - see "Tooling" below).
* `net.ipv4.tcp_syncookies` on server: starts **off** (0).
* Diagnostic SSH account on server, given to students: `seedlab` / `Att@ckTCP25`.
* `client` keeps three persistent, auto-reconnecting connections to `server` at all times (telnet, SSH, radio-stream), so every attack always has a live target.
* Session-hijacking proof file: `/tmp/hijack_proof.txt` on the server, must contain `TCPHIJACK-9f41`.
* Final flag, readable only via reverse shell as `victim`: `~/flag_final.txt` -> `SEED-TCPLAB-FINAL-7e2b9c`.

## Tooling: Scapy only, no Netwox

All attacks are performed with **Scapy**, not Netwox. The attached PDF's own Task 1 note explicitly warns that Scapy's packet rate is far lower than Netwox's, so a realistic (large) SYN backlog would never fill in reasonable time with Scapy alone - that's why `net.ipv4.tcp_max_syn_backlog` is set to a small, non-default value (**8**) instead of the PDF's example.

Three skeleton scripts (with blanks the student must fill in from their own recon - not copy/pasteable) are provisioned on `attacker` at `/home/seed/scripts/`:
* `synflood_skeleton.py` - loops spoofed SYNs at a target `ip:port`.
* `rst_attack_skeleton.py` - sniffs one live packet of a session, then sends a matching spoofed RST.
* `hijack_skeleton.py` - sniffs one live packet, then injects a payload without resetting the connection (reused for both the session-hijacking and reverse-shell levels, with a different injected command).

## Levels

### Level 1: Mapping the LAN
**Learning outcomes:** host/service discovery with `nmap` on an unfamiliar subnet.
**Flag:** the telnet service's (non-default) port number -> `2323`.

### Level 2: Diagnostic access & reading the SYN backlog
**Learning outcomes:** using a legitimate diagnostic SSH account; reading kernel TCP parameters with `sysctl`.
**Flag:** the configured `net.ipv4.tcp_max_syn_backlog` value -> `8`.

### Level 3: SYN Flooding Attack
**Learning outcomes:** performing and verifying a SYN flood (SEED Labs Task 1) with Scapy (`synflood_skeleton.py`); recognizing a full half-open connection queue via `ss -tn state syn-recv` and a hanging new connection attempt.
**Flag:** the one-word observation (`timeout`) describing what happens to a brand-new, legitimate connection once the queue is full.

### Level 4: Turning on SYN cookies
**Learning outcomes:** understanding and applying the SYN cookie countermeasure.
**Flag:** the exact `sysctl -w` command.

### Level 5: TCP RST Attack - telnet
**Learning outcomes:** performing a TCP RST attack (SEED Labs Task 2) with Scapy (`rst_attack_skeleton.py`) against an unencrypted session, including sniffing a live packet to get a valid seq/ack.
**Flag:** the exact destination targeted, `ip:port`.

### Level 6: TCP RST Attack - SSH
**Learning outcomes:** showing that TCP RST attacks work identically against encrypted TCP sessions, since they exploit the transport layer, not the application layer.
**Flag:** the exact destination targeted, `ip:port`.

### Level 7: TCP RST Attack - radio stream
**Learning outcomes:** applying the RST attack against a persistent "streaming" service (stand-in for SEED Labs Task 3, kept self-contained instead of pointing at a real external website).
**Flag:** the exact destination targeted, `ip:port`.

### Level 8: TCP Session Hijacking
**Learning outcomes:** performing TCP session hijacking (SEED Labs Task 4) with Scapy (`hijack_skeleton.py`) by sniffing live seq/ack/port values and injecting a spoofed packet without resetting the connection.
**Flag:** the proof string written to the server by the injected command.

### Level 9: Reverse Shell via TCP Session Hijacking
**Learning outcomes:** chaining session hijacking into a reverse shell (SEED Labs Task 5) for persistent access.
**Flag:** the content of the final flag file, read through the obtained reverse shell.

## License

This work is licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0

## Attribution

Game design and topology style based on `library-junior-hacker` (CyberRangeCZ), itself based on:
junior-hacker (https://gitlab.ics.muni.cz/muni-kypo-trainings/games/junior-hacker), Cybersecurity Laboratory, Faculty of Informatics, Masaryk University.

Attack techniques and task structure adapted from the **SEED Labs TCP/IP Attack Lab**, Wenliang Du, Copyright (c) 2018, free to use for non-commercial educational purposes (see the attached PDF for the original license statement). This derivative training is likewise for non-commercial educational use only.
