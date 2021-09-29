#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 2 Part I
# Frequency analysis method to crack the cipher text for Part I
# James Raphael Tiovalen / 1004555

import requests
import secrets
import string

STORY_ENDPOINT_URL = "http://35.197.130.121/story"

# Given that the ciphertext is sufficiently long and assuming that the original plaintext message is in English language, we can utilize a frequency analysis attack to attempt to decrypt it
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

# Relative frequency taken from https://en.wikipedia.org/wiki/Letter_frequency
ENGLISH_LETTER_FREQ = {'E': 12.702, 'T': 9.056, 'A': 8.167, 'O': 7.507, 'I': 6.966, 'N': 6.749, 'S': 6.327, 'H': 6.094, 'R': 5.987, 'D': 4.253, 'L': 4.025, 'C': 2.782, 'U': 2.758, 'M': 2.406, 'W': 2.360, 'F': 2.228, 'G': 2.015, 'Y': 1.974, 'P': 1.929, 'B': 1.492, 'V': 0.978, 'K': 0.772, 'J': 0.153, 'X': 0.150, 'Q': 0.095, 'Z': 0.074}

def get_letter_count(message):
    """
    Returns a dictionary with keys of single letters and values of the count of how many times they appear in the message parameter.
    """
    letter_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    for letter in message.upper():
        if letter in ALPHABET:
            letter_count[letter] += 1
    
    return letter_count

def get_frequency_order(message):
    """
    Returns a string of the alphabet letters arranged in order of most frequently occurring in the message parameter.
    """

    # First, get a dictionary of each letter and its frequency count.
    letter_to_freq = get_letter_count(message)

    # Second, make a dictionary of each frequency count to each letter(s) with that frequency.
    freq_to_letter = {}
    for letter in ALPHABET:
        if letter_to_freq[letter] not in freq_to_letter:
            freq_to_letter[letter_to_freq[letter]] = [letter]
        else:
            freq_to_letter[letter_to_freq[letter]].append(letter)

    # Third, put each list of letters in reverse "ETAOIN" order, and then convert it to a string.
    for freq in freq_to_letter:
        freq_to_letter[freq].sort(key=ETAOIN.find, reverse=True)
        freq_to_letter[freq] = "".join(freq_to_letter[freq])

    # Fourth, convert the freqToLetter dictionary to a list of tuple pairs (key, value), then sort them.
    freq_pairs = list(freq_to_letter.items())
    freq_pairs.sort(key=lambda x: x[0], reverse=True)

    # Fifth, now that the letters are ordered by frequency, extract all the letters for the final string.
    freq_order = []
    for freq_pair in freq_pairs:
        freq_order.append(freq_pair[1])

    return "".join(freq_order)

def get_english_freq_match_score(message):
    """
    # Return the number of matches that the string in the message parameter has when its letter frequency is compared to English letter frequency. A "match" is how many of its six most frequent and six least frequent letters is among the six most frequent and six least frequent letters for English.
    """
    freq_order = get_frequency_order(message)

    match_score = 0

    # Find how many matches for the six most common letters there are.
    for common_letter in ETAOIN[:6]:
        if common_letter in freq_order[:6]:
            match_score += 1
    # Find how many matches for the six least common letters there are.
    for uncommon_letter in ETAOIN[-6:]:
        if uncommon_letter in freq_order[-6:]:
            match_score += 1

    return match_score

def first_naive_replacement_attempt(message):
    """
    Naively attempt to remap according to the standard English relative letter frequency order.
    """
    output = ""
    message_text_freq_order = get_frequency_order(message)
    naive_mapping = dict(list(zip(message_text_freq_order, ETAOIN)))

    for c in message:
        if c in ALPHABET:
            output += naive_mapping[c]
        else:
            output += c

    return output

if __name__ == "__main__":
    with open("story_cipher.txt", mode="r", encoding="utf-8", newline="\n") as fin:
        ciphertext = fin.read()

    print(f"ENGLISH FREQUENCY MATCH SCORE: {get_english_freq_match_score(ciphertext)}\n")

    # Additional manual remapping work needs to be done
    print(f"Naive remapping output:\n\n{first_naive_replacement_attempt(ciphertext)}")
