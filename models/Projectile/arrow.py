from Projectile.projectile import *

class Arrow(Projectile):

    def __init__(self, cell_Y, cell_X, position, entity_target, _map, team, damage = 4, representation = 'pa', element = ""):
        global ARROW_ARRAY_2D
        super().__init__(cell_Y, cell_X, position, entity_target,_map, team, damage, representation , element)
