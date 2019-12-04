# CHANGELOG

* v1.1.0 [2019-11-08]: Added a SmartAI computer opponent.
  Added strategy players.SmartAI
  None of the bugs have been fixed.

* v1.1.0 [2019-10-25]: First major release.
  This version is known to contain some bugs.

* v1.1.1 [2019-12-03]: All relevant functions were made private in this version, to ensure encapsulation
  (in switch.py).

* v1.1.2 [2019-12-03]: Fixed typo "discarded" in docsting of class switch.

* v1.1.3 [2019-12-03]: Fixed typo "Continuously" in docsting of function "run_round".

* v1.1.4 [2019-12-03]: Functions in test_switch are now private and methods are accessible

* v1.1.5 [2019-12-03]: Fixed inline comment spacing. It now has at least 2 spaces as conventional. Changed
"i = 0  #current player index" 

* v1.1.6 [2019-12-03]: Fixed variable value assignment from "==" to "=" in switch.py. Example:
"self.draw4 == False" to "self.draw4 = False"

* v1.1.7 [2019-12-03]: Fixed closed parentheses missing in players.py 
("sorted_choices = sorted(choices, key=score, reverse=True)")

* v1.1.8 [2019-12-03]: Fixed import statement in switch.py and players.py "import user_interface as ui". Variable
name should be lowercase. 

* v1.1.9 [2019-12-03]: Fixed name python function name shadowing in file user_interface.py. Used "minimum" instead of
"min" and maximum instead of "max".

* v1.1.10 [2019-12-03]: Fixed player index out of bounds error to "i = self.direction % len(self.players) - i" in
switch.py. test_switch updated some methods privacy.

* v1.1.11 [2019-12-03]: Updated initial card dealing method to provide 7 cards to players instead of 6 (range updated)
"for i in range(1, n+1):".

* v1.1.12 [2019-12-03]: Fixed method that reverses game direction through "self.direction *= -1". The direction is 
now reversed if any player selects the card with value K.

* v1.1.13 [2019-12-04]: Fixed a section of the game according to rules. Before if a player selected a card with value 4
in the next turn the player had to draw 2. According to rules, this happens when the selected card's value is 2 and not 
4: "if card.value == '2' ".

* v1.1.14 [2019-12-04]: Fixed a test which checks if aces are always allowed to be discarded.
Test: "test_can_discard__allows_ace" The test was wrong as it tested 2 different Aces and a King. It no longer tests
the King, testing Aces only. "assert s.can_discard(Card('♠', 'A'))"

* v1.1.15 [2019-12-04]: Fixed deck size in file cards.py. Before it had duplicated aces (2 of each suit). It now has
the correct number of cards. "values = '2 3 4 5 6 7 8 9 10 J Q K A'.split()"

* v1.1.16 [2019-12-04]: Fixed condition from AND to OR to discard all cards that have the same value OR the same suit.
Before only discarded if both conditions were true. "card.suit == top_card.suit or card.value == top_card.value"

* v1.1.17 [2019-12-04]: Fixed list rotation so that the player plays first in "sizes = sizes[idx:] + sizes[:idx]".
Now the order is correct.

