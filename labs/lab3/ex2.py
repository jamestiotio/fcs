#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 3 Part II
# James Raphael Tiovalen / 1004555

import timeit
import os
import string
import hashlib
import itertools

ALPHANUMERIC_CHARSET = string.ascii_lowercase + string.digits

with open("hash5.txt", mode="r", encoding="utf-8", newline="\n") as input_file:
    hashes = input_file.read().splitlines()

def bruteforcer():
    output = []

    if not hashes:
        return

    # We go in-order to preserve hash-plaintext order equality in both input and output files (instead of just cracking whichever hashes are found first)
    # This might result in a longer time taken to crack all the 15 hashes (worst-case bruteforce scenario in terms of time complexity)
    for hash in hashes:
        for item in itertools.product(ALPHANUMERIC_CHARSET, repeat=5):
            guess = "".join(item)
            # Save in terms of function call overhead at the cost of less abstraction
            guess_hash = hashlib.md5(guess.encode()).hexdigest()
            if guess_hash == hash:
                output.append(guess)

    return output

def write_output_to_file():
    OUTPUT_FILENAME = "ex2_hash.txt"

    # Start from scratch
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

    output_lines = bruteforcer()

    # We should not benchmark the auxiliary file operations
    with open(OUTPUT_FILENAME, mode="w", encoding="utf-8", newline="\n") as output_file:
        output_file.writelines([f"{result}\n" for result in output_lines])

if __name__ == "__main__":
    number_of_iterations = 1
    time_spent = timeit.timeit(stmt="bruteforcer()", setup="from __main__ import bruteforcer", number=number_of_iterations)
    print(f"Average time spent per iteration through all 15 hashes: {time_spent/number_of_iterations:.2f} seconds.")
    # write_output_to_file()
