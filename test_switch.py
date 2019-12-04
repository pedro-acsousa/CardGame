import switch

from cards import Card


class MockPlayer:
    is_ai = True

    def __init__(self, hand):
        self.name = "Mock player"
        self.hand = hand

    def select_card(self, choices, hands):
        return choices[0]

    def ask_for_swap(self, others):
        return others[0]


def mock_setup_round(hands, stock, discards,
                         skip=False, draw2=False, draw4=False, direction=1):
    def str_to_cards(spec):
        return [Card(sv[:1], sv[1:]) for sv in spec.split()]

    s = switch.Switch()
    s.players = [MockPlayer(str_to_cards(hand)) for hand in hands]
    s.discards = str_to_cards(discards)
    s.stock = str_to_cards(stock)
    s.skip = skip
    s.draw2 = draw2
    s.draw4 = draw4
    s.direction = direction
    return s


def test_setup_round__resets_flags():
    """setup_round sets all flags to initial value"""
    s = switch.Switch()
    s.players = [MockPlayer([]), MockPlayer([])]
    s.__setup_round__()
    assert s.skip is False
    assert s.draw2 is False
    assert s.draw4 is False
    assert s.direction == 1


def test_setup_round__deals_cards():
    """setup_round deals correct number of cards"""
    s = switch.Switch()
    s.players = [MockPlayer([]), MockPlayer([])]
    s.__setup_round__()
    assert all(len(p.hand) == 7 for p in s.players)
    assert len(s.discards) == 1
    assert len(s.stock) == 52 - len(s.players) * 7 - 1


def test_pick_up_card__pick_correct_number():
    """pick_up_card picks up correct number of cards"""
    s = mock_setup_round(['♣4', '♣9'], '♠7 ♢8 ♠5 ♢6 ♢7', '♠5 ♢6 ♡3')
    player = s.players[0]
    picked = s.__pick_up_card__(player, 4)
    assert picked == 4
    assert len(player.hand) == 5
    assert len(s.stock) == 1

    picked = s.__pick_up_card__(player, 4)
    assert picked == 3
    assert len(player.hand) == 8
    assert len(s.stock) == 0


def test_can_discard__follows_suit():
    s = mock_setup_round([], '', '♣5')
    assert s.__can_discard__(Card('♣', '2'))
    assert s.__can_discard__(Card('♣', '3'))
    assert s.__can_discard__(Card('♣', '4'))
    assert s.__can_discard__(Card('♣', '6'))
    assert s.__can_discard__(Card('♣', '7'))
    assert s.__can_discard__(Card('♣', '8'))
    assert s.__can_discard__(Card('♣', '9'))
    assert s.__can_discard__(Card('♣', '10'))
    assert s.__can_discard__(Card('♣', 'J'))
    assert s.__can_discard__(Card('♣', 'K'))


def test_can_discard__follows_value():
    s = mock_setup_round([], '', '♣5')
    assert s.__can_discard__(Card('♢', '5'))
    assert s.__can_discard__(Card('♡', '5'))
    assert s.__can_discard__(Card('♠', '5'))


def test_can_discard__allows_ace():
    s = mock_setup_round([], '', '♣5')
    assert s.__can_discard__(Card('♢', 'A'))
    assert s.__can_discard__(Card('♡', 'A'))
    assert s.__can_discard__(Card('♠', 'K'))


def test_can_discard__allows_queen():
    s = mock_setup_round([], '', '♣5')
    assert s.__can_discard__(Card('♢', 'Q'))
    assert s.__can_discard__(Card('♡', 'Q'))
    assert s.__can_discard__(Card('♠', 'Q'))


def test_discard_card__sets_skip():
    s = mock_setup_round(['♣4 ♡8', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    s.__discard_card__(s.players[0], Card('♡', '8'))
    assert s.skip


def test_discard_card__sets_draw2():
    s = mock_setup_round(['♣4 ♡2', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    s.__discard_card__(s.players[0], Card('♡', '2'))
    assert s.draw2


def test_discard_card__sets_draw4():
    s = mock_setup_round(['♣4 ♡Q', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    s.__discard_card__(s.players[0], Card('♡', 'Q'))
    assert s.draw4


def test_discard_card__reverses():
    s = mock_setup_round(['♣4 ♡K', '♣K ♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    s.__discard_card__(s.players[0], Card('♡', 'K'))
    assert s.direction == -1
    s.__discard_card__(s.players[1], Card('♣', 'K'))
    assert s.direction == 1


def test_discard_card__swaps():
    s = mock_setup_round(['♣4 ♡J', '♣K ♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    s.__discard_card__(s.players[0], Card('♡', 'J'))
    assert s.players[0].hand == [Card('♣', 'K'), Card('♣', '9')]
    assert s.players[1].hand == [Card('♣', '4')]


def test_get_normalized_hand_sizes():
    """test hand size normalization"""
    s = mock_setup_round(['♣4', '♣K ♣9', '♡J ♢5 ♢6'], '♢7 ♢8', '♡3')
    assert s.__get_normalized_hand_sizes__(s.players[0]) == [1, 2, 3]
    assert s.__get_normalized_hand_sizes__(s.players[1]) == [2, 3, 1]
    assert s.__get_normalized_hand_sizes__(s.players[2]) == [3, 1, 2]

    s = mock_setup_round(['♣4', '♣K ♣9', '♡J ♢5 ♢6'], '♢7 ♢8', '♡3', direction=-1)
    assert s.__get_normalized_hand_sizes__(s.players[0]) == [1, 3, 2]
    assert s.__get_normalized_hand_sizes__(s.players[1]) == [2, 1, 3]
    assert s.__get_normalized_hand_sizes__(s.players[2]) == [3, 2, 1]


def test_swap_hands():
    """Test swapping of hands"""
    s = mock_setup_round(['♣4', '♣K ♣9', '♡J ♢5 ♢6'], '♢7 ♢8', '♡3')
    s.__swap_hands__(s.players[1], s.players[2])
    assert len(s.players[1].hand) == 3
    assert len(s.players[2].hand) == 2


def test_run_player__adheres_to_skip_flag():
    """run_player adheres to switch.skip"""
    from copy import deepcopy
    s = mock_setup_round(['', '', ''], '', '♣3', skip=True)
    player = s.players[1]
    hand_before = deepcopy(player.hand)
    s.__run_player__(player)
    assert player.hand == hand_before
    assert not s.skip


def test_run_player__adheres_to_draw2_flag():
    """run_player adheres to switch.draw2"""
    s = mock_setup_round(['', ''], '♢5 ♣6 ♣7', '♢3', draw2=True)
    player = s.players[1]
    s.__run_player__(player)
    assert len(player.hand) == 2
    assert not s.draw2


def test_run_player__adheres_to_draw4_flag():
    """run_player adheres to switch.draw4"""
    s = mock_setup_round(['', ''], '♢5 ♣5 ♣6 ♣7 ♣8', '♢3', draw4=True)
    player = s.players[1]
    s.__run_player__(player)
    assert len(player.hand) == 4
    assert not s.draw4


def test_run_player__returns_true_upon_win():
    """run_player returns True if player wins"""
    s = mock_setup_round(['♣4 ♣5', '♣9', '♣10'], '♣6 ♣7 ♣8', '♣3')
    player = s.players[0]
    assert not s.__run_player__(player)
    assert s.__run_player__(player)


def test_run_player__draws_card():
    """run_player forces pick up if no discard possible"""
    s = mock_setup_round(['♣4', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    player = s.players[0]
    s.__run_player__(player)
    assert len(player.hand) == 2
    assert len(s.stock) == 3
    assert len(s.discards) == 1


def test_run_player__draws_card_and_discards():
    """run_player discards drawn card if possible"""
    s = mock_setup_round(['♣4', '♣9'], '♢5 ♢6 ♢7 ♡8', '♡3')
    player = s.players[0]
    s.__run_player__(player)
    assert len(player.hand) == 1
    assert len(s.stock) == 3
    assert len(s.discards) == 2
