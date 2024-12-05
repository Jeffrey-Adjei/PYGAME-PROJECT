# screens.py
import pygame
from game_objects import Deck, HumanPlayer, AIPlayer
from utils import load_card_images
from main import WINDOW_WIDTH, WINDOW_HEIGHT
from game_objects import Button

game_over = False
current_screen = None
num_player = 0


        






class PlayerNumberLabel(ClickableLabel):
    def click(self):
        global current_screen
        num_players = int(self.text)
        ai_types = AITypeLabel.selected_ai[:num_players - 1]
        current_screen = PlayScreen(num_players, ai_types)


class RuleLabel(ClickableLabel):
    def click(self):
        global current_screen
        current_screen = RuleScreen()


class StartGameLabel(ClickableLabel):
    def click(self):
        global current_screen
        current_screen = MainScreen()


class NewGameLabel(ClickableLabel):
    def click(self):
        global current_screen
        current_screen = StartScreen()


class CloseWindowLabel(ClickableLabel):
    def click(self):
        global game_over
        game_over = True


class ScreenBase:
    def __init__(self, background_colour, background_filename = None):
        self.background_colour = background_colour
        self.objects = []
        if background_filename is not None:
            self.background_image = pygame.image.load(background_filename)
        else:
            self.background_image = None


    def draw(self, screen):
        screen.fill(self.background_colour)

        if self.background_image is not None:
            screen.blit(self.background_image, (0, 0))
        
        for o in self.objects:
            o.draw(screen)

    def update(self):
        for o in self.objects:
            o.update()

    def keydown(self, event):
        pass

    def mouseup(self, event):
        for o in self.objects:
            o.mouseup(event)



class MulticolorLabel(VisualObject):
    def __init__(self, text, pos, colors):
        self.text = text
        self.pos = pos
        self.colors = colors
        self.size = 36
        self.font = pygame.font.Font('Fonts/PressStart2P-Regular.ttf', self.size)

    def draw(self, screen):
        x, y = self.pos
        for i, char in enumerate(self.text):
            img = self.font.render(char, True, self.colors[i % len(self.colors)])
            screen.blit(img, (x, y))
            x += img.get_width()  # Increment x position for each character
            

class StartScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('black'))
        
        
        # Add labels and buttons (as in the code above)
        
        # Title position
        title_text = "WELCOME TO THE NOTTY GAME!"
        title_colors = [pygame.Color('red'), pygame.Color('yellow'), pygame.Color('blue'), pygame.Color('green')]
        title_pos = (
            (WINDOW_WIDTH - sum([pygame.font.Font('Fonts/PressStart2P-Regular.ttf', 36).render(c, True, title_colors[i % len(title_colors)]).get_width() for i, c in enumerate(title_text)])) // 2,
            100
        )
        title = MulticolorLabel(title_text, title_pos, title_colors)
        self.objects.append(title)


        # Number of players
        num_players_label = Label('NUMBER OF PLAYERS:', (0, 0), pygame.Color('white'))
        num_players_label.pos = (
            (WINDOW_WIDTH - num_players_label.font.size('Number of players:')[0]) // 2,
            200
        )
        self.objects.append(num_players_label)

        # Player number buttons
        btn_padding = 50  # Space between buttons
        btn_width = 50  # Approximate width of buttons
        total_btn_width = 2 * btn_width + btn_padding

        self.objects.append(PlayerNumberLabel(
            '2',
            ((WINDOW_WIDTH - total_btn_width) // 2, 400),
            pygame.Color('white'),
            pygame.Color('red')
        ))

        self.objects.append(PlayerNumberLabel(
            '3',
            ((WINDOW_WIDTH + btn_width) // 2, 400),
            pygame.Color('white'),
            pygame.Color('red')
        ))

        # Rules button
        rules_text = "CLICK HERE TO READ THE GAME RULES!"
        rules_label = RuleLabel(rules_text, (0, 0), pygame.Color('white'), pygame.Color('red'))
        rules_label.pos = (
            (WINDOW_WIDTH - rules_label.font.size(rules_text)[0]) // 2,
            600
        )
        self.objects.append(rules_label)

        ai_label = Label('SELECT AI OPPONENTS:', (0, 0), pygame.Color('white'))
        text_width, _ = ai_label.font.size('SELECT AI OPPONENTS:')
        ai_label.pos = (
            (WINDOW_WIDTH - text_width) // 2,
            350
        )
        self.objects.append(ai_label)

        # AI type buttons
        ai_types = ['Aggressive', 'Defensive', 'Balanced']
        btn_x_start = (WINDOW_WIDTH - (len(ai_types) * 100 + (len(ai_types) - 1) * 50)) // 2
        for idx, ai_type in enumerate(ai_types):
            self.objects.append(AITypeLabel(
                ai_type,
                (btn_x_start + idx * 150, 400),
                pygame.Color('white'),
                pygame.Color('red')
            ))

class AITypeLabel(ClickableLabel):
    selected_ai = []

    def click(self):
        if self.text in self.selected_ai:
            self.selected_ai.remove(self.text)
            self.colour1 = pygame.Color('white')
        else:
            self.selected_ai.append(self.text)
            self.colour1 = pygame.Color('yellow')


class RuleScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('black'))
        
        # Title at the top center
        title = "Description of the Game"
        font_size_title = 28  # Font size for the title
        title_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', font_size_title)
        title_width = title_font.size(title)[0]
        title_x = (WINDOW_WIDTH - title_width) // 2  # Center the title horizontally
        self.objects.append(Label(
            title,
            (title_x, 20),  # Position near the top
            pygame.Color('white'),
            font_size_title
        ))
        
        # Rules text
        rules = [
            "Each card has a colour (red, blue, green, or yellow) and a number (1 to 10).",
            
            "There are exactly two cards for each combination of colour and number, making a total of 80 cards in the deck.",
            "At the beginning of the game, the deck is shuffled, and each player is dealt 5 cards.",
            "Players take turns. On a player’s turn, they can perform any of the following actions:",
            "1. (At most once per turn) Draw up to 3 cards from the deck.",
            "2. (At most once per turn) Choose another player and take a random card from them.",
            "3. (Any number of times per turn) Discard a valid group of cards. A valid group is either:",
            "   a. A sequence of at least three cards of the same colour with consecutive numbers.",
            "   b. A set of at least three cards of the same number but different colours.",
            "The first player to empty their hand wins the game."
        ]

        # Font size and line spacing
        font_size_text = 18  # Smaller font size for text
        line_spacing = 8
        margin = 50
        available_width = WINDOW_WIDTH - 2 * margin

        # Calculate total height of the text
        total_height = 0
        wrapped_lines = []
        for rule in rules:
            lines = self.wrap_text(rule, font_size_text, available_width)
            wrapped_lines.append(lines)
            total_height += len(lines) * (font_size_text + line_spacing)

        # Render the wrapped text
        y_position = 100  # Start below the title
        for lines in wrapped_lines:
            for line in lines:
                self.objects.append(Label(
                    line,
                    (margin, y_position),
                    pygame.Color('white'),
                    font_size_text
                ))
                y_position += font_size_text + line_spacing

        # Add Back button
        self.objects.append(NewGameLabel(
            'Back',
            (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - margin),
            pygame.Color('white'),
            pygame.Color('red')
        ))

    def wrap_text(self, text, font_size, max_width):
        """Wrap text into lines that fit within the given max_width."""
        font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', font_size)
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        lines.append(current_line)  # Add the last line
        return lines
    

class PlayScreen(ScreenBase):
    def __init__(self, num_players):
        super().__init__()
        self.num_players = num_players
        self.card_images = load_card_images()
        self.deck = Deck(self.card_images)
        self.players = []
        self.current_player_index = 0
        self.font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 18)
        self.message = ""
        self.message_timer = 0

    def display_message(self, text, duration=2000):
        self.message = text
        self.message_timer = pygame.time.get_ticks() + duration

        # Initialize players
        self.players.append(HumanPlayer("You"))

        ai_class_map = {
            'Aggressive': AggressiveAIPlayer,
            'Defensive': DefensiveAIPlayer,
            'Balanced': BalancedAIPlayer
        }
        for i, ai_type in enumerate(ai_types):
            ai_class = ai_class_map.get(ai_type, AIPlayer)
            self.players.append(ai_class(f"AI {i + 1}"))


        # Deal initial hands
        for player in self.players:
            player.draw_cards(self.deck, 5)

        # Positioning variables
        self.player_hand_y = WINDOW_HEIGHT - Card.CARD_HEIGHT - 20
        self.ai_hand_y = 20
        self.hand_spacing = 10

        # Initialize UI elements (buttons, etc.)
        # We'll add these in the next steps

    def handle_event(self, event):
        # Handle user input
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in self.buttons:
                if button.is_clicked(mouse_pos):
                    self.handle_action(button.action)
                    return  # Action handled

            # Check if any cards are clicked
            self.handle_card_click(mouse_pos)
        pass

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
            elif action == 'discard':
                selected_cards = [card for card in current_player.hand if card.selected]
                if current_player.can_discard_group(selected_cards):
                    current_player.discard_group(selected_cards, self.deck)
                    # Deselect cards
                    for card in selected_cards:
                        card.selected = False
                else:
                    print("Invalid group selected.")
            elif action == 'play_for_me':
                # Implement AI logic to take over
                ai_player = AIPlayer(current_player.name)
                ai_player.hand = current_player.hand.copy()
                ai_player.choose_action({'players': self.players, 'deck': self.deck})
                current_player.hand = ai_player.hand.copy()
                current_player.actions_taken = ai_player.actions_taken.copy()
        else:
            self.display_message("Action not available.")


    def handle_card_click(self, mouse_pos):
        current_player = self.players[self.current_player_index]
        if isinstance(current_player, HumanPlayer):
            for card in current_player.hand:
                if card.is_clicked(mouse_pos):
                    card.selected = not card.selected
                    break


    def update(self):
        current_player = self.players[self.current_player_index]
        if isinstance(current_player, HumanPlayer):
        # Update buttons based on actions taken
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
                if self.message and pygame.time.get_ticks() > self.message_timer:
                    self.message = ""

    # Check for winner
        winner = self.check_winner()
        if winner:
            global current_screen
            current_screen = WinnerScreen(winner.name)
            return        
        
    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.players[self.current_player_index].reset_actions()

    def check_winner(self):
        for player in self.players:
            if not player.hand:
                return player
        return None



    def draw(self, screen):
        screen.fill((0, 128, 0))  # Green background
        self.draw_hands(screen)

        for button in self.buttons:
            button.draw(screen)
        # Draw other UI elements
        # We'll add these later
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

        # Draw human player's name
        name_text = self.font.render(self.players[0].name, True, (255, 255, 255))
        screen.blit(name_text, (50, self.player_hand_y - 30))


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


class WinnerScreen(ScreenBase):
    def __init__(self, winner_name):
        super().__init__(pygame.Color('black'))
        self.winner_name = winner_name
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

class PlayAgainLabel(ClickableLabel):
    def click(self):
        global current_screen
        current_screen = StartScreen()

class ExitLabel(ClickableLabel):
    def click(self):
        global game_over
        game_over = True
