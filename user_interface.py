#!/usr/bin/env python3


def say_welcome():
    """print welcome information"""
    print_message("Welcome to Switch v1.1")


def print_game_menu():
    """tell user of the menu options"""
    print("\nPlease select from one of the following options: [1-2]")
    print("1 - New Game")
    print("2 - Exit")


def print_player_info(player, top_card, hands):
    print("\nHANDS: " + str(hands))
    print("PLAYER: " + player.name)
    if not player.is_ai:
        print('HAND: ' + ', '.join(str(card) for card in player.hand))
    print('TOP CARD: ' + str(top_card))


def print_discard_result(discarded, card):
    if discarded:
        print("Discarded: " + str(card) + "\n")
    else:
        print("Unable to discard card: " + str(card))


def print_winner_of_game(player):
    """print winner information"""
    print_message('\n'+80*'-')
    print_message("Woohoo!!! Winner of the game is: " + player.name)
    print_message(80*'-')


def say_goodbye():
    """say goodbye to my little friend"""
    print_message("Goodbye!")


def print_message(msg):
    print(msg)


# helper method for get_int_input method
def convert_to_int(string):
    """converts string to int"""
    result = -1
    try:
        result = int(string)
    except Exception:
        pass
    return result


# methods get information from user
def get_int_input(minimum, maximum):
    """get int value from user"""
    choice = -1
    while choice < minimum or choice > maximum:
        print("> ", end="")
        choice = convert_to_int(input())
        if choice < minimum or choice > maximum:
            print(f"Try again: Input should be an integer between [{minimum:d}-{maximum:d}]")
    return choice


def get_string_input():
    """get word from user"""
    print("> ", end="")
    s = input()
    return s


def get_player_information(MAX_PLAYERS):
    """get player information"""
    import random
    from players import Player, SimpleAI, SmartAI

    # create players list
    players = []
    # how many human players?
    print("\nHow many human players [1-4]:")
    no_of_players = get_int_input(1, MAX_PLAYERS)
    # for each player, get name
    for i in range(no_of_players):
        print("Please enter the name of player " + str(i + 1) + ":")
        players.append(Player(get_string_input()))

    ai_names = ['Angela', 'Bart', 'Charly', 'Dorothy']

    # how many AI players? ensure there are at least 2 players
    minimum = 1 if (len(players) == 1) else 0
    maximum = MAX_PLAYERS - no_of_players
    print(f"\nHow many ai players [{minimum:d}-{maximum:d}]:")
    no_of_players = get_int_input(minimum, maximum)
    # for each ai player, get name
    for name in ai_names[:no_of_players]:
        if random.choice([True, False]):
            players.append(SimpleAI(name))
        else:
            players.append(SmartAI("Smart "+name))

    return players


def select_card(cards):
    """select card from hand"""
    print(f"Please select from one of the following cards: [1-{len(cards):d}]")
    for i, card in enumerate(cards, 1):
        print(str(i) + " - " + str(card))

    # get choice
    choice = get_int_input(0, len(cards))
    # get card
    if choice == 0:
        return None
    return cards[choice - 1]


def select_player(players):
    """select other player"""
    print(f"Please select from one of the following players: [1-{len(players):d}]")
    # print out for each player in players
    for i in range(len(players)):
        p = players[i]
        print(f"{i + 1:d} - {p.name}={len(p.hand):d}")

    # get choice
    choice = get_int_input(1, len(players))
    # get player
    return players[choice - 1]
