from Entity.Resources.resources import *
class Gold(Resources):
    def __init__(self, cell_Y, cell_X, position, representation = 'G', storage = GOLD_CAPACITY, resource_indicator = "gold"):
        super().__init__(cell_Y, cell_X, position, representation, storage, resource_indicator)
        self.image = GOLD_ARRAY_1D
        self.resources = {"gold":storage}
        self.display_choice = random.randint(0, len(GOLD_ARRAY_1D) - 1)
