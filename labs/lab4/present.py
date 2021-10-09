#!/usr/bin/env python3
# PRESENT skeleton file for SUTD 50.042 FCS Lab 4
# James Raphael Tiovalen / 1004555


# constants
FULLROUND = 31

# S-Box Layer
sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

# Inverted S-Box Layer
# We pre-establish and use lookup table to allow O(1) time complexity, instead of O(n) by alternatively calling .index()
# This is okay since nowadays, we are not limited so much by memory space anymore (and the size of the lookup table is small enough anyway)
# Another method would be: [sbox.index(i) for i in range(16)]
inverted_sbox = [
    0x5,
    0xE,
    0xF,
    0x8,
    0xC,
    0x1,
    0x2,
    0xD,
    0xB,
    0x4,
    0x6,
    0x3,
    0x0,
    0x7,
    0x9,
    0xA,
]

# PLayer
pmt = [
    0,
    16,
    32,
    48,
    1,
    17,
    33,
    49,
    2,
    18,
    34,
    50,
    3,
    19,
    35,
    51,
    4,
    20,
    36,
    52,
    5,
    21,
    37,
    53,
    6,
    22,
    38,
    54,
    7,
    23,
    39,
    55,
    8,
    24,
    40,
    56,
    9,
    25,
    41,
    57,
    10,
    26,
    42,
    58,
    11,
    27,
    43,
    59,
    12,
    28,
    44,
    60,
    13,
    29,
    45,
    61,
    14,
    30,
    46,
    62,
    15,
    31,
    47,
    63,
]

# Inverted pLayer
# Another way would be: [pmt.index(i) for i in range(64)]
# Closed mathematical formula forms and sequence/series patterns are always preferable in terms of elegance and performance
inverted_pmt = [x for i in range(0, 4) for x in range(i, i + 64, 4)]

# Rotate left: 0b1001 --> 0b0011
def rol(val, r_bits, max_bits):
    return (val << r_bits % max_bits) & (2 ** max_bits - 1) | (
        (val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits))
    )


# Rotate right: 0b1001 --> 0b1100
def ror(val, r_bits, max_bits):
    return ((val & (2 ** max_bits - 1)) >> r_bits % max_bits) | (
        val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1)
    )


def genRoundKeys(key):
    # Hardcoded hotfix for 0th key
    round_keys = [32]
    # Copy the original user-supplied input key
    key_register = key

    # Loop through all rounds
    for round_counter in range(1, FULLROUND + 2):
        # Extract 64 leftmost bits and add round key to master key list
        round_keys.append(key_register >> 16)
        # Step 1 (rotate by 61 bit positions to the left is equivalent to rotate by 19 bit positions to the right)
        key_register = ror(key_register, 19, 80)
        # Step 2
        key_register = (sbox[key_register >> 76] << 76) | (key_register % (2 ** 76))
        # Step 3
        key_register ^= round_counter << 15

    return round_keys


# This function is fully invertible (reusable without any modifications)
def addRoundKey(state, Ki):
    return state ^ Ki


# For best practice, we do not modify original inputs at all
# Work in the realm of binary bits using much faster bitwise operations (instead of converting to integers, strings, or hexadecimal representations)
def sBoxLayer(state):
    output = 0
    # Define mask to select word from state
    mask = 0xF

    # Loop from right-most word to left-most word
    for i in range(16):
        # Select w_i
        x = (state >> (i * 4)) & mask
        # Find S[w_i], the corresponding substitution value from S-Box
        sx = sbox[x]
        # Add S[w_i] to output
        output |= sx << (i * 4)

    return output


def pLayer(state):
    output = 0
    # Define mask to select bit from state
    mask = 0x1

    # Loop from right-most word to left-most bit
    for i in range(64):
        # Select b_i
        bi = (state >> i) & mask
        # Find P(i)
        pi = pmt[i]
        # Assign bit b_i to new position P(i) of output
        output |= bi << pi

    return output


def sBoxLayer_inv(state):
    output = 0
    # Define mask to select word from state
    mask = 0xF

    # Loop from right-most word to left-most word
    for i in range(16):
        # Select S[w_i]
        sx = (state >> (i * 4)) & mask
        # Find w_i, the corresponding substitution value from inverted S-Box
        x = inverted_sbox[sx]
        # Add w_i to output
        output |= x << (i * 4)

    return output


def pLayer_inv(state):
    output = 0
    # Define mask to select bit from state
    mask = 0x1

    # Loop from right-most word to left-most bit
    for i in range(64):
        # Select b_i
        bi = (state >> i) & mask
        # Find P(i)
        pi = inverted_pmt[i]
        # Assign bit b_i to original position P(i) of output
        output |= bi << pi

    return output


def present_round(state, roundKey):
    # One encryption round: addRoundKey() -> sBoxLayer() -> pLayer()
    state = addRoundKey(state, roundKey)
    state = sBoxLayer(state)
    state = pLayer(state)
    return state


def present_inv_round(state, roundKey):
    # One decryption round: pLayer_inv() -> sBoxLayer_inv() -> addRoundKey()
    state = pLayer_inv(state)
    state = sBoxLayer_inv(state)
    state = addRoundKey(state, roundKey)
    return state


def present(plain, key):
    K = genRoundKeys(key)
    state = plain
    for i in range(1, FULLROUND + 1):
        state = present_round(state, K[i])
    state = addRoundKey(state, K[32])
    return state


def present_inv(cipher, key):
    K = genRoundKeys(key)
    state = cipher
    state = addRoundKey(state, K[32])
    for i in range(FULLROUND, 0, -1):
        state = present_inv_round(state, K[i])
    return state


if __name__ == "__main__":
    # Test vector for key schedule
    key1 = 0x00000000000000000000
    keys = genRoundKeys(key1)
    # The 0th-index "key" is there to show that there are 32 cases
    # First key to actually be used starts from index 1
    keysTest = {
        0: 32,
        1: 0,
        2: 13835058055282163712,
        3: 5764633911313301505,
        4: 6917540022807691265,
        5: 12682149744835821666,
        6: 10376317730742599722,
        7: 442003720503347,
        8: 11529390968771969115,
        9: 14988212656689645132,
        10: 3459180129660437124,
        11: 16147979721148203861,
        12: 17296668118696855021,
        13: 9227134571072480414,
        14: 4618353464114686070,
        15: 8183717834812044671,
        16: 1198465691292819143,
        17: 2366045755749583272,
        18: 13941741584329639728,
        19: 14494474964360714113,
        20: 7646225019617799193,
        21: 13645358504996018922,
        22: 554074333738726254,
        23: 4786096007684651070,
        24: 4741631033305121237,
        25: 17717416268623621775,
        26: 3100551030501750445,
        27: 9708113044954383277,
        28: 10149619148849421687,
        29: 2165863751534438555,
        30: 15021127369453955789,
        31: 10061738721142127305,
        32: 7902464346767349504,
    }
    for k in keysTest.keys():
        assert keysTest[k] == keys[k]

    # Test vectors for single rounds without key scheduling
    plain1 = 0x0000000000000000
    key1 = 0x00000000000000000000
    round1 = present_round(plain1, key1)
    round11 = 0xFFFFFFFF00000000
    assert round1 == round11

    round2 = present_round(round1, key1)
    round22 = 0xFF00FFFF000000
    assert round2 == round22

    round3 = present_round(round2, key1)
    round33 = 0xCC3FCC3F33C00000
    assert round3 == round33

    # Invert single rounds
    plain11 = present_inv_round(round1, key1)
    assert plain1 == plain11
    plain22 = present_inv_round(round2, key1)
    assert round1 == plain22
    plain33 = present_inv_round(round3, key1)
    assert round2 == plain33

    # Everything together
    plain1 = 0x0000000000000000
    key1 = 0x00000000000000000000
    cipher1 = present(plain1, key1)
    plain11 = present_inv(cipher1, key1)
    assert plain1 == plain11

    plain2 = 0x0000000000000000
    key2 = 0xFFFFFFFFFFFFFFFFFFFF
    cipher2 = present(plain2, key2)
    plain22 = present_inv(cipher2, key2)
    assert plain2 == plain22

    plain3 = 0xFFFFFFFFFFFFFFFF
    key3 = 0x00000000000000000000
    cipher3 = present(plain3, key3)
    plain33 = present_inv(cipher3, key3)
    assert plain3 == plain33

    plain4 = 0xFFFFFFFFFFFFFFFF
    key4 = 0xFFFFFFFFFFFFFFFFFFFF
    cipher4 = present(plain4, key4)
    plain44 = present_inv(cipher4, key4)
    assert plain4 == plain44
