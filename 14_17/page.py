import pygame
from pygame.locals import *
import random
from main import Game
import random
import pygame.mixer


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

game_over = False
current_screen = None
num_player = 0


class VisualObject:
    def __init__(self):
        pass

    def draw(self, screen):
        pass

    def update(self):
        pass

    def mouseup(self, event):
        pass

class MulticolorLabel(VisualObject):
    def __init__(self, text, pos, colors):
        self.text = text
        self.pos = pos
        self.colors = colors
        self.font = pygame.font.Font('PressStart2P-Regular.ttf', 36)

    def draw(self, screen):
        x, y = self.pos
        for i, char in enumerate(self.text):
            img = self.font.render(char, True, self.colors[i % len(self.colors)])
            screen.blit(img, (x, y))
            x += img.get_width()


class Label(VisualObject):
    def __init__(self, text, pos, colour, head):
        self.text = text
        self.pos = pos
        self.colour = colour
        if head == 'title':
            self.font = pygame.font.Font('PressStart2P-Regular.ttf', 60)
        elif head == 'heading':
            self.font = pygame.font.Font('PressStart2P-Regular.ttf', 18)
        elif head == 'body':
            self.font = pygame.font.Font('PressStart2P-Regular.ttf', 10)

    def draw(self, screen):
        img = self.font.render(self.text, True, self.colour)
        self.width = img.get_width()
        self.height = img.get_height()
        screen.blit(img, self.pos)


class ClickableLabel(Label):
    def __init__(self, text, pos, colour1, colour2, head):
        super().__init__(text, pos, colour1, head)
        self.colour1 = colour1
        self.colour2 = colour2

    def is_inside(self, pos):
        return self.pos[0] <= pos[0] <= self.pos[0] + self.width \
            and self.pos[1] <= pos[1] <= self.pos[1] + self.height

    def update(self):
        if self.is_inside(pygame.mouse.get_pos()):
            self.colour = self.colour2
        else:
            self.colour = self.colour1

    def mouseup(self, event):
        if event.button == 1 and self.is_inside(event.pos):
            self.click()

    def click(self):
        pass


class PlayerNumberLabel(ClickableLabel):
    def click(self):
        global num_players
        global current_screen
        if self.text == '2':
            num_players = 2
        elif self.text == '3':
            num_players = 3
        current_screen = AIStyleSelectionScreen(num_players)




class RuleLabel(ClickableLabel):
    def click(self):
        global game_over, num_player
        global current_screen
        current_screen = RuleScreen()

        if isinstance(current_screen, AIStyleSelectionScreen):
            ai_style = current_screen.selected_ai_style
            if ai_style is not None:
                print(f"Starting game with {num_player} players and AI style: {ai_style}")
                card_game = Game(num_player, ai_style)  # 确保这里传递了正确的参数
                card_game.run()
                game_over = True
            else:
                print("No AI style selected. Cannot start game.")
        else:
            print("Not in AI selection screen.")



class NewGameLabel(ClickableLabel):
    def click(self):
        global current_screen
        current_screen = StartScreen()


class CloseWindowLabel(ClickableLabel):
    def click(self):
        global game_over
        game_over = True


class ScreenBase:
    def __init__(self, background_colour, background_filename=None):
        self.background_colour = background_colour
        self.objects = []
        if background_filename is not None:
            self.background_image = pygame.image.load("images/background_image.jpg")
            self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
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

class AIStyleLabel(ClickableLabel):
    def click(self):
        global current_screen,selected_ai_style
        selected_ai_style = self.text
        print(f"Selected AI Style: {selected_ai_style}")
        if isinstance(current_screen, AIStyleSelectionScreen):
            current_screen.set_ai_style(self.text)  # 保存用户选择的 AI 风格
        else:
            print("Not in AI selection screen.")


class AIStyleSelectionScreen(ScreenBase):
    def __init__(self, num_players):
        super().__init__(pygame.Color('black'))
        self.num_players = num_players
        self.selected_ai_style = None  # 用于存储选择的风格

        self.objects.append(Label(
            "Choose the AI Style for the Game!",  # 显示的文字
            (300 , 150),  # 文本位置（居中显示）
            pygame.Color('white'),  # 字体颜色
            'heading'  # 字体样式
        ))

        # 添加风格选择按钮
        ai_styles = ['Aggressive', 'Defensive', 'Balanced']
        for idx, style in enumerate(ai_styles):
            self.objects.append(AIStyleLabel(
                style,
                (500, 300 + idx * 50),
                pygame.Color('white'),
                pygame.Color('yellow')
            ,'heading'))

    def set_ai_style(self, ai_style):
        self.selected_ai_style = ai_style
        print(f"AI style selected: {ai_style}")
        global current_screen
        current_screen = PlayScreen(self.num_players, self.selected_ai_style)  # 跳转到游戏界面


class AITypeButton(ClickableLabel):
    def __init__(self, text, pos, screen):
        super().__init__(text, pos, pygame.Color('white'), pygame.Color('yellow'),'heading')
        self.screen = screen

    def click(self):
        self.screen.selected_ai_style = self.text  # 记录选择的风格
        print(f"Selected AI Style: {self.text}")
        self.screen.start_game()  # 直接开始游戏

class StartScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('black'))


        pygame.mixer.init()
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)




        title_text = "WELCOME TO THE NOTTY GAME!"
        title_colors = [pygame.Color('red'), pygame.Color('yellow'), pygame.Color('blue'), pygame.Color('green')]
        title_pos = (WINDOW_WIDTH // 2 - 450, 100)
        self.objects.append(MulticolorLabel(title_text, title_pos, title_colors))


        self.objects.append(Label("NUMBER OF PLAYERS:", (430, 200), pygame.Color('white'), 'heading'))


        self.objects.append(PlayerNumberLabel('2', (520, 350), pygame.Color('white'), pygame.Color('red'), 'heading'))
        self.objects.append(PlayerNumberLabel('3', (620, 350), pygame.Color('white'), pygame.Color('red'), 'heading'))


        self.objects.append(RuleLabel("CLICK HERE TO READ THE GAME RULES!", (290, 500), pygame.Color('white'), pygame.Color('red'), 'heading'))



class PlayScreen(ScreenBase):
    def __init__(self, num_players, ai_style):
        super().__init__(pygame.Color('blue'), 'images/background_image.jpg')
        self.game = Game(num_players, ai_style)  # 使用选择的 AI 风格初始化游戏
        self.game.run()
        global num_player
        self.objects.append(Label('Notty', (500, 200), pygame.Color('black'), 'title'))
        if num_player == 2:
            self.objects.append(Label('2 players Game (1 CPU)', (100, 300), pygame.Color('white'), 'heading'))
        if num_player == 3:
            self.objects.append(Label('3 players Game (2 CPU)', (100, 300), pygame.Color('white'), 'heading'))
        self.objects.append(
            StartGameLabel('Start a game', (300, 400), pygame.Color('white'), pygame.Color('red'), 'heading'))
        self.objects.append(NewGameLabel('Back', (300, 500), pygame.Color('white'), pygame.Color('red'), 'heading'))

class StartGameLabel(ClickableLabel):
    def click(self):
        global game_over, num_player
        global current_screen  # 确保能够访问当前屏幕对象

        if isinstance(current_screen, AIStyleSelectionScreen):
            ai_style = current_screen.selected_ai_style
            if ai_style is not None:
                print(f"Starting game with {num_player} players and AI style: {ai_style}")
                card_game = Game(num_player, ai_style)
                card_game.run()
                game_over = True
            else:
                print("No AI style selected. Cannot start game.")
        else:
            print("Not in AI selection screen.")

class RuleScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('Black'))
        self.objects.append(Label('Description of the Game', (50, 50), pygame.Color('yellow'), 'heading'))
        self.objects.append(
            Label('Each card has a colour (red, blue, green, or yellow) and a number (1 to 10).', (100, 100),
                  pygame.Color('white'), 'body'))
        self.objects.append(Label(
            'There are exactly two cards for each combination of colour and number, making a total of 80 cards in the deck.',
            (100, 150), pygame.Color('white'), 'body'))
        self.objects.append(Label('Gameplay', (50, 200), pygame.Color('yellow'), 'heading'))
        self.objects.append(
            Label('At the beginning of the game, the deck is shuffled, and each player is dealt 5 cards.', (100, 250),
                  pygame.Color('white'), 'body'))
        self.objects.append(
            Label('Players take turns.  On a player’s turn, they can perform any of the following actions:', (100, 300),
                  pygame.Color('white'), 'body'))
        self.objects.append(
            Label('1. (At most once per turn) Draw up to 3 cards from the deck.', (150, 350), pygame.Color('white'),
                  'body'))
        self.objects.append(
            Label('2. (At most once per turn) Choose another player and take a random card from them.', (150, 400),
                  pygame.Color('white'), 'body'))
        self.objects.append(
            Label('3. (Any number of times per turn) Discard a valid group of cards. A valid group is either:',
                  (150, 450), pygame.Color('white'), 'body'))
        self.objects.append(
            Label('a. A sequence of at least three cards of the same colour with consecutive numbers', (200, 500),
                  pygame.Color('white'), 'body'))
        self.objects.append(
            Label('b. A set of at least three cards of the same number but different colours', (200, 550),
                  pygame.Color('white'), 'body'))
        self.objects.append(
            Label('The first player to empty their hand wins the game.', (100, 600), pygame.Color('white'), 'body'))
        self.objects.append(NewGameLabel('Back', (50, 630), pygame.Color('yellow'), pygame.Color('red'), 'heading'))


class MainScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('black'))


class GameOverScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('blue'))
        self.objects.append(Label('Notty', (500, 200), pygame.Color('black'), 'title'))
        self.objects.append(Label('Player X Wins', (500, 300), pygame.Color('white'), 'heading'))
        self.objects.append(
            NewGameLabel('Start a new game', (100, 400), pygame.Color('white'), pygame.Color('red'), 'heading'))
        self.objects.append(
            CloseWindowLabel('Close the window', (100, 500), pygame.Color('white'), pygame.Color('red'), 'heading'))

    def keydown(self, event):
        if event.key == K_ESCAPE:
            global game_over
            game_over = True


def run_game():
    global current_screen

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption('Notty')

    current_screen = StartScreen()

    while not game_over:
        # Handling the events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                current_screen.keydown(event)
            elif event.type == MOUSEBUTTONUP:
                current_screen.mouseup(event)

        # Rendering the picture
        current_screen.draw(screen)

        pygame.display.flip()

        # Updating the objects
        current_screen.update()

        # A delay
        pygame.time.wait(10)


run_game()
pygame.quit()