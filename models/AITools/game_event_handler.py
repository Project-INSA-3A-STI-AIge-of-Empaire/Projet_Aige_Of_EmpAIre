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
            'military_units': len(self.players.get_entities_by_class(['h', 'a', 's','x','m','c'])),
            'ratio_military':len(self.players.get_entities_by_class(['h', 'a', 's','x','m','c']))/len(self.players.get_entities_by_class(['h', 'a', 's','v','x','m','c'])) if len(self.players.get_entities_by_class(['h','a','s','v','x','m','c'])) != 0 else 0,
            'military_units_details': {
                'archers': len(self.players.get_entities_by_class(['a'])),
                'infantry': len(self.players.get_entities_by_class(['s'])),
            },
            'enemy_visible': enemy_visible,
            'buildings': {
                'storage': self.players.is_free(),
                'training': self.players.get_entities_by_class(['B','S','A','K']),
                'critical': self.players.is_free(),
                'ratio':{
                    'T' : len(self.players.entities_dict['T'])/sum(len(self.players.entities_dict[k]) for k in self.players.entities_dict.keys()) if 'T' in self.players.entities_dict.keys() else 0,
                    'H' : len(self.players.entities_dict['H'])/sum(len(self.players.entities_dict[k]) for k in self.players.entities_dict.keys()) if 'H' in self.players.entities_dict.keys() else 0,
                    'C' : len(self.players.entities_dict['C'])/sum(len(self.players.entities_dict[k]) for k in self.players.entities_dict.keys()) if 'C' in self.players.entities_dict.keys() else 0,
                    'F' : len(self.players.entities_dict['F'])/sum(len(self.players.entities_dict[k]) for k in self.players.entities_dict.keys()) if 'F' in self.players.entities_dict.keys() else 0,
                    'B' : len(self.players.entities_dict['B'])/sum(len(self.players.entities_dict[k]) for k in self.players.entities_dict.keys()) if 'B' in self.players.entities_dict.keys() else 0,
                    'S' : len(self.players.entities_dict['S'])/sum(len(self.players.entities_dict[k]) for k in self.players.entities_dict.keys()) if 'S' in self.players.entities_dict.keys() else 0,
                    'A' : len(self.players.entities_dict['A'])/sum(len(self.players.entities_dict[k]) for k in self.players.entities_dict.keys()) if 'A' in self.players.entities_dict.keys() else 0,
                    'K' : len(self.players.entities_dict['K'])/sum(len(self.players.entities_dict[k]) for k in self.players.entities_dict.keys()) if 'K' in self.players.entities_dict.keys() else 0,
                }
            },
            'enemy_distance': enemy_distance,
            'units' : {
                'military': [self.players.linked_map.get_entity_by_id(m_id) for m_id in self.players.get_entities_by_class(['h', 'a', 's'])],
                'villager': [self.players.linked_map.get_entity_by_id(v_id) for v_id in self.players.get_entities_by_class(['v'])],
            },
            'enemy_id': enemy_id,
            'resource_id': self.players.entity_closest_to(['G', 'W'], self.players.cell_Y, self.players.cell_X),
            'drop_off_id': self.players.entity_closest_to(['T'], self.players.cell_Y, self.players.cell_X),
            'player': self.players,
            'closest_town_center': self.players.entity_closest_to(['T'], self.players.cell_Y, self.players.cell_X),
            'map' : self.map,
            'under_attack' : (self.players.get_closest_ennemy()[1] < 20),
        }
        return context




