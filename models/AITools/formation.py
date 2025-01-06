
import math
from GLOBAL_VAR import *
from Entity.Unit.unit import Unit

FORMATION_PADDING = 20

class FormationNode:

    def __init__(self, position, direction = None):
        self.position = position
        self.direction = direction

        self.parent = None
        
        self.unit_id = None

        self.left = None
        self.middle = None
        self.right = None

        self.is_leader = False
        self.leader = None

    def link_to(self, parent, child):

        self.parent = parent

        if parent.is_leader:
            self.leader = parent
        else:
            self.leader = parent.leader

        if child == "right":
            parent.right = self
        elif child == "middle":
            parent.middle = self
        elif child == "left":
            parent.left = self

        self.direction = parent.direction

        # this does all the linking to the nodes so they follow the leader

    



class Formation:

    def __init__(self, leader):
        self.leader = leader
        self.linked_map = None

    @classmethod
    def Create(cls, position, direction, depth, units_id_list, linked_map):
        instance = cls.__new__(cls)
        leader = FormationNode(position, direction)
        leader.is_leader = True # make it the leader
        leader.unit_id = units_id_list.pop(0)
        print(units_id_list)
        current_node = leader

        id_giver_list = units_id_list

        for wings_depth in range(depth, 0, -1):
            id_giver_list = Formation.init_wings(current_node, wings_depth,id_giver_list, child="left")
            id_giver_list = Formation.init_wings(current_node, wings_depth,id_giver_list, child="right")

            if wings_depth > 1:
                new_node = FormationNode(PVector2(current_node.position.x- FORMATION_PADDING*1.5, current_node.position.y ))
                new_node.link_to(current_node, "middle")
                if id_giver_list:
                    print("adding")
                    print(id_giver_list)
                    new_node.unit_id = id_giver_list[0]
                    id_giver_list = id_giver_list[1:]
                current_node = new_node
        
        instance.leader = leader
        instance.linked_map = linked_map

        return instance

    @staticmethod
    def init_wings(parent, wings_depth,id_giver_list, child):
        current_node = parent
        for _ in range(1, wings_depth + 1):
            print("adding")
            print(id_giver_list)
            new_node = FormationNode(
                PVector2(current_node.position.x - FORMATION_PADDING,
                            current_node.position.y - FORMATION_PADDING if child == "left" else current_node.position.y + FORMATION_PADDING))
            new_node.link_to(current_node, child)
            if id_giver_list:
                new_node.unit_id = id_giver_list[0]
                id_giver_list = id_giver_list[1:]
        
            current_node = new_node  # Move to the newly created node

        return id_giver_list
    
    def update_formation_direction(self):
        def update_direction(node):
            if node != None:

                if node.is_leader == False: 
                    node.position.rotate_with_respect_to(node.leader.direction - node.direction, node.leader.position) #rotate the position of the node 
                    node.direction = node.leader.direction # and set to the new direction
                
                update_direction(node.left)
                update_direction(node.middle)
                update_direction(node.right)

        update_direction(self.leader)

    def update_formation_position(self, scale):
        
        def update_position(node, scale):

            if node != None :
                

                amountx = math.cos(node.direction) * scale
                amounty = math.sin(node.direction) * scale

                node.position.x += amountx
                node.position.y += amounty
                    
                    
                update_position(node.left, scale)
                update_position(node.middle, scale)
                update_position(node.right, scale)
        update_position(self.leader, scale)
    
    def units_follow_formation(self):
        
        def node_follow(node):
            if node != None:
                if node.is_leader == False and node.unit_id != None:
                    unit = self.linked_map.get_entity_by_id(node.unit_id)
                    if unit.move_position != node.position:
                        unit.move_to(PVector2(node.position.x, node.position.y))
                    elif unit.state == UNIT_IDLE:
                        unit.target_direction = node.direction
                node_follow(node.right)
                node_follow(node.middle)
                node_follow(node.left)

        node_follow(self.leader)
        
    def display(self):
        def recursive_node(node):
            if node != None:
                print("------")
                print(f"node:{node.position},{node.direction},unit_id:{node.unit_id}")

                recursive_node(node.left)
                recursive_node(node.middle)
                recursive_node(node.right)

        recursive_node(self.leader)