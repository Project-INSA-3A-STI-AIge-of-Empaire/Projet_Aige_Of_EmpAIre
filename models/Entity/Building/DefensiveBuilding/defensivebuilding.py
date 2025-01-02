from Entity.Building.building import *
class DefensiveBuilding(Building):

    def __init__(self, cell_Y, cell_X, position, team,representation, sq_size, hp, cost, build_time, attack, _range):
        super().__init__(cell_Y, cell_X, position, team,representation, sq_size, hp, cost, build_time)
        self.attack = attack
        self.range = _range

    