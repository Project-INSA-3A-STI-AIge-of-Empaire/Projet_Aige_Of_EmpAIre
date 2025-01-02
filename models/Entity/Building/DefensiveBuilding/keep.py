from Entity.Building.DefensiveBuilding.defensivebuilding import *
class Keep(DefensiveBuilding):
    def __init__(self, cell_Y, cell_X, position, team,representation = 'K', hp = 800, cost = {"gold":125,"wood":35,"food":0}, build_time = 80, sq_size = 1, attack = 4, _range = 5):
        global KEEP_ARRAY_3D
        super().__init__(cell_Y, cell_X, position, team, representation, sq_size, hp, cost, build_time, attack, _range)
        self.image = KEEP_ARRAY_3D