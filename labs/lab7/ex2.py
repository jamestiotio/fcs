#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 7 Part II
# James Raphael Tiovalen / 1004555

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from rsa_utils import *


if __name__ == "__main__":
    # Import message, private key, and public key from files
    with open("message.txt", "r") as msg_file:
        msg = msg_file.read()
    with open("mykey.pem.pub", "r") as pubkey_file:
        pubkey = RSA.import_key(pubkey_file.read())
    with open("mykey.pem.priv", "r") as privkey_file:
        privkey = RSA.import_key(privkey_file.read())

    encrypted_message = encrypt_message(msg, pubkey.e, pubkey.n)
    decrypted_message = decrypt_message(encrypted_message, privkey.d, privkey.n)
    print(
        f"Original message: {msg}\n\nEncrypted message: {encrypted_message}\n\nDecrypted message: {decrypted_message}\n"
    )
    assert msg == decrypted_message
    if msg == decrypted_message:
        print("The decrypted message is the same as the original message.\n")
    else:
        print("The decrypted message is different from the original message.\n")

    # Demonstrate message hash signing
    msg_hash = SHA256.new(msg.encode()).hexdigest()
    signature = encrypt_message(msg_hash, privkey.d, privkey.n)
    signature_to_verify = decrypt_message(signature, pubkey.e, pubkey.n)
    print(
        f"Message hash: {msg_hash}\n\nSignature: {signature}\n\nVerified signature: {signature_to_verify}\n"
    )
    assert msg_hash == signature_to_verify
    if msg_hash == signature_to_verify:
        print(
            "The received message signature is the same as the original message hash."
        )
    else:
        print(
            "The received message signature is different from the original message hash."
        )
