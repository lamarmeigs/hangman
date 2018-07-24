import markovify

from guessers.probability import FrequentLetterGuesser


class SingleStateMarkovGuesser(FrequentLetterGuesser):
    """Uses Markov chains to guess subsequent letters"""
    def __init__(self, word_length, potential_words, *args, **kwargs):
        super().__init__(word_length, potential_words, *args, **kwargs)
        self.markov_model = markovify.Chain(
            [list(word) for word in potential_words],
            state_size=1
        )
        self.alphabet = self._derive_alphabet(self.potential_words)

    def update_state(self, letter_match, guessed_word):
        super().update_state(letter_match, guessed_word)
        self.alphabet = self._derive_alphabet(self.potential_words)

    def guess(self, guessed_word, *args, **kwargs):
        guess = None

        # When only one potential word remains, return it
        if len(self.potential_words) == 1:
            return self.potential_words[0]

        # If the word's first letter hasn't been found, try guessing it
        elif guessed_word.startswith('.'):
            guess = self._select_most_frequent_follower(
                self.markov_model,
                (markovify.chain.BEGIN,)
            )

        # Otherwise, rely on the pre-computed Markov chains to select the most
        # likely letter following previously discovered letters
        else:
            letter_series = guessed_word.lstrip('.')[:guessed_word.lstrip('.').find('.')]
            guess = self._select_most_frequent_follower(
                self.markov_model,
                letter_series[-1]
            )

        return guess

    def _select_most_frequent_follower(self, chain, letter_series):
        """Return the letter that most frequently follows the given letter series.

        :param chain: a trained Markov model
        :type chain: markovify.Chain
        :param letter_series: a letter or string of letters
        :type letter_series: str
        :return: most frequent, unguessed letter following the letter series
        :rtype: str
        """
        potential_letter_frequency = (
            (letter, frequency)
            for letter, frequency in chain.model[tuple(letter_series)].items()
            if letter not in self.guesses and letter in self.alphabet
        )
        return sorted(
            potential_letter_frequency,
            key=lambda t: t[1],
            reverse=True
        )[0][0]
