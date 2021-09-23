#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 2
# Genetic algorithm method to crack the cipher text for Part I
# James Raphael Tiovalen / 1004555

import requests
import secrets
import string

STORY_ENDPOINT_URL = "http://35.197.130.121/story"
POP_SIZE = 26
FITNESS_REQUIREMENT = 0
GENERATIONS = 50

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

# Initialize initial "guess"/individual candidate solution
with open("story_cipher.txt", mode="r", encoding="utf-8", newline="\n") as fin:
    current_guess = fin.read()

DNA_SIZE = len(current_guess)


def get_random_char():
    return secrets.choice(string.printable[36:62])


def mutate(dna):
    dna_out = dna
    dna_out.replace(get_random_char(), get_random_char())
    return dna_out


def swap(dna):
    dna_out = ""
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
        if ind_fitness <= minimum_fitness:
            fittest_string = individual
            minimum_fitness = ind_fitness

    return (fittest_string, minimum_fitness)


if __name__ == "__main__":
    generation_count = 0
    population = generate_population(current_guess)

    for _ in range(GENERATIONS):
        generation_count += 1
        print("Generation: " + f"{generation_count}")
        current_fittest, temp_min_fitness = get_fittest(population[0])
        print(f"Current Minimum Fitness: {temp_min_fitness}")
        population = generate_population(current_fittest)

    fittest_string, minimum_fitness = get_fittest(population)

    print(f"Optimal String:\n\n{fittest_string}")
