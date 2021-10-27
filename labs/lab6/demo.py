#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 6 Year 2021
# Cracking demo code file
# James Raphael Tiovalen / 1004555

import numpy as np
from scipy.optimize import curve_fit
from sklearn import metrics
import csv
import time
import primes
import dhke
import babygiant
import math


def crack(filename):
    with open(filename, "w") as csv_file:
        writer = csv.writer(
            csv_file,
            delimiter=",",
            lineterminator="\n",
            quoting=csv.QUOTE_NONE,
            escapechar="\\",
        )

        # Write CSV headers
        writer.writerow(["key_length", "time_taken"])

        # We start cracking from 16 bits onwards
        # (MemoryError encountered with key length of 53 bits onwards...)
        for i in range(16, 81):
            try:
                while True:
                    p, alpha = dhke.dhke_setup(i)
                    a = dhke.gen_priv_key(p)
                    b = dhke.gen_priv_key(p)
                    A = dhke.get_pub_key(alpha, a, p)
                    B = dhke.get_pub_key(alpha, b, p)
                    shared_key = dhke.get_shared_key(B, a, p)

                    if shared_key.bit_length() == i:
                        break

                # Actual cracking starts here proper
                start_time = time.perf_counter()
                a = babygiant.baby_giant(alpha, A, p)
                b = babygiant.baby_giant(alpha, B, p)
                guesskey1 = primes.square_multiply(A, b, p)
                guesskey2 = primes.square_multiply(B, a, p)

                if guesskey1 == shared_key or guesskey2 == shared_key:
                    end_time = time.perf_counter()
                    writer.writerow([i, end_time - start_time])
                    print(
                        f"Cracked key of length {i} in {end_time - start_time} seconds."
                    )

            except KeyboardInterrupt:
                csv_file.close()
                print(
                    "\nCracking process was interrupted, gracefully breaking and saving progress..."
                )
                break


# Define general exponential function
def exponential(nb, a, b):
    return a * np.exp(nb) + b


# Assume that relationship between cracking time and key length is exponential
def get_safe_key_length(filename):
    # Read data from CSV and parse as data points
    key_length, time_taken = np.genfromtxt(
        "result.csv", delimiter=",", skip_header=1, dtype=np.float64, unpack=True
    )
    # Perform exponential regression
    popt, pcov = curve_fit(exponential, key_length, time_taken, method="lm")
    # Get curve-fitting metrics
    r_squared = round(metrics.r2_score(exponential(key_length, *popt), time_taken), 10)
    print(f"Equation: t = {popt[0]} * e^(nb) + {popt[1]}")
    print(f"R^2 = {r_squared}")
    # Get the key length with reasonable security, in terms of time taken to crack (about a millennium with local computational resources)
    target_time = 32_000_000_000
    desired_key_length = math.ceil(np.log((target_time - popt[1]) / popt[0]))
    print(f"Potentially secure key length: {desired_key_length} bits.")


if __name__ == "__main__":
    filename = "result.csv"
    # crack(filename)
    get_safe_key_length(filename)
