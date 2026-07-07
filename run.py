#!/usr/bin/env python3
import subprocess
import sys

try:
    subprocess.run([sys.executable, "main.py"], check=True)
except Exception as e:
    print(f"Error running application: {e}")
    input("Press Enter to exit...")
