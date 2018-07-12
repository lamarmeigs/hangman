# Hangman

A buddy related how he had to solve hangman during a technical interview. After broaching the topic, and having spent too much time medidating on iterative development and rapid prototyping, we came up with too many strategies not to implement for the hell of it. This repo contains a generic hangman game and a collection of increasingly complex (and hopefully effective) guessers.

The guesser implementations include: 

0. (Pending) Manual (user-driven) letter selection
1. (Pending) Random selection of letters from the alphabet
2. (Pending) Ordered random selection (guess vowels first)
3. (Pending) Random selection from an alphabet composed of only the unique letters in words of the appropriate length
4. (Pending) As above, but limit the potential word matches and re-derive the alphabet after each guess
5. (Pending) As above, but with a last-ditch guess
6. (Pending) Prioritize guessing letters that occur more frequently in the words of appropriate length
7. (Pending) Use Markov chains to guess letters that are most likely to occur after a found match
8. (Pending) Hire a statistician; implement whatever they want
9. (Pending) ?
10. (Pending) Profit!
