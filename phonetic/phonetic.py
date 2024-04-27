from argparse import ArgumentParser
from pathlib import Path


alphabet = {
    'a': "Alfa",
    'b': "Bravo",
    'c': "Charlie",
    'd': "Delta",
    'e': "Echo",
    'f': "Foxtrot",
    'g': "Golf",
    'h': "Hotel",
    'i': "India",
    'j': "Juliett",
    'k': "Kilo",
    'l': "Lima",
    'm': "Mike",
    'n': "November",
    'o': "Oscar",
    'p': "Papa",
    'q': "Quebec",
    'r': "Romeo",
    's': "Sierra",
    't': "Tango",
    'u': "Uniform",
    'v': "Victor",
    'w': "Whiskey",
    'x': "X-ray",
    'y': "Yankee",
    'z': "Zulu",
}


parser = ArgumentParser()
parser.add_argument('words', nargs='*')
parser.add_argument('-f', '--filename')
args = parser.parse_args()


if args.filename:
    for line in Path(args.filename).read_text().splitlines():
        letter, word = line.split()
        alphabet[letter.lower()] = word


words = " ".join(args.words)
if not words:
    words = input("Text to spell out: ")
for char in words.lower():
    if char in alphabet:
        print(alphabet[char])
    elif char == ' ':
        print()