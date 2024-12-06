from hand import *

def probability_of_valid_group_hand(players_hand, opponents_hands):
    """
    计算从对手手牌随机选牌后，当前玩家手牌形成有效组的概率。
    :param players_hand: 当前玩家的手牌对象 (Hand)
    :param opponents_hands: 对手的手牌列表 (List of Hand)
    :return: 每个对手手牌的概率列表
    """
    prob = []

    for opponent_hand in opponents_hands:
        success = 0
        if len(opponent_hand.cards) == 0:
            prob.append(0)
            continue

        for card in opponent_hand.cards:
            # 不使用 deepcopy，直接创建新列表模拟添加卡牌
            temp_cards = players_hand.cards + [card]
            temp_hand = Hand(players_hand.name, players_hand.x, players_hand.y)
            temp_hand.cards = temp_cards

            # 检查是否能形成有效组
            if temp_hand.find_valid_group():
                success += 1

        # 计算概率
        prob.append(success / len(opponent_hand.cards) if opponent_hand.cards else 0)

    return prob
