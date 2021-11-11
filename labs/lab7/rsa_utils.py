#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 7
# James Raphael Tiovalen / 1004555

from primes import square_multiply
from base64 import decodebytes, encodebytes


def encrypt(x, e, n):
    return square_multiply(x, e, n)


def decrypt(x, d, n):
    return square_multiply(x, d, n)


def get_byte_from_int(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, "big")


def get_int_from_byte(x: bytes) -> int:
    return int.from_bytes(x, "big")


def encrypt_message(message, e, n):
    encoded_message = get_int_from_byte(encodebytes(message.encode()))
    return encrypt(encoded_message, e, n)


def decrypt_message(encrypted, d, n):
    decrypted_message = decrypt(encrypted, d, n)
    return decodebytes(get_byte_from_int(decrypted_message)).decode()
