# Switch

Switch is a card game similar to the popular UNO game. The objective
of the game is to be the first player who managed to discard all his
or her cards. Some discards have consequences on the subsequent player
or mode of play.

## Rules

Switch is played by 2-4 players. Each player is initially dealt a hand
of seven cards. The stock of remaining cards is put on the table face
down. One card is taken from the stock and placed face up to form the
discard pile.

Players take turns in discarding cards from their hand. In general,
a card can be discarded if it matches the top-most card of the discard
pile ("top card") in either suit (diamond, hearts, clubs, or spade) or
value. In addition, aces and queens can always be discarded, no matter
the current top card.

Some discards have special effects on the game flow:

| Card  | Discard Rule       | Effect                                                                  |
| :---: | ------------------ | ----------------------------------------------------------------------- |
| 2     | Same suit or value | Next player must draw two stock cards at the beginning of his turn      |
| 8     | Same suit or value | Next player is skipped and the turn proceeds with the subsequent player |
| J     | Same suit or value | The player must swap his hand with the hand of any other player         |
| Q     | Anytime            | Next player must draw four stock cards at the beginning of his turn     |
| K     | Same suit or value | The direction of game changes before the start of the next players turn |
| A     | Anytime            | None                                                                    |

If a player is not able to discard any card, he must draw a card from
the stock pile. If that card can be discarded, the player must do so
immediately, otherwise the card goes into the players hand and play
proceeds with the next player.

If there is no more card in the stock pile, all discards but the top
card are shuffled and placed face down to form a new stock pile.

#README UPDATE
## Running the game

Start switch on the command line with

	$ pipenv run switch.py


Run the test suite with

	$ pipenv run pytest -s
	
	Click option 2 (Exit game) then pytest runs
