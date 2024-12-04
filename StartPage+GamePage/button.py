import pygame

class Button:
    """通用按钮类"""
    def __init__(self, rect, color, text, font, text_color):
        """
        初始化按钮
        :param rect: 按钮的位置和尺寸 (x, y, width, height)
        :param color: 按钮的背景颜色
        :param text: 按钮上的文字
        :param font: 用于绘制文字的字体对象
        :param text_color: 按钮文字颜色
        """
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.visible = True  # 按钮是否可见

    def draw(self, surface):
        """绘制按钮"""
        if self.visible:
            pygame.draw.rect(surface, self.color, self.rect)
            text_surface = self.font.render(self.text, True, self.text_color)
            text_x = self.rect.centerx - text_surface.get_width() // 2
            text_y = self.rect.centery - text_surface.get_height() // 2
            surface.blit(text_surface, (text_x, text_y))

    def handle_click(self, pos):
        """
        检查按钮是否被点击
        :param pos: 鼠标点击的位置 (x, y)
        :return: 如果被点击返回 True，否则返回 False
        """
        if self.visible and self.rect.collidepoint(pos):
            return True
        return False

    def hide(self):
        """隐藏按钮"""
        self.visible = False

    def show(self):
        """显示按钮"""
        self.visible = True
