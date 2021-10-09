#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for SUTD 50.042 FCS Lab 4
# James Raphael Tiovalen / 1004555

import argparse


def getInfo(headerfile):
    with open(headerfile, "rb") as header:
        content = header.read()

    return content


def extract(infile, outfile, headerfile):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract PBM pattern.")
    parser.add_argument("-i", dest="infile", help="input file, PBM encrypted format")
    parser.add_argument("-o", dest="outfile", help="output PBM file")
    parser.add_argument("-hh", dest="headerfile", help="known header file")

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    headerfile = args.headerfile

    print("Reading from: %s" % infile)
    print("Reading header file from: %s" % headerfile)
    print("Writing to: %s" % outfile)

    success = extract(infile, outfile, headerfile)
