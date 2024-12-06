from card import *
from setting import *

class Hand:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.cards = []
        self.actions_taken = {'draw': False, 'steal': False}  # 初始化动作记录


    def add_card(self, card):
        if len(self.cards) < 20:  # 手牌上限为 20
            self.cards.append(card)
        else:
            print(f"{self.name}'s hand has reached its limit")

    def draw_name(self, surface):
        # Draw the player's name
        name_text = Player_Name_FONT.render(self.name, True, Player_Name_COLOUR)
        surface.blit(name_text, (self.x-80, self.y - 40))

    def draw(self, surface, selected_cards=None):
        max_cards_per_row = 8
        card_spacing = 52
        row_spacing = 80

        for i, card in enumerate(self.cards):
            row = i // max_cards_per_row
            col = i % max_cards_per_row

            # position
            card.x = self.x + col * card_spacing
            card.y = self.y + row * row_spacing

            is_selected = card in selected_cards if selected_cards else False
            card.draw(surface, selected=is_selected)

    # if click
    def get_card_at(self, pos):
        for card in self.cards:
            if card.is_clicked(pos):  
                return card
        return None

    def is_valid_group(self):
        number_of_card = len(self.cards)
        if number_of_card < 3:
            valid = False
        else:
            self.cards = sorted(self.cards, key=lambda x: x.value)
            is_consecutive = all \
                (self.cards[i].value == self.cards[i - 1].value + 1 for i in range(1, len(self.cards)))
            is_same_num = all \
                (self.cards[j].value == self.cards[j - 1].value for j in range(1, len(self.cards)))
            if is_consecutive:
                is_same_color = all \
                    (self.cards[k].color == self.cards[k - 1].color for k in range(1, number_of_card))
                valid = is_same_color
            elif is_same_num:
                l = 0
                is_different_color = True
                while (l < number_of_card - 1) and is_different_color:
                    for m in range(l + 1, number_of_card):
                        if self.cards[l].color == self.cards[m].color:
                            is_different_color = False
                            break
                    l += 1
                valid = is_different_color
            else:
                valid = False
        return valid

    def discard_group(self, group, deck):
        """
        丢弃有效的卡牌组到牌堆，并从手牌移除。
        :param group: 要丢弃的卡牌组
        :param deck: 牌堆对象
        """
        if group:  # 确认组不为空
            for card in group:
                if card in self.cards:
                    self.cards.remove(card)  # 确保从手牌移除
                    deck.add_card(card)  # 添加到牌堆
            deck.shuffle()  # 洗牌
        else:
            print("Invalid group. Cannot discard.")

    def draw_cards(self, deck, num):
        """
        从牌堆中抽取一定数量的卡牌并加入手牌。
        :param deck: 牌堆对象
        :param num: 要抽取的卡牌数量
        """
        for _ in range(num):
            card = deck.draw_card()  # 从牌堆中抽取一张牌
            if card:
                self.add_card(card)  # 加入手牌
            else:
                print("deck empty")

    def take_card_from(self, other_player):
        """
        从另一个玩家的手牌中随机拿走一张卡。
        :param other_player: 被偷牌的玩家 (Hand 对象)
        """
        if not other_player.cards:
            print(f"{other_player.name} 手牌为空，无法偷牌。")
            return
        stolen_card = random.choice(other_player.cards)
        other_player.cards.remove(stolen_card)
        self.add_card(stolen_card)  # 加入自己的手牌
        print(f"{self.name} 偷了一张卡 {stolen_card} 从 {other_player.name}")

    def find_consec_num_gp(self):
        color_list = [[], [], [], []]
        for i in self.cards:
            if i.color == 'blue':
                color_list[0].append(i)
            elif i.color == 'red':
                color_list[1].append(i)
            elif i.color == 'green':
                color_list[2].append(i)
            elif i.color == 'yellow':
                color_list[3].append(i)
        list_3_consec_num = []
        for c_cards in color_list:
            if len(c_cards) >= 3:
                c_cards = sorted(c_cards, key=lambda x: x.value)
                consec_num = [c_cards[0]]
                for i in range(1, len(c_cards)):
                    if c_cards[i].value == c_cards[i - 1].value + 1:
                        consec_num.append(c_cards[i])
                        if len(consec_num) >= 3:
                            for j in range(3, len(consec_num) + 1):
                                list_3_consec_num.append(consec_num[-j:])
                    elif c_cards[i].value == c_cards[i - 1].value:
                        pass
                    else:
                        consec_num = [c_cards[i]]
        return list_3_consec_num

    def find_same_num_gp(self):
        self.cards = sorted(self.cards, key=lambda x: x.value)
        same_num = [self.cards[0]]
        list_same_num = []
        for i in range(1, len(self.cards)):
            if self.cards[i].value == same_num[-1].value:
                same_num.append(self.cards[i])
            else:
                list_same_num.append(same_num)
                same_num = [self.cards[i]]
        list_same_num.append(same_num)
        list_3_diff_color = []
        for i in list_same_num:
            if len(i) >= 3:
                color = []
                list_diff_color = []
                for j in i:
                    if j.color not in color:
                        color.append(j.color)
                        list_diff_color.append(j)
                        if len(list_diff_color) >= 3:
                            for k in range(3, len(list_diff_color) + 1):
                                list_3_diff_color.append(list_diff_color[-k:])
        return list_3_diff_color

    def find_valid_group(self):
        valid_groups = self.find_consec_num_gp() + self.find_same_num_gp()
        # 返回第一个有效组，或者空
        return valid_groups[0] if valid_groups else None

    def find_largest_valid_group(self):
        consecutive_num = self.find_consec_num_gp()
        same_num = self.find_same_num_gp()
        largest_con_gp = []
        largest_same_gp = []
        if consecutive_num != []:
            for i in consecutive_num:
                if len(i) > len(largest_con_gp):
                    largest_con_gp = i
        if same_num != []:
            for j in same_num:
                if len(j) > len(largest_same_gp):
                    largest_same_gp = j
        if largest_con_gp == [] and largest_same_gp == []:
            return None
        elif len(largest_con_gp) >= len(largest_same_gp):
            return largest_con_gp
        else:
            return largest_same_gp





