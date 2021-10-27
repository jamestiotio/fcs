#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 6 template
# Year 2021
# James Raphael Tiovalen / 1004555

import primes
import secrets

# Import lab 4 code materials
import ecb


def dhke_setup(nb):
    # Prime number nearest/closest to 2**80
    # p = 1208925819614629174706189
    p = primes.gen_prime_nbits(nb)
    # Get generator
    alpha = secrets.SystemRandom().randint(2, p - 2)
    return p, alpha


def gen_priv_key(p):
    return secrets.SystemRandom().randint(2, p - 2)


def get_pub_key(alpha, a, p):
    # (alpha ** a) % p
    return primes.square_multiply(alpha, a, p)


def get_shared_key(keypub, keypriv, p):
    # (keypub ** keypriv) % p
    return primes.square_multiply(keypub, keypriv, p)


if __name__ == "__main__":
    p, alpha = dhke_setup(80)
    print("Generate P and alpha:")
    print("P:", p)
    print("alpha:", alpha)
    print()
    a = gen_priv_key(p)
    b = gen_priv_key(p)
    print("My private key is:", a)
    print("Test other private key is:", b)
    print()
    A = get_pub_key(alpha, a, p)
    B = get_pub_key(alpha, b, p)
    print("My public key is:", A)
    print("Test other public key is:", B)
    print()
    sharedKeyA = get_shared_key(B, a, p)
    sharedKeyB = get_shared_key(A, b, p)
    print("My shared key is:", sharedKeyA)
    print("Test other shared key is:", sharedKeyB)
    print("Length of key is %d bits." % sharedKeyA.bit_length())

    # DHKE protocol key exchange demonstration using PRESENT cipher encryption
    while True:
        print("Negotiating shared key of length 80...")
        p, alpha = dhke_setup(80)
        sender_private_key = gen_priv_key(p)
        sender_public_key = get_pub_key(alpha, sender_private_key, p)

        rcvr_private_key = gen_priv_key(p)
        rcvr_public_key = get_pub_key(alpha, rcvr_private_key, p)

        sender_shared_key = get_shared_key(rcvr_public_key, sender_private_key, p)
        rcvr_shared_key = get_shared_key(sender_public_key, rcvr_private_key, p)
        assert sender_shared_key == rcvr_shared_key

        # Ensure that generated key is of length 80 bits
        if sender_shared_key.bit_length() == 80:
            print("Negotiation successful!\n")
            break

    print("###### Performing Key Exchange ######")
    print("Sender private key:", sender_private_key)
    print("Sender public key:", sender_public_key)
    print("Receiver private key:", rcvr_private_key)
    print("Receiver public key:", rcvr_public_key)
    print("Shared key given by:", rcvr_shared_key, "===", sender_shared_key)
    print()

    print("###### Entering Encryption Stage ######")

    with open("message_to_send.txt", "r") as fin1:
        plaintext_message_sender = fin1.read()
    print("Sender plaintext file:", plaintext_message_sender)
    ecb.ecb("message_to_send.txt", "encrypted_message.enc", sender_shared_key, "e")
    print("Encrypted file generated: encrypted_message.enc")
    print()
    print(
        "Simulating transmission of encrypted message over to receiver (assuming no data transmission errors)..."
    )
    print()

    print("###### Entering Decryption Stage ######")
    ecb.ecb("encrypted_message.enc", "decrypted_message.txt", rcvr_shared_key, "d")
    print("Decrypted file generated: decrypted_message.txt")
    with open("decrypted_message.txt", "r") as fin2:
        plaintext_message_receiver = fin2.read()
    print("Receiver plaintext file:", plaintext_message_receiver)

    # Ensure that receiver's message is the same as sender's message
    assert plaintext_message_sender == plaintext_message_receiver
    if plaintext_message_sender == plaintext_message_receiver:
        print(
            "Sender's plaintext message is the same as receiver's plaintext message. Data transfer successful!"
        )
    else:
        print(
            "Sender's plaintext message is different compared to receiver's plaintext message. Data transfer failed!"
        )
