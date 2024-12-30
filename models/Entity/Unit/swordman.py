from Entity.Unit.unit import *
class SwordMan(Unit):

    def __init__(self, cell_Y, cell_X, position, team, representation = 's', hp = 40, cost = 50, training_time = 20, speed = 0.9, attack = 4, attack_speed = 0.5):
        global SWORDMAN_ARRAY_3D
        super().__init__(cell_Y, cell_X, position, team, representation, hp, cost, training_time, speed, attack, attack_speed)
        self.image = SWORDMAN_ARRAY_3D
        
        self.animation_speed = [30, 30, 30/self.attack_speed, 30]
        self.attack_frame = 17
