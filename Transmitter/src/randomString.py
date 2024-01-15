# Program to generate random words based on their length and number of them

import random
import string
import os
def gen_characters():
    return string.ascii_letters + string.digits + string.punctuation
def generate_string(length, characters):
    word = ""
    for i in range(length):
        word = word + random.choice(characters)
    return word

def write_to_file(word):
    f = open(file_path, "a")
    f.write(word + "\n")
    f.close()

numOfWords = 10
lengthOfWord = 10
file_path = r"Transmitter\dist\wordList.txt"

if os.path.getsize(file_path) > 0:
    with open(file_path, "w"):
        pass  # This leaves the file empty
characters = gen_characters()



for i in range(numOfWords):
    word = generate_string(lengthOfWord, characters)
    write_to_file(word)
    