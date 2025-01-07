
import math
from GLOBAL_VAR import *

from shape import *
FORMATION_PADDING = 20

BOX_DEFAULT = 10
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
    """
    def avoid_others(self, _map):
            if self != None:
                cell_Y, cell_X = math.floor(self.position.y/_map.tile_size_2d), math.floor(self.position.x/_map.tile_size_2d)
                
                collided = False
                avoidance_force = PVector2(0, 0)  # We will store the avoidance force here
                box_size = BOX_DEFAULT
                
                if self.unit_id:
                    unit = _map.get_entity_by_id(self.unit_id)

                    box_size = unit.box_size

                # Check surrounding cells for nearby units
                for offsetY in [-1, 0, 1]:
                    for offsetX in [-1, 0, 1]:

                        currentY = cell_Y + offsetY
                        currentX = cell_X + offsetX

                        
                        current_region = _map.entity_matrix.get((currentY//_map.region_division, currentX//_map.region_division))

                        if current_region:
                            current_set = current_region.get((currentY, currentX))

                            if current_set:
                                for entity in current_set:

                                    if entity.id != self.unit_id:
                                        distance = self.position.abs_distance(entity.position)
                                        if not(entity.walkable):
                                            
                                            if entity.collide_with_shape(Circle(self.position.x, self.position.y, box_size)):

                                                diff = self.position - entity.position
                                                diff.normalize()  # Normalize to get direction
                                                diff *= 2 *_map.tile_size_2d/distance  # Stronger force the closer the units are
                                                avoidance_force += diff
                                                collided = True

                return collided, avoidance_force
            return None, None
        """


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
            id_giver_list = Formation.init_wings(current_node, wings_depth,id_giver_list, child="left", _linked_map = linked_map)
            id_giver_list = Formation.init_wings(current_node, wings_depth,id_giver_list, child="right", _linked_map = linked_map)

            if wings_depth > 1:
                new_node = FormationNode(PVector2(current_node.position.x- FORMATION_PADDING*1.5, current_node.position.y ))
                new_node.link_to(current_node, "middle")
                if id_giver_list:
                    print("adding")
                    print(id_giver_list)

                    new_node.unit_id = id_giver_list[0]
                    id_giver_list = id_giver_list[1:]

                    unit = linked_map.get_entity_by_id(new_node.unit_id)
                    unit.role_in_group = UNIT_FOLLOWER
                    unit.group_node = new_node

                current_node = new_node
        
        instance.leader = leader
        instance.linked_map = linked_map

        return instance

    @staticmethod
    def init_wings(parent, wings_depth,id_giver_list, child, _linked_map):
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
                unit = _linked_map.get_entity_by_id(new_node.unit_id)
                unit.role_in_group = UNIT_FOLLOWER
                unit.group_node = new_node
        
            current_node = new_node  # Move to the newly created node

        return id_giver_list
    
    def update_formation_avoidance(self, avoidance_force):
        def update_avoidance(node, avoidance_force):
            if node != None:

                
                node.position += avoidance_force
                update_avoidance(node.left, avoidance_force)
                update_avoidance(node.right, avoidance_force)
                update_avoidance(node.middle, avoidance_force)

        update_avoidance(self.leader, avoidance_force)

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
    
    
        
