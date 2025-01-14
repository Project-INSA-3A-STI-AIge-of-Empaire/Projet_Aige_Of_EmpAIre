from Entity.Building.TrainingBuilding.trainingbuilding import *
class Barracks(TrainingBuilding):

    def __init__(self, cell_Y, cell_X, position, team,representation = 'B', sq_size = 3, hp = 500, cost = {"gold":0,"wood":175,"food":0}, build_time = 50, trainable_units = ['s','x']):
        global BARRACKS_ARRAY_3D
        super().__init__(cell_Y, cell_X, position, team,representation, sq_size, hp, cost, build_time, trainable_units)
        