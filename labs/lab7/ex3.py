#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 7 Part III
# James Raphael Tiovalen / 1004555

from Crypto.PublicKey import RSA
from rsa_utils import *

if __name__ == "__main__":
    # Import private key and public key from files
    with open("mykey.pem.pub", "r") as pubkey_file:
        pubkey = RSA.import_key(pubkey_file.read())
    with open("mykey.pem.priv", "r") as privkey_file:
        privkey = RSA.import_key(privkey_file.read())

    # RSA Encryption Protocol Attack Demonstration
    chosen_int = 100
    s = 2
    print(f"Encrypting: {chosen_int}\n")
    y = encrypt(chosen_int, pubkey.e, pubkey.n)
    print(f"Result: {y}\n")
    y_s = encrypt(s, pubkey.e, pubkey.n)
    print(
        f"Multiplying the encryption result by the encrypted value of the multiplier factor {s}, which is: {y_s}\n"
    )
    m = y * y_s
    print(f"Modified to: {m}\n")
    decrypted = decrypt(m, privkey.d, privkey.n)
    print(f"Decrypted: {decrypted}\n")
    assert chosen_int * s == decrypted
    if chosen_int * s == decrypted:
        print("Attack is successful!")
    else:
        print("Attack has failed.")
