import math
from AITools.formation import * 
import random 

def calc_depth_from_unit_num(unit_num):
    return math.ceil(math.sqrt( unit_num + 1 ) - 1)

class Group:

    def __init__(self, units_id_list, linked_map = None):
        self.units_id_list = units_id_list
        self.leader_id = units_id_list[0]
        print(units_id_list)
        print(self.leader_id)
        self.linked_map = linked_map
        self.action = None
        leader = linked_map.get_entity_by_id(self.leader_id)
        leader.leader_of_a_group = True
        
        leader.linked_group = self
        self.formation = Formation.Create(PVector2(leader.position.x, leader.position.y), leader.direction, calc_depth_from_unit_num(len(units_id_list)),units_id_list, linked_map)


    def update(self):
        self.formation.units_follow_formation()
    
    def move_to(self, position):
        leader = self.linked_map.get_entity_by_id(self.leader_id)
        print(leader)
        leader.move_to(position)

 
    