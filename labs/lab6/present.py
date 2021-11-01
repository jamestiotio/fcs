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
# Yet another method would be: [x for i in range(0, 4) for x in range(i, i + 64, 4)]
# Closed mathematical formula forms and sequence/series patterns are always preferable in terms of elegance and performance
inverted_pmt = [
    0,
    4,
    8,
    12,
    16,
    20,
    24,
    28,
    32,
    36,
    40,
    44,
    48,
    52,
    56,
    60,
    1,
    5,
    9,
    13,
    17,
    21,
    25,
    29,
    33,
    37,
    41,
    45,
    49,
    53,
    57,
    61,
    2,
    6,
    10,
    14,
    18,
    22,
    26,
    30,
    34,
    38,
    42,
    46,
    50,
    54,
    58,
    62,
    3,
    7,
    11,
    15,
    19,
    23,
    27,
    31,
    35,
    39,
    43,
    47,
    51,
    55,
    59,
    63,
]

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

    # Loop from right-most bit to left-most bit
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

    # Loop from right-most bit to left-most bit
    for i in range(64):
        # Select b_i
        bi = (state >> i) & mask
        # Find P(i)
        pi = inverted_pmt[i]
        # Assign bit b_i to original position P(i) of output
        output |= bi << pi

    return output


### WARNING: Extra random nonsense stuff just to optimize and speed up the cipher algorithm's processing time
### Create 256-bytes squared S-Box
larger_better_f4ster_stronger_beeg_sbox_lut = [
    0xCC,
    0xC5,
    0xC6,
    0xCB,
    0xC9,
    0xC0,
    0xCA,
    0xCD,
    0xC3,
    0xCE,
    0xCF,
    0xC8,
    0xC4,
    0xC7,
    0xC1,
    0xC2,
    0x5C,
    0x55,
    0x56,
    0x5B,
    0x59,
    0x50,
    0x5A,
    0x5D,
    0x53,
    0x5E,
    0x5F,
    0x58,
    0x54,
    0x57,
    0x51,
    0x52,
    0x6C,
    0x65,
    0x66,
    0x6B,
    0x69,
    0x60,
    0x6A,
    0x6D,
    0x63,
    0x6E,
    0x6F,
    0x68,
    0x64,
    0x67,
    0x61,
    0x62,
    0xBC,
    0xB5,
    0xB6,
    0xBB,
    0xB9,
    0xB0,
    0xBA,
    0xBD,
    0xB3,
    0xBE,
    0xBF,
    0xB8,
    0xB4,
    0xB7,
    0xB1,
    0xB2,
    0x9C,
    0x95,
    0x96,
    0x9B,
    0x99,
    0x90,
    0x9A,
    0x9D,
    0x93,
    0x9E,
    0x9F,
    0x98,
    0x94,
    0x97,
    0x91,
    0x92,
    0x0C,
    0x05,
    0x06,
    0x0B,
    0x09,
    0x00,
    0x0A,
    0x0D,
    0x03,
    0x0E,
    0x0F,
    0x08,
    0x04,
    0x07,
    0x01,
    0x02,
    0xAC,
    0xA5,
    0xA6,
    0xAB,
    0xA9,
    0xA0,
    0xAA,
    0xAD,
    0xA3,
    0xAE,
    0xAF,
    0xA8,
    0xA4,
    0xA7,
    0xA1,
    0xA2,
    0xDC,
    0xD5,
    0xD6,
    0xDB,
    0xD9,
    0xD0,
    0xDA,
    0xDD,
    0xD3,
    0xDE,
    0xDF,
    0xD8,
    0xD4,
    0xD7,
    0xD1,
    0xD2,
    0x3C,
    0x35,
    0x36,
    0x3B,
    0x39,
    0x30,
    0x3A,
    0x3D,
    0x33,
    0x3E,
    0x3F,
    0x38,
    0x34,
    0x37,
    0x31,
    0x32,
    0xEC,
    0xE5,
    0xE6,
    0xEB,
    0xE9,
    0xE0,
    0xEA,
    0xED,
    0xE3,
    0xEE,
    0xEF,
    0xE8,
    0xE4,
    0xE7,
    0xE1,
    0xE2,
    0xFC,
    0xF5,
    0xF6,
    0xFB,
    0xF9,
    0xF0,
    0xFA,
    0xFD,
    0xF3,
    0xFE,
    0xFF,
    0xF8,
    0xF4,
    0xF7,
    0xF1,
    0xF2,
    0x8C,
    0x85,
    0x86,
    0x8B,
    0x89,
    0x80,
    0x8A,
    0x8D,
    0x83,
    0x8E,
    0x8F,
    0x88,
    0x84,
    0x87,
    0x81,
    0x82,
    0x4C,
    0x45,
    0x46,
    0x4B,
    0x49,
    0x40,
    0x4A,
    0x4D,
    0x43,
    0x4E,
    0x4F,
    0x48,
    0x44,
    0x47,
    0x41,
    0x42,
    0x7C,
    0x75,
    0x76,
    0x7B,
    0x79,
    0x70,
    0x7A,
    0x7D,
    0x73,
    0x7E,
    0x7F,
    0x78,
    0x74,
    0x77,
    0x71,
    0x72,
    0x1C,
    0x15,
    0x16,
    0x1B,
    0x19,
    0x10,
    0x1A,
    0x1D,
    0x13,
    0x1E,
    0x1F,
    0x18,
    0x14,
    0x17,
    0x11,
    0x12,
    0x2C,
    0x25,
    0x26,
    0x2B,
    0x29,
    0x20,
    0x2A,
    0x2D,
    0x23,
    0x2E,
    0x2F,
    0x28,
    0x24,
    0x27,
    0x21,
    0x22,
]

larger_better_f4ster_stronger_beeg_sbox_inv_lut = [
    0x55,
    0x5E,
    0x5F,
    0x58,
    0x5C,
    0x51,
    0x52,
    0x5D,
    0x5B,
    0x54,
    0x56,
    0x53,
    0x50,
    0x57,
    0x59,
    0x5A,
    0xE5,
    0xEE,
    0xEF,
    0xE8,
    0xEC,
    0xE1,
    0xE2,
    0xED,
    0xEB,
    0xE4,
    0xE6,
    0xE3,
    0xE0,
    0xE7,
    0xE9,
    0xEA,
    0xF5,
    0xFE,
    0xFF,
    0xF8,
    0xFC,
    0xF1,
    0xF2,
    0xFD,
    0xFB,
    0xF4,
    0xF6,
    0xF3,
    0xF0,
    0xF7,
    0xF9,
    0xFA,
    0x85,
    0x8E,
    0x8F,
    0x88,
    0x8C,
    0x81,
    0x82,
    0x8D,
    0x8B,
    0x84,
    0x86,
    0x83,
    0x80,
    0x87,
    0x89,
    0x8A,
    0xC5,
    0xCE,
    0xCF,
    0xC8,
    0xCC,
    0xC1,
    0xC2,
    0xCD,
    0xCB,
    0xC4,
    0xC6,
    0xC3,
    0xC0,
    0xC7,
    0xC9,
    0xCA,
    0x15,
    0x1E,
    0x1F,
    0x18,
    0x1C,
    0x11,
    0x12,
    0x1D,
    0x1B,
    0x14,
    0x16,
    0x13,
    0x10,
    0x17,
    0x19,
    0x1A,
    0x25,
    0x2E,
    0x2F,
    0x28,
    0x2C,
    0x21,
    0x22,
    0x2D,
    0x2B,
    0x24,
    0x26,
    0x23,
    0x20,
    0x27,
    0x29,
    0x2A,
    0xD5,
    0xDE,
    0xDF,
    0xD8,
    0xDC,
    0xD1,
    0xD2,
    0xDD,
    0xDB,
    0xD4,
    0xD6,
    0xD3,
    0xD0,
    0xD7,
    0xD9,
    0xDA,
    0xB5,
    0xBE,
    0xBF,
    0xB8,
    0xBC,
    0xB1,
    0xB2,
    0xBD,
    0xBB,
    0xB4,
    0xB6,
    0xB3,
    0xB0,
    0xB7,
    0xB9,
    0xBA,
    0x45,
    0x4E,
    0x4F,
    0x48,
    0x4C,
    0x41,
    0x42,
    0x4D,
    0x4B,
    0x44,
    0x46,
    0x43,
    0x40,
    0x47,
    0x49,
    0x4A,
    0x65,
    0x6E,
    0x6F,
    0x68,
    0x6C,
    0x61,
    0x62,
    0x6D,
    0x6B,
    0x64,
    0x66,
    0x63,
    0x60,
    0x67,
    0x69,
    0x6A,
    0x35,
    0x3E,
    0x3F,
    0x38,
    0x3C,
    0x31,
    0x32,
    0x3D,
    0x3B,
    0x34,
    0x36,
    0x33,
    0x30,
    0x37,
    0x39,
    0x3A,
    0x05,
    0x0E,
    0x0F,
    0x08,
    0x0C,
    0x01,
    0x02,
    0x0D,
    0x0B,
    0x04,
    0x06,
    0x03,
    0x00,
    0x07,
    0x09,
    0x0A,
    0x75,
    0x7E,
    0x7F,
    0x78,
    0x7C,
    0x71,
    0x72,
    0x7D,
    0x7B,
    0x74,
    0x76,
    0x73,
    0x70,
    0x77,
    0x79,
    0x7A,
    0x95,
    0x9E,
    0x9F,
    0x98,
    0x9C,
    0x91,
    0x92,
    0x9D,
    0x9B,
    0x94,
    0x96,
    0x93,
    0x90,
    0x97,
    0x99,
    0x9A,
    0xA5,
    0xAE,
    0xAF,
    0xA8,
    0xAC,
    0xA1,
    0xA2,
    0xAD,
    0xAB,
    0xA4,
    0xA6,
    0xA3,
    0xA0,
    0xA7,
    0xA9,
    0xAA,
]


### I think this is the easiest way to speed up the S-Box, at least at this stage... (small brain moment)
### Any larger LUT size would be inconvenient for both disk space and physical memory (RAM) needed... :(
### Possible micro optimization in the future would be to implement polynomial factorization/reduction over the finite field GF(2^4) for the original PRESENT S-Box or matrix multiplication/inverse multiplication with affine mapping
### For more information on algebraic attacks and alternative PRESENT implementations:
### - https://bitbucket.org/malb/research-snippets/src/master/present.py
### - https://bitbucket.org/malb/research-snippets/src/master/present_bitslice.c
def turbo_boosted_jamestiotio_sBoxLayer(state):
    output = 0
    mask = 0xFF

    for i in range(8):
        x = (state >> (i * 8)) & mask
        sx = larger_better_f4ster_stronger_beeg_sbox_lut[x]
        output |= sx << (i * 8)

    return output


def turbo_boosted_jamestiotio_sBoxLayer_inv(state):
    output = 0
    mask = 0xFF

    for i in range(8):
        sx = (state >> (i * 8)) & mask
        x = larger_better_f4ster_stronger_beeg_sbox_inv_lut[sx]
        output |= x << (i * 8)

    return output


### Possible improvement: Use virtual butterfly/Benes/Omega-Flip network implementation instead of a normal, naive for loop to make the original pLayer much faster (logn cycles instead of n cycles)
### For more information: http://palms.ee.princeton.edu/PALMSopen/lee01efficient.pdf
### This implementation uses the GRP instruction (check PEX and PDEP as well) - we de-interleave the odd and even bits (Morton encoding/decoding)
### Avoid hitting the lookup tables at all (trace the bits)
### This is halfway/a middle ground between a naive for loop and a one-permutation-per-clock-period FPGA operation (big brain moment)
### I will be honest, I don't know why it's 2 instead of 4. But it works. Don't ask me why it works.
def turbo_boosted_jamestiotio_pLayer(state):
    output = state
    for _ in range(2):
        x = output
        y = output >> 1
        x &= 0x5555555555555555
        y &= 0x5555555555555555

        x = (x | (x >> 1)) & 0x3333333333333333
        x = (x | (x >> 2)) & 0x0F0F0F0F0F0F0F0F
        x = (x | (x >> 4)) & 0x00FF00FF00FF00FF
        x = (x | (x >> 8)) & 0x0000FFFF0000FFFF
        x = (x | (x >> 16)) & 0x00000000FFFFFFFF

        y = (y | (y >> 1)) & 0x3333333333333333
        y = (y | (y >> 2)) & 0x0F0F0F0F0F0F0F0F
        y = (y | (y >> 4)) & 0x00FF00FF00FF00FF
        y = (y | (y >> 8)) & 0x0000FFFF0000FFFF
        y = (y | (y >> 16)) & 0x00000000FFFFFFFF

        output = (y << 32) | x
    return output


### We interleave the odd and even bits back
def turbo_boosted_jamestiotio_pLayer_inv(state):
    output = state
    for _ in range(2):
        x = output & 0xFFFFFFFF
        y = (output & 0xFFFFFFFF00000000) >> 32

        x = (x | (x << 16)) & 0x0000FFFF0000FFFF
        x = (x | (x << 8)) & 0x00FF00FF00FF00FF
        x = (x | (x << 4)) & 0x0F0F0F0F0F0F0F0F
        x = (x | (x << 2)) & 0x3333333333333333
        x = (x | (x << 1)) & 0x5555555555555555

        y = (y | (y << 16)) & 0x0000FFFF0000FFFF
        y = (y | (y << 8)) & 0x00FF00FF00FF00FF
        y = (y | (y << 4)) & 0x0F0F0F0F0F0F0F0F
        y = (y | (y << 2)) & 0x3333333333333333
        y = (y | (y << 1)) & 0x5555555555555555

        output = x | (y << 1)
    return output


def present_round(state, roundKey):
    # One encryption round: addRoundKey() -> sBoxLayer() -> pLayer()
    state = addRoundKey(state, roundKey)
    # state = sBoxLayer(state)
    state = turbo_boosted_jamestiotio_sBoxLayer(state)
    # state = pLayer(state)
    state = turbo_boosted_jamestiotio_pLayer(state)
    return state


def present_inv_round(state, roundKey):
    # One decryption round: pLayer_inv() -> sBoxLayer_inv() -> addRoundKey()
    # state = pLayer_inv(state)
    state = turbo_boosted_jamestiotio_pLayer_inv(state)
    # state = sBoxLayer_inv(state)
    state = turbo_boosted_jamestiotio_sBoxLayer_inv(state)
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
