# screens.py
import pygame
from game_objects import Label, ClickableLabel, MulticolorLabel, NewGameLabel, PlayerNumberLabel, RuleLabel, Button
from game_objects import Card, Deck, HumanPlayer
from ai_player import AggressiveAIPlayer, DefensiveAIPlayer, BalancedAIPlayer
from utils import load_card_images, is_valid_group, WINDOW_WIDTH, WINDOW_HEIGHT
from utils import wrap_text

class ScreenBase:
    def __init__(self, background_colour=pygame.Color('black'), background_image=None):
        self.background_colour = background_colour
        self.background_image = background_image
        self.objects = []

    def handle_event(self, event):
        for obj in self.objects:
            obj.handle_event(event)
        return self

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(self.background_colour)
        for obj in self.objects:
            obj.draw(screen)

class StartScreen(ScreenBase):
    def __init__(self):
        super().__init__()
        self.selected_ai = []
        self.font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 24)

        # Title
        title_text = "WELCOME TO THE NOTTY GAME!"
        title_colors = [pygame.Color('red'), pygame.Color('yellow'), pygame.Color('blue'), pygame.Color('green')]
        title_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 36)
        total_width = sum([title_font.size(c)[0] for c in title_text])
        title_pos = (
            (WINDOW_WIDTH - total_width) // 2,
            100
        )
        title = MulticolorLabel(title_text, title_pos, title_colors)
        self.objects.append(title)

        # Number of players label
        num_players_label = Label('NUMBER OF PLAYERS:', (0, 0), pygame.Color('white'))
        text_width, _ = num_players_label.font.size('NUMBER OF PLAYERS:')
        num_players_label.pos = (
            (WINDOW_WIDTH - text_width) // 2,
            200
        )
        self.objects.append(num_players_label)

        # Player number buttons
        btn_padding = 50  # Space between buttons
        btn_width = 50  # Approximate width of buttons
        total_btn_width = 2 * btn_width + btn_padding
        btn_x_start = (WINDOW_WIDTH - total_btn_width) // 2

        self.objects.append(PlayerNumberLabel(
            '2',
            (btn_x_start, 250),
            pygame.Color('white'),
            pygame.Color('red'),
            self
        ))

        self.objects.append(PlayerNumberLabel(
            '3',
            (btn_x_start + btn_width + btn_padding, 250),
            pygame.Color('white'),
            pygame.Color('red'),
            self
        ))

        # AI Selection Label
        ai_label = Label('SELECT AI OPPONENTS:', (0, 0), pygame.Color('white'))
        text_width, _ = ai_label.font.size('SELECT AI OPPONENTS:')
        ai_label.pos = (
            (WINDOW_WIDTH - text_width) // 2,
            350
        )
        self.objects.append(ai_label)

        # AI type buttons
        ai_types = ['Aggressive', 'Defensive', 'Balanced']
        btn_x_start = (WINDOW_WIDTH - (len(ai_types) * 150 + (len(ai_types) - 1) * 50)) // 2
        for idx, ai_type in enumerate(ai_types):
            self.objects.append(AITypeLabel(
                ai_type,
                (btn_x_start + idx * 200, 400),
                pygame.Color('white'),
                pygame.Color('yellow'),
                self
            ))

        # Rules button
        rules_text = "CLICK HERE TO READ THE GAME RULES!"
        rules_label = RuleLabel(rules_text, (0, 0), pygame.Color('white'), pygame.Color('red'))
        text_width, _ = rules_label.font.size(rules_text)
        rules_label.pos = (
            (WINDOW_WIDTH - text_width) // 2,
            500
        )
        self.objects.append(rules_label)

    def handle_event(self, event):
        for obj in self.objects:
            next_screen = obj.handle_event(event)
            if next_screen:
                return next_screen
        return self

class RuleScreen(ScreenBase):
    def __init__(self):
        super().__init__()
        # Title at the top center
        title = "DESCRIPTION OF THE GAME"
        font_size_title = 28
        title_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', font_size_title)
        title_width = title_font.size(title)[0]
        title_x = (WINDOW_WIDTH - title_width) // 2
        self.objects.append(Label(
            title,
            (title_x, 20),
            pygame.Color('white'),
            font_size_title
        ))

        # Rules text
        rules = [
            "Each card has a colour (red, blue, green, or yellow) and a number (1 to 10).",
            "There are exactly two cards for each combination, making a total of 80 cards.",
            "At the beginning, the deck is shuffled, and each player is dealt 5 cards.",
            "Players take turns. On a player’s turn, they can perform any of the following:",
            "1. Draw up to 3 cards from the deck (once per turn).",
            "2. Take a random card from another player (once per turn).",
            "3. Discard a valid group of cards (any number of times per turn):",
            "   a. A sequence of at least three cards of the same colour with consecutive numbers.",
            "   b. A set of at least three cards of the same number but different colours.",
            "The first player to empty their hand wins the game."
        ]

        # Font size and line spacing
        font_size_text = 18
        line_spacing = 8
        margin = 50
        available_width = WINDOW_WIDTH - 2 * margin

        # Render the wrapped text
        y_position = 80  # Start below the title
        for rule in rules:
            lines = wrap_text(rule, font_size_text, available_width)
            for line in lines:
                self.objects.append(Label(
                    line,
                    (margin, y_position),
                    pygame.Color('white'),
                    font_size_text
                ))
                y_position += font_size_text + line_spacing
            y_position += line_spacing  # Extra space after each rule

        # Add Back button
        self.objects.append(NewGameLabel(
            'Back',
            (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - margin),
            pygame.Color('white'),
            pygame.Color('red')
        ))

    def handle_event(self, event):
        for obj in self.objects:
            next_screen = obj.handle_event(event)
            if next_screen:
                return next_screen
        return self

class PlayScreen(ScreenBase):
    def __init__(self, num_players, ai_types):
        super().__init__()
        self.num_players = num_players
        self.card_images = load_card_images()
        self.deck = Deck(self.card_images)
        self.players = []
        self.current_player_index = 0
        self.font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 18)

        # Initialize human player
        self.players.append(HumanPlayer("You"))

        # Initialize AI players
        ai_class_map = {
            'Aggressive': AggressiveAIPlayer,
            'Defensive': DefensiveAIPlayer,
            'Balanced': BalancedAIPlayer
        }
        for i, ai_type in enumerate(ai_types):
            ai_class = ai_class_map.get(ai_type, AggressiveAIPlayer)
            self.players.append(ai_class(f"AI {i + 1}"))

        # Deal initial hands
        for player in self.players:
            player.draw_cards(self.deck, 5)

        # Positioning variables
        self.player_hand_y = WINDOW_HEIGHT - Card.CARD_HEIGHT - 100
        self.ai_hand_y = 150
        self.hand_spacing = 10

        # Initialize UI elements (buttons, etc.)
        self.buttons = []

        button_actions = [
            ('Draw Cards', 'draw'),
            ('Steal Card', 'steal'),
            ('Discard Group', 'discard'),
            ('Play for Me', 'play_for_me')
        ]

        button_x = WINDOW_WIDTH - 200
        button_y = WINDOW_HEIGHT / 2 - 100

        for idx, (text, action) in enumerate(button_actions):
            button = Button(text, (button_x, button_y + idx * 50), action)
            self.buttons.append(button)

        self.message = ""
        self.message_timer = 0  # Duration to display the message

        # Load background image
        self.background_image = pygame.image.load('assets/images/background.png').convert()

    def handle_event(self, event):
        current_player = self.players[self.current_player_index]
        if isinstance(current_player, HumanPlayer):
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Check if any buttons are clicked
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        self.handle_action(button.action)
                        return self

                # Check if any cards are clicked
                self.handle_card_click(mouse_pos)
        return self

    def update(self):
        current_player = self.players[self.current_player_index]

        # Update buttons based on actions taken
        if isinstance(current_player, HumanPlayer):
            for button in self.buttons:
                if button.action == 'draw':
                    button.enabled = not current_player.actions_taken['draw'] and len(current_player.hand) < 20
                elif button.action == 'steal':
                    other_players = [p for p in self.players if p != current_player and p.hand]
                    button.enabled = not current_player.actions_taken['steal'] and bool(other_players)
                elif button.action == 'discard':
                    selected_cards = [card for card in current_player.hand if card.selected]
                    button.enabled = current_player.can_discard_group(selected_cards)
                else:
                    button.enabled = True

        # AI Players' turns
        if isinstance(current_player, (AggressiveAIPlayer, DefensiveAIPlayer, BalancedAIPlayer)):
            current_player.choose_action({'players': self.players, 'deck': self.deck})
            current_player.reset_actions()
            self.next_player()

        # Check for winner
        winner = self.check_winner()
        if winner:
            return WinnerScreen(winner.name, self.players)
        else:
            return self
        # Clear message after duration
        if self.message and pygame.time.get_ticks() > self.message_timer:
            self.message = ""

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        self.draw_hands(screen)

        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

        # Draw message
        if self.message:
            message_surface = self.font.render(self.message, True, (255, 255, 0))
            screen.blit(message_surface, (WINDOW_WIDTH // 2 - message_surface.get_width() // 2, WINDOW_HEIGHT // 2))

    def draw_hands(self, screen):
        # Draw human player's hand
        x = 50
        y = self.player_hand_y
        for card in self.players[0].hand:
            card.rect.topleft = (x, y)
            card.draw(screen)
            x += Card.CARD_WIDTH + self.hand_spacing

        # Draw human player's name
        name_text = self.font.render(self.players[0].name, True, (255, 255, 255))
        screen.blit(name_text, (50, self.player_hand_y - 30))

        # Draw AI players' hands
        for idx, player in enumerate(self.players[1:], start=1):
            x = 50
            y = self.ai_hand_y + (idx - 1) * (Card.CARD_HEIGHT + 50)
            for card in player.hand:
                card.rect.topleft = (x, y)
                card.draw(screen)
                x += Card.CARD_WIDTH + self.hand_spacing

            # Draw AI player's name
            name_text = self.font.render(player.name, True, (255, 255, 255))
            screen.blit(name_text, (50, y - 30))

    def handle_action(self, action):
        current_player = self.players[self.current_player_index]
        if isinstance(current_player, HumanPlayer):
            if action == 'draw' and not current_player.actions_taken['draw']:
                num_to_draw = min(3, 20 - len(current_player.hand))
                current_player.draw_cards(self.deck, num_to_draw)
                current_player.actions_taken['draw'] = True
            elif action == 'steal' and not current_player.actions_taken['steal']:
                other_players = [p for p in self.players if p != current_player and p.hand]
                if other_players:
                    target_player = other_players[0]  # For simplicity, pick the first
                    current_player.take_card_from(target_player)
                    current_player.actions_taken['steal'] = True
                else:
                    self.display_message("No players to steal from.")
            elif action == 'discard':
                selected_cards = [card for card in current_player.hand if card.selected]
                if current_player.can_discard_group(selected_cards):
                    current_player.discard_group(selected_cards, self.deck)
                    # Deselect cards
                    for card in selected_cards:
                        card.selected = False
                else:
                    self.display_message("Invalid group selected.")
            elif action == 'play_for_me':
                # Implement AI logic to take over
                ai_player = BalancedAIPlayer(current_player.name)
                ai_player.hand = current_player.hand.copy()
                ai_player.choose_action({'players': self.players, 'deck': self.deck})
                current_player.hand = ai_player.hand.copy()
                current_player.actions_taken = ai_player.actions_taken.copy()
            else:
                self.display_message("Action not available.")
        # After action, check if the player wants to end turn
        if current_player.actions_taken['draw'] and current_player.actions_taken['steal']:
            self.next_player()

    def handle_card_click(self, mouse_pos):
        current_player = self.players[self.current_player_index]
        if isinstance(current_player, HumanPlayer):
            for card in current_player.hand:
                if card.is_clicked(mouse_pos):
                    card.selected = not card.selected
                    break

    def next_player(self):
        self.players[self.current_player_index].reset_actions()
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def check_winner(self):
        for player in self.players:
            if not player.hand:
                return player
        return None

    def display_message(self, text, duration=2000):
        self.message = text
        self.message_timer = pygame.time.get_ticks() + duration

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

class AITypeLabel(ClickableLabel):
    def __init__(self, text, pos, colour1, colour2, parent_screen):
        super().__init__(text, pos, colour1, colour2)
        self.parent_screen = parent_screen

    def click(self):
        if self.text in self.parent_screen.selected_ai:
            self.parent_screen.selected_ai.remove(self.text)
            self.colour1 = pygame.Color('white')
        else:
            self.parent_screen.selected_ai.append(self.text)
            self.colour1 = pygame.Color('yellow')

class PlayAgainLabel(ClickableLabel):
    def click(self):
        return StartScreen()

class ExitLabel(ClickableLabel):
    def click(self):
        return None  # Signal to exit the game
