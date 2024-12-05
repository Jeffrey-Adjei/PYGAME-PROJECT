from card import *
import random

 # Cards diaplay logic refer to Poker Project:https://github.com/ScienceGamez/pygame_cards and some other UNO Project
class CardDeck:
    def __init__(self):
        self.cards = []
        self.generate_deck()

    def generate_deck(self):
        colors = ['Red', 'Yellow', 'Green', 'Blue']
        for color in colors:
            for value in range(1, 11):
                self.cards.append(Card(color, value))
                self.cards.append(Card(color, value))

    def shuffle(self):

        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None

    def __str__(self):

        # Return a string representation of the deck

        return ", ".join(str(card) for card in self.cards)