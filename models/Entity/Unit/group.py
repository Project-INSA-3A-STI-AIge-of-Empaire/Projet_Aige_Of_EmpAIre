import math
from AITools.formation import * 
import random 

def calc_depth_from_unit_num(unit_num):
    return math.ceil(math.sqrt( unit_num + 1 ) - 1)

class Group:

    def __init__(self, units_id_list, linked_map = None):
        self.units_id_list = units_id_list
        self.leader_id = units_id_list[0]
    
        self.linked_map = linked_map

        self.action = None

        leader = linked_map.get_entity_by_id(self.leader_id)
        leader.role_in_group = UNIT_LEADER
        
        leader.linked_group = self
        self.formation = Formation.Create(PVector2(leader.position.x, leader.position.y), leader.direction, calc_depth_from_unit_num(len(units_id_list)),units_id_list, linked_map)

        self.state = GROUP_IDLE

        self.entity_target_id = None


    
    def move_to(self, position):
        leader = self.linked_map.get_entity_by_id(self.leader_id)
        
        leader.move_to(position)

    def attack_entity(self, entity_id):
        
        leader = self.linked_map.get_entity_by_id(self.leader_id)
        leader.attack_entity(entity_id)
 
    def try_attack(self):
        leader = self.linked_map.get_entity_by_id(self.leader_id)
        self.formation.leader.direction = leader.direction
        if leader.locked_with_target:
            self.formation.update_target(leader.entity_target_id)
            return True
        else:
            self.formation.update_target(None)
            return False

           
    
    def update(self):
         
        self.formation.update_formation_direction()
        if not(self.try_attack()):
            self.formation.units_follow_formation()
        self.formation.update_followers_state()

                
        