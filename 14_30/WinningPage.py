from page import *

class WinnerScreen(ScreenBase):
    def __init__(self, winner_name, players):
        super().__init__()
        self.winner_name = winner_name
        self.players = players
        self.font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 36)
        self.small_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 24)

        # Display winner message
        message = f"{winner_name} wins!"
        text_width, _ = self.font.size(message)
        self.objects.append(Label(
            message,
            ((WINDOW_WIDTH - text_width) // 2, WINDOW_HEIGHT // 2 - 100),
            pygame.Color('yellow'),
            36
        ))

        # Play Again button
        self.objects.append(PlayAgainLabel(
            'Play Again',
            (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2),
            pygame.Color('white'),
            pygame.Color('red')
        ))

        # Exit button
        self.objects.append(ExitLabel(
            'Exit',
            (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 50),
            pygame.Color('white'),
            pygame.Color('red')
        ))

        # Display scores
        y_offset = WINDOW_HEIGHT // 2 + 100
        for player in players:
            score_text = f"{player.name}: {player.score} points"
            text_surface = self.small_font.render(score_text, True, pygame.Color('white'))
            self.objects.append(Label(
                score_text,
                (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, y_offset),
                pygame.Color('white'),
                24
            ))
            y_offset += 30

    def handle_event(self, event):
        for obj in self.objects:
            next_screen = obj.handle_event(event)
            if next_screen:
                return next_screen
        return self

class PlayAgainLabel(ClickableLabel):
    def click(self):
        return StartScreen()

class ExitLabel(ClickableLabel):
    def click(self):
        return None  # Signal to exit the game