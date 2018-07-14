from unittest import mock, TestCase

import run
from guessers.base import BaseGuesser


class LoadWordsTestCase(TestCase):
    def test_parses_words(self):
        with mock.patch(
            'builtins.open',
            mock.mock_open(read_data='foo\nbar\nbaz')
        ) as mock_open:
            words = run.load_words('/path/to/file')

        mock_open.assert_called_once_with('/path/to/file')
        self.assertCountEqual(words, ['foo', 'bar', 'baz'])


class RunGuesserTestCase(TestCase):
    class PredictableGuesser(BaseGuesser):
        letters_to_guess = []

        def guess(self, *args, **kwargs):
            return self.letters_to_guess.pop(0)

    def test_output_on_win(self):
        self.PredictableGuesser.letters_to_guess = list('protean')
        with mock.patch('builtins.print') as mock_print:
            run.run_guesser(
                self.PredictableGuesser,
                'protean',
                ['protean'],
                max_guesses=8,
                verbose=False
            )
        mock_print.assert_called_once_with(
            'PredictableGuesser successfully guessed "protean" '
            'after 7 attempts (7 correct, 0 incorrect)'
        )

    def test_output_on_loss(self):
        self.PredictableGuesser.letters_to_guess = list('abcfghjkmnp')
        with mock.patch('builtins.print') as mock_print:
            run.run_guesser(
                self.PredictableGuesser,
                'deleterious',
                ['deleterious'],
                max_guesses=8,
                verbose=False
            )
        mock_print.assert_called_once_with(
            'PredictableGuesser failed to guess "deleterious"'
            ' (discovered "...........") after 8 attempts (0 correct, 8 incorrect)'
        )


class RunAllGuessersTestCase(TestCase):
    def test_runs_each_guesser(self):
        with mock.patch.object(run, 'run_guesser') as mock_run:
            run.run_all_guessers('antediluvian', ['antediluvian'], max_guesses=8)
        self.assertEqual(mock_run.call_count, len(run.GUESSERS) - 1)
