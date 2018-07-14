import random
import re

from guessers.base import BaseGuesser
from guessers.exc import TableFlipError


class BaseDerivedAlphabetGuesser(BaseGuesser):
    @staticmethod
    def _cull_words(word_length, potential_words):
        """Extract all words of a specific length from a list of words"""
        return [word for word in potential_words if len(word) == word_length]

    @staticmethod
    def _derive_alphabet(potential_words):
        """Extract all unique letters in the given list of words"""
        return set(''.join(potential_words))


class DerivedAlphabetGuesser(BaseDerivedAlphabetGuesser):
    """Restrict guesses to only letters in words of appropriate length"""
    def __init__(self, word_length, potential_words, *args, **kwargs):
        self.potential_words = self._cull_words(word_length, potential_words)
        self.alphabet = list(self._derive_alphabet(potential_words))
        random.shuffle(self.alphabet)

    def guess(self, *args, **kwargs):
        return self.alphabet.pop()


class OrderedDerivedAlphabetGuesser(DerivedAlphabetGuesser):
    """Guess only letters in words of appropriate length, starting with vowels."""
    def __init__(self, word_length, potential_words, *args, **kwargs):
        self.potential_words = self._cull_words(word_length, potential_words)
        alphabet = self._derive_alphabet(potential_words)
        vowels = set('aeiou').intersection(alphabet)
        consonants = set(alphabet).difference(vowels)

        vowels = list(vowels)
        consonants = list(consonants)

        random.shuffle(vowels)
        random.shuffle(consonants)
        self.alphabet = consonants + vowels


class RederivedAlphabetGuesser(BaseDerivedAlphabetGuesser):
    """Recompute the alphabet on each guess.

    Guesses are restricted to the unique letters of words that are of the
    appropriate and match all letters guessed so far.
    """
    def __init__(self, word_length, potential_words, *args, **kwargs):
        self.potential_words = self._cull_words(word_length, potential_words)

    def guess(self, guessed_word, *args, **kwargs):
        guess = None
        if len(self.potential_words) == 1:
            guess = self.potential_words[0][0]
            self.potential_words[0] = self.potential_words[1:]
        else:
            self.potential_words = self._match_words(guessed_word, self.potential_words)
            if not self.potential_words:
                raise TableFlipError('No possible solution found')
            self.alphabet = self._derive_alphabet(len(guessed_word))
            guess = random.choice(list(self.alphabet))
        return guess

    @staticmethod
    def _match_words(guessed_word, potential_words):
        """Extract words that match the pattern of the word guessed so far"""
        pattern = re.compile(guessed_word)
        return [word for word in potential_words if pattern.match(word)]