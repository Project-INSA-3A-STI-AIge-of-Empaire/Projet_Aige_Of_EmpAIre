from Entity.Unit.unit import *
class HorseMan(Unit):

    def __init__(self, cell_Y, cell_X, position, team, representation = 'h', hp = 45, cost = 80, training_time = 30*ONE_SEC, speed = 1.2, attack = 4, attack_speed = 1.2):
        global HORSEMAN_ARRAY_3D
        super().__init__(cell_X, cell_Y, position, team, representation, hp, cost, training_time, speed, attack, attack_speed)
        self.image = HORSEMAN_ARRAY_3D
        self.animation_speed = [30,70,45/attack_speed,30]
        self.attack_frame = 33