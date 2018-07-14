from guessers.base import BaseGuesser


class ManualGuesser(BaseGuesser):
    """Delegates all guesses to the user via an input prompt"""

    def guess(self, *args, **kwargs):
        return input('Guess: ').strip()
