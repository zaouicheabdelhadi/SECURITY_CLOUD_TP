Place the netwox/netwag .deb package here as:
    netwox_3.00.0_amd64.deb

Netwox is no longer in the Debian/Ubuntu repositories (same issue the
original library-junior-hacker scenario had with fcrackzip), so it must be
shipped as a binary asset, exactly like fcrackzip_1.0-10_amd64.deb was in
that scenario. Sources:
  - https://github.com/sfrancis23/netwox (build from source), or
  - any internally-hosted mirror of the Netwox 3.00/5.x .deb your team trusts.

If you do not want to ship netwox at all, remove the two netwox tasks from
provisioning/roles/attacker/tasks/main.yml and change level "SYN Flooding
Attack", "TCP RST Attack..." and "TCP Session Hijacking" content/hints to
only reference Scapy (a cheat-sheet is already provisioned for students at
/home/user/scapy_cheatsheet.txt).
