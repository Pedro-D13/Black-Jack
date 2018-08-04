import os

import pdb

import random

import re

import tkinter

from pick import pick

"""Create a class that is able to have a few attributes hand, player"""


class Deck:
    """class that creates the deck"""
    """We set the numbers and suits that are able to be will be in the game"""
    numbers = [
        'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
        'Jack', 'Queen', 'King'
    ]
    suits = ['hearts', 'clubs', 'diamonds', 'spades']

    def create_deck(self):
        """ create_deck is called to create a deck of 52 cards"""
        self.deck = list(
            ([v + " of " + s] for s in Deck.suits for v in Deck.numbers))
        return self.deck

    def shuffling(self):
        """Shuffles the cards in a random order, cards are shuffled when
        they're dealt"""
        random.shuffle(self.deck)
        random.shuffle(self.deck)
        return self.deck

    def deal(self):
        self.hand1 = []
        self.hand2 = []
        Deck.shuffling(self)
        while len(self.hand1) < 7 and len(self.hand2) < 7:
            to_me = self.deck.pop(0)
            to_you = self.deck.pop(0)
            self.hand1.extend(to_me)
            self.hand2.extend(to_you)
        return self.deck, self.hand1, self.hand2


class Play:

    def __init__(self, deck, hand1, hand2):
        self.hand1 = hand1
        self.hand2 = hand2
        self.deck_of_cards = deck
        self.turn = []
        self.in_play = []
        self.starting_card = []

    def switch(self):
        print("\n")
        print(f"player {self.turn} has ended")
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1

    def start(self):
        ask = True
        while ask:
            ans = (input(
                "\nWho dealt the cards,Player ONE(1) or Player TWO(2)?,please input the number: ")
            )
            try:
                starting = int(ans)
                if starting == 1 or starting == 2:
                    self.turn = starting + 1
                    if self.turn == 3:
                        self.turn = 1
                    print(f"Player {self.turn} goes First")
                    self.in_play.extend(self.deck_of_cards.pop(0))
                    self.starting_card = self.in_play[0]
                    ask = False
                    os.system('clear')
            except ValueError:
                os.system('clear')
                if ans == '' or ans != 1 or ans != 2:
                    print(
                        f"You did not input a played_value or input:\n({ans})\nis not 1 or 2! \nplease try again")
                    os.system('clear')

    def ask(self):
        print("\n"*1)
        print(f"Currently Player {self.turn}'s turn")
        print('\n')
        print(f"Current Card in play: {self.in_play[-1]}")
        if self.turn == 2:
            print(f"Player {self.turn}'s hand:", "\n",
                  f"Total number of cards {len(self.hand2)}", "\n", f"{self.hand2}", "\n")
        else:
            print(f"Player {self.turn}'s hand:", "\n",
                  f"Total number of cards {len(self.hand1)}", "\n", f"{self.hand1}", "\n")
        ans = input("Play a card(enter) or pickup(p): ")
        return ans

    def turns(self):
        while self.hand1 != 0 or self.hand2 != 0:
            if self.turn == 1:
                answer = Play.ask(self)
                if answer.lower() == 'p':
                    self.pick_up()
                    self.switch()
                elif answer == '':
                    print(self.in_play)
                    self.currently_in_play()
                    self.switch()

            elif self.turn == 2:
                answer = Play.ask(self)
                if answer == 'p':
                    self.pick_up()
                    self.switch()
                else:
                    print(self.in_play)
                    self.currently_in_play()
                    self.switch()

        if self.hand1 == 0 and self.turn == 2:
            print("bring backs?")
        elif self.hand2 == 0 and self.turn == 1:
            print("bring backs?")

    def pick_up(self):
        if self.turn == 1:
            os.system('clear')
            card = self.deck_of_cards.pop(0)
            self.hand1.extend(card)
            print(self.hand1)
            Play.switch(self)
            Play.turns(self)
        elif self.turn == 2:
            os.system('clear')
            card = self.deck_of_cards.pop(0)
            self.hand2.extend(card)
            print(self.hand2)
            Play.switch(self)
            Play.turns(self)
        """ Create an if Statement that when the last card is drawn the cards in play are shuffled """

    def currently_in_play(self):

        if self.turn == 1:
            lists = []
            list(lists.append(f'{each}') for each in self.hand1)
            print(f'{lists}?')
            os.system('clear')
            selected = pick(
                self.hand1,
                title=(f"{self.in_play[-1]}: What card would you like to play: "),
                multi_select=True,
                min_selection_count=0)
            Play.Logic.verify(self, selected)

        elif self.turn == 2:
            lists = []
            list(lists.append(f'{each}') for each in self.hand2)
            print(f'{lists}?')
            os.system('clear')
            # root = Tk()

            # tkinter.messagebox.showinfo(f'{self.turns} turn', f"{self.hand2}")

            # answer = tkinter.messagebox.askquestion(
            #     "Move", f"Play a card or skip you go,{self.hand2}")

            # if answer == "yes":
            #     print("you have chosen yes")
            # else:
            #     print("you have chosen no")
            # root.mainloop()
            played = True
            while played:
                selected = pick(
                    self.hand2,
                    title=(f"{self.in_play[-1]}: What card would you like to play: "),
                    multi_select=True,
                    min_selection_count=0)
                if len(selected) == 0:
                    try:
                        sure = input(
                            "do you want to end your turn without playing a card?(y or n): ").lower()
                        if sure == "y":
                            print("You picked up since you did not play")
                            self.pick_up()
                            break
                        elif sure == "n":
                            pass
                    except ValueError:
                        print("Please type (y)es or (n)o: ")
                else:
                    break

            Play.Logic.verify(self, selected)

    class Logic:
        def verify(self, selected):
            self.power_cards = ['Ace', '2', '8', 'Jack', 'Queen', 'King']
            self.standard_cards = ['3', '4', '5', '6', '7', '9', '10']
            self.suits = Deck.suits
            self.order = Deck.numbers
            self.pot = []
            self.selected = selected
            if len(selected) == 0:
                pass
            else:
                selected_cards = list(selected)
                Play.Logic.match(self)

        def match(self):
            """ verifies if the suit matches or the same number with the exception of certain power_cards"""
            """Use the Map Function"""
            print("Matching")
            # while len(self.selected) > 0:
            #     power_cards_pattern = r"(Ace)(2)(8)(Jack)(Queen)(King)"
            #     pdb.set_trace()
            #     card_to_validate = self.selected[0]
            #     current_card_in_play = self.in_play[-1]
            #     if re.match()
            while len(self.selected) > 0:
                each = self.selected[0]
                current_card_in_play = self.in_play[-1]
                current_card_in_play = str(current_card_in_play)
                current_card_value, current_card_suit = current_card_in_play.split(' of ')
                played_value, played_suit = self.selected[0][0].split(' of ')
                if played_value in self.power_cards:
                    if played_value == "Ace":
                        print("Change the suit")
                        Play.Logic.change_suit(self,)
                    elif current_card_suit == playedcurrent_card_value == played_value:
                        if played_value == "2" or played_value == "Jack":
                            if played == "hearts" or played == "diamonds":
                                Play.Logic.cancel_pick_up_x(self)
                            else:
                                print(f"Pick up time")
                                Play.Logic.pick_up_x(self)
                        elif played_value == "8" or played_value == "King":
                            print(f"Miss a go")
                            Play.Logic.miss_a_go(self)
                        elif played_value == "Queen":
                            print("Cover the Queen")
                            Play.Logic.cover(self)
                elif current_card_suit == played_suit or current_card_value == played_value:
                    print(current_card_value)
                    x_to_be_removed, num_to_be_removed = self.selected.pop(0)
                    if self.turn == 1:
                        self.in_play = self.in_play + [x_to_be_removed]
                        self.hand1.remove(x_to_be_removed)
                    elif self.turn == 2:
                        self.in_play = self.in_play + [x_to_be_removed]
                        self.hand2.remove(x_to_be_removed)
                else:
                    two_for_mistake(self, card)
                    break

        def two_for_mistake(self):
            if self.turn == 1:
                for _ in range(2):
                    self.hand1 = self.hand1 + self.deck_of_cards.pop(0)
                    print(self.hand1, len(self.hand2))
            else:
                for _ in range(2):
                    self.hand2 = self.hand2 + self.deck_of_cards.pop(0)
                    print(self.hand2, len(self.hand2))

        def pick_up_x(self):
            pass

        def cancel_pick_up_x(self):
            pass

        def miss_a_go(self):
            pass

        def reverse(self):
            pass

        def cover(self):
            pass

        def change_suit(self):
            pass
            # try:
            #     new_suit = "what suit would you like to change it to, "
            # pattern = r"Ace"

            # if re.match(pattern, "Ace") use the re.sub
            # num = "07593960224"
            # pattern = r"9"
            # num = re.sub(pattern,"0",num)
            # subs all the 9 to 0's


deck = Deck()
deck.create_deck()
deck1, player1, player2 = deck.deal()
Game = Play(deck1, player1, player2)
Game.start()
Game.turns()


#
# def verify(self,selected):
#     setattr(self,'selected',selected)
#     Play.Logic.is_power_card(self)
#
#             if played_value == "Ace":
#                 self.change_suit(self,played_value,card)
#             elif played_value == "2" or played_value == "Jack":
#                 self.pick_up_x(self, played_value,card)
#             elif played_value == "8" or played_value == "King":
#                 self.pick_up_x(self,played_value,card)
#             elif played_value == "queen":
#                 self.cover(self.played_value,card)
#         else:
#             two_for_mistake(self,card)
#


"""
re.match function is used determine whether it matches at the beginning of the string


"""
