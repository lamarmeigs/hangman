from collections import defaultdict

from guessers.derived import RederivedAlphabetGuesser
from guessers.exc import TableFlipError


class FrequentLetterGuesser(RederivedAlphabetGuesser):
    """Guess the most frequent letter in words of the appropriate length"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.correct_guesses = set()

    @property
    def guesses(self):
        return self.correct_guesses.union(self.incorrect_guesses)

    def update_state(self, letter_match):
        """Record all guesses"""
        for letter, is_correct in letter_match.items():
            if is_correct:
                self.correct_guesses.add(letter)
            else:
                self.incorrect_guesses.add(letter)

    def guess(self, guessed_word, *args, **kwargs):
        guess = None
        if len(self.potential_words) == 1:
            guess = self.potential_words[0][0]
            self.potential_words[0] = self.potential_words[0][1:]
        else:
            self.potential_words = self._cull_words(
                len(guessed_word),
                self.potential_words,
                self.incorrect_guesses,
            )
            guess = self._select_most_frequent_letter(self.potential_words)
        return guess

    def _select_most_frequent_letter(self, potential_words):
        """Select most frequent unguessed letter in the given words.

        Args:
            potential words (list of str): an iterable of words

        Return:
            str

        Raise:
            TableFlipError: if all letters have been guessed previously
        """
        letter_counts = defaultdict(int)
        for word in potential_words:
            for letter in word:
                if letter not in self.guesses:
                    letter_counts[letter] += 1
        if not letter_counts:
            raise TableFlipError('No possible solution found')
        return sorted(list(letter_counts.items()), key=lambda t: t[1], reverse=True)[0][0]