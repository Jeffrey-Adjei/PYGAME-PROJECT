from hand import *
from card import *
from CardDeck import *
from button import *
from OpponentSelectionWindow import *
from setting import *
import ctypes, pygame, sys, time
from pygame import *

class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()

        # 初始化玩家
        self.players = [
            Hand("self_player", 400, 520),
            Hand("left_player", 100, 150),
            Hand("right_player", 800, 150)
        ]

        # 初始化牌组
        self.deck = CardDeck()
        self.deck.shuffle()

        # 背景图片
        self.floor_image = pygame.image.load("images/floor.png")
        self.wall_image = pygame.image.load("images/wall.png")
        self.table_image = pygame.image.load("images/table.png")
        self.wall_image = pygame.transform.scale(self.wall_image, (WIDTH, HEIGHT-200))
        self.floor_image = pygame.transform.scale(self.floor_image, (WIDTH, HEIGHT))
        self.table_image = pygame.transform.scale(self.table_image, (800, 400))

        # 创建发牌按钮
        self.deal_button = Button(
            rect=(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50),
            color=button_colour,
            text=" deal cards ",
            font=font_large,
            text_color= COLORS["Black"]
        )

        # 创建回合结束按钮
        self.end_turn_button = Button(
            rect=(WIDTH // 2 + 300, HEIGHT - 100, 200, 50),
            color=(0, 255, 0),  # 绿色按钮
            text="finish turn ",
            font=font_large,
            text_color= COLORS["Black"]
        )
        self.end_turn_button.hide()  # 初始化时隐藏按钮

        # 创建出牌按钮
        self.discard_button = Button(
            rect=(WIDTH // 2 + 300, HEIGHT - 160, 200, 50),
            color=(255, 140, 0),  # 绿色按钮
            text="discard",
            font=font_large,
            text_color= COLORS["Black"]
        )
        self.discard_button.hide()  # 初始化时隐藏按钮

        # 摸牌按钮
        self.remaining_draws = 3  # 每回合最多摸牌次数
        self.draw_card_button = Button(
            rect=(WIDTH // 2 + 300, HEIGHT - 280, 200, 50),
            color=(255, 140, 0),  # 橙色按钮
            text="Draw Card",
            font=font_large,
            text_color=COLORS["Black"]
        )
        self.draw_card_button.hide() # 初始化时隐藏按钮

        # 偷牌按钮
        self.steal_card_button = Button(
            rect=(WIDTH // 2 + 300, HEIGHT - 220, 200, 50),
            color=(200, 0, 255),  # 紫色按钮
            text="Steal Card",
            font=font_large,
            text_color=COLORS["Black"]
        )
        self.steal_card_button.hide()  # 初始隐藏
        self.selecting_opponent = False  # 是否正在选择对手
        self.selected_opponent = None  # 当前选中的对手

        self.selected_cards = []  # 当前选中的牌

        self.dealing_cards = False
        self.current_player_index = 0

        self.current_turn = 0  # 当前回合的玩家索引
        self.total_players = len(self.players)  # 总玩家数



    def next_turn(self):
        """切换到下一个玩家的回合"""
        self.current_turn = (self.current_turn + 1) % self.total_players
        print(f"Now is the turn of {self.players[self.current_turn].name} ")
        self.remaining_draws = 3  # 重置摸牌次数

        # 更新按钮的显隐状态
        if self.current_turn == 0:  # 自己的回合
            self.end_turn_button.show()
            self.discard_button.show()
            self.draw_card_button.show()
            self.steal_card_button.show()
        else:  # AI 玩家回合
            self.end_turn_button.hide()
            self.discard_button.hide()
            self.draw_card_button.hide()
            self.steal_card_button.hide()
            self.selecting_opponent = False
            self.selected_opponent = None

        # 在切换回合后立即更新显示
        self.update_display()

        # 如果是 AI 玩家，立即行动
        if self.current_turn != 0:
            self.ai_doing(self.current_turn)

    def update_display(self):
        """更新屏幕显示的所有内容
        self.screen.fill(BG_COLOUR)
        pygame.draw.ellipse(self.screen, TABLE_COLOR, TABLE_Parameter)
        """


        # 绘制墙壁和地板背景
        self.screen.blit(self.floor_image, (0, HEIGHT // 2))  # 地板背景
        self.screen.blit(self.wall_image, (0, 0))  # 墙壁背景

        # 绘制桌子
        table_x = (WIDTH - self.table_image.get_width()) // 2
        table_y = (HEIGHT - self.table_image.get_height()) // 2 + 100
        self.screen.blit(self.table_image, (table_x, table_y))

        # 绘制按钮
        self.deal_button.draw(self.screen)
        if self.current_turn == 0:
            self.end_turn_button.draw(self.screen)
            self.discard_button.draw(self.screen)
            self.draw_card_button.draw(self.screen)
            draw_count_text = font_large.render(f"Draws Left: {self.remaining_draws}", True, COLORS["Black"])
            self.screen.blit(draw_count_text, (WIDTH // 2 + 310, HEIGHT - 320))
            self.steal_card_button.draw(self.screen)

        # 显示当前回合
        turn_text = font_large.render(f"Now is the turn of: {self.players[self.current_turn].name}", True, COLORS["Black"])
        self.screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, 50))

        for player in self.players:
            player.draw_name(self.screen)

        # 绘制手牌，放大选中牌
        for player in self.players:
            player.draw(self.screen, selected_cards=self.selected_cards)

        pygame.display.flip()  # Update the display

    def ai_doing(self, player_index):
        """
            模拟 AI 玩家行动
            :param player_index: 当前 AI 玩家索引
            """
        player = self.players[player_index]
        if player.cards:  # 确保玩家有牌

            pygame.time.wait(1000)  # 暂停1秒

            # 随机选择一张牌作为出牌
            selected_card = random.choice(player.cards)
            print(f"{player.name} played {selected_card}")
            # 模拟出牌逻辑（移除牌）
            player.cards.remove(selected_card)

            pygame.time.wait(1000)

        # 切换到下一个玩家回合
        self.next_turn()

    def shuffle_and_steal_card(self, opponent):
        """展示对手手牌背面并让玩家选择一张"""

        print(f"Shuffling {opponent.name}'s cards...")
        random.shuffle(opponent.cards)  # 洗牌

        # 显示对手手牌背面
        temp_positions = []
        for i, card in enumerate(opponent.cards):
            card.x = WIDTH // 2 - len(opponent.cards) * 26 + i * 65
            card.y = HEIGHT // 2
            temp_positions.append((card.x, card.y))

        while True:
            # 清理屏幕并绘制背景
            self.screen.fill(BACKGROUND_COLOR)

            # 绘制提示文字
            tap_text = GAME_FONT.render("The cards are shuffled, please select one!", True, COLORS["Black"])
            self.screen.blit(tap_text, (WIDTH // 2 - tap_text.get_width() // 2, HEIGHT // 2 - 150))

            for card, pos in zip(opponent.cards, temp_positions):
                pygame.draw.rect(self.screen, COLORS["Black"], (pos[0], pos[1], card.width, card.height), 2)
                card.draw(self.screen, back=True)

            pygame.display.flip()  # 强制刷新显示内容

            # 等待玩家选择一张卡
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
                            return  # 选择完成后退出方法

    def run(self):
        # Time variables
        self.start_time = pygame.time.get_ticks()
        self.last_deal_time = pygame.time.get_ticks()
        self.deal_complete_time = None  # 记录发牌完成的时间


        while True:
            # handle quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 按钮点击事件
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    # 如果点击发牌按钮且轮到当前玩家
                    if self.deal_button.handle_click(event.pos):
                        self.deal_button.hide()
                        self.dealing_cards = True
                        self.deal_complete_time = pygame.time.get_ticks() # 记录发牌完成的开始时间

                    # 点击“回合结束”按钮时切换回合
                    if self.current_turn == 0 and self.end_turn_button.handle_click(event.pos):
                        self.next_turn()

                    # 点击手牌
                    if self.current_turn == 0:
                        clicked_card = self.players[0].get_card_at(event.pos)
                        if clicked_card:
                            if clicked_card in self.selected_cards:
                                # 如果牌已被选中，则取消选中
                                self.selected_cards.remove(clicked_card)
                            else:
                            # 如果牌未被选中，则选中
                                self.selected_cards.append(clicked_card)  # 设置选中的牌

                    # 点击“出牌”按钮
                    if self.current_turn == 0 and self.discard_button.handle_click(event.pos):
                        if self.selected_cards:
                            # 从手牌中移除选中的牌
                            for card in self.selected_cards:
                                self.players[0].cards.remove(card)
                            self.selected_cards = []  # 清空选中列表

                    # 处理摸牌按钮点击
                    if self.current_turn == 0 and self.remaining_draws > 0:
                        if self.draw_card_button.handle_click(event.pos):
                            card = self.deck.draw_card()
                            if card:
                                self.players[self.current_turn].add_card(card)
                                self.remaining_draws -= 1
                                print(f"Drew card: {card}. Remaining draws: {self.remaining_draws}")

                    # 处理偷牌按钮点击
                    if self.current_turn == 0 and self.steal_card_button.handle_click(event.pos):
                        print("Steal card button clicked.")
                        opponent_window = OpponentSelectionWindow(
                            self.screen,
                            [player for i, player in enumerate(self.players) if i != self.current_turn],
                            font_large
                        )

                        # 显示对手选择窗口
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
                        self.shuffle_and_steal_card(selected_opponent)

            # 如果是 AI 玩家回合，自动行动
            if self.current_turn != 0:  # 当前是 AI 玩家回合
                print(self.current_turn)
                self.ai_doing(self.current_turn)

            # 发牌完成后等待两秒再显示按钮
            if self.deal_complete_time:
                current_time = pygame.time.get_ticks()
                if current_time - self.deal_complete_time > 4500:  # 等待两秒
                    self.end_turn_button.show()
                    self.discard_button.show()
                    self.draw_card_button.show()
                    self.deal_complete_time = None  # 重置以防止重复显示按钮
                    self.steal_card_button.show()

            if self.selecting_opponent:
                for i, player in enumerate(self.players):
                    if i != self.current_turn:  # 排除自己
                        # 检查鼠标是否点击到玩家名字或手牌区域
                        if player.get_card_at(event.pos):  # 模拟点击区域检测
                            self.selected_opponent = player
                            self.selecting_opponent = False
                            print(f"Selected opponent: {player.name}")
                            self.shuffle_and_steal_card(player)

            self.update_display()
            # 控制帧率
            self.clock.tick(FPS)
            '''
            # 绘制牌桌
            self.screen.fill(BG_COLOUR)
            pygame.draw.ellipse(
                self.screen,
                TABLE_COLOR,
                TABLE_Parameter,
            )
            
            # 绘制按钮
            self.deal_button.draw(self.screen)
            if self.current_turn == 0:
                self.end_turn_button.draw(self.screen)
                self.discard_button.draw(self.screen)
            '''
            if self.dealing_cards:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_deal_time > deal_delay and self.deck.cards:
                    # 给当前玩家发一张牌
                    card = self.deck.draw_card()
                    if card:
                        self.players[self.current_player_index].add_card(card)

                    # 更新发牌状态
                    self.current_player_index = (self.current_player_index + 1) % len(self.players)
                    self.last_deal_time = current_time

                    # 检查是否发完所有牌
                    if all(len(player.cards) == cards_per_player for player in self.players):
                        self.dealing_cards = False
                        self.current_turn = 0  # 发牌完成后进去自己的回合
'''
            print(self.current_turn)

            # 显示当前回合
            turn_text = font_large.render(f"Now is the turn of : {self.players[self.current_turn].name}", True, COLORS["Black"])
            print(f"Now is the turn of : {self.players[self.current_turn].name}")
            self.screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, 50))
'''










if __name__ == '__main__':
    game = Game()
    game.run()

