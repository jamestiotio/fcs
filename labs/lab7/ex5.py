#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 7 Part V
# James Raphael Tiovalen / 1004555

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from base64 import b64decode, b64encode
from rsa_utils import *
import secrets


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
    # Import data from file
    with open("mydata.txt", "r") as msg_file:
        data = msg_file.read().encode()
    public_key_filename = "public_key.pem"
    private_key_filename = "private_key.pem"

    # Perform secure version of RSA encryption
    encrypted_data = encrypt_RSA(public_key_filename, data)
    decrypted_data = decrypt_RSA(private_key_filename, encrypted_data)
    print(
        f"Original data: {data.decode()}\n\nEncrypted data: {encrypted_data.decode()}\n\nDecrypted data: {decrypted_data.decode()}\n"
    )

    # Perform secure version of message hash signing
    signature = sign_data(private_key_filename, data)
    verification_result = verify_sign(public_key_filename, signature, data)
    assert verification_result
    print(
        f"Signature: {signature}\n\nIs signature verified? {'Yes.' if verification_result else 'No.'}\n"
    )

    # Attempt another round of the RSA Encryption Protocol Attack
    chosen_integer = 100
    multiplier_value = 2
    print(f"Encrypting: {chosen_integer}\n")
    encrypted_integer = encrypt_RSA(
        public_key_filename, get_byte_from_int(chosen_integer)
    )
    print(f"Result: {encrypted_integer}\n")
    y_s = encrypt_RSA(public_key_filename, get_byte_from_int(multiplier_value))
    print(
        f"Multiplying the encryption result by the encrypted value of the multiplier factor {multiplier_value}, which is: {y_s}\n"
    )
    new_integer = get_byte_from_int(
        get_int_from_byte(encrypted_integer) * get_int_from_byte(y_s)
    )
    print(f"Modified to: {new_integer}\n")
    try:
        decrypted_integer = decrypt_RSA(private_key_filename, new_integer)
        if chosen_integer * multiplier_value == decrypted_integer:
            print(
                f"Successful attack with final modified integer: {decrypted_integer}\n"
            )
        else:
            print("Attack has failed. Decryption fails the built-in integrity check.\n")
    except ValueError:
        print("Attack has failed. Decryption fails the built-in integrity check.\n")

    random_signature = secrets.SystemRandom().randint(0, 2 ** 687)
    existential_message = encrypt_RSA(
        public_key_filename, get_byte_from_int(random_signature)
    )
    print(
        f"Random signature: {random_signature}\n\nMessage from signature: {existential_message}\n"
    )
    try:
        verification_result = verify_sign(
            public_key_filename,
            get_byte_from_int(random_signature),
            existential_message,
        )
        assert not verification_result
        if verification_result:
            print("Valid signature attack successful.")
        else:
            print("Attack has failed since signature verification has failed.")
    except Exception:
        print("Attack has failed since signature verification has failed.")
