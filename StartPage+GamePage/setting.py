import os
import pygame


pygame.init()
TITLE_STRING = 'Notty'
FPS = 60
HEIGHT = 700
WIDTH = 1200
BG_COLOUR = (0, 200, 230)
COLORS = {
    "Red": (255, 0, 0),
    "Yellow": (255, 255, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
}
BACKGROUND_COLOR = (205, 230, 208)
if os.path.exists("Outfit.ttf"):
    GAME_FONT = pygame.font.Font("Outfit.ttf", 48)
    font_card = pygame.font.Font("Outfit.ttf", 24)
#GAME_AUDIO_DIR =
TABLE_COLOR = (220, 179, 92)

TABLE_Parameter = (WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 400)
Player_Name_COLOUR = (0, 0, 0)
if os.path.exists("Bangers.ttf"):
    Player_Name_FONT = pygame.font.Font("Bangers.ttf", 36)
    font_large = pygame.font.Font("Bangers.ttf", 36)
# 按钮设置
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
button_visible = True
button_colour = (255, 140, 0) # orange
# 发牌设置

cards_per_player = 5
deal_delay = 300  # 发牌间隔（毫秒）
