import pygame
from pygame.locals import *
import random
from main import Game
import random
import pygame.mixer


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

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
        self.size = 36
        self.font = pygame.font.Font('PressStart2P-Regular.ttf', self.size)

    def draw(self, screen):
        x, y = self.pos
        for i, char in enumerate(self.text):
            img = self.font.render(char, True, self.colors[i % len(self.colors)])
            screen.blit(img, (x, y))
            x += img.get_width()


class Label(VisualObject):
    def __init__(self, text, pos, colour):
        self.text = text
        self.pos = pos
        self.colour = colour
        self.size = 30  # Adjust for the Press Start 2P font, as it's compact
        self.font = pygame.font.Font('PressStart2P-Regular.ttf', self.size)

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
        global num_player
        global current_screen
        if self.text == '2':
            num_player = 2
        elif self.text == '3':
            num_player = 3
        current_screen = PlayScreen()


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


class StartScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('black'))  # 使用黑色背景

        # 初始化音乐
        pygame.mixer.init()
        pygame.mixer.music.load('music.mp3')  # 替换为你的音乐路径
        pygame.mixer.music.play(-1)  # 无限循环播放音乐

        # 添加彩色标题
        title_text = "WELCOME TO THE NOTTY GAME!"
        title_colors = [pygame.Color('red'), pygame.Color('yellow'), pygame.Color('blue'), pygame.Color('green')]
        title_pos = (200, 50)  # 设置标题位置
        self.objects.append(MulticolorLabel(title_text, title_pos, title_colors))

        # 添加“玩家人数”标签
        self.objects.append(Label("NUMBER OF PLAYERS:", (500, 150), pygame.Color('white')))

        # 添加选择玩家人数按钮
        self.objects.append(PlayerNumberLabel('2', (500, 250), pygame.Color('white'), pygame.Color('red')))
        self.objects.append(PlayerNumberLabel('3', (600, 250), pygame.Color('white'), pygame.Color('red')))

        # 添加规则按钮
        self.objects.append(RuleLabel("CLICK HERE TO READ THE GAME RULES!", (400, 400), pygame.Color('white'), pygame.Color('red')))



class PlayScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('blue'), 'images/background_image.jpg')
        global num_player
        self.objects.append(Label('Notty', (500, 200), pygame.Color('black')))
        if num_player == 2:
            self.objects.append(Label('2 players Game (1 CPU)', (100, 300), pygame.Color('white')))
        if num_player == 3:
            self.objects.append(Label('3 players Game (2 CPU)', (100, 300), pygame.Color('white')))
        self.objects.append(
            StartGameLabel('Start a game', (300, 400), pygame.Color('white'), pygame.Color('red')))
        self.objects.append(NewGameLabel('Back', (300, 500), pygame.Color('white'), pygame.Color('red')))

class StartGameLabel(ClickableLabel):
    def click(self):
        global game_over, num_player
        # 初始化并运行卡牌游戏
        card_game = Game(num_player)
        card_game.run()
        # 返回到主菜单后结束当前游戏循环
        game_over = True

class RuleScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('blue'), 'Pictures/Saved Pictures/background_image.jpg')
        self.objects.append(Label('Description of the Game', (100, 50), pygame.Color('yellow')))
        self.objects.append(
            Label('Each card has a colour (red, blue, green, or yellow) and a number (1 to 10).', (150, 100),
                  pygame.Color('white')))
        self.objects.append(Label(
            'There are exactly two cards for each combination of colour and number, making a total of 80 cards in the deck.',
            (150, 150), pygame.Color('white')))

        self.objects.append(Label('Gameplay', (100, 200), pygame.Color('yellow')))
        self.objects.append(
            Label('At the beginning of the game, the deck is shuffled, and each player is dealt 5 cards.', (150, 250),
                  pygame.Color('white')))
        self.objects.append(
            Label('Players take turns.  On a player’s turn, they can perform any of the following actions:', (150, 300),
                  pygame.Color('white')))
        self.objects.append(
            Label('1. (At most once per turn) Draw up to 3 cards from the deck.', (200, 350), pygame.Color('white')))
        self.objects.append(
            Label('2. (At most once per turn) Choose another player and take a random card from them.', (200, 400),
                  pygame.Color('white')))
        self.objects.append(
            Label('3. (Any number of times per turn) Discard a valid group of cards. A valid group is either:',
                  (200, 450), pygame.Color('white')))
        self.objects.append(
            Label('a. A sequence of at least three cards of the same colour with consecutive numbers', (250, 500),
                  pygame.Color('white')))
        self.objects.append(
            Label('b. A set of at least three cards of the same number but different colours', (250, 550),
                  pygame.Color('white')))
        self.objects.append(
            Label('The first player to empty their hand wins the game.', (150, 600), pygame.Color('white')))
        self.objects.append(NewGameLabel('Back', (100, 630), pygame.Color('yellow'), pygame.Color('red')))


class MainScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('black'))

        paddle = Paddle()
        self.objects.append(paddle)

        self.ball = Ball(WINDOW_WIDTH / 2,
                         WINDOW_HEIGHT / 2,
                         random.uniform(-1, 1),
                         random.uniform(-1, 1),
                         paddle)
        self.objects.append(self.ball)

    def keydown(self, event):
        if event.key == K_UP:
            self.ball.vx *= 2
            self.ball.vy *= 2
        elif event.key == K_DOWN:
            self.ball.vx /= 2
            self.ball.vy /= 2


class GameOverScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('blue'))
        self.objects.append(Label('Notty', (500, 200), pygame.Color('black')))
        self.objects.append(Label('Player X Wins', (500, 300), pygame.Color('white')))
        self.objects.append(
            NewGameLabel('Start a new game', (100, 400), pygame.Color('white'), pygame.Color('red')))
        self.objects.append(
            CloseWindowLabel('Close the window', (100, 500), pygame.Color('white'), pygame.Color('red')))

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