from unittest import TestCase

import guessers


class GuessersTestCase(TestCase):
    def test_interface(self):
        self.assertIs(guessers.TableFlipError, guessers.exc.TableFlipError)
        self.assertIs(guessers.ManualGuesser, guessers.manual.ManualGuesser)
        self.assertIs(
            guessers.OrderedRandomGuesser,
            guessers.naive.OrderedRandomGuesser
        )
        self.assertIs(guessers.RandomGuesser, guessers.naive.RandomGuesser)
        self.assertIs(
            guessers.DerivedAlphabetGuesser,
            guessers.derived.DerivedAlphabetGuesser
        )
        self.assertIs(
            guessers.OrderedDerivedAlphabetGuesser,
            guessers.derived.OrderedDerivedAlphabetGuesser
        )
        self.assertIs(
            guessers.RederivedAlphabetGuesser,
            guessers.derived.RederivedAlphabetGuesser
        )
        self.assertIs(
            guessers.FrequentLetterGuesser,
            guessers.probability.FrequentLetterGuesser
        )
        self.assertIs(
            guessers.SingleStateMarkovGuesser,
            guessers.markov.SingleStateMarkovGuesser
        )
