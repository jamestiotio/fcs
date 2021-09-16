#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out


# Import libraries
import sys
import argparse
import string


def key_type(k):
    k = int(k)
    if not 1 <= k <= len(string.printable) - 1:
        raise argparse.ArgumentTypeError(
            "Please input a valid key between 1 and len(string.printable) - 1, inclusive."
        )
    return k


def mode_type(m):
    m = str(m).lower()
    if m not in ["d", "e"]:
        raise argparse.ArgumentTypeError(
            'Select either decryption ("d") or encryption ("e") mode.'
        )
    return m


def doStuff(filein, fileout, key, mode):
    # PROTIP: Pythonic way to open file handle in binary read mode
    with open(filein, mode="rb") as fin:
        text = fin.read()
        # do stuff

        # file stream will be closed automatically when interpreter reaches end of the block


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file", default="out")
    parser.add_argument("-k", dest="key", help="key", type=key_type)
    parser.add_argument("-m", dest="mode", help="mode", type=mode_type)

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.key
    mode = args.mode

    doStuff(filein, fileout, key, mode)

    # all done
