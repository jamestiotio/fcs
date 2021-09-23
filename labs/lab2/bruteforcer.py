#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 2
# Bruteforce method to crack the cipher text for Part I
# James Raphael Tiovalen / 1004555

# Import libraries
import sys
import argparse
import string

# Define a bunch of input argument validators
def key_type(k):
    try:
        k = int(k)
        # Use %= len(string.printable) to allow and accommodate for key overflows outside of specified range
        if not 1 <= k <= len(string.printable) - 1:
            raise argparse.ArgumentTypeError(
                "Please input a valid key between 1 and len(string.printable) - 1, inclusive."
            )
        return k
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Please input an integer between 1 and len(string.printable) - 1, inclusive, for the key."
        )


def mode_type(m):
    m = str(m).lower()
    if m not in ["d", "e"]:
        raise argparse.ArgumentTypeError(
            'Select either decryption ("d") or encryption ("e") mode.'
        )
    return m

def main(filein, fileout, key, mode):
    shifted_printables = string.printable[36:62][key:] + string.printable[36:62][:key]
    output_text = ""
    # PROTIP: Pythonic way to open file handle in read mode
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        text = fin.read()
        # Do stuff
        if mode == "e":
            for c in text:
                if c.isalpha():
                    idx = string.printable[36:62].index(c)
                    output_text += shifted_printables[idx]
                else:
                    output_text += c
        elif mode == "d":
            for c in text:
                if c.isalpha():
                    idx = shifted_printables.index(c)
                    output_text += string.printable[36:62][idx]
                else:
                    output_text += c
        # File stream will be closed automatically when interpreter reaches end of the block

    # Write to fileout (open in another separate context to prevent simultaneous file opening/modification, race conditions, or corruptions due to unexpected crashes)
    # Tradeoff would be that the entire output needs to be temporarily stored in memory before directed and written to the output file
    with open(fileout, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.write(output_text)

# Our main function
if __name__ == "__main__":
    # Key is 16
    main("story_cipher.txt", "solution.txt", 16, "d")
