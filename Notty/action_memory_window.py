import pygame
from setting import *

class action_memory_window:
    def __init__(self, screen, font, width=400, height=200, alpha=180):
        self.screen = screen
        self.font = font_card
        self.width = width
        self.height = height
        self.alpha = alpha  # transparent
        self.rect = pygame.Rect(0, 500, width, height)
        self.logs = []
        self.max_logs = 10

        # transparent Surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def add_log(self, log):
        self.logs.append(log)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

    def draw(self):

        self.surface.fill((200, 200, 200, self.alpha))  # white

        pygame.draw.rect(self.surface, (0, 0, 0, 255), (0, 0, self.width, self.height), 2)

        # every logs
        for i, log in enumerate(self.logs):
            shadow = self.font.render(log, True, (128, 128, 128))
            self.surface.blit(shadow, (11, 11 + i * 20))
            log_text = self.font.render(log, True, (0, 0, 0))
            self.surface.blit(log_text, (10, 10 + i * 20))

        self.screen.blit(self.surface, (self.rect.x, self.rect.y))