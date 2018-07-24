from unittest import mock, TestCase

import markovify

from guessers.markov import SingleStateMarkovGuesser


class SingleStateMarkovGuesserTestCase(TestCase):
    def test_init_trains_markov_model(self):
        with mock.patch('markovify.Chain') as mock_chain:
            guesser = SingleStateMarkovGuesser(
                word_length=12,
                potential_words=['interstitial', 'formative']
            )
        mock_chain.assert_called_once_with(
            [
                ['i', 'n', 't', 'e', 'r', 's', 't', 'i', 't', 'i', 'a', 'l'],
                ['f', 'o', 'r', 'm', 'a', 't', 'i', 'v', 'e'],
            ],
            state_size=1
        )
        self.assertIs(guesser.markov_model, mock_chain.return_value)

    def test_guess_returns_final_word(self):
        guesser = SingleStateMarkovGuesser(
            word_length=11,
            potential_words=['desperation']
        )
        self.assertEqual(len(guesser.potential_words), 1)

        with mock.patch.object(guesser, '_select_most_frequent_follower') as mock_select:
            guess = guesser.guess(guessed_word='...........')

        self.assertEqual(guess, 'desperation')
        mock_select.assert_not_called()

    def test_guess_select_frequent_first_letter_for_unknown_words(self):
        guesser = SingleStateMarkovGuesser(
            word_length=8,
            potential_words=['illusory', 'derelish']
        )
        with mock.patch.object(guesser, '_select_most_frequent_follower') as mock_select:
            guess = guesser.guess('........')
        mock_select.assert_called_once_with(
            guesser.markov_model,
            (markovify.chain.BEGIN,)
        )
        self.assertEqual(guess, mock_select.return_value)

        with mock.patch.object(guesser, '_select_most_frequent_follower') as mock_select:
            guess = guesser.guess('....sory')
        mock_select.assert_called_once_with(
            guesser.markov_model,
            (markovify.chain.BEGIN,)
        )
        self.assertEqual(guess, mock_select.return_value)

    def test_guess_selects_guessed_letter_follower(self):
        guesser = SingleStateMarkovGuesser(
            word_length=12,
            potential_words=['anticipatory', 'unsinokorean']
        )
        with mock.patch.object(guesser, '_select_most_frequent_follower') as mock_select:
            guess = guesser.guess('ant....a....')
        mock_select.assert_called_once_with(guesser.markov_model, 't')
        self.assertEqual(guess, mock_select.return_value)

        with mock.patch.object(guesser, '_select_most_frequent_follower') as mock_select:
            guess = guesser.guess('antici.atory')
        mock_select.assert_called_once_with(guesser.markov_model, 'i')
        self.assertEqual(guess, mock_select.return_value)

    def test_select_most_frequent_follower_retrieves_unguessed_letter(self):
        chain = markovify.Chain(
            [
                ['a', 'b'],
                ['a', 'b', 'a', 'b'],
                ['a', 'c'],
            ],
            state_size=1
        )
        guesser = SingleStateMarkovGuesser(
            word_length=9,
            potential_words=['implosion']
        )
        guesser.incorrect_guesses = {'b'}
        guess = guesser._select_most_frequent_follower(chain, ('a',))
        self.assertEqual(guess, 'c')
