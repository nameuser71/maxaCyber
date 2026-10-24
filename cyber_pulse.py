#!/usr/bin/env python3
"""
CyberPulse Recon Framework v1.0
Automated Cybersecurity Reconnaissance, Network Scanner & Web Header Audit Tool
Author: MAXA Cyber
"""

import sys
import os
import socket
import ssl
import json
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# ANSI Color Codes for Terminal
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
  ██████╗██╗███╗   ██╗███████╗██████╗ ██████╗ ██╗   ██╗██╗     ███████╗███████╗
 ██╔════╝██║████╗  ██║██╔════╝██╔══██╗██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
 ██║     ██║██╔██╗ ██║█████╗  ██████╔╝██████╔╝██║   ██║██║     ███████╗█████╗  
 ██║     ██║██║╚██╗██║██╔══╝  ██╔══██╗██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  
 ╚██████╗██║██║ ╚████║███████╗██║  ██║██║     ╚██████╔╝███████╗███████║███████╗
  ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
{Colors.ENDC}{Colors.WARNING}         Automated Reconnaissance & Security Header Auditor v1.0{Colors.ENDC}
"""

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    1433: "MSSQL", 1521: "Oracle", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt"
}

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "X-XSS-Protection"
]

class CyberPulse:
    def __init__(self, target):
        self.target = target.replace("http://", "").replace("https://", "").strip("/")
        self.ip = None
        self.results = {
            "target": self.target,
            "scan_time": datetime.now().isoformat(),
            "ip_info": {},
            "open_ports": [],
            "http_headers": {},
            "missing_security_headers": [],
            "ssl_info": {}
        }

    def resolve_target(self):
        print(f"\n{Colors.BOLD}[+] Targetni IP manzilga aylantirish:{Colors.ENDC} {self.target}")
        try:
            self.ip = socket.gethostbyname(self.target)
            self.results["ip"] = self.ip
            print(f"    {Colors.OKGREEN}[✓] IP Manzil:{Colors.ENDC} {self.ip}")
            return True
        except socket.gaierror:
            print(f"    {Colors.FAIL}[✗] Xatolik: Target IP ga aylantirilmadi.{Colors.ENDC}")
            return False

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.2)
            result = sock.connect_ex((self.ip, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                banner = ""
                try:
                    sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                    banner = sock.recv(1024).decode(errors='ignore').split('\r\n')[0]
                except:
                    pass
                sock.close()
                return {"port": port, "service": service, "banner": banner}
            sock.close()
        except:
            pass
        return None

    def run_port_scan(self):
        print(f"\n{Colors.BOLD}[+] Portlarni skanerlash (Top portlar):{Colors.ENDC}")
        open_ports = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(self.scan_port, port) for port in COMMON_PORTS.keys()]
            for future in futures:
                res = future.result()
                if res:
                    open_ports.append(res)
                    print(f"    {Colors.OKGREEN}[OPEN]{Colors.ENDC} Port {res['port']}/TCP ({res['service']}) {res['banner']}")

        self.results["open_ports"] = open_ports
        if not open_ports:
            print(f"    {Colors.WARNING}[!] Ochiq standart portlar topilmadi.{Colors.ENDC}")

    def audit_http_headers(self):
        print(f"\n{Colors.BOLD}[+] Web Sarlavhalar va Xavfsizlik Sarlavhalari Auditi:{Colors.ENDC}")
        url = f"https://{self.target}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=5) as response:
                headers = dict(response.headers)
                self.results["http_headers"] = headers

                print(f"    {Colors.OKCYAN}[i] Server:{Colors.ENDC} {headers.get('Server', 'Yashiringan/Mavjud emas')}")

                missing = []
                for header in SECURITY_HEADERS:
                    if header in headers:
                        print(f"    {Colors.OKGREEN}[✓] {header}:{Colors.ENDC} {headers[header][:50]}...")
                    else:
                        print(f"    {Colors.FAIL}[✗] YETISHMAYDI:{Colors.ENDC} {header}")
                        missing.append(header)
                self.results["missing_security_headers"] = missing

        except urllib.error.URLError as e:
            print(f"    {Colors.WARNING}[!] HTTP/HTTPS ulanishda xatolik: {e}{Colors.ENDC}")

    def check_ssl_certificate(self):
        print(f"\n{Colors.BOLD}[+] SSL/TLS Sertifikati Ma'lumotlari:{Colors.ENDC}")
        ctx = ssl.create_default_context()
        try:
            with socket.create_connection((self.target, 443), timeout=3) as sock:
                with ctx.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    subject = dict(x[0] for x in cert.get('subject', []))
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    valid_to = cert.get('notAfter')
                    
                    ssl_info = {
                        "commonName": subject.get('commonName', ''),
                        "issuer": issuer.get('organizationName', ''),
                        "validTo": valid_to
                    }
                    self.results["ssl_info"] = ssl_info

                    print(f"    {Colors.OKGREEN}[✓] Sertifikat egasi:{Colors.ENDC} {ssl_info['commonName']}")
                    print(f"    {Colors.OKGREEN}[✓] Imzolagan markaz (Issuer):{Colors.ENDC} {ssl_info['issuer']}")
                    print(f"    {Colors.OKGREEN}[✓] Amal qilish muddati:{Colors.ENDC} {ssl_info['validTo']}")

        except Exception as e:
            print(f"    {Colors.WARNING}[!] SSL Ma'lumotlarini olib bo'lmadi: {e}{Colors.ENDC}")

    def fetch_ip_geo(self):
        print(f"\n{Colors.BOLD}[+] IP Geolokatsiya va ASN Ma'lumotlari:{Colors.ENDC}")
        try:
            url = f"http://ip-api.com/json/{self.ip}"
            req = urllib.request.Request(url, headers={'User-Agent': 'CyberPulse/1.0'})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode())
                if data.get('status') == 'success':
                    self.results["ip_info"] = data
                    print(f"    {Colors.OKGREEN}[✓] Mamlakat:{Colors.ENDC} {data.get('country')} ({data.get('countryCode')})")
                    print(f"    {Colors.OKGREEN}[✓] Shahar:{Colors.ENDC} {data.get('city')}")
                    print(f"    {Colors.OKGREEN}[✓] ISP/Provayder:{Colors.ENDC} {data.get('isp')}")
                    print(f"    {Colors.OKGREEN}[✓] AS Raqami:{Colors.ENDC} {data.get('as')}")
        except Exception as e:
            print(f"    {Colors.WARNING}[!] Geolocation olinmadi: {e}{Colors.ENDC}")

    def export_report(self):
        filename = f"report_{self.target.replace('.', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}[✓] Hisobot muvaffaqiyatli saqlandi:{Colors.ENDC} {filename}")

def main():
    print(BANNER)
    if len(sys.argv) < 2:
        print(f"{Colors.BOLD}Foydalanish:{Colors.ENDC} python3 cyber_pulse.py <target_domain>")
        print(f"{Colors.BOLD}Misol:{Colors.ENDC} python3 cyber_pulse.py example.com\n")
        sys.exit(1)

    target = sys.argv[1]
    scanner = CyberPulse(target)
    
    if scanner.resolve_target():
        scanner.fetch_ip_geo()
        scanner.run_port_scan()
        scanner.audit_http_headers()
        scanner.check_ssl_certificate()
        scanner.export_report()

    print(f"\n{Colors.OKCYAN}{Colors.BOLD}[+] Skanerlash yakunlandi!{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
