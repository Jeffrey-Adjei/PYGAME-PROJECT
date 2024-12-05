from card import *
from setting import *

class Hand:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def draw_name(self, surface):
        # Draw the player's name
        name_text = Player_Name_FONT.render(self.name, True, Player_Name_COLOUR)
        surface.blit(name_text, (self.x-80, self.y - 40))

    def draw(self, surface, selected_cards=None):
        max_cards_per_row = 8
        card_spacing = 52
        row_spacing = 80

        for i, card in enumerate(self.cards):
            row = i // max_cards_per_row
            col = i % max_cards_per_row

            # position
            card.x = self.x + col * card_spacing
            card.y = self.y + row * row_spacing

            is_selected = card in selected_cards if selected_cards else False
            card.draw(surface, selected=is_selected)

    # if click
    def get_card_at(self, pos):
        for card in self.cards:
            if card.is_clicked(pos):  
                return card
        return None