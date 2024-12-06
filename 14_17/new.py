





import copy
import math
from card import *
# drawing one card from deck
def probability_of_valid_group_deck_card(Players_hand):
    P1_hand = Players_hand[0]

    # making a deck list
    deck = []
    # put all card in the deck list
    for i in range(2):
        for color in ['red', 'blue', 'green', 'yellow']:
            for numbers in list(range(1 ,11)):
                deck.append(Card(color, numbers))
    # remove those card in player's hand
    for j in range(len(Players_hand)):
        for k in Players_hand[j].cards:
            for l in deck:
                if k.color == l.color and k.value == l.value:
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
            success_3 += ((len(deck) - 1) * (len(deck ) -2))
        else:
            for n in range(len(deck)):
                if n != m:
                    hands_2 = copy.deepcopy(hands_1)
                    copied_card = copy.deepcopy(deck[n])
                    hands_2.cards.append(copied_card)
                    if hands_2.find_valid_group() is not None:
                        success_2 += 1
                        success_3 += (len(deck ) -2)
                    else:
                        for x in range(len(deck)):
                            if x != m and x != n:
                                hands_3 = copy.deepcopy(hands_2)
                                copied_card = copy.deepcopy(deck[x])
                                hands_3.cards.append(copied_card)
                                if hands_3.find_valid_group() is not None:
                                    success_3 += 1

    prob1 = success_1 / len(deck)
    prob2 = success_2 / math.perm(len(deck) ,2)
    prob3 = success_3 / math.perm(len(deck) ,3)
    listOfProb = [prob1, prob2, prob3]
    return listOfProb







import copy
def probability_of_valid_group_hand(Players_hand):
    P1_hand = Players_hand[0]
    # 创建牌堆
    deck = []
    for i in range(2):
        for color in ['red', 'blue', 'green', 'yellow']:
            for numbers in list(range(1, 11)):
                deck.append(Card(color, numbers))

    # 从牌堆中移除玩家手牌
    for player_hand in Players_hand:
        for card in player_hand.cards:
            deck = [deck_card for deck_card in deck if
                    not (card.color == deck_card.color and card.value == deck_card.value)]

    # 计算形成有效组合的概率
    success_1 = 0
    for deck_card in deck:
        temp_hand = copy.deepcopy(P1_hand)
        temp_hand.cards.append(deck_card)
        if temp_hand.find_valid_group():
            success_1 += 1

    prob1 = success_1 / len(deck)
    return [prob1]
