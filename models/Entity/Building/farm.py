from Entity.Building.building import *
class Farm(Building):

    def __init__(self,cell_Y, cell_X, position, team,representation = 'F', hp = 100, cost = 175, build_time = 50*ONE_SEC, sq_size = 2):
        super().__init__(cell_Y, cell_X, position, team,representation, sq_size, hp, cost, build_time, walkable = True)
        self.image = FARM