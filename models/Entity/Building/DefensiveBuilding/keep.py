from Entity.Building.DefensiveBuilding.defensivebuilding import *
class Keep(DefensiveBuilding):
    def __init__(self, cell_Y, cell_X, position, team,representation = 'K', hp = 800, cost = 35, build_time = 80, sq_size = 1, attack = 4, _range = 5):
        global KEEP 
        super().__init__(cell_Y, cell_X, position, team, representation, sq_size, hp, cost, build_time, attack, _range)
        self.image = KEEP