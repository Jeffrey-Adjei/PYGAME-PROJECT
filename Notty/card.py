import pygame
import random
import sys
from setting import *



class Card:
    def __init__(self, color, value, x=0, y=0):

        self.color = color
        self.value = int(value)
        self.x = x
        self.y = y
        self.width = 52
        self.height = 80

        self.image = pygame.image.load(f"images/{color.lower()}_{value}.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def __str__(self):
        return f"{self.color} {self.value}"

    def draw(self, surface, selected=False, back=False):
            #Draw the card
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if selected:
            rect.inflate_ip(20, 20)  # larger

        if back:
            back_image = pygame.image.load("images/card_back.png")
            back_image = pygame.transform.scale(back_image, (rect.width, rect.height))
            surface.blit(back_image, rect.topleft)
        else:
            scaled_image = pygame.transform.scale(self.image, (rect.width, rect.height))
            surface.blit(scaled_image, rect.topleft)

    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height