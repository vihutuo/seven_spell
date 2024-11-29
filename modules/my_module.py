import random
import csv
import random
from itertools import permutations

def ShuffleString(s):
    L1 = list(s)
    random.shuffle(L1)
    return "".join(L1)


def ReadCSV(filename):
    with open(filename, mode='r') as file:
        csvFile = list(csv.reader(file))
    return csvFile


def GetRandomWord(file_name):
    with open(file_name, "r") as f:
        L1 = f.read().splitlines()
    print(len(L1))
    return random.choice(L1)


def GetAllWords(file_name):
    with open(file_name, "r") as f:
        L1 = f.read().upper().splitlines()
    return L1

def generate_valid_words(letters, word_set, min_length=3):
    # List to store valid words
    valid_words = []

    # Iterate over all possible word lengths
    for length in range(min_length, len(letters) + 1):
        for perm in permutations(letters, length):
            candidate_word = ''.join(perm)
            if candidate_word in word_set:
                valid_words.append(candidate_word)  # Add valid word to the list

    return valid_words  # Return the list of valid words