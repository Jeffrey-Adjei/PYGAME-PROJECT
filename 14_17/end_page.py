import pygame
import sys
def show_victory_screen(screen, winner):
    screen.fill(pygame.Color('black'))
    font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 36)
    message = f"{winner} wins!"
    text_surface = font.render(message, True, pygame.Color('yellow'))
    text_rect = text_surface.get_rect(center=(610, 300))
    screen.blit(text_surface, text_rect)
    small_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 24)
    exit_message = "Press any key to exit"
    exit_surface = small_font.render(exit_message, True, pygame.Color('white'))
    exit_rect = exit_surface.get_rect(center=(610, 350))
    screen.blit(exit_surface, exit_rect)
    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()