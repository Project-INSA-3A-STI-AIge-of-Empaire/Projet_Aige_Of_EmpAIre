from Projectile.projectile import *

class Arrow(Projectile):

    def __init__(self, cell_Y, cell_X, position, entity_target, _map,  damage = 4, representation = 'na'):
        global ARROW_ARRAY_2D
        super().__init__(cell_Y, cell_X, position, entity_target,_map, damage, representation)
        self.image = ARROW_ARRAY_2D