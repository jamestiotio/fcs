#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 6 template
# Year 2021
# James Raphael Tiovalen / 1004555

import random


def square_multiply(a, x, n):
    y = 1
    for i in bin(x)[2:]:
        res = (res * res) % n
        if i == "1":
            res = (res * a) % n
    return res


def miller_rabin(n, a):
    pass


def gen_prime_nbits(n):
    pass


if __name__ == "__main__":
    print("Is 561 a prime?")
    print(miller_rabin(561, 2))
    print("Is 27 a prime?")
    print(miller_rabin(27, 2))
    print("Is 61 a prime?")
    print(miller_rabin(61, 2))

    print("Random number (100 bits):")
    print(gen_prime_nbits(100))
    print("Random number (80 bits):")
    print(gen_prime_nbits(80))
