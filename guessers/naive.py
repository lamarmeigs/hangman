import random
import string

from guessers.base import BaseGuesser


class RandomGuesser(BaseGuesser):
    """Randomly selects letters from the alphabet"""
    def __init__(self, *args, **kwargs):
        self.alphabet = list(string.ascii_lowercase)
        random.shuffle(self.alphabet)

    def guess(self):
        return self.alphabet.pop()


class OrderedRandomGuesser(BaseGuesser):
    """Randomly selects letters from the alphabet, starting with vowels"""
    def __init__(self, *args, **kwargs):
        vowels = list('aeiou')
        consonants = [l for l in string.ascii_lowercase if l not in vowels]
        random.shuffle(vowels)
        random.shuffle(consonants)
        self.alphabet = consonants + vowels

    def guess(self):
        return self.alphabet.pop()
