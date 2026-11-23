# TCP/IP Attack Lab
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-orange.svg)](https://creativecommons.org/licenses/by/4.0/)

Linear training for [CyberRangeCZ Platform](https://docs.platform.cyberrange.cz/), built from the `library-junior-hacker` scenario template and adapted to cover the **SEED Labs TCP/IP Attack Lab** (SYN flooding, TCP RST attacks, TCP session hijacking, reverse shells).

## Game Levels Summary
All attacks use **Scapy only** (no Netwox) - skeleton scripts with blanks for students to fill in are provisioned on `attacker` at `/home/seed/scripts/`.
- recon the LAN with `nmap` (service discovery - IPs and ports deliberately non-default)
- use a diagnostic SSH account to read kernel TCP parameters with `sysctl`
- SYN flooding attack (`synflood_skeleton.py`), verified via `ss -tn state syn-recv` and a timed-out connection attempt
- SYN cookie countermeasure
- TCP RST attack against a telnet session (`rst_attack_skeleton.py`)
- TCP RST attack against an SSH session (same script/technique, shows encryption doesn't help)
- TCP RST attack against a persistent "streaming" service (stand-in for SEED Labs' video-streaming task)
- TCP session hijacking: sniff live seq/ack/port and inject a command (`hijack_skeleton.py`)
- reverse shell via TCP session hijacking (same script, different injected payload)

Scored **20/20 points**, hint penalties between **0.5 and 2 points** per hint. See `game_design.md` for the full point breakdown.

## Topology summary
|Host|Image|Flavor|
|-|-|-|
|attacker|seed|m1.medium|
|server|seed|m1.medium|
|client|seed|m1.medium|
|router|debian-12-x86_64|m1.medium|

`attacker`, `server`, and `client` share a single LAN switch (`10.1.26.0/24`), unlike the original `library-junior-hacker` topology, because the TCP/IP Attack Lab requires the attacker to sniff the client<->server traffic.

## Before you deploy this sandbox

1. **No external attack-tool package needed.** All attacks run through Scapy (preinstalled via `python3-scapy`), using the skeleton scripts in `provisioning/roles/attacker/files/`. Nothing to source or build.
2. **`seed` base image.** This topology assumes an image literally named `seed` exists in your CyberRangeCZ image catalog (per your request, replacing `kali`). If your catalog uses a different name for a Debian/Ubuntu-based pentesting-capable image, update `topology.yml` accordingly.
3. **`m1.medium` flavor.** Same note - make sure this flavor name exists in your OpenStack/cloud backend; swap it in `topology.yml` otherwise.
4. **Attach the PDF.** The SEED Labs `TCP_Attacks.pdf` handout is referenced throughout the level text (section numbers) but is not embedded in `training.json`. Upload it as an attachment on the `Introduction` level (or on each relevant training level) through the CyberRangeCZ admin UI after import.
5. **SYN flood timing.** The `syn_backlog` value (currently `8`) controls how many spoofed SYNs are needed to fill the queue and how quickly `synflood_skeleton.py`'s `COUNT` (2000) achieves it. If your `seed` image's Scapy performs very differently, you may need to adjust one or both values - test this level first.
6. This has **not been deployed/tested on an actual CyberRangeCZ Platform instance** - it was authored from the `library-junior-hacker` template and the attached PDF only. Please dry-run the Ansible provisioning and walk through every level yourself before assigning it to students, and let me know if anything needs adjusting (exact `sysctl`/package names, or Scapy's actual achievable packet rate on `seed`, can vary by base image).

## License

This repository uses a dual licensing approach:

* The code (Ansible and custom code) is licensed under the terms of the MIT License (https://opensource.org/license/mit).
* The game design is licensed under a Creative Commons Attribution 4.0 International License (CC BY 4.0).

**Attribution:**

Topology/role structure based on `library-junior-hacker` (CyberRangeCZ), itself based on junior-hacker (https://gitlab.ics.muni.cz/muni-kypo-trainings/games/junior-hacker), Cybersecurity Laboratory, Faculty of Informatics, Masaryk University.

Attack tasks adapted from the **SEED Labs TCP/IP Attack Lab**, Copyright (c) 2018 Wenliang Du, free to use for non-commercial educational purposes.
