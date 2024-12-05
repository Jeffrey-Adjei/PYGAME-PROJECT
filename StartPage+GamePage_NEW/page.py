import pygame
from pygame.locals import *
import random
from main import Game


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


class Label(VisualObject):
    def __init__(self, text, pos, colour, head):
        self.text = text
        self.pos = pos
        self.colour = colour
        if head == 'title':
            self.font = pygame.font.SysFont(None, 60)
        elif head == 'heading':
            self.font = pygame.font.SysFont(None, 36)
        elif head == 'body':
            self.font = pygame.font.SysFont(None, 20)

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
        super().__init__(pygame.Color('blue'), 'images/background_image.jpg')
        self.objects.append(Label('Notty', (550, 200), pygame.Color('black'), 'title'))
        self.objects.append(Label('Number of players:', (500, 300), pygame.Color('white'), 'heading'))
        self.objects.append(PlayerNumberLabel('2', (575, 350), pygame.Color('white'), pygame.Color('red'), 'heading'))
        self.objects.append(PlayerNumberLabel('3', (625, 350), pygame.Color('white'), pygame.Color('red'), 'heading'))
        self.objects.append(RuleLabel('Game rule', (540, 400), pygame.Color('white'), pygame.Color('red'), 'heading'))


class PlayScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('blue'), 'images/background_image.jpg')
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
        # 初始化并运行卡牌游戏
        card_game = Game(num_player)
        card_game.run()
        # 返回到主菜单后结束当前游戏循环
        game_over = True

class RuleScreen(ScreenBase):
    def __init__(self):
        super().__init__(pygame.Color('blue'), 'Pictures/Saved Pictures/background_image.jpg')
        self.objects.append(Label('Description of the Game', (100, 50), pygame.Color('yellow'), 'heading'))
        self.objects.append(
            Label('Each card has a colour (red, blue, green, or yellow) and a number (1 to 10).', (150, 100),
                  pygame.Color('white'), 'body'))
        self.objects.append(Label(
            'There are exactly two cards for each combination of colour and number, making a total of 80 cards in the deck.',
            (150, 150), pygame.Color('white'), 'body'))
        self.objects.append(
            Label('Each card has a colour (red, blue, green, or yellow) and a number (1 to 10).', (150, 200),
                  pygame.Color('white'), 'body'))
        self.objects.append(Label('Gameplay', (100, 250), pygame.Color('yellow'), 'heading'))
        self.objects.append(
            Label('At the beginning of the game, the deck is shuffled, and each player is dealt 5 cards.', (150, 300),
                  pygame.Color('white'), 'body'))
        self.objects.append(
            Label('Players take turns.  On a player’s turn, they can perform any of the following actions:', (150, 350),
                  pygame.Color('white'), 'body'))
        self.objects.append(
            Label('1. (At most once per turn) Draw up to 3 cards from the deck.', (200, 400), pygame.Color('white'),
                  'body'))
        self.objects.append(
            Label('2. (At most once per turn) Choose another player and take a random card from them.', (200, 450),
                  pygame.Color('white'), 'body'))
        self.objects.append(
            Label('3. (Any number of times per turn) Discard a valid group of cards. A valid group is either:',
                  (200, 500), pygame.Color('white'), 'body'))
        self.objects.append(
            Label('a. A sequence of at least three cards of the same colour with consecutive numbers', (250, 550),
                  pygame.Color('white'), 'body'))
        self.objects.append(
            Label('b. A set of at least three cards of the same number but different colours', (250, 600),
                  pygame.Color('white'), 'body'))
        self.objects.append(
            Label('The first player to empty their hand wins the game.', (150, 650), pygame.Color('white'), 'body'))
        self.objects.append(NewGameLabel('Back', (100, 680), pygame.Color('yellow'), pygame.Color('red'), 'heading'))


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