import random
import user_interface as UI


class Player:
    is_ai = False

    def __init__(self, name):
        self.name = name
        self.hand = []

    def select_card(self, choices, _):
        return UI.select_card(choices)

    def ask_for_swap(self, others):
        return UI.select_player(others)


class SimpleAI:
    is_ai = True

    def __init__(self, name):
        self.name = name
        self.hand = []

    def select_card(self, choices, _):
        return random.choice(choices)

    def ask_for_swap(self, others):
        return random.choice(others)


class SmartAI(SimpleAI):
    def select_card(self, choices, hands):
        def score(card):
            in_suit = len([c for c in self.hand
                           if c.suit == card.suit and c is not card])

            offset = {
                'J': 3*(hands[0]-1-min(hands[1:])),
                'Q': 6 + in_suit,
                '2': 4 + in_suit,
                '8': 2 + in_suit,
                'K': (3 if hands[-1] > hands[1] else -1) + in_suit,
                'A': -2 + in_suit,
            }

            return offset.get(card.value, in_suit)

        sorted_choices = sorted(choices, key=score, reverse=True)
        candidate = sorted_choices[0]
        return candidate if score(candidate) > -2 else None

    def ask_for_swap(self, others):
        smallest = min(len(p.hand) for p in others)
        best = [p for p in others if len(p.hand) == smallest]
        return random.choice(best)
