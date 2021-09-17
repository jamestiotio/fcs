#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple shift cipher with auxiliary file read in/out capabilities


# Import libraries
import sys
import argparse
import string

# Define a bunch of input argument validators
def key_type(k):
    try:
        k = int(k)
        # Use %= 256 to allow and accommodate for key overflows outside of specified range
        if not 0 <= k <= 255:
            raise argparse.ArgumentTypeError(
                "Please input a valid key between 0 and 255, inclusive."
            )
        return k
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Please input an integer between 0 and 255, inclusive, for the key."
        )


def mode_type(m):
    m = str(m).lower()
    if m not in ["d", "e"]:
        raise argparse.ArgumentTypeError(
            'Select either decryption ("d") or encryption ("e") mode.'
        )
    return m


def do_stuff(filein, fileout, key, mode):
    output_bin = []
    # PROTIP: Pythonic way to open file handle in binary read mode
    with open(filein, mode="rb") as fin_b:
        text = fin_b.read()
        # Do stuff
        if mode == "e":
            for p in text:
                c = (p + key) % 256
                output_bin.append(c)
        elif mode == "d":
            for c in text:
                p = (c - key) % 256
                output_bin.append(p)
        # File stream will be closed automatically when interpreter reaches end of the block

    # Write to fileout (open in another separate context to prevent simultaneous file opening/modification and race conditions)
    with open(fileout, mode="wb") as fout_b:
        fout_b.write(bytearray(output_bin))


# Our main function
if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file", default="sherlock.txt")
    parser.add_argument("-o", dest="fileout", help="output file", default="out")
    parser.add_argument("-k", dest="key", help="key", type=key_type, default=0)
    parser.add_argument("-m", dest="mode", help="mode", type=mode_type, default="e")

    # Parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.key
    mode = args.mode

    do_stuff(filein, fileout, key, mode)

    # All done
