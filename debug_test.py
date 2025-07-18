#!/usr/bin/env python3
"""
⚡ SIMPLE STEALTH TEST - Debug Version
"""

try:
    import subprocess
    import os
    import time
    import sys
    import psutil
    from pathlib import Path
    from datetime import datetime
    from colorama import Fore, Style, init
    
    print("All imports successful!")
    
    init(autoreset=True)
    print("Colorama initialized!")
    
    # Test system info
    TOTAL_RAM_GB = psutil.virtual_memory().total / (1024**3)
    print(f"Total RAM: {TOTAL_RAM_GB:.1f} GB")
    
    # Test banner
    print(f"{Fore.GREEN}✅ Debug test successful!{Style.RESET_ALL}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
