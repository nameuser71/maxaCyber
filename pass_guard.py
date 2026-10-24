#!/usr/bin/env python3
"""
PassGuard Pro v1.0 - Password Security Analyzer & Entropy Calculator
Author: MAXA Cyber
"""

import math
import sys
import re

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

class PassGuard:
    def __init__(self, password):
        self.password = password

    def calculate_entropy(self):
        charset_size = 0
        if re.search(r'[a-z]', self.password):
            charset_size += 26
        if re.search(r'[A-Z]', self.password):
            charset_size += 26
        if re.search(r'[0-9]', self.password):
            charset_size += 10
        if re.search(r'[^a-zA-Z0-9]', self.password):
            charset_size += 32

        if charset_size == 0 or len(self.password) == 0:
            return 0.0

        entropy = len(self.password) * math.log2(charset_size)
        return round(entropy, 2)

    def evaluate_strength(self, entropy):
        length = len(self.password)
        checks = {
            "Uzunlik (>= 12 belgi)": length >= 12,
            "Katta harflar (A-Z)": bool(re.search(r'[A-Z]', self.password)),
            "Kichik harflar (a-z)": bool(re.search(r'[a-z]', self.password)),
            "Raqamlar (0-9)": bool(re.search(r'[0-9]', self.password)),
            "Maxsus belgilar (!@#$)": bool(re.search(r'[^a-zA-Z0-9]', self.password))
        }

        if entropy < 30:
            rating = "JUDA ZAIF (Juda tez buziladi)"
            color = Colors.RED
        elif entropy < 50:
            rating = "ZAIF (Lug'at hujumiga ojiz)"
            color = Colors.RED
        elif entropy < 70:
            rating = "O'RTACHA (Qoniqarli)"
            color = Colors.YELLOW
        elif entropy < 90:
            rating = "KUCHLI (Xavfsiz)"
            color = Colors.GREEN
        else:
            rating = "JUDA KUCHLI (Yuqori darajada himoyalangan)"
            color = Colors.CYAN

        return rating, color, checks

    def print_analysis(self):
        entropy = self.calculate_entropy()
        rating, color, checks = self.evaluate_strength(entropy)

        print(f"\n{Colors.CYAN}{Colors.BOLD}=== PassGuard Pro v1.0 ==={Colors.END}")
        print(f"{Colors.BOLD}Parol uzunligi:{Colors.END} {len(self.password)} belgi")
        print(f"{Colors.BOLD}Entropiya darajasi:{Colors.END} {entropy} bit")
        print(f"{Colors.BOLD}Xavfsizlik darajasi:{Colors.END} {color}{rating}{Colors.END}\n")

        print(f"{Colors.BOLD}Tahlil mezonlari:{Colors.END}")
        for check_name, passed in checks.items():
            status = f"{Colors.GREEN}[✓] O'tdi{Colors.END}" if passed else f"{Colors.RED}[✗] Yo'q{Colors.END}"
            print(f"  - {check_name:<30} : {status}")

        print("\n" + "="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Foydalanish: python3 pass_guard.py <parol>")
        sys.exit(1)
    guard = PassGuard(sys.argv[1])
    guard.print_analysis()
