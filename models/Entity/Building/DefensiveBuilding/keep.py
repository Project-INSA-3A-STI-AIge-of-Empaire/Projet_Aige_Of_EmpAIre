from Entity.Building.DefensiveBuilding.defensivebuilding import *
class Keep(DefensiveBuilding):
    def __init__(self, cell_Y, cell_X, position, team,representation = 'K', sq_size = 1,hp = 800, cost = {"gold":125,"wood":35,"food":0}, build_time = 80, attack = 4,attack_speed = 1, _range = 10, projectile_type = "fpa"):
        global KEEP_ARRAY_3D
        print(cell_Y, cell_X, position, team, representation, sq_size, hp, cost, build_time, attack, _range, projectile_type)
        super().__init__(cell_Y, cell_X, position, team, representation, sq_size, hp, cost, build_time, attack,attack_speed, _range, projectile_type)
        self.projetctile_padding =TILE_SIZE_2D*3