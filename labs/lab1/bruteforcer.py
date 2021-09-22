#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# James Raphael Tiovalen / 1004555


# Import libraries
from subprocess import run

if __name__ == "__main__":
    for key in range(0, 256):
        print(f"CURRENT KEY: {key}")
        flag_decryption_command = run(
            ["python3", "ex2.py", "-i", "flag", "-o", "out", "-k", f"{key}", "-m", "d"]
        )
        filetype_inspection_command = run(
            ["file", "out"],
        )
        print("")
