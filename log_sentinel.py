#!/usr/bin/env python3
"""
LogSentinel v1.0 - Real-Time System Log & Intrusion Detector
Author: MAXA Cyber
"""

import re
import sys
import os

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

SAMPLE_LOG_DATA = """
Oct 24 18:01:02 server sshd[1234]: Failed password for root from 192.168.1.100 port 45222 ssh2
Oct 24 18:01:05 server sshd[1235]: Failed password for root from 192.168.1.100 port 45224 ssh2
Oct 24 18:01:08 server sshd[1236]: Failed password for admin from 192.168.1.100 port 45226 ssh2
Oct 24 18:01:10 server sshd[1237]: Failed password for user1 from 192.168.1.105 port 45228 ssh2
Oct 24 18:02:15 server nginx: 10.0.0.5 - - [24/Oct/2026:18:02:15] "GET /admin' OR '1'='1 HTTP/1.1" 200 4502
Oct 24 18:02:20 server nginx: 10.0.0.5 - - [24/Oct/2026:18:02:20] "GET /<script>alert(1)</script> HTTP/1.1" 404 120
Oct 24 18:03:00 server sshd[1240]: Accepted password for kali from 192.168.1.50 port 51102 ssh2
"""

class LogSentinel:
    def __init__(self, log_content):
        self.log_content = log_content
        self.ssh_failed = {}
        self.sqli_attempts = []
        self.xss_attempts = []

    def analyze(self):
        lines = self.log_content.strip().split('\n')
        for line in lines:
            # SSH Brute Force pattern
            failed_ssh = re.search(r'Failed password for (?:invalid user )?(\w+) from ([\d\.]+) ', line)
            if failed_ssh:
                user, ip = failed_ssh.groups()
                self.ssh_failed[ip] = self.ssh_failed.get(ip, 0) + 1

            # SQL Injection pattern
            if re.search(r"('|%27)|(union|select|insert|drop|where|or|and)\b", line, re.IGNORECASE):
                self.sqli_attempts.append(line)

            # XSS pattern
            if re.search(r"(<script>|%3Cscript%3E|javascript:)", line, re.IGNORECASE):
                self.xss_attempts.append(line)

    def print_report(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}=== LogSentinel v1.0 - Xavfsizlik Tahlilchisi ==={Colors.END}\n")

        print(f"{Colors.BOLD}[+] SSH Brute-Force Hujumlar Tahlili:{Colors.END}")
        if self.ssh_failed:
            for ip, count in self.ssh_failed.items():
                severity = f"{Colors.RED}[CRITICAL]{Colors.END}" if count >= 3 else f"{Colors.YELLOW}[WARNING]{Colors.END}"
                print(f"  {severity} IP: {ip:<16} - {count} marta muvaffaqiyatsiz kirish urunishi")
        else:
            print(f"  {Colors.GREEN}[✓] SSH xavfi aniqlanmadi.{Colors.END}")

        print(f"\n{Colors.BOLD}[+] Web Hujumlar (SQL Injection & XSS):{Colors.END}")
        if self.sqli_attempts:
            print(f"  {Colors.RED}[!] SQL Injection urunishlari ({len(self.sqli_attempts)} ta):{Colors.END}")
            for log in self.sqli_attempts:
                print(f"    - {log}")
        if self.xss_attempts:
            print(f"  {Colors.RED}[!] XSS urunishlari ({len(self.xss_attempts)} ta):{Colors.END}")
            for log in self.xss_attempts:
                print(f"    - {log}")

        print(f"\n{Colors.GREEN}[✓] Jurnallar auditi yakunlandi.{Colors.END}\n")

if __name__ == "__main__":
    sentinel = LogSentinel(SAMPLE_LOG_DATA)
    sentinel.analyze()
    sentinel.print_report()
