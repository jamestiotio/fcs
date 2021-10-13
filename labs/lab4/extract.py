#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for SUTD 50.042 FCS Lab 4
# James Raphael Tiovalen / 1004555

import argparse
from collections import Counter


def getInfo(headerfile):
    header_content = b""
    header_length = -1
    with open(headerfile, "rb") as header:
        header_content = header.read()
        header_length = len(header_content)

    return header_content, header_length


# We do some kind of frequency analysis attack (using some eye power as well)
def extract(infile, outfile, headerfile):
    header_content, header_length = getInfo(headerfile)
    if header_length == -1:
        return False
    encrypted = []

    with open(infile, "rb") as fin:
        # Skip to just after the header in the ciphertext (+1 for line feed)
        fin.read(header_length + 1)
        while byte := fin.read(8):
            encrypted.append(byte)

    # Find block with highest frequency
    block_frequency = dict(Counter(encrypted))

    frequency = -1
    for block, count in block_frequency.items():
        if count > frequency:
            most_frequent_block = block
            frequency = count

    if frequency == -1:
        return False

    # Decrypt based on frequency
    # We assign the blocks with highest frequency as 00000000 (all white)
    # For the rest of the blocks, we assign as 11111111 (all black)
    # This is interchangeable since we know that the image is only black and white
    decrypted = [
        b"0" * 8 if block == most_frequent_block else b"1" * 8 for block in encrypted
    ]

    # Combine decrypted blocks together
    decrypted = "".join([block.decode() for block in decrypted]).encode()

    # Write header + decrypted content to output file
    with open(outfile, "wb") as fout:
        fout.write(header_content + b"\n" + decrypted)

    return True


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

    print(f"PBM pattern extraction {'successful' if success else 'failed'}!")
