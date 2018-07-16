import abc


class BaseGuesser(abc.ABC):
    """Abstract base class defining the required structure for all guessers."""

    def __init__(self, *args, **kwargs):
        return

    @abc.abstractmethod
    def guess(self, *args, **kwargs):
        """Return a letter to match against a game's word"""
        pass

    def update_state(self, letter_match):
        """Update any internal guesser state to make future guesses more accurate"""
        pass
