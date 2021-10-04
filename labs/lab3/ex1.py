#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 3 Part I
# James Raphael Tiovalen / 1004555

import hashlib

full_plaintext = "Pancakes are really fluffy!"
current_plaintext = ""
current_hash_result = hashlib.md5(current_plaintext.encode())

print(f"Plaintext: {current_plaintext}\nHash: {current_hash_result.hexdigest()}\n")

for c in full_plaintext:
    current_plaintext += c
    current_hash_result = hashlib.md5(current_plaintext.encode())
    print(f"Plaintext: {current_plaintext}\nHash: {current_hash_result.hexdigest()}\n")
