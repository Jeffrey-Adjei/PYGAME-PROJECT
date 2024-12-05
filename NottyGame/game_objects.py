# game_objects.py
import pygame
import random
from screens import *
from utils import  is_valid_group, find_possible_groups, WINDOW_WIDTH, WINDOW_HEIGHT

class VisualObject:
    def __init__(self):
        pass

    def draw(self, screen):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        pass

class Label(VisualObject):
    def __init__(self, text, pos, colour, font_size=24, max_width=WINDOW_WIDTH - 40):
        super().__init__()
        self.text = text
        self.pos = pos
        self.colour = colour
        self.font_size = font_size
        self.max_width = max_width
        self.font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', self.font_size)

        self.width = 0
        self.height = 0

        self.calculate_size()

    def calculate_size(self):
        img = self.font.render(self.text, True, self.colour)
        self.width = img.get_width()
        self.height = img.get_height()

    def draw(self, screen):
        img = self.font.render(self.text, True, self.colour)
        self.calculate_size()  # Recalculate size in case of dynamic text changes
        screen.blit(img, self.pos)

class ClickableLabel(Label):
    def __init__(self, text, pos, colour1, colour2):
        super().__init__(text, pos, colour1)
        self.colour1 = colour1
        self.colour2 = colour2

    def is_inside(self, pos):
        return self.pos[0] <= pos[0] <= self.pos[0] + self.width \
            and self.pos[1] <= pos[1] <= self.pos[1] + self.height

    def update(self):
        if self.is_inside(pygame.mouse.get_pos()):
            self.colour = self.colour2
        else:
            self.colour = self.colour1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_inside(event.pos):
                return self.click()
        return None

    def click(self):
        pass

class PlayerNumberLabel(ClickableLabel):
    def __init__(self, text, pos, colour1, colour2, parent_screen):
        super().__init__(text, pos, colour1, colour2)
        self.parent_screen = parent_screen

    def click(self):
        num_players = int(self.text)
        ai_types = self.parent_screen.selected_ai[:num_players - 1]
        return PlayScreen(num_players, ai_types)

class RuleLabel(ClickableLabel):
    def click(self):
        return RuleScreen()

class NewGameLabel(ClickableLabel):
    def click(self):
        return StartScreen()

class MulticolorLabel(VisualObject):
    def __init__(self, text, pos, colors):
        super().__init__()
        self.text = text
        self.pos = pos
        self.colors = colors
        self.size = 36
        self.font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', self.size)

    def draw(self, screen):
        x, y = self.pos
        for i, char in enumerate(self.text):
            img = self.font.render(char, True, self.colors[i % len(self.colors)])
            screen.blit(img, (x, y))
            x += img.get_width()  # Increment x position for each character

class Card(VisualObject):
    CARD_WIDTH = 80
    CARD_HEIGHT = 120

    def __init__(self, color, number, image):
        super().__init__()
        self.color = color
        self.number = number
        self.image = image
        self.rect = self.image.get_rect()
        self.selected = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.selected:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, 3)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Deck:
    def __init__(self, card_images):
        self.cards = []
        self.discard_pile = []
        colors = ['red', 'blue', 'green', 'yellow']
        numbers = range(1, 11)
        for color in colors:
            for number in numbers:
                for _ in range(2):  # Two cards of each combination
                    image = card_images[f"{color}_{number}"]
                    card = Card(color, number, image)
                    self.cards.append(card)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            self.reshuffle()
        if self.cards:
            return self.cards.pop()
        else:
            return None  # No cards left to draw

    def add_to_discard_pile(self, cards):
        self.discard_pile.extend(cards)

    def reshuffle(self):
        self.cards = self.discard_pile
        self.discard_pile = []
        self.shuffle()

class Button:
    def __init__(self, text, position, action, image=None):
        self.text = text
        self.position = position
        self.action = action
        self.font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 18)
        self.color = pygame.Color('white')
        self.image = pygame.image.load(image).convert_alpha() if image else None
        if self.image:
            self.rect = self.image.get_rect(topleft=self.position)
        else:
            self.rect = self.font.render(self.text, True, self.color).get_rect(topleft=self.position)
        self.enabled = True

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.position)
            if not self.enabled:
                overlay = pygame.Surface(self.rect.size)
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, self.position)
        else:
            text_color = self.color if self.enabled else pygame.Color('gray')
            text_surface = self.font.render(self.text, True, text_color)
            screen.blit(text_surface, self.position)

    def is_clicked(self, mouse_pos):
        return self.enabled and self.rect.collidepoint(mouse_pos)

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.actions_taken = {'draw': False, 'steal': False}
        self.score = 0

    def reset_actions(self):
        self.actions_taken = {'draw': False, 'steal': False}

    def draw_cards(self, deck, num_cards):
        actual_drawn = 0
        for _ in range(num_cards):
            if len(self.hand) < 20:
                card = deck.draw_card()
                if card:
                    self.hand.append(card)
                    actual_drawn += 1
                else:
                    break  # No more cards to draw
        return actual_drawn

    def take_card_from(self, other_player):
        if other_player.hand and len(self.hand) < 20:
            taken_card = random.choice(other_player.hand)
            other_player.hand.remove(taken_card)
            self.hand.append(taken_card)
            return True
        return False

    def discard_group(self, group, deck):
        for card in group:
            self.hand.remove(card)
        deck.add_to_discard_pile(group)

    def can_discard_group(self, group):
        return is_valid_group(group)

class HumanPlayer(Player):
    def choose_action(self, game_state):
        pass  # Handled via UI interactions in PlayScreen
