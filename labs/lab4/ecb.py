#!/usr/bin/env python3
# ECB wrapper skeleton file for SUTD 50.042 FCS Lab 4
# James Raphael Tiovalen / 1004555

from present import *
import argparse
import random
import secrets

nokeybits = 80
blocksize = 64
byte_blocksize = blocksize // 8


# Utility function to generate a random key file
def generate_key(key_filename, key_length):
    with open(key_filename, "wb") as keyfile:
        keyfile.write(secrets.token_bytes(key_length))


# PKCS#7-standard padding instead of zero padding (condition: byte_blocksize < 256)
# This padding scheme ensures unambiguity
def pad(data_to_pad):
    padding_len = byte_blocksize - len(data_to_pad) % byte_blocksize
    padding = bytes([padding_len]) * padding_len
    return data_to_pad + padding


def unpad(padded_data):
    pdata_len = len(padded_data)
    if pdata_len == 0:
        raise ValueError("Zero-length input cannot be unpadded!")
    if pdata_len % byte_blocksize:
        raise ValueError("Input data is not padded.")
    padding_len = padded_data[-1]
    if padding_len < 1 or padding_len > min(byte_blocksize, pdata_len):
        raise ValueError("Padding is incorrect.")
    if padded_data[-padding_len:] != bytes([padding_len]) * padding_len:
        raise ValueError("PKCS#7 padding is incorrect.")
    return padded_data[:-padding_len]


# Combined with PKCS#7 padding, this implementation actually greatly highlights, exemplifies, and somehow exaggerates the weakness of ECB mode
def ecb(infile, outfile, key, mode):
    with open(infile, "rb") as source, open(outfile, "wb") as dest:
        # Encryption
        if mode == "e":
            while byte := source.read(byte_blocksize):
                byte = pad(bytes(byte))
                for i in range(len(byte) // 8):
                    # Big-endian format (MSB at the beginning)
                    block = int.from_bytes(byte[i * 8 : 8 * (i + 1)], "big")
                    block = present(block, key)
                    chunk = block.to_bytes(byte_blocksize, "big")
                    dest.write(chunk)
        # Decryption
        else:
            while byte := source.read(byte_blocksize * 2):
                chunk = b""
                for i in range(len(byte) // 8):
                    # Big-endian format (MSB at the beginning)
                    block = int.from_bytes(byte[i * 8 : 8 * (i + 1)], "big")
                    block = present_inv(block, key)
                    chunk += block.to_bytes(byte_blocksize, "big")
                chunk = unpad(bytes(chunk))
                dest.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Block cipher using ECB mode.")
    parser.add_argument("-i", dest="infile", help="input file")
    parser.add_argument("-o", dest="outfile", help="output file")
    parser.add_argument("-k", dest="keyfile", help="key file")
    parser.add_argument("-m", dest="mode", help="mode")

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    keyfile = args.keyfile
    mode = args.mode

    # Argument validator checks
    if infile is None:
        sys.exit("Error: Please specify an input file.")
    if outfile is None:
        sys.exit("Error: Please specify an output file.")
    if mode is None:
        sys.exit("Error: Please specify a mode.")
    valid_modes = ["d", "e"]
    if mode.lower() not in valid_modes:
        sys.exit("Error: Invalid cipher mode.")
    if keyfile is None:
        sys.exit("Error: Please specify a file as the key.")

    # Parse key file as input bytes
    with open(keyfile, "rb") as file:
        key_content = file.read()
        seed = int.from_bytes(key_content, "big")

    # Use additional layer of separation for slightly higher security
    random.seed(seed)
    key = random.getrandbits(80)

    ecb(infile, outfile, key, mode)
