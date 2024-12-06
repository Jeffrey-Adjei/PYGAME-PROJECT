import pygame
from setting import *
from button import *

    # Windows class refer to the  UI part from: https://github.com/AustL/PygameWidgets
class select_opponent_window:
    def __init__(self, screen, opponents, font):
        self.screen = screen
        self.opponents = opponents
        self.font = font
        self.width = 400
        self.height = 300
        self.rect = pygame.Rect(
            (WIDTH - self.width) // 2,
            (HEIGHT - self.height) // 2,
            self.width,
            self.height
        )
        self.buttons = []

        # Create buttons for each opponent
        button_width = 150
        button_height = 50
        button_spacing = 20
        for i, opponent in enumerate(opponents):
            button_x = self.rect.x + (self.width - button_width) // 2
            button_y = self.rect.y + 50 + i * (button_height + button_spacing)
            self.buttons.append(
                Button(
                    rect=(button_x, button_y, button_width, button_height),
                    color=(100, 200, 100),
                    text=opponent.name,
                    font=self.font,
                    text_color=COLORS["Black"]
                )
            )

    def draw(self):
        # Draw the background
        pygame.draw.rect(self.screen, COLORS["White"], self.rect)
        pygame.draw.rect(self.screen, COLORS["Black"], self.rect, 2)

        # Draw the title
        title_text = self.font.render("Select an Opponent", True, COLORS["Black"])
        self.screen.blit(
            title_text,
            (self.rect.centerx - title_text.get_width() // 2, self.rect.y + 10)
        )

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def handle_click(self, pos):
        # Check if any button was clicked
        for i, button in enumerate(self.buttons):
            if button.handle_click(pos):
                return self.opponents[i]
        return None
