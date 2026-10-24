#!/usr/bin/env python3
"""
@maxaCyber AUTO DEPENDENCY INSTALLER v1.0
Automated Library & Dependency Manager for all MAXA Cyber Security Tools
Author: @maxaCyber
"""

import sys
import subprocess
import time

# Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
END = '\033[0m'
BOLD = '\033[1m'

ASCII_BANNER = f"""{CYAN}{BOLD}
   ██████╗  ███╗   ███╗██████╗  ██╗  ██╗██████╗ ██╗██████╗ ███████╗██████╗ 
  ██╔════╝  ████╗ ████║██╔══██╗ ██║  ██║██╔════╝██║██╔══██╗██╔════╝██╔══██╗
  ██║  ███╗ ██╔████╔██║███████║ ███████║██║     ██║██████╔╝█████╗  ██████╔╝
  ██║   ██║ ██║╚██╔╝██║██╔══██║ ██╔══██║██║     ██║██╔══██╗██╔══╝  ██╔══██╗
  ╚██████╔╝ ██║ ╚═╝ ██║██║  ██║ ██║  ██║╚██████╗██║██████╔╝███████╗██║  ██║
   ╚═════╝  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═════╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
{END}{YELLOW}                 AUTOMATED ALL-IN-ONE DEPENDENCY INSTALLER{END}
"""

REQUIRED_PACKAGES = [
    "requests",
    "urllib3",
    "dnspython",
    "cryptography",
    "pycryptodome",
    "beautifulsoup4",
    "scapy",
    "colorama",
    "pyzipper",
    "tqdm"
]

def check_and_install():
    print(ASCII_BANNER)
    print(f"{BOLD}[+] Barcha MAXA Cyber toollari uchun kerakli kutubxonalar o'rnatilmoqda...{END}\n")

    failed_packages = []
    
    for pkg in REQUIRED_PACKAGES:
        print(f"  {BOLD}[*] {pkg:<20}:{END} ", end="", flush=True)
        try:
            # Run pip install
            cmd = [sys.executable, "-m", "pip", "install", pkg, "--break-system-packages"]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode == 0:
                print(f"{GREEN}[✓] O'RNATILDI / MAVJUD{END}")
            else:
                # Retry without --break-system-packages
                cmd_fallback = [sys.executable, "-m", "pip", "install", pkg]
                res_fb = subprocess.run(cmd_fallback, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if res_fb.returncode == 0:
                    print(f"{GREEN}[✓] O'RNATILDI{END}")
                else:
                    print(f"{RED}[✗] XATOLIK{END}")
                    failed_packages.append(pkg)
        except Exception as e:
            print(f"{RED}[✗] XATOLIK: {e}{END}")
            failed_packages.append(pkg)

    print("\n" + "=" * 60)
    if not failed_packages:
        print(f"{GREEN}{BOLD}[✓] BARCHA KUTUBXONALAR MUVAFFAQIYATLI O'RNATILDI!{END}")
        print(f"{CYAN}Barcha toollarni muammosiz ishlatishingiz mumkin.{END}\n")
    else:
        print(f"{YELLOW}[!] Quyidagi paketlarni o'rnatishda xatolik bo'ldi:{END} {', '.join(failed_packages)}")
        print(f"{YELLOW}Tarmoq ulanishini tekshiring yoki qo'lda 'pip install <package>' qilib ko'ring.{END}\n")

if __name__ == "__main__":
    check_and_install()
