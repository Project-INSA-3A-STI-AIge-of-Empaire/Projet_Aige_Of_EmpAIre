from Projectile.projectile import *

class Arrow(Projectile):

    def __init__(self, cell_Y, cell_X, position, entity_target, _map,  damage = 4, representation = 'na', element = ""):
        global ARROW_ARRAY_2D
        super().__init__(cell_Y, cell_X, position, entity_target,_map, damage, representation, element)
        self.image = ARROW_ARRAY_2D