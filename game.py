class CheaterError(Exception):
    """Exception raised when untowards behavior has been noticed"""
    pass


class Game:
    """Represents a single instance of a Hangman game"""

    def __init__(self, word, max_failures=8):
        self._word = word.lower()
        self.max_failures = max_failures
        self.correct_guesses = set()
        self.incorrect_guesses = set()

    @property
    def word(self):
        """Obscures unguessed letters from the word to be guessed"""
        return ''.join(
            letter if letter in self.correct_guesses else '.'
            for letter in self._word
        )

    @property
    def failure_count(self):
        return len(self.incorrect_guesses)

    @property
    def remaining_guess_count(self):
        return self.max_failures - self.failure_count

    @property
    def is_game_over(self):
        return self.has_won or not self.remaining_guess_count

    @property
    def has_won(self):
        return set(self._word) == self.correct_guesses

    def process_guess(self, letters):
        """Given a guessed letter, or collection of letters, update the state
        of the game.

        Args:
            letters (str): any letters the player is trying to guess

        Raises:
            CheaterError: if any of the letter surpass the number of allowable guesses
        """
        for letter in letters:
            if letter in self.correct_guesses.union(self.incorrect_guesses):
                continue

            if not self.remaining_guess_count:
                raise CheaterError(
                    'Attempt to make guesses after {} failures'.format(self.max_failures)
                )

            if letter in self._word:
                self.correct_guesses.add(letter)
            else:
                self.incorrect_guesses.add(letter)
