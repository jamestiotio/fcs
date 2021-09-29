#!/usr/bin/env python3
# Backup file for SUTD 50.042 FCS Lab 2 Part II
# In case the server goes down
# James Raphael Tiovalen / 1004555

import os
import base64


def XOR(a, b):
    r = b""
    for x, y in zip(a, b):
        r += (x ^ y).to_bytes(1, "big")
    return r


def gen_OTP(length):
    return bytearray(os.urandom(length))


def decrypt(cipher, OTP):
    # DO NOT change this function
    return XOR(cipher, OTP)


# Original message
original_plaintext = b"Student ID 1004555 gets a total of 0 points!\n"

# Randomly generated OTP
OTP = gen_OTP(length=len(original_plaintext))

# Encrypt
original_cipher = XOR(original_plaintext, OTP)

# Decrypt
print(decrypt(original_cipher, OTP))

target_string = b"Student ID 1004555 gets a total of 4 points!\n"


def hax():
    # Here, we manipulate the ciphertext without referring to the secret OTP to decrypt to:
    # "Student ID 100XXXX gets a total of 4 points!"
    mask = XOR(original_plaintext, target_string)
    new_cipher = XOR(original_cipher, mask)
    return new_cipher


new_cipher = hax()

# Decrypt function should provide the manipulated message:
print(decrypt(new_cipher, OTP))
