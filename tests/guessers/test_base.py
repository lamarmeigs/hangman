from unittest import TestCase

from guessers.base import BaseGuesser


class BaseGuesserTestCase(TestCase):
    def test_guess_is_abstract(self):
        class UnfinishedGuesser(BaseGuesser):
            pass

        with self.assertRaises(TypeError):
            UnfinishedGuesser()
