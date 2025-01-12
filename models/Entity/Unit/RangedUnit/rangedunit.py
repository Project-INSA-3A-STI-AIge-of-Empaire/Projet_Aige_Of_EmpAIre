from Entity.Unit.unit import *
from PACKAGE_IMPORT import *
PACKAGE_DYNAMIC_IMPORT("Projectile")

PROJECTILE_TYPE_MAPPING = {
    "pa":Arrow,
    "ps":Spear,
    "fpa":FireArrow,
    "fps":FireSpear 
}


class RangedUnit(Unit):

    def __init__(self, cell_Y, cell_X, position, team, representation, hp, cost, training_time, speed, attack, attack_speed , _range, _projetctile_type):
        super().__init__(cell_Y, cell_X, position, team, representation, hp, cost, training_time, speed, attack, attack_speed, _range)
        self.projetctile_type = _projetctile_type
        self.projetctile_padding = None 

    def check_in_range_with(self, entity):
        print(self.linked_map.tile_size_2d * (self.range + math.floor(entity.sq_size/2)))
        range_circle = Circle(self.position.x, self.position.y, self.linked_map.tile_size_2d * self.range)
        #return self.position.abs_distance(entity.position) < (self.linked_map.tile_size_2d * (self.range + math.floor(entity.sq_size/2)))
        return entity.collide_with_shape(range_circle)

    def try_to_damage(self, current_time, _entity):
        global PROJECTILE_TYPE_MAPPING
        if self.first_time_pass or (current_time - self.last_time_attacked > self.attack_delta_time):
            if (self.first_time_pass):
                self.first_time_pass = False
            if not(self.state == UNIT_ATTACKING):
                self.change_state(UNIT_ATTACKING)

            self.last_time_attacked = current_time

            self.will_attack = True
        
        if self.state == UNIT_ATTACKING:
            if self.animation_frame == self.attack_frame and self.will_attack:
                self.will_attack = False
                
                print(f"attack { current_time - self.last}")
                self.last = current_time
                ProjectileClass = PROJECTILE_TYPE_MAPPING.get(self.projetctile_type, None)
                projectile = ProjectileClass(self.cell_Y, self.cell_X, PVector2(self.position.x - self.projetctile_padding, self.position.y - self.projetctile_padding), _entity, self.linked_map, self.attack)
                self.linked_map.add_projectile(projectile)

            elif self.animation_frame == (self.len_current_animation_frames() - 1):
                self.check_range_with_target = False # we need to recheck if it is still in range
                self.change_state(UNIT_IDLE) # if the entity is killed we stop


    def try_to_attack(self,current_time, camera, screen):
        if (self.state != UNIT_DYING):
            
            if self.entity_target_id != None:
                entity = self.linked_map.get_entity_by_id(self.entity_target_id)
                
                if (entity != None):
                    
                    if (entity.team != 0 and entity.team != self.team):
                        
                        if (entity.is_dead() == False):
                            
                            
                            if not(self.check_range_with_target):
                                
                                if (self.check_in_range_with(entity)):
                                    
                                    self.check_range_with_target = True
                                    self.locked_with_target = True
                                    
                                    
                                else:
                                    
                                    if not(self.state == UNIT_WALKING): # we need to reach it in range
                                        self.change_state(UNIT_WALKING)

                                    self._entity_optional_target_id = entity.id
                                    self.move_position.x = entity.position.x
                                    self.move_position.y = entity.position.y
                                    

                                    
                                    self.locked_with_target = False
                                    self.first_time_pass = True
                                    self.try_to_move(current_time,camera,screen)
                            else: # enemy in range  
                                self.target_direction = self.position.alpha_angle(entity.position)
                                dist_to_entity = self.position.abs_distance(entity.position)

                                if (dist_to_entity <= (self.range * (entity.sq_size) * self.linked_map.tile_size_2d + entity.box_size + self.box_size)):
                                    self.try_to_damage(current_time, entity)
                                else:
                                    self.check_range_with_target = False
                                    if not(self.state == UNIT_IDLE):
                                        self.change_state(UNIT_IDLE)
                        
                        
                        else:
                            if not(self.state == UNIT_IDLE):
                                self.change_state(UNIT_IDLE)
                            self.entity_target_id = None
                            self.locked_with_target = False
                    else:
                        if not(self.state == UNIT_IDLE):
                                self.change_state(UNIT_IDLE)
                
    def display(self, current_time, screen, camera, g_width, g_height):
        draw_isometric_circle(camera, screen, self.position.x, self.position.y, self.range*TILE_SIZE_2D, TEAM_COLORS.get(self.team)) 
        super().display(current_time, screen, camera, g_width, g_height)