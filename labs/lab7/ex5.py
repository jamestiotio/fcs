#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 7 Part V
# James Raphael Tiovalen / 1004555

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from base64 import b64decode, b64encode


def generate_RSA(bits=1024):
    key = RSA.generate(bits)
    private_key = key.export_key("PEM")
    public_key = key.public_key().export_key("PEM")
    with open("private_key.pem", "wb") as private_key_file, open(
        "public_key.pem", "wb"
    ) as public_key_file:
        private_key_file.write(private_key)
        public_key_file.write(public_key)


def encrypt_RSA(public_key_file, message):
    with open(public_key_file, "r") as file:
        rsa_pubkey = RSA.import_key(file.read())
    cipher = PKCS1_OAEP.new(rsa_pubkey)
    ciphertext = b64encode(cipher.encrypt(message))
    return ciphertext


def decrypt_RSA(private_key_file, cipher):
    with open(private_key_file, "r") as file:
        rsa_privkey = RSA.import_key(file.read())
    decipher = PKCS1_OAEP.new(rsa_privkey)
    plaintext = decipher.decrypt(b64decode(cipher))
    return plaintext


def sign_data(private_key_file, data):
    with open(private_key_file, "r") as file:
        rsa_privkey = RSA.import_key(file.read())
    cipher = PKCS1_PSS.new(rsa_privkey)
    hashed_message = SHA256.new(data)
    signature = b64encode(cipher.sign(hashed_message))
    return signature


def verify_sign(public_key_file, sign, data):
    with open(public_key_file, "r") as file:
        rsa_pubkey = RSA.import_key(file.read())
    verifier = PKCS1_PSS.new(rsa_pubkey)
    hashed_message = SHA256.new(data)
    return verifier.verify(hashed_message, b64decode(sign))


if __name__ == "__main__":
    # Generate new RSA keys
    generate_RSA()
    # Import data, private key, and public key from files
    with open("mydata.txt", "r") as msg_file:
        data = msg_file.read()
    with open("public_key.pem", "r") as pubkey_file:
        pubkey = RSA.import_key(pubkey_file.read())
    with open("private_key.pem", "r") as privkey_file:
        privkey = RSA.import_key(privkey_file.read())

    # Perform secure version of RSA encryption

    # Attempt another round of the RSA Encryption Protocol Attack
