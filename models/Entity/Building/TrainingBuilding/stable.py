from Entity.Building.TrainingBuilding.trainingbuilding import *

class Stable(TrainingBuilding):

    def __init__(self, cell_Y, cell_X, position, team,representation = 'S', sq_size = 3, hp = 500, cost = {"gold":0,"wood":175,"food":0}, build_time = 50, trainable_units = ['h']):
        global STABLE_ARRAY_3D

        super().__init__(cell_Y, cell_X, position, team,representation, sq_size, hp, cost, build_time, trainable_units)
        self.image = STABLE_ARRAY_3D
        self.animation_frame= 0
        self.last_time_animation = pygame.time.get_ticks()
        self.animation_speed = [27/2, 27/2, 20]

