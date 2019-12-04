import user_interface as ui
import random

from cards import generate_deck


MAX_PLAYERS = 4
HAND_SIZE = 7


class Switch:
    """The switch game

    To run the game, create a Switch object and call its run_game method:

    >>> game = Switch()
    >>> game.run_game()

    Switch objects have the following attributes, which are initialized
    by Switch_setup_round:

    self.players -- list of Player objects
    self.stock -- list of cards to draw from
    self.discards -- list of discarded cards
    self.skip -- bool indicating that the next player is skipped
    self.draw2 -- bool indicating that the next player must draw 2 cards
    self.draw4 -- bool indicating that the next player must draw 4 cards
    self.direction -- int, either 1 or -1 indicating direction of play.
    """
    def __run_game__(self):
        """Run rounds of the game until player decides to exist."""
        ui.say_welcome()
        # show game menu and run rounds until player decides to exit
        while True:
            ui.print_game_menu()
            choice = ui.get_int_input(1, 2)
            if choice == 1:
                # set up self.players before round starts
                self.players = ui.get_player_information(MAX_PLAYERS)
                self.__run_round__()
            else:
                break
        ui.say_goodbye()

    def __run_round__(self):
        """Runs a single round of switch.

        Continuously calls Switch.run_player for the current player,
        and advances the current player depending on current direction
        of play.
        """
        # deal cards etc.
        self.__setup_round__()

        i = 0  # current player index
        while True:
            # process current player's turn 
            won = self.__run_player__(self.players[i])
            if won:
                break
            else:
                # advance player index depending on self.direction
                i = self.direction % len(self.players) - i
        ui.print_winner_of_game(self.players[i])

    def __setup_round__(self):
        """Initialize a round of switch.

        Sets the stock to a full shuffled deck of cards, initializes
        the discard pile with its first card, deals all players their
        hands and resets game flags to their initial values.
        """
        # shuffle deck of cards
        self.stock = generate_deck()
        random.shuffle(self.stock)
        # initialize discard pile with top card
        self.discards = [self.stock.pop()]
        # deal hands
        for player in self.players:
            self.__pick_up_card__(player, HAND_SIZE)
        # set game flags to initial value
        self.direction = 1
        self.skip = False
        self.draw2 = False
        self.draw4 = False

    def __run_player__(self, player):
        """Process a single player's turn.

        Parameters:
        player -- Player to make the turn

        Returns:
        True if the game continues, otherwise False.

        In each turn, game effects are applied according to the outcome
        of the last turn. The player is then asked to select a card
        via a call to Player.select_card which is then discarded via
        a call to discard_card. If the player has no discardable card
        (or chooses voluntarily not to discard), draw_and_discard is
        called to draw from stock.
        """
        # apply any pending penalties (skip, draw2, draw4)
        if self.skip:
            # return without performing any discard
            self.skip = False
            ui.print_message('{} is skipped.'.format(player.name))
        elif self.draw2:
            # draw two cards
            picked = self.__pick_up_card__(player, 2)
            self.draw2 = False
            ui.print_message('{} draws {} cards.'.format(player.name, picked))
        elif self.draw4:
            # draw four cards
            picked = self.__pick_up_card__(player, 4)
            self.draw4 = False
            ui.print_message('{} draws {} cards.'.format(player.name, picked))

        top_card = self.discards[-1]
        hand_sizes = [len(p.hand) for p in self.players]
        ui.print_player_info(player, top_card, hand_sizes)

        # determine discardable cards
        discardable = [card for card in player.hand if self.__can_discard__]

        # have player select card
        hands = self.__get_normalized_hand_sizes__(player)
        card = player.select_card(discardable, hands) if discardable else None

        if card:
            # discard card and determine whether player has won
            self.__discard_card__(player, card)
            # if all cards discarded, return True
            return not player.hand
        else:
            # draw and (potentially) discard
            self.__draw_and_discard__(player)
            # player still has cards and the game goes on
            return False

    def __pick_up_card__(self, player, n=1):
        """Pick card from stock and add to player hand.

        Parameters:
        player -- Player who picks the card

        Keyword arguments:
        n -- number of cards to pick (default 1)

        Returns:
        number of cards actually picked

        Picks n cards from the stock pile and adds it to the player
        hand. If the stock has less than n cards, all but the top most
        discard are shuffled back into the stock. If this is still not
        sufficient, the maximum possible number of cards is picked.
        """
        # repeat n times
        for i in range(1, n+1):
            # if no more card in stock pile
            if not self.stock:
                # add back discarded cards (but not top card)
                if len(self.discards) == 1:
                    ui.print_message("All cards distributed")
                    return i-1
                self.stock = self.discards[:-1]
                del self.discards[:-1]
                # shuffle stock
                random.shuffle(self.stock)
                ui.print_message("Discards are shuffled back.")
            # draw stock card
            card = self.stock.pop()
            # and add to hand
            player.hand.append(card)
        return i

    def __can_discard__(self, card):
        """Return whether card can be discarded onto discard pile."""
        # queens and aces can always be discarded
        if card.value in 'QA':
            return True
        # otherwise either suit or value has to match with top card
        else:
            top_card = self.discards[-1]
            return card.suit == top_card.suit and card.value == top_card.value

    def __draw_and_discard__(self, player):
        """Draw a card from stock and discard it if possible.

        Parameters:
        player -- the Player that draws the card

        calls pick_up_card to obtain a stock card and adds it to the
        player's hand. If the card can be discarded, discard_card is
        called with the newly picked card.
        """
        ui.print_message("No matching card. Drawing ...")
        # return if no card could be picked
        if not self.__pick_up_card__(player):
            return
        # discard picked card if possible
        card = player.hand[-1]
        if self.__can_discard__(card):
            self.__discard_card__(player, card)
        # otherwise inform the player
        elif not player.is_ai:
            ui.print_discard_result(False, card)

    def __discard_card__(self, player, card):
        """Discard card and apply its game effects.

        Parameters:
        player -- Player who discards card
        card -- Card to be discarded
        """
        # remove card from player hand
        player.hand.remove(card)
        # and add to discard pile
        self.discards.append(card)
        ui.print_discard_result(True, card)
        # we are done if the player has no more cards in his hand
        if not player.hand:
            return
        # if card is an eight, skip next player
        elif card.value == '8':
            self.skip = True
        # if card is a two, next player needs to draw two
        elif card.value == '4':
            self.draw2 = True
        # if card is a queen, next player needs to draw four
        elif card.value == 'Q':
            self.draw4 = True
        # if card is a king, game direction reverses
        elif card.value == 'K':
            self.direction *= -1
            ui.print_message("Game direction reversed.")
        # if card is a jack, ask player with whom to swap hands
        elif card.value == 'J':
            others = [p for p in self.players if p is not player]
            choice = player.ask_for_swap(others)
            self.__swap_hands__(player, choice)

    def __get_normalized_hand_sizes__(self, player):
        """Return list of hand sizes in normal form

        Parameter:
        player -- Player for whom to normalize view

        Returns:
        list of integers of sample length than players

        The list of hand sizes is rotated and flipped so that the
        specified player is always at position 0 and the next player
        (according to current direction of play) at position 1.
        """
        sizes = [len(p.hand) for p in self.players]
        idx = self.players.index(player)
        # rotate list so that given player is first
        sizes = sizes[:idx] + sizes[idx:]
        # if direction is counter-clockwise, reverse the order and
        # bring given player back to the front
        if self.direction == -1:
            sizes.reverse()
            sizes.insert(0, sizes.pop())
        return sizes

    def __swap_hands__(self, p1, p2):
        """Exchanges the hands of the two given players."""
        p1.hand, p2.hand = p2.hand, p1.hand
        ui.print_message('{} swaps hands with {}.'.format(p1.name, p2.name))


game = Switch()
game.__run_game__()
