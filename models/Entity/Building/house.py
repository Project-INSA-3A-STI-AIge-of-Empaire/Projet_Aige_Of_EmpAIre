from Entity.Building.building import *
class House(Building):

    def __init__(self, cell_Y, cell_X, position, team,representation = 'H', sq_size = 2, hp = 200, cost = {"gold":0,"wood":25,"food":0}, build_time = 25):
        global HOUSES_ARRAY_3D
        super().__init__(cell_Y, cell_X, position, team,representation, sq_size, hp, cost, build_time)

        self.image = HOUSES_ARRAY_3D
        self.display_choice = random.randint(0, len(HOUSES_ARRAY_3D) - 1)
    
    