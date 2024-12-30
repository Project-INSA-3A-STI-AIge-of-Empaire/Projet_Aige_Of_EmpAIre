from Entity.Unit.unit import *
from PACKAGE_IMPORT import *
PACKAGE_DYNAMIC_IMPORT("Projectile")

PROJECTILE_TYPE_MAPPING = {
    "na", Arrow 
}
class RangedUnit(Unit):

    def __init__(self, cell_Y, cell_X, position, team, representation, hp, cost, training_time, speed, attack, attack_speed , _range, _projetctile_type):
        super().__init__(cell_Y, cell_X, position, team, representation, hp, cost, training_time, speed, attack, attack_speed, _range)
        self.projetctile_type = _projetctile_type
        
    def check_in_range_with(self, entity):
        return self.position.abs_distance(entity.position) < (self.linked_map.tile_size_2d * self.range)
    

    def try_to_damage(self, current_time, _entity, camera):
        
        if self.first_time_pass or (current_time - self.last_time_attacked > self.attack_speed * ONE_SEC):
            if (self.first_time_pass):
                self.first_time_pass = False
            if not(self.state == UNIT_ATTACKING):
                self.change_state(UNIT_ATTACKING)

            self.last_time_attacked = current_time

            self.will_attack = True
        
        if self.state == UNIT_ATTACKING:
            if self.animation_frame == self.attack_frame and self.will_attack:
                self.will_attack = False

                arrow = Arrow(self.cell_Y, self.cell_X, PVector2(self.position.x - self.linked_map.tile_size_2d/2, self.position.y- self.linked_map.tile_size_2d/2), _entity, self.linked_map)
                self.linked_map.add_projectile(arrow)

            elif self.animation_frame == (self.len_current_animation_frames() - 1):
                self.check_range_with_target = False # we need to recheck if it is still in range
                self.change_state(UNIT_IDLE) # if the entity is killed we stop


    def try_to_attack(self,current_time, entity_id, camera):

        entity = self.linked_map.get_entity_by_id(entity_id)

        if (entity != None): 
            if (entity.team != 0 and entity.team != self.team):

                if (entity.is_dead() == False):
                    
                    
                    if not(self.check_range_with_target):
                        if (self.check_in_range_with(entity)):
                            self.check_range_with_target = True
                            
                            print(f"animation_frame:{self.animation_frame}")
                            
                        else:
                            if not(self.state == UNIT_WALKING): # we need to reach it in range
                                self.change_state(UNIT_WALKING)
                                self.move_position = entity.position
                            self.first_time_pass = True
                            self.try_to_move(current_time, camera)
                    else: # enemy in range  
                        self.direction = self.position.alpha_angle(entity.position)
                        dist_to_entity = self.position.abs_distance(entity.position)

                        if (dist_to_entity <= (self.range * (entity.sq_size) * TILE_SIZE_2D + entity.box_size + self.box_size)):
                            self.try_to_damage(current_time, entity, camera)
                        else:
                            self.check_range_with_target = False
                            if not(self.state == UNIT_IDLE):
                                self.change_state(UNIT_IDLE)
                
                
                else:
                    if not(self.state == UNIT_IDLE):
                        self.change_state(UNIT_IDLE)
            else:
                if not(self.state == UNIT_IDLE):
                        self.change_state(UNIT_IDLE)
        else:        
            if not(self.state == UNIT_IDLE):
                self.change_state(UNIT_IDLE)