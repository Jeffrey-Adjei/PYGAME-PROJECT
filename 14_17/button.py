import pygame

#Generic button class from cardgame course: https://github.com/cangoman/CardGameStarter/blob/main/cardgame_classes.py
class Button:

    def __init__(self, rect, color, text, font, text_color):

        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.visible = True

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, self.color, self.rect)
            text_surface = self.font.render(self.text, True, self.text_color)
            text_x = self.rect.centerx - text_surface.get_width() // 2
            text_y = self.rect.centery - text_surface.get_height() // 2
            surface.blit(text_surface, (text_x, text_y))

    # Check if clicked
    def handle_click(self, pos):
        if self.visible and self.rect.collidepoint(pos):
            return True
        return False

    #Hide the button
    def hide(self):
        self.visible = False
    #Show the button
    def show(self):
        self.visible = True
