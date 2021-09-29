#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 2 Part I
# Genetic algorithm method to crack the cipher text for Part I
# James Raphael Tiovalen / 1004555

import requests
import secrets
import string

STORY_ENDPOINT_URL = "http://35.197.130.121/story"
POP_SIZE = 26
FITNESS_REQUIREMENT = 0
GENERATIONS = 64

# Initialize initial "guess"/individual candidate solution
with open("story_cipher.txt", mode="r", encoding="utf-8", newline="\n") as fin:
    current_guess = fin.read()

ORIGINAL_CIPHERTEXT = current_guess
CHARSET_CONSIDERED = string.printable[36:62]
DNA_SIZE = len(ORIGINAL_CIPHERTEXT)


def get_random_char():
    return secrets.choice(CHARSET_CONSIDERED)


def mutate(dna):
    dna_out = dna
    x = get_random_char()
    y = get_random_char()
    while (x == y) or (x not in dna_out):
        x = get_random_char()
        y = get_random_char()
    dna_out.replace(x, y)
    return dna_out


# This assumes that the original ciphertext has all of the characters available in the charset
def swap(dna):
    dna_out = ""
    first_char_to_swap = get_random_char()
    second_char_to_swap = get_random_char()
    while (first_char_to_swap == second_char_to_swap) or (first_char_to_swap not in dna) or (second_char_to_swap not in dna):
        first_char_to_swap = get_random_char()
        second_char_to_swap = get_random_char()
    for c in dna:
        if c == first_char_to_swap:
            dna_out += second_char_to_swap
        elif c == second_char_to_swap:
            dna_out += first_char_to_swap
        else:
            dna_out += c
    return dna_out


# Generate mutations, starting from the fittest (to maintain overall structure/rigidity)
def generate_population(fittest):
    pop = []
    pop.append(fittest)
    for _ in range(POP_SIZE - 1):
        new_individual = swap(fittest)
        pop.append(new_individual)
    return pop


# Define function to get "fitness" measure
def get_fitness(candidate):
    solution = str(candidate).lower().strip()
    data = {"solution": solution}
    r = requests.post(STORY_ENDPOINT_URL, json=data).json()
    return int(r["distance"])


def get_fittest(population):
    fittest_string = population[0]
    minimum_fitness = get_fitness(population[0])

    for individual in population:
        ind_fitness = get_fitness(individual)
        if ind_fitness < minimum_fitness:
            fittest_string = individual
            minimum_fitness = ind_fitness

    return (fittest_string, minimum_fitness)


if __name__ == "__main__":
    generation_count = 0
    population = generate_population(current_guess)

    for _ in range(GENERATIONS):
        generation_count += 1
        print("Generation: " + f"{generation_count}")
        current_fittest, temp_min_fitness = get_fittest(population)
        print(f"Current Minimum Fitness: {temp_min_fitness}")
        population = generate_population(current_fittest)
        print("")

    fittest_string, minimum_fitness = get_fittest(population)

    # Try to compensate for missing characters
    if minimum_fitness > FITNESS_REQUIREMENT:
        chars_not_in_ciphertext = set(CHARSET_CONSIDERED) - set(ORIGINAL_CIPHERTEXT)
        # If only one character is missing, we can attempt to replace it by bruteforce
        if len(chars_not_in_ciphertext) == 1:
            print("Attempting to fix/replace a single character missing in the original ciphertext... Please wait patiently!")
            print("")
            target_char = chars_not_in_ciphertext.pop()
            while minimum_fitness > FITNESS_REQUIREMENT:
                rand_char = get_random_char()
                while rand_char not in fittest_string:
                    rand_char = get_random_char()
                modified_string = fittest_string.replace(rand_char, target_char)
                temp_fitness = get_fitness(modified_string)
                if temp_fitness < minimum_fitness:
                    fittest_string = modified_string
                    minimum_fitness = temp_fitness
        else:
            print("The optimal string is not within standard. Please conduct additional manual analysis due to missing characters in the original ciphertext!")

    # Additional manual analysis might be needed since the original ciphertext might have missing characters
    print(f"Optimal String:\n\n{fittest_string}")
