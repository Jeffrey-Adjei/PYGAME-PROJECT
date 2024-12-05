import pygame
import sys
from screens import StartScreen
from utils import initialise_music, WINDOW_WIDTH, WINDOW_HEIGHT

def run_game():
    # Initialize Pygame and music
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Notty Card Game")

    initialise_music()

    # Set up the initial screen
    current_screen = StartScreen()
    game_over = False
    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            else:
                next_screen = current_screen.handle_event(event)
                if next_screen is None:
                    game_over = True
                elif next_screen != current_screen:
                    current_screen = next_screen

        current_screen.update()

        current_screen.draw(screen)

        pygame.display.flip()

        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
