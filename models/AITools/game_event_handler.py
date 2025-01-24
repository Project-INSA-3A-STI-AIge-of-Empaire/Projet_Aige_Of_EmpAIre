# from GameField.map import Map
# from ai_profiles import AIProfile
from Entity.entity import Entity


class GameEventHandler:
    def __init__(self, map, players, ai_profiles):
        self.map = map
        self.players = players
        self.ai_profiles = ai_profiles

    def process_ai_decisions(self, tree):
        for player_id, ai_profile in self.ai_profiles.items():
            context = self.get_context_for_player()
            print(f"Here is the context : {context}")
            actions = ai_profile.decide_action(tree, context)
            print(f"Player {player_id} Actions: {actions}")

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
            # 'units': [{'type': 'military' if unit.is_military() else 'villager', 'instance': unit} for unit in self.players.units],
            'enemy_id': enemy_id,
            # 'resource_id': self.map.get_nearest_resource_id(player),
            # 'drop_off_id': self.map.get_nearest_drop_off_id(player),
            'player': self.players,
            # 'current_time': self.map.current_time,
            # 'closest_town_center': self.players.entity_closest_to('T', self.players.cell_Y, self.players.cell_X),
        }
        context['under_attack'] = True
        return context

