#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 3 Part IV
# James Raphael Tiovalen / 1004555

import os
import string
import hashlib
import secrets

TARGET_PLAINTEXT_FILE = "plain6.txt"
TARGET_HASH_FILE = "salted6.txt"

def hasher(message):
    return hashlib.md5(message.encode()).hexdigest()

if __name__ == "__main__":
    # Start from scratch
    if os.path.exists(TARGET_HASH_FILE):
        os.remove(TARGET_HASH_FILE)

    if os.path.exists(TARGET_PLAINTEXT_FILE):
        os.remove(TARGET_PLAINTEXT_FILE)

    if os.path.exists("ex2_hash.txt"):
        with open("ex2_hash.txt", mode="r", encoding="utf-8", newline="\n") as input_file:
            plaintexts = input_file.read().splitlines()

        salted_plaintexts = []

        for plaintext in plaintexts:
            random_lowercase_char = secrets.choice(string.ascii_lowercase)
            salted_plaintexts.append(f"{plaintext}{random_lowercase_char}")

        with open(TARGET_PLAINTEXT_FILE, mode="w", encoding="utf-8", newline="\n") as plaintext_output_file:
            plaintext_output_file.writelines([f"{plaintext}\n" for plaintext in salted_plaintexts])

        new_hashes = [hasher(plaintext) for plaintext in salted_plaintexts]

        with open(TARGET_HASH_FILE, mode="w", encoding="utf-8", newline="\n") as hash_output_file:
            hash_output_file.writelines([f"{hash}\n" for hash in new_hashes])
