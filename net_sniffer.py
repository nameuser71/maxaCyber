#!/usr/bin/env python3
"""
NetSniffer Light v1.0 - Packet Header Analyzer & Plaintext Credential Auditor
Author: MAXA Cyber
"""

import socket
import struct
import sys

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

class NetSniffer:
    def parse_packet(self, packet):
        ip_header = packet[0:20]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = iph[0]
        ihl = (version_ihl & 0xF) * 4
        ttl = iph[5]
        protocol = iph[6]
        src_ip = socket.inet_ntoa(iph[8])
        dst_ip = socket.inet_ntoa(iph[9])

        proto_name = "TCP" if protocol == 6 else ("UDP" if protocol == 17 else f"Proto:{protocol}")

        print(f"{Colors.CYAN}[PACKET]{Colors.END} {src_ip:<15} -> {dst_ip:<15} | {proto_name:<6} | TTL: {ttl}")

if __name__ == "__main__":
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== NetSniffer Light v1.0 ==={Colors.END}")
    print(f"{Colors.BOLD}Eslatma:{Colors.END} Raw socket yaratish va tarmoq trafigini kuzatish uchun root huquqi talab qilinadi.\n")
    print("Paket sarlavhalarini namuna sifatida parser qilish rejimi ishga tushdi.")
    
    # Simulate packet header dissection demonstration
    dummy_packet = b'\x45\x00\x00\x3c\x1c\x46\x40\x00\x40\x06\xb1\xe6\xc0\xa8\x01\x32\xc0\xa8\x01\x01'
    sniffer = NetSniffer()
    sniffer.parse_packet(dummy_packet)
    print(f"\n{Colors.GREEN}[✓] Paket tahlili yakunlandi.{Colors.END}\n")
