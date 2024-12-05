from hand import *
from card import *
from CardDeck import *
from button import *
from select_opponent_window import *
from select_card_window import *
from setting import *
from page import *
from action_memory_window import *
from new import *
import ctypes, pygame, sys, time
from pygame import *



# The project code structure refers to open source project pokerhands: https://github.com/notaSWE/pokerhands
# and the video course on YouTube: https://www.youtube.com/watch?v=uwgRf51YUGY&t=2050s

class Game:
    def __init__(self,num_player):
        self.player_number = num_player
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()

        if  self.player_number == 2:
            self.players = [
                Hand("self_player", 400, 500),
                Hand("left_player", 100, 150),
            ]
        if self.player_number == 3:
            self.players = [
                Hand("self_player", 400, 500),
                Hand("left_player", 100, 150),
                Hand("right_player", 800, 150)
            ]

        self.action_log = action_memory_window(self.screen, font_large)

        self.deck = CardDeck()
        self.deck.shuffle()


        self.floor_image = pygame.image.load("images/floor.png")
        self.wall_image = pygame.image.load("images/wall.png")
        self.table_image = pygame.image.load("images/table.png")
        self.wall_image = pygame.transform.scale(self.wall_image, (WIDTH, HEIGHT-200))
        self.floor_image = pygame.transform.scale(self.floor_image, (WIDTH, HEIGHT))
        self.table_image = pygame.transform.scale(self.table_image, (800, 400))


        self.deal_button = Button(
            rect=(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50),
            color=button_colour,
            text=" deal cards ",
            font=font_large,
            text_color= COLORS["Black"]
        )


        self.finish_turn_button = Button(
            rect=(WIDTH // 2 + 300, HEIGHT - 100, 200, 50),
            color=(0, 255, 0),
            text="finish turn ",
            font=font_large,
            text_color= COLORS["Black"]
        )
        self.finish_turn_button.hide()  # Hide the button


        self.discard_button = Button(
            rect=(WIDTH // 2 + 300, HEIGHT - 160, 200, 50),
            color=(255, 140, 0),  # blue
            text="discard",
            font=font_large,
            text_color= COLORS["Black"]
        )
        self.discard_button.hide()

        self.if_have_drew = True
        self.remaining_draws = 3
        self.draw_card_button = Button(
            rect=(WIDTH // 2 + 300, HEIGHT - 280, 200, 50),
            color=(255, 140, 0),
            text="Draw Card",
            font=font_large,
            text_color=COLORS["Black"]
        )
        self.draw_card_button.hide()


        self.steal_card_button = Button(
            rect=(WIDTH // 2 + 300, HEIGHT - 220, 200, 50),
            color=(200, 0, 255),  # purple
            text="Steal Card",
            font=font_large,
            text_color=COLORS["Black"]
        )
        self.steal_card_button.hide()
        self.selecting_opponent = False
        self.selected_opponent = None
        self.if_have_steal = True  # once each turn

        self.selected_cards = []

        self.dealing_cards = False
        self.current_player_index = 0

        self.current_turn = 0
        self.all_players = len(self.players)



    def next_turn(self):
        # to the next player's turn
        self.current_turn = (self.current_turn + 1) % self.all_players
        print(f"Now is the turn of {self.players[self.current_turn].name} ")
        self.if_have_drew = True
        self.remaining_draws = 3


        if self.current_turn == 0:
            self.finish_turn_button.show()
            self.discard_button.show()
            self.draw_card_button.show()
            self.steal_card_button.show()
        else:
            self.finish_turn_button.hide()
            self.discard_button.hide()
            self.draw_card_button.hide()
            self.steal_card_button.hide()
            self.selecting_opponent = False
            self.selected_opponent = None


        self.update_screen()


        if self.current_turn != 0:
            self.ai_doing(self.current_turn)

    # update all display on screen
    def update_screen(self):

        # Draw wall and floor backgrounds
        self.screen.blit(self.floor_image, (0, HEIGHT // 2))
        self.screen.blit(self.wall_image, (0, 0))


        table_x = (WIDTH - self.table_image.get_width()) // 2
        table_y = (HEIGHT - self.table_image.get_height()) // 2 + 100
        self.screen.blit(self.table_image, (table_x, table_y))

        # Draw buttons
        self.deal_button.draw(self.screen)
        if self.current_turn == 0:
            self.finish_turn_button.draw(self.screen)
            self.discard_button.draw(self.screen)
            self.draw_card_button.draw(self.screen)
            self.steal_card_button.draw(self.screen)


        turn_text = font_large.render(f"Now is the turn of: {self.players[self.current_turn].name}", True, COLORS["Black"])
        self.screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, 50))

        for player in self.players:
            player.draw_name(self.screen)


        for player in self.players:
            player.draw(self.screen, selected_cards=self.selected_cards)

        self.action_log.draw()

        pygame.display.flip()

    def ai_doing(self, player_index):
        # ai's logic
        player = self.players[player_index]
        if player.cards:  # check if True

            if player.cards:
                # 优先检查是否可以形成有效组合
                valid_group = player.find_valid_group()
                if valid_group:
                    for card in valid_group:
                        player.cards.remove(card)
                    print(f"{player.name} formed a valid group and discarded: {valid_group}")
                    self.action_log.add_log(f"{player.name} formed and discarded: {valid_group}")
                else:
                    # 如果没有有效组合，随机选择抽牌或偷牌
                    action = random.choice(["draw", "steal"])
                    if action == "draw":
                        drawn_card = self.deck.draw_card()
                        if drawn_card:
                            player.add_card(drawn_card)
                            print(f"{player.name} drew a card: {drawn_card}")
                            self.action_log.add_log(f"{player.name} drew: {drawn_card}")
                    elif action == "steal":
                        opponents = [p for p in self.players if p != player and p.cards]
                        if opponents:
                            opponent = random.choice(opponents)
                            self.shuffle_when_steal_card(opponent)
                            print(f"{player.name} stole a card from {opponent.name}")
                            self.action_log.add_log(f"{player.name} stole a card from {opponent.name}")


        self.next_turn()

    # steal after shuffle
    # this complex logic refers to functions from https://github.com/vannov/pygame_cards
    def shuffle_when_steal_card(self, opponent):

        print(f"Shuffling {opponent.name}'s cards...")
        random.shuffle(opponent.cards)

        # 如果当前玩家是AI（不是玩家），随机选择一张卡牌
        if self.current_turn != 0:  # AI的回合
            if opponent.cards:
                stolen_card = random.choice(opponent.cards)  # 从对手牌中随机选择一张
                self.players[self.current_turn].add_card(stolen_card)
                opponent.cards.remove(stolen_card)
                print(f"{self.players[self.current_turn].name} stole {stolen_card} from {opponent.name}.")
                self.action_log.add_log(
                    f"{self.players[self.current_turn].name} stole {stolen_card} from {opponent.name}."
                )
            return

        # display the card_back
        temp_positions = []
        for i, card in enumerate(opponent.cards):
            card.x = WIDTH // 2 - len(opponent.cards) * 26 + i * 65
            card.y = HEIGHT // 2
            temp_positions.append((card.x, card.y))

        while True:
            self.screen.fill(BACKGROUND_COLOR)

            tap_text = GAME_FONT.render("The cards are shuffled, please select one!", True, COLORS["Black"])
            self.screen.blit(tap_text, (WIDTH // 2 - tap_text.get_width() // 2, HEIGHT // 2 - 150))

            for card, pos in zip(opponent.cards, temp_positions):
                pygame.draw.rect(self.screen, COLORS["Black"], (pos[0], pos[1], card.width, card.height), 2)
                card.draw(self.screen, back=True)

            pygame.display.flip()

            # choose one card
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for card, pos in zip(opponent.cards, temp_positions):
                        rect = pygame.Rect(pos[0], pos[1], card.width, card.height)
                        if rect.collidepoint(event.pos):
                            print(f"Selected card: {card}")
                            self.players[self.current_turn].add_card(card)
                            opponent.cards.remove(card)
                            return

    def run(self):
        # Time variables
        self.start_time = pygame.time.get_ticks()
        self.last_deal_time = pygame.time.get_ticks()
        self.deal_complete_time = None


        while True:
            # handle quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # most of  button click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    # deal card button
                    if self.deal_button.handle_click(event.pos):
                        self.deal_button.hide()
                        self.dealing_cards = True
                        self.deal_complete_time = pygame.time.get_ticks()

                    # finish turn
                    if self.current_turn == 0 and self.finish_turn_button.handle_click(event.pos):
                        self.next_turn()

                    # click hand cards
                    if self.current_turn == 0:
                        clicked_card = self.players[0].get_card_at(event.pos)
                        if clicked_card:
                            if clicked_card in self.selected_cards:
                                self.selected_cards.remove(clicked_card)
                            else:
                                self.selected_cards.append(clicked_card)

                    # discard
                    if self.current_turn == 0 and self.discard_button.handle_click(event.pos):
                        if self.selected_cards:
                            # build a new temp object
                            temp_hand = Hand("temp_hand", 0, 0)
                            temp_hand.cards = self.selected_cards

                            if temp_hand.is_valid_group():  # use is_valid_group
                                for card in self.selected_cards:
                                    self.players[0].cards.remove(card)
                                    self.action_log.add_log(f"{self.players[0].name} discarded {card}.")
                                self.selected_cards = []
                            else:

                                print("Invalid group of cards selected. Please try again.")
                                self.action_log.add_log("Invalid group of cards selected.")

                    # draw card
                    if self.current_turn == 0 and self.if_have_drew:
                        if self.draw_card_button.handle_click(event.pos):

                            selection_window = select_card_window(self.screen, font_large)
                            selected_number = None
                            while selected_number is None:
                                selection_window.draw()
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                        selected_number = selection_window.handle_click(event.pos)

                            for _ in range(selected_number):
                                card = self.deck.draw_card()
                                if card:
                                    self.players[self.current_turn].add_card(card)
                                    print(f"Drew card: {card}")
                                    self.action_log.add_log(f"{self.players[self.current_turn].name} drew {card}.")

                            self.if_have_drew = False

                    # steal
                    if self.current_turn == 0 and self.if_have_steal:
                        if self.steal_card_button.handle_click(event.pos):
                            print("Steal card button clicked.")
                            self.if_have_steal = False
                            opponent_window = select_opponent_window(
                            self.screen,
                            [player for i, player in enumerate(self.players) if i != self.current_turn],
                            font_large
                        )

                            # window
                            selected_opponent = None
                            while not selected_opponent:
                                opponent_window.draw()
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                        selected_opponent = opponent_window.handle_click(event.pos)

                            print(f"Selected opponent: {selected_opponent.name}")
                            self.shuffle_when_steal_card(selected_opponent)
                            self.action_log.add_log(
                                f"{self.players[self.current_turn].name} stole a card from {selected_opponent.name}.")

            # ai turn
            if self.current_turn != 0:
                print(self.current_turn)
                self.ai_doing(self.current_turn)

            # show the button after some time
            if self.deal_complete_time:
                current_time = pygame.time.get_ticks()
                if current_time - self.deal_complete_time > 4500:
                    self.finish_turn_button.show()
                    self.discard_button.show()
                    self.draw_card_button.show()
                    self.deal_complete_time = None
                    self.steal_card_button.show()

            if self.selecting_opponent:
                for i, player in enumerate(self.players):
                    if i != self.current_turn:
                        if player.get_card_at(event.pos):
                            self.selected_opponent = player
                            self.selecting_opponent = False
                            print(f"Selected opponent: {player.name}")
                            self.shuffle_when_steal_card(player)

            self.update_screen()
            self.clock.tick(FPS)
            '''
            # Draw the card table
            self.screen.fill(BG_COLOUR)
            pygame.draw.ellipse(
                self.screen,
                TABLE_COLOR,
                TABLE_Parameter,
            )
            
            # Draw buttons
            self.deal_button.draw(self.screen)
            if self.current_turn == 0:
                self.end_turn_button.draw(self.screen)
                self.discard_button.draw(self.screen)
            '''

            # deal card logic
            if self.dealing_cards:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_deal_time > deal_delay and self.deck.cards:

                    card = self.deck.draw_card()
                    if card:
                        self.players[self.current_player_index].add_card(card)


                    self.current_player_index = (self.current_player_index + 1) % len(self.players)
                    self.last_deal_time = current_time


                    if all(len(player.cards) == cards_per_player for player in self.players):
                        self.dealing_cards = False
                        self.current_turn = 0
'''
            print(self.current_turn)

            
            turn_text = font_large.render(f"Now is the turn of : {self.players[self.current_turn].name}", True, COLORS["Black"])
            print(f"Now is the turn of : {self.players[self.current_turn].name}")
            self.screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, 50))
'''










if __name__ == '__main__':
    game = Game()
    game.run()

