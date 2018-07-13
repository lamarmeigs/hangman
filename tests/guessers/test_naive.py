import string
from unittest import TestCase

from guessers.naive import OrderedRandomGuesser, RandomGuesser


class RandomGuesserTestCase(TestCase):
    def test_init_prepares_random_alphabet_ordering(self):
        guesser = RandomGuesser()
        self.assertNotEqual(guesser.alphabet, list(string.ascii_lowercase))
        self.assertEqual(set(guesser.alphabet), set(string.ascii_lowercase))

    def test_guess_pops_letter_from_alphabet(self):
        guesser = RandomGuesser()
        last_letter = guesser.alphabet[-1]
        self.assertEqual(guesser.guess(), last_letter)
        self.assertNotIn(last_letter, guesser.alphabet)


class OrderedRandomGuesserTestCase(TestCase):
    def test_init_prepares_semi_random_alphabet_ordering(self):
        guesser = OrderedRandomGuesser()
        self.assertNotEqual(guesser.alphabet, list(string.ascii_lowercase))
        self.assertEqual(set(guesser.alphabet), set(string.ascii_lowercase))
        self.assertEqual(set(guesser.alphabet[-5:]), set('aeiou'))

    def test_guess_pops_letter_from_alphabet(self):
        guesser = RandomGuesser()
        last_letter = guesser.alphabet[-1]
        self.assertEqual(guesser.guess(), last_letter)
        self.assertNotIn(last_letter, guesser.alphabet)
