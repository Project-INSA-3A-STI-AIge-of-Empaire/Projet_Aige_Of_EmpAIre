# from GameField.map import Map
# from ai_profiles import AIProfile
from Entity.entity import Entity


class GameEventHandler:
    def __init__(self, map, players, ai_profiles):
        self.map = map
        self.players = players
        self.ai_profiles = ai_profiles

    def process_ai_decisions(self, tree):
        all_action = []
        context = self.get_context_for_player()
        print(f"Here is the context : {context}")
        actions = self.ai_profiles.decide_action(tree, context)
        all_action.append(actions)
        print(f"Player {self.players.team} Actions: {actions}")

    def get_context_for_player(self):
        enemy_visible, enemy_distance, enemy_id = self.players.get_closest_ennemy()
        context = {
            'resources': self.players.get_current_resources(),
            'military_units': len(self.players.get_entities_by_class(['h', 'a', 's'])),
            'military_units_details': {
                'archers': len(self.players.get_entities_by_class(['a'])),
                'infantry': len(self.players.get_entities_by_class(['s'])),
            },
            'enemy_visible': enemy_visible,
            'buildings': {
                'storage': self.players.is_free(),
                'training': self.players.get_entities_by_class(['b']),
                'critical': self.players.is_free(),
            },
            'enemy_distance': enemy_distance,
            'units': {'military' : self.players.get_entities_by_class(['h', 'a', 's']), 'villager' : self.players.get_entities_by_class(['v'])},
            'enemy_id': enemy_id,
            'resource_id': self.players.entity_closest_to(['G', 'W'], self.players.cell_Y, self.players.cell_X),
            'drop_off_id': self.players.entity_closest_to(['T'], self.players.cell_Y, self.players.cell_X),
            'player': self.players,
            'closest_town_center': self.players.entity_closest_to(['T'], self.players.cell_Y, self.players.cell_X),
            'map' : self.map,
        }
        context['under_attack'] = True
        return context

