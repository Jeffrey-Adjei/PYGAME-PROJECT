from card import *
from setting import *

class Hand:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.cards = []

    def add_card(self, card):
        """添加一张牌到玩家的手牌"""
        self.cards.append(card)

    def draw_name(self, surface):
        # 绘制玩家名字
        name_text = Player_Name_FONT.render(self.name, True, Player_Name_COLOUR)
        surface.blit(name_text, (self.x-80, self.y - 40))

    def draw(self, surface, selected_cards=None):
        """绘制玩家的牌"""
         # 绘制每张牌
        """绘制玩家的牌，支持多行显示"""
        max_cards_per_row = 8  # 每行最多显示的牌数量
        card_spacing = 52  # 卡牌之间的水平间距
        row_spacing = 80  # 行之间的垂直间距

        for i, card in enumerate(self.cards):
            row = i // max_cards_per_row  # 当前卡牌所在的行
            col = i % max_cards_per_row  # 当前卡牌所在的列

            # 计算卡牌的绘制位置
            card.x = self.x + col * card_spacing
            card.y = self.y + row * row_spacing

            # 判断是否选中
            is_selected = card in selected_cards if selected_cards else False
            card.draw(surface, selected=is_selected)

    def get_card_at(self, pos):
        """
        根据鼠标位置获取被点击的牌
        :param pos: 鼠标点击的位置 (x, y)
        :return: 被点击的牌对象，如果没有点击到牌则返回 None
        """
        for card in self.cards:
            if card.is_clicked(pos):  # 使用 Card 类的点击检测
                return card
        return None