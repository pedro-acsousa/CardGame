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
switch.py. test_switch updated some methods privacy




