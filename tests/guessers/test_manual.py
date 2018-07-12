from unittest import mock, TestCase

from guessers.manual import ManualGuesser


class ManualGuesserTestCase(TestCase):
    def test_guess_returns_user_input(self):
        guesser = ManualGuesser()
        with mock.patch('builtins.input', return_value='x '):
            guess = guesser.guess()
        self.assertEqual(guess, 'x')
