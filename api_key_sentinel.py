#!/usr/bin/env python3
"""
API Key Sentinel v1.0 - High-Entropy Token & Secret Leak Detector
Author: MAXA Cyber
"""

import sys
import re
import json
import base64

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

KEY_PATTERNS = {
    "AWS Access Key ID": r'AKIA[0-9A-Z]{16}',
    "GitHub Personal Access Token": r'ghp_[a-zA-Z0-9]{36}',
    "Google API Key": r'AIzaSy[a-zA-Z0-9_\-]{33}',
    "Slack Webhook URL": r'https://hooks\.slack\.com/services/T[a-zA-Z0-9_]+/B[a-zA-Z0-9_]+/[a-zA-Z0-9_]+',
    "RSA Private Key Header": r'-----BEGIN RSA PRIVATE KEY-----',
    "JWT Token": r'eyJ[a-zA-Z0-9_\-]+\.eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+'
}

SAMPLE_CODE = """
# Config File Sample
AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
GOOGLE_KEY = "AIzaSyD1234567890abcdefghijklmnopqrstuv"
JWT_AUTH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
"""

class KeySentinel:
    def __init__(self, content):
        self.content = content

    def scan(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}=== API Key Sentinel v1.0 - Kalit va Tokenlar Auditi ==={Colors.END}\n")
        found_leaks = 0

        for key_type, pattern in KEY_PATTERNS.items():
            matches = re.findall(pattern, self.content)
            if matches:
                found_leaks += len(matches)
                print(f"{Colors.RED}[CRITICAL LEAK]{Colors.END} {key_type} topildi:")
                for m in matches:
                    print(f"  -> {Colors.YELLOW}{m[:35]}...{Colors.END}")

                    if key_type == "JWT Token":
                        self._decode_jwt(m)

        if found_leaks == 0:
            print(f"{Colors.GREEN}[✓] Hech qanday maxfiy kalit yoki token sizishi aniqlanmadi.{Colors.END}")
        else:
            print(f"\n{Colors.RED}[!] Jami {found_leaks} ta xavfli kalit va tokenlar topildi!{Colors.END}")

    def _decode_jwt(self, jwt_str):
        try:
            parts = jwt_str.split('.')
            if len(parts) >= 2:
                payload = parts[1]
                padded = payload + '=' * (-len(payload) % 4)
                decoded = base64.b64decode(padded).decode('utf-8')
                data = json.loads(decoded)
                print(f"     {Colors.CYAN}[JWT Payload Structure]:{Colors.END} {json.dumps(data)}")
        except Exception as e:
            pass

if __name__ == "__main__":
    sentinel = KeySentinel(SAMPLE_CODE)
    sentinel.scan()
