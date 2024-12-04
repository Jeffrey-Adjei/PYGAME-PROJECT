import pygame
import random
import sys
from setting import *



class Card:
    """
    表示一张UNO牌的类，同时包含逻辑和图形绘制功能
    """
    def __init__(self, color, value, x=0, y=0):
        """
        初始化UNO牌
        :param color: 牌的颜色
        :param value: 牌的数值
        :param x: 牌的左上角X坐标
        :param y: 牌的左上角Y坐标
        """
        self.color = color
        self.value = value
        self.x = x
        self.y = y
        self.width = 52
        self.height = 80

        self.image = pygame.image.load(f"images/{color.lower()}_{value}.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def __str__(self):
        return f"{self.color} {self.value}"

    def draw(self, surface, selected=False, back=False):
        """
            绘制卡牌
            :param surface: 绘图表面
            :param selected: 如果为 True，绘制放大的卡牌
            """
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if selected:
            rect.inflate_ip(20, 20)  # 放大显示

        if back:
            back_image = pygame.image.load("images/card_back.png")
            back_image = pygame.transform.scale(back_image, (rect.width, rect.height))
            surface.blit(back_image, rect.topleft)
        # 绘制图片
        else:
            scaled_image = pygame.transform.scale(self.image, (rect.width, rect.height))
            surface.blit(scaled_image, rect.topleft)

    def is_clicked(self, pos):
        """
        检查是否点击到这张牌
        :param pos: 鼠标点击位置 (x, y)
        :return: 如果点击到这张牌，返回True；否则返回False
        """
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height