#!/usr/bin/env python3
"""
SubTakeover Auditor v1.0 - DNS Misconfiguration & Subdomain Takeover Auditor
Author: MAXA Cyber
"""

import sys
import socket
import urllib.request
import urllib.error

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

TAKEOVER_SIGNATURES = {
    "GitHub Pages": ["There isn't a GitHub Pages site here", "For root domain metadata or custom domain"],
    "Heroku": ["Heroku | No such app", "There's nothing here, points to a Heroku app"],
    "AWS S3 Bucket": ["The specified bucket does not exist", "NoSuchBucket"],
    "Shopify": ["Sorry, this shop is currently unavailable"],
    "Tumblr": ["Whatever you were looking for doesn't currently exist at this address"],
    "Ghost": ["The thing you were looking for is no longer here"]
}

class SubTakeoverAuditor:
    def __init__(self, target_domain):
        self.target = target_domain.replace("http://", "").replace("https://", "").strip("/")

    def audit(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}=== SubTakeover Auditor v1.0 ==={Colors.END}")
        print(f"{Colors.BOLD}Nishon domen:{Colors.END} {self.target}\n")

        subdomains = ["dev", "blog", "app", "status", "shop", "api", "staging", "test", "docs"]
        print(f"{'SUBDOMEN':<25} {'IP MANZIL':<18} {'HOLAT / SIGNATURA'}")
        print("-" * 65)

        for sub in subdomains:
            full_domain = f"{sub}.{self.target}"
            try:
                ip = socket.gethostbyname(full_domain)
                self._check_http_response(full_domain, ip)
            except socket.gaierror:
                pass

    def _check_http_response(self, domain, ip):
        url = f"http://{domain}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'SubTakeover-Checker/1.0'})
            with urllib.request.urlopen(req, timeout=3) as res:
                body = res.read().decode('utf-8', errors='ignore')
                vulnerable_to = None
                for service, sigs in TAKEOVER_SIGNATURES.items():
                    if any(sig in body for sig in sigs):
                        vulnerable_to = service
                        break

                if vulnerable_to:
                    print(f"{Colors.RED}[VULN TAKE_OVER]{Colors.END} {domain:<25} {ip:<18} -> {vulnerable_to}")
                else:
                    print(f"{Colors.GREEN}[ACTIVE/OK]{Colors.END} {domain:<25} {ip:<18} -> Xavfsiz")
        except urllib.error.HTTPError as e:
            print(f"{Colors.YELLOW}[HTTP {e.code}]{Colors.END} {domain:<25} {ip:<18} -> Javob berdi")
        except Exception:
            print(f"{Colors.GREEN}[ACTIVE/OK]{Colors.END} {domain:<25} {ip:<18} -> Port ochiq")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Foydalanish: python3 sub_takeover_checker.py <target_domain>")
        sys.exit(1)
    auditor = SubTakeoverAuditor(sys.argv[1])
    auditor.audit()
