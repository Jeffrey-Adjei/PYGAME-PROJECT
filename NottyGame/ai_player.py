from game_objects import AIPlayer
import random

class AggressiveAIPlayer(AIPlayer):
    def choose_action(self, game_state):
        # Prioritize stealing over other actions
        if not self.actions_taken['steal']:
            other_players = [p for p in game_state['players'] if p != self and p.hand]
            if other_players:
                target_player = random.choice(other_players)
                self.take_card_from(target_player)
                self.actions_taken['steal'] = True
                return
        super().choose_action(game_state)

class DefensiveAIPlayer(AIPlayer):
    def choose_action(self, game_state):
        # Prioritize discarding groups
        groups = find_possible_groups(self.hand)
        if groups:
            self.discard_group(groups[0], game_state['deck'])
        elif not self.actions_taken['draw']:
            num_to_draw = min(3, 20 - len(self.hand))
            self.draw_cards(game_state['deck'], num_to_draw)
            self.actions_taken['draw'] = True
        else:
            super().choose_action(game_state)

class BalancedAIPlayer(AIPlayer):
    def choose_action(self, game_state):
        groups = find_possible_groups(self.hand)
        if groups:
            self.discard_group(groups[0], game_state['deck'])
        elif len(self.hand) < 15 and not self.actions_taken['draw']:
            num_to_draw = min(3, 20 - len(self.hand))
            self.draw_cards(game_state['deck', num_to_draw])
            self.actions_taken['draw'] = True
        elif not self.actions_taken['steal']:
            other_players = [p for p in game_state['players'] if p != self and p.hand]
            if other_players:
                target_player = random.choice(other_players)
                self.take_card_from(target_player)
                self.actions_taken['steal'] = True
        else:
            super().choose_action(game_state)
