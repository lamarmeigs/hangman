from unittest import TestCase

import guessers


class GuessersTestCase(TestCase):
    def test_interface(self):
        self.assertIs(guessers.ManualGuesser, guessers.manual.ManualGuesser)
