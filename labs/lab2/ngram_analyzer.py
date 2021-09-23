#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 2
# N-gram frequency analysis helper
# James Raphael Tiovalen / 1004555

import nltk

with open("story_cipher.txt", mode="r", encoding="utf-8", newline="\n") as fin:
    ciphertext = fin.read()

for n in range(2, 4):
    print(f"N: {n}")
    grams = nltk.ngrams(ciphertext.split(), n)
    fdist = nltk.FreqDist(grams)
    descending_fdist = sorted(fdist.items(), key=lambda x: x[1], reverse=True)
    for k, v in descending_fdist:
        print("Ngram: " + str(k) + ", Count: " + str(v))
    print("")
