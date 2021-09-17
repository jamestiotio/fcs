#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple shift cipher with auxiliary file read in/out capabilities
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


def do_stuff(filein, fileout, key, mode):
    shifted_printables = string.printable[key:] + string.printable[:key]
    output_text = ""
    # PROTIP: Pythonic way to open file handle in read mode
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        text = fin.read()
        # Do stuff
        if mode == "e":
            for c in text:
                idx = string.printable.index(c)
                output_text += shifted_printables[idx]
        elif mode == "d":
            for c in text:
                idx = shifted_printables.index(c)
                output_text += string.printable[idx]
        # File stream will be closed automatically when interpreter reaches end of the block

    # Write to fileout (open in another separate context to prevent simultaneous file opening/modification and race conditions)
    with open(fileout, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.write(output_text)


# Our main function
if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file", default="sherlock.txt")
    parser.add_argument("-o", dest="fileout", help="output file", default="output.txt")
    parser.add_argument("-k", dest="key", help="key", type=key_type, default=1)
    parser.add_argument("-m", dest="mode", help="mode", type=mode_type, default="e")

    # Parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.key
    mode = args.mode

    do_stuff(filein, fileout, key, mode)

    # All done
