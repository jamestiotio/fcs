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
    output_text = ""
    # PROTIP: Pythonic way to open file handle in read mode
    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        text = fin.read()
        # do stuff
        shifted_printables = string.printable[key:] + string.printable[:key]
        if mode == "e":
            for c in text:
                idx = string.printable.index(c)
                output_text += shifted_printables[idx]
        elif mode == "d":
            for c in text:
                idx = shifted_printables.index(c)
                output_text += string.printable[idx]
        # file stream will be closed automatically when interpreter reaches end of the block

    # write to fileout (open in another separate context to prevent simultaneous file opening/modification and race conditions)
    with open(fileout, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.write(output_text)


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file", default="output.txt")
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
