from setting import *
from button import *
import pygame

    # Windows class refer to the  UI part from: https://github.com/AustL/PygameWidgets

class select_card_window:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.width = 400
        self.height = 200
        self.rect = pygame.Rect(
            (WIDTH - self.width) // 2,
            (HEIGHT - self.height) // 2,
            self.width,
            self.height
        )
        self.buttons = []

        # button to select
        options = ["1", "2", "3"]
        button_width = 100
        button_height = 50
        button_spacing = 20
        for i, option in enumerate(options):
            button_x = self.rect.x + 50 + i * (button_width + button_spacing)
            button_y = self.rect.y + 100
            self.buttons.append(
                Button(
                    rect=(button_x, button_y, button_width, button_height),
                    color=(100, 200, 100),
                    text=option,
                    font=self.font,
                    text_color=COLORS["Black"]
                )
            )

    def draw(self):
        # background
        pygame.draw.rect(self.screen, COLORS["White"], self.rect)
        pygame.draw.rect(self.screen, COLORS["Black"], self.rect, 2)

        # title
        title_text = self.font.render("Select Cards to Draw", True, COLORS["Black"])
        self.screen.blit(
            title_text,
            (self.rect.centerx - title_text.get_width() // 2, self.rect.y + 20)
        )

        # button
        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def handle_click(self, pos):
        for button in self.buttons:
            if button.handle_click(pos):
                return int(button.text)
        return None
