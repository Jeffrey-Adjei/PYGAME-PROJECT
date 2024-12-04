from card import *
import random

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
        """
        返回牌组的字符串表示
        """
        return ", ".join(str(card) for card in self.cards)