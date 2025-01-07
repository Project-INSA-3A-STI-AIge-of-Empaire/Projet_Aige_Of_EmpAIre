from Entity.entity import Entity
from Entity.building import Building
from GameField.map import Map
from Player.player import Player

class AIProfile:
    def __init__(self, strategy, aggressiveness=1.0, defense=1.0):
        self.strategy = strategy
        self.aggressiveness = aggressiveness
        self.defense = defense

    def decide_action(self, context):
        player = context['player']
        map = context['map']

        if self.strategy == "aggressive":
            return self._aggressive_strategy(player, map)
        elif self.strategy == "defensive":
            return self._defensive_strategy(player, map)
        elif self.strategy == "balanced":
            return self._balanced_strategy(player, map)

    def _aggressive_strategy(self, player, map):
        if player.resources['gold'] >= 100:
            return "Train an attack unit"
        return "Gather resources"

    def _defensive_strategy(self, player, map):
        if any(building.hp < building.max_hp for building in map.entity_matrix.values() if isinstance(building, Building)):
            return "Repair buildings"
        return "Build defensive structures"

    def _balanced_strategy(self, player, map):
        if player.resources['gold'] >= 50 and player.resources['wood'] >= 50:
            return "Build a balanced army"
        return "Gather resources"
