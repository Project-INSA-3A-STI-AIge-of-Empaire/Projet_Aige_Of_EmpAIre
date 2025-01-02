from Entity.Unit.RangedUnit.rangedunit import *
from Projectile.arrow import *

class Archer(RangedUnit):

    def __init__(self, cell_Y, cell_X, position, team, representation = 'a', hp = 30, cost = {"gold":45,"wood":25,"food":0}, training_time = 5, speed = 1, attack = 50, attack_speed = 1.1, _range = 5, _projectile_type = "na"):
        super().__init__(cell_Y, cell_X, position, team, representation, hp, cost, training_time, speed, attack, attack_speed, _range, _projectile_type)
        self.image = ARCHER_ARRAY_3D
        self.last_time_sent_arrow = pygame.time.get_ticks()
        
        self.animation_speed = [60,30,30,30]
        self.attack_frame = 17

    def display(self, current_time, screen, camera, g_width, g_height):
        
        super().display(current_time, screen, camera, g_width, g_height)
        
        """
        for arrow_index in range(len(self.arrow_array)): # tmp test
            
             
            self.arrow_array[arrow_index].update_position(current_time)
            o_x, o_y = camera.convert_to_isometric_3d(self.arrow_array[arrow_index].position.x, self.arrow_array[arrow_index].position.y,self.arrow_array[arrow_index].projectile_z_pos)

            self.arrow_array[arrow_index].display(current_time, screen, camera)
        """
    
   