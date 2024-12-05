from card import *
from setting import *

class Hand:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.cards = []


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
        consecutive_num = self.find_consec_num_gp()
        same_num = self.find_same_num_gp()
        if consecutive_num != []:
            return consecutive_num[0]
        elif same_num != []:
            return same_num[0]
        else:
            return None

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

import copy
import math
# drawing one card from deck

def probability_of_valid_group_deck_card(Players_hand):
    P1_hand = Players_hand[0]

    # making a deck list
    deck = []
    # puting all card in the deck list
    for i in range(2):
        for color in ['red', 'blue', 'green', 'yellow']:
            for numbers in list(range(1, 11)):
                deck.append(Card(color, numbers))
    # remove those card in player's hand
    for j in range(len(Players_hand)):
        for k in Players_hand[j].cards:
            for l in deck:
                if k.color == l.colour and k.value == l.value:
                    deck.remove(l)
                    break

    # calculate the prob. of forming a valid group
    # (if you have a more efficient way for the collectionOfCard class, feel free to modify the above code)
    success_1 = 0
    success_2 = 0
    success_3 = 0
    for m in range(len(deck)):
        hands_1 = copy.deepcopy(P1_hand)
        copied_card = copy.deepcopy(deck[m])
        hands_1.cards.append(copied_card)
        if hands_1.find_valid_group() is not None:
            success_1 += 1
            success_2 += (len(deck) - 1)
            success_3 += ((len(deck) - 1) * (len(deck) - 2))
        else:
            for n in range(len(deck)):
                if n != m:
                    hands_2 = copy.deepcopy(hands_1)
                    copied_card = copy.deepcopy(deck[n])
                    hands_2.cards.append(copied_card)
                    if hands_2.find_valid_group() is not None:
                        success_2 += 1
                        success_3 += (len(deck) - 2)
                    else:
                        for x in range(len(deck)):
                            if x != m and x != n:
                                hands_3 = copy.deepcopy(hands_2)
                                copied_card = copy.deepcopy(deck[x])
                                hands_3.cards.append(copied_card)
                                if hands_3.find_valid_group() is not None:
                                    success_3 += 1

    prob1 = success_1 / len(deck)
    prob2 = success_2 / math.perm(len(deck), 2)
    prob3 = success_3 / math.perm(len(deck), 3)
    listOfProb = [prob1, prob2, prob3]
    return listOfProb

import copy
def probability_of_valid_group_hand(Players_hand):
    P1_hand = Players_hand[0]
    success = 0
    prob = []
    i = 1
    while i < len(Players_hand):
        for j in Players_hand[i]:
            hands = copy.deepcopy(P1_hand)
            hands.cards.append(j)
            if hands.find_valid_group() is not None:
                success += 1
        prob.append(success / len(Players_hand[i]))
        i += 1
    if i == 2:
        return prob[0]
    elif i == 3:
        # if prob of forming a valid group after taking a card from P2 > that of P3
        if prob[0] >= prob[1]:
            return prob[0]
        # if prob of forming a valid group after taking a card from P3 > that of P2
        else:
            return prob[1]