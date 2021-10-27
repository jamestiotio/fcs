#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 6 Template
# Year 2021
# James Raphael Tiovalen / 1004555

from math import sqrt, ceil
import primes


def baby_step(alpha, beta, p, fname="baby.txt"):
    m = ceil(sqrt(p - 1))
    with open(fname, "w") as fout:
        for i in range(m):
            result = (primes.square_multiply(alpha, i, p) * beta) % p
            fout.write(str(result) + "\n")


def giant_step(alpha, p, fname="giant.txt"):
    m = ceil(sqrt(p - 1))
    with open(fname, "w") as fout:
        for i in range(m):
            result = primes.square_multiply(alpha, m * i, p)
            fout.write(str(result) + "\n")


# An algorithm to solve the discrete logarithm problem
def baby_giant(alpha, beta, p):
    m = ceil(sqrt(p - 1))
    baby_step(alpha, beta, p)
    giant_step(alpha, p)

    baby_lookup = {}
    with open("baby.txt", "r") as baby_file:
        index = 0
        for line in baby_file:
            baby_lookup[line] = int(index)
            index += 1

    with open("giant.txt", "r") as giant_file:
        x_g = 0
        for candidate in giant_file:
            if candidate in baby_lookup:
                # Get the first collision
                x_b = baby_lookup.get(candidate)
                # This will close the file automatically as well
                return (x_g * m) - x_b
            else:
                x_g += 1


if __name__ == "__main__":
    """
    Test 1
    My private key is: 264
    Test other private key is: 7265
    """
    p = 17851
    alpha = 17511
    A = 2945
    B = 11844
    sharedkey = 1671
    a = baby_giant(alpha, A, p)
    b = baby_giant(alpha, B, p)
    guesskey1 = primes.square_multiply(A, b, p)
    guesskey2 = primes.square_multiply(B, a, p)
    print("Guess key 1:", guesskey1)
    print("Guess key 2:", guesskey2)
    print("Actual shared key:", sharedkey)
