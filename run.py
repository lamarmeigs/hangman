import argparse
import random

import guessers
from game import Game


GUESSERS = {
    'manual': guessers.ManualGuesser,
    'random': guessers.RandomGuesser,
    'ordered-random': guessers.OrderedRandomGuesser,
    'derived': guessers.DerivedAlphabetGuesser,
    'ordered-derived': guessers.OrderedDerivedAlphabetGuesser,
    'rederived': guessers.RederivedAlphabetGuesser,
    'frequent': guessers.FrequentLetterGuesser,
}


def load_words(file_path):
    """Parse all words from the specified file.

    Args:
        file_path (str): path to a file containaing a collection of
            newline-delimited words.

    Return:
        list of str
    """
    with open(file_path) as wordfile:
        words = wordfile.read().lower().split()
    return words


def run_guesser(guesser_class, word, word_list, max_guesses, verbose=False):
    """Run an instance of the specified guesser on a randomly-selected word.

    Args:
        guesser_class (type): a class inheriting from guessers.base.BaseGuesser
        word (str): the word to guess
        word_list (list of str): a collection of all potential words to guess
        max_guesses (int): a maximum number of guesses allowed per game
        verbose (bool): whether to output progress reports
    """
    game = Game(word, max_failures=max_guesses)
    guesser = guesser_class(word_length=len(game.word), potential_words=word_list)
    while not game.is_game_over:
        if verbose:
            print(
                '{}\nIncorrect guesses: {}\nRemaining guesses: {}\n'.format(
                    game.word,
                    ' '.join(game.incorrect_guesses),
                    game.remaining_guess_count
                )
            )

        guess = guesser.guess(guessed_word=game.word, word_length=len(game.word))
        letter_correctness = game.process_guess(guess)
        guesser.update_state(letter_correctness)

        if verbose:
            print('{} guessed {}\n'.format(type(guesser).__name__, guess))

    guess_status = '{} attempts ({} correct, {} incorrect)'.format(
        len(game.correct_guesses) + len(game.incorrect_guesses),
        len(game.correct_guesses),
        len(game.incorrect_guesses),
    )
    if game.has_won:
        print(
            '{} successfully guessed "{}" after {}'.format(
                type(guesser).__name__,
                game.word,
                guess_status,
            )
        )
    else:
        print(
            '{} failed to guess "{}" (discovered "{}") after {}'.format(
                type(guesser).__name__,
                word,
                game.word,
                guess_status,
            )
        )


def run_all_guessers(word, word_list, max_guesses, verbose=False):
    """Run an instance of each defined guesser on a randomly-selected word.

    Args:
        word (str): the word to guess
        word_list (list of str): a collection of all potential words to guess
        max_guesses (int): a maximum number of guesses allowed per game
        verbose (bool): whether to output progress reports
    """
    for guesser_name in GUESSERS.keys():
        if guesser_name != 'manual':
            guesser_class = GUESSERS.get(guesser_name)
            run_guesser(guesser_class, word, word_list, max_guesses, verbose=verbose)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run hangman guessers'
    )
    parser.add_argument('-w', '--word', help='the word to guess')
    parser.add_argument(
        '-f',
        '--wordfile',
        default='/usr/share/dict/words',
        help='path to a file of newline-delimited potential words to guess'
    )
    parser.add_argument(
        '-g',
        '--guesser',
        choices=GUESSERS.keys(),
        help='name of a specific guesser to run'
    )
    parser.add_argument(
        '-c',
        '--count',
        type=int,
        default=8,
        help='number of guesses allowed'
    )
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    words = [args.word] if args.word else load_words(args.wordfile)
    word = random.choice(words)
    if args.guesser:
        guesser_class = GUESSERS.get(args.guesser)
        run_guesser(
            guesser_class,
            word,
            words,
            max_guesses=args.count,
            verbose=args.verbose
        )
    else:
        run_all_guessers(word, words, max_guesses=args.count, verbose=args.verbose)
