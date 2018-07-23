from unittest import mock, TestCase

from guessers.exc import TableFlipError
from guessers.probability import FrequentLetterGuesser


class FrequentLetterGuesserTestCase(TestCase):
    def test_init_sets_known_guesses(self):
        guesser = FrequentLetterGuesser(9, ['decadence'])
        self.assertEqual(guesser.correct_guesses, set())
        self.assertEqual(guesser.incorrect_guesses, set())

    def test_guesses_returns_all_submitted_guesses(self):
        guesser = FrequentLetterGuesser(4, ['rend'])
        guesser.correct_guesses = {'a', 'e'}
        guesser.incorrect_guesses = {'z', 'x', 'w'}
        self.assertEqual(guesser.guesses, {'a', 'e', 'z', 'x', 'w'})

    def test_update_state_records_guesses_by_correctness(self):
        guesser = FrequentLetterGuesser(8, ['residual'])
        self.assertEqual(guesser.correct_guesses, set())
        self.assertEqual(guesser.incorrect_guesses, set())

        guesser.update_state({'g': True, 'p': False}, '....orality')
        self.assertEqual(guesser.correct_guesses, {'g'})
        self.assertEqual(guesser.incorrect_guesses, {'p'})

    def test_update_state_rematches_words(self):
        guesser = FrequentLetterGuesser(11, ['temporality'])
        with mock.patch.object(guesser, '_match_words') as mock_match:
            guesser.update_state({'x': False}, 'temp...lity')

        mock_match.assert_called_once_with('temp...lity', ['temporality'])
        self.assertEqual(guesser.potential_words, mock_match.return_value)

    def test_guess_returns_most_frequent_letter(self):
        guesser = FrequentLetterGuesser(6, ['latter', 'barrel', 'rabbit'])
        with mock.patch.object(guesser, '_select_most_frequent_letter') as mock_select:
            guess = guesser.guess(guessed_word='......')

        mock_select.assert_called_once_with(guesser.potential_words)
        self.assertEqual(guess, mock_select.return_value)

    def test_guess_pops_letters_off_single_word(self):
        guesser = FrequentLetterGuesser(6, ['gauche'])
        self.assertEqual(len(guesser.potential_words), 1)

        with mock.patch.object(guesser, '_select_most_frequent_letter') as mock_select:
            guess = guesser.guess(guessed_word='......')

        self.assertIn(guess, 'gauche')
        self.assertNotIn(guess, guesser.potential_words[0])
        mock_select.assert_not_called()

    def test_select_most_frequent_letter_works_as_expected(self):
        guesser = FrequentLetterGuesser(5, ['peeve'])
        letter = guesser._select_most_frequent_letter(['peeve', 'reave', 'lease'])
        self.assertEqual(letter, 'e')

        letter = guesser._select_most_frequent_letter(['aardvark', 'awkward'])
        self.assertEqual(letter, 'a')

    def test_select_most_frequent_letter_discards_previous_guesses(self):
        guesser = FrequentLetterGuesser(10, ['irreverent', 'irritable'])
        guesser.correct_guesses = {'e'}
        guesser.incorrect_guesses = {'r'}
        letter = guesser._select_most_frequent_letter(['irreverent', 'irritable'])
        self.assertEqual(letter, 'i')

    def test_select_most_frequent_letter_raises_error_when_all_letters_guessed(self):
        guesser = FrequentLetterGuesser(4, 'oort')
        guesser.correct_guesses = set('oort')
        with self.assertRaises(TableFlipError) as cm:
            guesser._select_most_frequent_letter(['oort', 'tor'])
        self.assertEqual(str(cm.exception), 'No possible solution found')
