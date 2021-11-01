#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 6 Template
# Year 2021
# James Raphael Tiovalen / 1004555

import secrets


def square_multiply(a, x, n):
    res = 1
    for i in bin(x)[2:]:
        res = (res * res) % n
        if i == "1":
            res = (a * res) % n
    return res


# Algorithm that determines whether a given number is prime or not
def miller_rabin(n, a):
    # Base cases
    if n < 2:
        return False

    if n == 2 or n == 3 or n == 5:
        return True

    if n % 2 == 0:
        return False

    # Find d and r
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Use a probabilistic/non-deterministic variant, which is much faster in terms of time complexity
    # WitnessLoop
    for _ in range(a):
        rng_int = secrets.SystemRandom().randint(2, n - 2)
        x = square_multiply(rng_int, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = square_multiply(x, 2, n)
            if x == n - 1:
                break

        # No break
        else:
            # Composite number
            return False

    # Probably prime number
    return True


def gen_prime_nbits(n):
    while True:
        # Generate random bits of length n
        candidate = secrets.SystemRandom().getrandbits(n)
        # Ensure that the candidate is odd and that proper n bits are generated
        lb_mask = 1
        fb_mask = 1 << n - 1
        candidate = candidate | lb_mask | fb_mask
        # Rationale: https://stackoverflow.com/a/6330138
        if miller_rabin(candidate, 40):
            return candidate


if __name__ == "__main__":
    print("Is 561 a prime?")
    print(miller_rabin(561, 2))
    assert miller_rabin(561, 2) == False
    print("Is 27 a prime?")
    print(miller_rabin(27, 2))
    assert miller_rabin(27, 2) == False
    print("Is 61 a prime?")
    print(miller_rabin(61, 2))
    assert miller_rabin(61, 2) == True

    print("Random number (100 bits):")
    print(gen_prime_nbits(100))
    print("Random number (80 bits):")
    print(gen_prime_nbits(80))
