import abc


class BaseGuesser(abc.ABC):
    """Abstract base class defining the required structure for all guessers."""

    def __init__(self, *args, **kwargs):
        return

    @abc.abstractmethod
    def guess(self, *args, **kwargs):
        pass
