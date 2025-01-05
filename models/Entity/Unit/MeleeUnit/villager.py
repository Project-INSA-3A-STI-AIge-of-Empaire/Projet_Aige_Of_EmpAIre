from Entity.Unit.MeleeUnit.meleeunit import *
from Entity.Building.farm import Farm

class Villager(MeleeUnit):

    def __init__(self, cell_Y, cell_X, position, team, representation = 'v', hp = 25, cost = {"gold":0,"wood":0,"food":50}, training_time = 5, speed = 0.8, attack = 2, attack_speed= 1.4, collect_ratio_per_min = 25):
        super().__init__(cell_Y, cell_X, position, team, representation, hp, cost, training_time, speed, attack, attack_speed)
        self.image = VILLAGER_ARRAY_3D
        
        self.resources = {"gold":0, "wood":0, "food":0}

        self.resource_target_id = None 
        self.drop_target_id = None

        self.collect_ratio_per_min = collect_ratio_per_min
        self.collect_capacity = 20

        self.collect_speed = 60/self.collect_ratio_per_min
        self.will_collect = False

        self.attack_frame = 27
        self.collect_frame = 26

        self.animation_speed = [60, 30, 60, 30, 60/self.collect_speed]
        self.adapte_attack_delta_time()
        
    def drop_gathered(self, entity):
        for resource, amount in self.resources.items():
            entity.resources[resource] += amount
            self.resources[resource] = 0

    def try_to_drop(self, current_time, camera):
        if (self.state != UNIT_DYING):
            if self.drop_target_id != None:
                entity = self.linked_map.get_entity_by_id(self.drop_target_id)
                     
                if (entity != None): 
                    if (entity.team == self.team):
                        if (entity.is_dead() == False):
                            print(entity)
                            if (entity.representation in ["C", "T"]  ):
                                print("yesss")
                                if (self.collide_with_entity(entity)):
                                    
                                    self.drop_gathered(entity)
                                    self.drop_target_id = None
                                    if not(self.state == UNIT_IDLE):
                                        self.change_state(UNIT_IDLE)
                                    
                                else:
                                    if not(self.state == UNIT_WALKING):
                                        self.change_state(UNIT_WALKING)
                                    self.move_position.x = entity.position.x
                                    self.move_position.y = entity.position.y

                                    self.try_to_move(current_time, entity)
                            else:
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



    def is_full(self):
        checker = 0
        for _, amount in self.resources.items():
            checker += amount

        return checker >= self.collect_capacity
    
    

    def try_to_gather(self, current_time, entity):   
            
        if not(self.state == UNIT_TASK):
            self.change_state(UNIT_TASK)
        
        
        if self.state == UNIT_TASK:
            if self.animation_frame == self.collect_frame and self.will_collect:
                self.will_collect = False
                # collect calculations

                amount_to_remove = 1
                self.resources[entity.resource_indicator] += entity.remove_resources(amount_to_remove)
                if isinstance(entity, Resources):
                    
                    if entity.is_dead():
                        self.linked_map.remove_entity(entity)
                
            elif self.animation_frame == self.len_current_animation_frames() - 1:
                self.will_collect = True 
            
        
    def try_to_collect(self,current_time):
        if (self.state != UNIT_DYING):
            if self.resource_target_id != None:
                if not(self.is_full()):
                    entity = self.linked_map.get_entity_by_id(self.resource_target_id)
                    
                    if (entity != None): 
                        if (entity.team == 0 or entity.team == self.team):
                            if (entity.is_dead() == False):
                                print(entity)
                                if (isinstance(entity, Resources) or (isinstance(entity, Farm) and not(entity.is_empty())) ):
                                    if (self.collide_with_entity(entity)):
                                        
                                        
                                        self.try_to_gather(current_time, entity)
                                        
                                    else:
                                        if not(self.state == UNIT_WALKING):
                                            self.change_state(UNIT_WALKING)
                                        self.move_position.x = entity.position.x
                                        self.move_position.y = entity.position.y

                                        self.try_to_move(current_time, entity)
                                else:
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
                else:        
                    if not(self.state == UNIT_IDLE):
                        self.change_state(UNIT_IDLE)
    
    def collect_entity(self, resource_target_id):
        self.entity_target_id = None # if attacking we stop and collect
        self.drop_target_id = None
        self.resource_target_id = resource_target_id

    def attack_entity(self, entity_id):
        self.resource_target_id = None # if collecting we stop and attack
        self.drop_target_id = None
        self.entity_target_id = entity_id

    def drop_to_entity(self, drop_target_id):
        self.resource_target_id = None # if collecting we stop and attack
        self.entity_target_id = None  
        self.drop_target_id = drop_target_id 

    def update(self, current_time, camera = None, screen = None):
        super().update(current_time, camera, screen)
        self.try_to_collect(current_time)