import os

import pdb

import random

from pick import pick

from itertools import cycle

def clear():
    os.system("cls" if os.name == "nt" else "clear")

class Deck:
    """Generates a deck of cards, using class variables , numbers and suits"""
    numbers = [
        'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
        'Jack', 'Queen', 'King'
    ]
    suits = ['hearts', 'clubs', 'diamonds', 'spades']

    def create_deck(self):
        """ create_deck is called to create a deck of 52 cards"""
        self.deck = list(
            (v + " of " + s for s in Deck.suits for v in Deck.numbers))
        return self.deck

    def shuffling(self):
        """Shuffles the cards in a random order, cards are shuffled when
        they're dealt"""
        random.shuffle(self.deck)
        random.shuffle(self.deck)
        return self.deck

    def num_of_players(self):
        """ Asks how many players will be playing and calls the deal method"""
        num_of_players = None
        while num_of_players is None:
            print("Black Jack is a 2-4 player game")
            try:
                num_of_players = int(
                    input("How many people would like to play interactive BlackJack: "))
                if num_of_players < 2 or num_of_players > 4:
                    num_of_players = None
                    raise ValueError
            except (ValueError, TypeError):
                clear()
                print("Please enter a value between 2 - 4 ")

        print(f"There are {num_of_players} players playing ")
        Deck.deal(self, num_of_players)

    def deal(self,num_of_players):
        """Deals out cards depending on the num_of_players"""
        Deck.shuffling(self)
        players_dict = {}
        for num in range(num_of_players):
            dicts= {f"hand{num+1}":[]}
            players_dict.update(dicts)
        while len(players_dict['hand1']) < 7:
            try:
                players_dict['hand1'].append(deck.deck.pop(0))
                players_dict['hand2'].append(deck.deck.pop(0))
                players_dict['hand3'].append(deck.deck.pop(0))
                players_dict['hand4'].append(deck.deck.pop(0))
            except (AttributeError, KeyError):
                continue
        setattr(self, 'players_dict', players_dict)
        

class Play(Deck):
    """ Class defines the game loop, of playing cards and switching turns"""
    def __init__(self,deck):
        self.deck_of_cards = deck
        self.hands = deck.players_dict
        self.players = list(deck.players_dict.keys())
        self.turn = []
        self.in_play = [self.deck_of_cards.deck.pop(0)]
        self.current_player = []
        self.saved = []

    def players_turn_generator(self):
        """ Method which uses Generators to create players turns"""
        saved = []
        for element in self.players:
            yield element
            saved.append(element)
        while saved:
            for element in saved:
                yield element

    def next_players_turn(self):
        """Method that calles the players_turn_generator and generates the next players turn"""
        self.turn = next(playing)
        print('- - ' * 12, "\n")
        Play.ask(self)

    def start(self):
        """starting player will be the player after the dealer """
        answered = False
        while answered is not True:
            try:
                answer = int(input("\n Which player would of dealt the cards: "))
                if answer < 1 or answer > len(self.players):
                    raise ValueError
                else:
                    for _ in range(answer):
                        self.current_player = next(playing)
                    break
            except ValueError:
                clear()
                print(f"Please, input a valid number between 1 and {len(self.players)}")
            else:
                clear()
                break
    
    def ask(self):
        """ Player option to either play card from hand, see their hand or pick up a card"""
        print(f"it's Player {self.turn[-1]}'s turn")
        x = self.turn
        while x and len(self.players) > 1:
            try:
                print(f"{self.in_play[-1]} - is the current card in play", "\n")
                print("""- input (V) to view your card(s)
- input (P) to pick up a card
- Hit (Enter) to play a card(s) """)
                hand = input(": ")
                print('- - ' * 12,"\n")
                if hand.upper() == "V":
                    clear()
                    print(f"Player{self.turn[-1]}'s' hand:", self.hands[f"{self.turn}"],"\n")
                elif hand.upper() == "P":
                    Play.pick_up(self)
                    Play.next_players_turn(self)
                elif hand.upper() == " " or hand.upper() == "":
                    while x:
                        Logic.__init__(self)
                else:
                    raise ValueError
            except ValueError: 
                print("Please input a value from the below options")
        if len(self.players) < 2:
            print(f"{self.turn} loses")
            #Break out of the game

    def pick_up(self):
        """ Pick up One card from the self.deck_of_cards """        
        for _ in range(1):
            self.hands[f"{self.turn}"].append(deck.deck.pop(0))
        Play.next_players_turn(self)

class Logic(Play):
    def __init__(self):
        self.card_type = {
            "standard_cards": {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '9': 9, '10': 10},
            "power_cards": {'Ace': (1, Logic.change_suit), '2': (2, Logic.pick_up), '8': (8, Logic.miss_a_go),
                            'Jack': (11, (Logic.pick_up, Logic.cancel_pick_up)), 'Queen': (12, Logic.cover), 
                            'King': (13, Logic.reverse) },
            "order": {"Ace": 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                      '9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13}
        }
        self.pot = []
        self.suits = Deck.suits
        self.values = Deck.numbers
        self.first_card = True
        self.no_mistakes = False
        self.looping = True
        Logic.pick_cards(self)
        
    def pick_cards(self):
        self.cards_to_play = ''
        if self.first_card:
            self.cards_to_play = ' '
        while len(self.cards_to_play) > 0 and self.no_mistakes is False:
            cards_to_play = pick(
                self.hands[self.turn],
                title=(f"{self.turn[-1]}'s turn: current card in play is: {self.in_play[-1]}"),
                multi_select=True,
                min_selection_count=0
            )
            if len(cards_to_play) == 0:
                try:
                    prompt = input("end turn without playing? (y/n)").lower()
                    if prompt == 'y':
                        print("picking up one card")
                        Play.pick_up(self)
                        break
                    elif prompt == "n":
                        pass
                except ValueError:
                    print("Please enter y/n")
            else:
                setattr(self, "cards_to_play", cards_to_play)
                Logic.suits_values(self)
        Play.next_players_turn(self)

    def suits_values(self):
        for _ in range(len(self.cards_to_play)):
            card_in_play = (self.in_play[-1])
            card_in_play = str(card_in_play)
            card_in_play_value, card_in_play_suit = card_in_play.split(' of ')
            to_be_played_value, to_be_played_suit = self.cards_to_play[0][0].split(" of ")
            Logic.match(self,card_in_play_suit,card_in_play_value,to_be_played_suit,to_be_played_value)

    def match(self, *args):
        card_in_play_suit, card_in_play_value, to_be_played_suit, to_be_played_value = args    
        if card_in_play_suit == to_be_played_suit or card_in_play_value == to_be_played_value:
            Logic.play_card_from_hand(self)
        elif card_in_play_suit != to_be_played_suit or card_in_play_value != to_be_played_value:
            Logic.pick_up_two_for_mistake(self)

    def play_card_from_hand(self, *args):
        card_to_be_removed = self.cards_to_play.pop(0)
        self.in_play.append(card_to_be_removed[0])
        self.hands[f"{self.turn}"].remove(card_to_be_removed[0])
        Logic.run(self)
        
    def run(self):
        self.first_card = False
        
    def pick_up_two_for_mistake(self):
        for _ in range(2):
            self.hands[f'{self.turn}'].append(deck.deck.pop(0))
        print(" \n")
        print("*" * 30)
        print(f"Player {self.turn[-1]}, {self.cards_to_play[0][0]} cannot go on {self.in_play[-1]}")
        self.no_mistakes = True
        print("*" * 30)
        print(" \n ")


    def is_power_card(self, args):
        to_be_played_suit, to_be_played_value = args[2:4]
        function_call = self.card_type['power_cards'][f'{to_be_played_value}'][-1]
        if to_be_played_value == "Jack":
            if to_be_played_suit == "hearts" or to_be_played_suit == "diamonds":
                function_call[-1](self, *args)
            elif to_be_played_suit == "spades" or to_be_played_suit == "clubs":
                function_call[-2](self, *args)
        else:
            function_call(self, *args)

    def change_suit(self, args):
        card_in_play_suit, to_be_played_value = args[0],[3]
        pdb.set_trace()
        changing_suit = pick(
            self.suits, title=f"What suit would you like to change too,current suit: {card_in_play_suit}",
            indicator=">>",
            min_selection_count=1
        )
        new_card = to_be_played_value + ' of ' + changing_suit[0]
        print(new_card)
        Logic.play_card_from_hand(self, new_card)

    def miss_a_go(self, *args):
        pass

    def pick_up(self, *args):
        pass

    def cancel_pick_up(self, *args):
        pass

    def cover(self, *args):
        pass

    def reverse(self, *args):
        pass

deck = Deck()
deck.create_deck()
deck.shuffling()
deck.num_of_players()
Game = Play(deck)
playing = Game.players_turn_generator()
Game.start()
# while len(deck.players_dict.values()) > 0:
Game.next_players_turn()
Game.ask()
