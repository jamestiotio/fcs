#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 7 Part IV
# James Raphael Tiovalen / 1004555

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from rsa_utils import *
import secrets

if __name__ == "__main__":
    # Import private key and public key from files
    with open("mykey.pem.pub", "r") as pubkey_file:
        pubkey = RSA.import_key(pubkey_file.read())
    with open("mykey.pem.priv", "r") as privkey_file:
        privkey = RSA.import_key(privkey_file.read())

    s = secrets.SystemRandom().randint(0, 2 ** 1024)
    signature = SHA256.new(get_byte_from_int(s)).hexdigest()
    x = encrypt_message(signature, pubkey.e, pubkey.n)
    x_prime = encrypt_message(signature, pubkey.e, pubkey.n)

    assert x == x_prime
    print(
        f"Signature: {signature}\n\nReceived digest: {x}\n\nVerified digest: {x_prime}"
    )
