from unittest import mock, TestCase

from guessers.derived import (
    BaseDerivedAlphabetGuesser,
    DerivedAlphabetGuesser,
    OrderedDerivedAlphabetGuesser,
    RederivedAlphabetGuesser,
)
from guessers.exc import TableFlipError


class BaseDerivedAlphabetGuesserTestCase(TestCase):
    class DummyDerivedAlphabetGuesser(BaseDerivedAlphabetGuesser):
        def guess(self, *args, **kwargs):
            pass

    def test_cull_words_limits_words_by_length(self):
        guesser = self.DummyDerivedAlphabetGuesser()
        culled_words = guesser._cull_words(
            12,
            ['haberdashery', 'horticulture', 'thalassophobia']
        )
        self.assertCountEqual(
            culled_words,
            ['haberdashery', 'horticulture']
        )

    def test_derive_alphabet_extracts_unique_letters(self):
        guesser = self.DummyDerivedAlphabetGuesser()
        unique_letters = guesser._derive_alphabet(
            ['stereoscopy', 'microscope']
        )
        self.assertEqual(unique_letters, set('sterocpymi'))


class DerivedAlphabetGuesserTestCase(TestCase):
    def test_init_sets_alphabet_and_words(self):
        with mock.patch.object(
            DerivedAlphabetGuesser,
            '_cull_words'
        ) as mock_cull:
            with mock.patch.object(
                DerivedAlphabetGuesser,
                '_derive_alphabet',
                return_value=set('sartoil')
            ) as mock_derive:
                guesser = DerivedAlphabetGuesser(8, ['sartorial'])

        self.assertEqual(guesser.potential_words, mock_cull.return_value)
        self.assertEqual(set(guesser.alphabet), set(mock_derive.return_value))

    def test_guess_pops_letter_from_alphabet(self):
        guesser = DerivedAlphabetGuesser(len('constituent'), ['constituent'])
        last_letter = guesser.alphabet[-1]
        self.assertEqual(guesser.guess(), last_letter)
        self.assertNotIn(last_letter, guesser.alphabet)


class OrderedDerivedAlphabetGuesserTestCase(TestCase):
    def test_init_sets_semi_ordered_alphabet_and_words(self):
        with mock.patch.object(
            DerivedAlphabetGuesser,
            '_cull_words'
        ) as mock_cull:
            with mock.patch.object(
                DerivedAlphabetGuesser,
                '_derive_alphabet',
                return_value=set('transdimentionally')
            ):
                guesser = OrderedDerivedAlphabetGuesser(
                    len('transdimensionally'),
                    ['transdimensionally']
                )
        self.assertEqual(guesser.potential_words, mock_cull.return_value)
        self.assertEqual(len(guesser.alphabet), len(set('transdimensionally')))
        self.assertEqual(set(guesser.alphabet[-4:]), set('aeio'))


class RederivedAlphabetGuesserTestCase(TestCase):
    def test_init_sets_words(self):
        with mock.patch.object(
            RederivedAlphabetGuesser,
            '_cull_words'
        ) as mock_cull:
            guesser = RederivedAlphabetGuesser(len('mendacity'), ['mendacity'])

        self.assertEqual(guesser.potential_words, mock_cull.return_value)
        mock_cull.assert_called_once_with(len('mendacity'), ['mendacity'])

    def test_guess_rederives_alphabet_and_words(self):
        with mock.patch.object(RederivedAlphabetGuesser, '_cull_words') as mock_cull:
            guesser = RederivedAlphabetGuesser(4, ['hoax', 'lull', 'aspartame'])

        with mock.patch.object(guesser, '_match_words') as mock_match:
            with mock.patch.object(
                guesser,
                '_derive_alphabet',
                return_value=set('hoaxlusprtme')
            ) as mock_derive:
                guess = guesser.guess(guessed_word='....')

        mock_match.assert_called_once_with('....', mock_cull.return_value)
        self.assertEqual(guesser.potential_words, mock_match.return_value)
        self.assertIn(guess, mock_derive.return_value)

    def test_guess_raises_error_on_no_possible_solutions(self):
        guesser = RederivedAlphabetGuesser(2, ['ornery'])
        with mock.patch.object(guesser, '_match_words', return_value=[]):
            with self.assertRaises(TableFlipError) as cm:
                guesser.guess(guessed_word='....')
            self.assertEqual(str(cm.exception), 'No possible solution found')

    def test_guess_pops_letters_off_single_word(self):
        guesser = RederivedAlphabetGuesser(6, ['pallor'])
        self.assertEqual(len(guesser.potential_words), 1)

        with mock.patch.object(guesser, '_match_words') as mock_match:
            with mock.patch.object(guesser, '_derive_alphabet') as mock_derive:
                guess = guesser.guess(guessed_word='......')

        self.assertIn(guess, 'pallor')
        self.assertNotIn(guess, guesser.potential_words[0])
        mock_match.assert_not_called()
        mock_derive.assert_not_called()

    def test_match_words_returns_words_matching_guessed_pattern(self):
        matched_words = RederivedAlphabetGuesser._match_words(
            '....otic',
            ['quixotic', 'neurotic', 'aberration']
        )
        self.assertCountEqual(matched_words, ['quixotic', 'neurotic'])
