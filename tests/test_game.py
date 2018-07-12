from unittest import TestCase

from game import CheaterError, Game


class CheaterErrorTestCase(TestCase):
    def test_inheritance(self):
        self.assertIsInstance(CheaterError(), Exception)


class GameTestCase(TestCase):
    def test_init_sets_attributes(self):
        game = Game('foobar', 5)
        self.assertEqual(game._word, 'foobar')
        self.assertEqual(game.max_guesses, 5)
        self.assertEqual(game.correct_guesses, set())
        self.assertEqual(game.incorrect_guesses, set())

    def test_word_obscures_unguessed_letters(self):
        game = Game('sisyphean')
        self.assertEqual(game.word, '.........')

        game.correct_guesses.update('sea')
        self.assertEqual(game.word, 's.s...ea.')

        game.correct_guesses.update('sisyphean')
        self.assertEqual(game.word, 'sisyphean')

    def test_guess_count_sums_all_guesses(self):
        game = Game('sybaritic', max_guesses=10)
        self.assertEqual(game.guess_count, 0)

        game.correct_guesses.update('syb')
        game.incorrect_guesses.update('xzhj')
        self.assertEqual(game.guess_count, 7)

    def test_remaining_guess_count_tracks_guesses(self):
        game = Game('ebullient', max_guesses=10)
        self.assertEqual(game.remaining_guess_count, 10)

        game.correct_guesses.update('ebul')
        game.incorrect_guesses.update('aoy')
        self.assertEqual(game.remaining_guess_count, 3)

        game.correct_guesses.update('nt')
        game.incorrect_guesses.update('c')
        self.assertEqual(game.remaining_guess_count, 0)

    def test_is_game_over_reflects_wins_and_losses(self):
        game = Game('zeitgeist', max_guesses=10)
        self.assertFalse(game.is_game_over)
        game.correct_guesses.update('zeitgeist')
        self.assertTrue(game.is_game_over)

        game = Game('zeitgeist', max_guesses=10)
        game.incorrect_guesses.update('abcdfhjklm')
        self.assertTrue(game.is_game_over)

    def test_has_won_reflects_complete_correct_guesses(self):
        game = Game('stochastic')
        self.assertFalse(game.has_won)

        game.correct_guesses.update('stoch')
        self.assertFalse(game.has_won)

        game.correct_guesses.update('astic')
        self.assertTrue(game.has_won)

    def test_process_guess_catches_cheaters(self):
        game = Game('toroidal', max_guesses=2)
        with self.assertRaises(CheaterError) as cm:
            game.process_guess('aei')
        self.assertEqual(
            str(cm.exception),
            'Attempt to make more than 2 guesses'
        )

    def test_process_guess_categorizes_guesses(self):
        game = Game('disenfranchisement', max_guesses=10)
        game.process_guess('aeiou')
        self.assertEqual(game.correct_guesses, {'a', 'e', 'i'})
        self.assertEqual(game.incorrect_guesses, {'o', 'u'})
