from hand import *

class AIPlayer(Hand):
    def choose_action(self, game_state):
        # 查找有效组并丢弃
        valid_group = self.find_valid_group()
        if valid_group:
            self.discard_group(valid_group, game_state['deck'])
        elif len(self.cards) < 20 and not self.actions_taken['draw']:
            # 抽牌
            num_to_draw = min(3, 20 - len(self.cards))
            self.draw_cards(game_state['deck'], num_to_draw)
            self.actions_taken['draw'] = True
        elif not self.actions_taken['steal']:
            # 偷牌
            other_players = [p for p in game_state['players'] if p != self]
            if other_players:
                target_player = max(other_players, key=lambda p: len(p.cards))  # 选择手牌最多的玩家
                self.take_card_from(target_player)
                self.actions_taken['steal'] = True
        else:
            print(f"{self.name} no action")


class AggressiveAIPlayer(AIPlayer):
    def choose_action(self, game_state):
        # 优先偷牌
        if not self.actions_taken['steal']:
            other_players = [p for p in game_state['players'] if p != self]
            if other_players:
                target_player = max(other_players, key=lambda p: len(p.cards))  # 偷牌目标：手牌最多的玩家
                self.take_card_from(target_player)
                self.actions_taken['steal'] = True
        else:
            super().choose_action(game_state)

class DefensiveAIPlayer(AIPlayer):
    def choose_action(self, game_state):
        # 优先抽牌
        if not self.actions_taken['draw']:
            num_to_draw = min(3, 20 - len(self.cards))
            self.draw_cards(game_state['deck'], num_to_draw)
            self.actions_taken['draw'] = True
        else:
            super().choose_action(game_state)

class BalancedAIPlayer(AIPlayer):
    def choose_action(self, game_state):
        # 优先丢弃组
        groups = self.find_valid_group()
        if groups:
            self.discard_group(groups[0], game_state['deck'])
        elif len(self.cards) < 15 and not self.actions_taken['draw']:
            # 抽牌
            num_to_draw = min(3, 20 - len(self.cards))
            self.draw_cards(game_state['deck'], num_to_draw)
            self.actions_taken['draw'] = True
        elif not self.actions_taken['steal']:
            # 偷牌
            other_players = [p for p in game_state['players'] if p != self]
            if other_players:
                target_player = random.choice(other_players)
                self.take_card_from(target_player)
                self.actions_taken['steal'] = True
        else:
            super().choose_action(game_state)


