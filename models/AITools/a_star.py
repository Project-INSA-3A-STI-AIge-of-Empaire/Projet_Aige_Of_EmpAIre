import heapq
import math


from Entity.Resources.resources import Resources
from Entity.Building.building import Building
class Node:
    def __init__(self, _X, _Y):
        self.X = _X
        self.Y = _Y
        self.G_cost = 0  # Cost from start node
        self.H_cost = 0  # Heuristic cost to target
        self.F_cost = 0  # Total cost
        self.previus = None

    def __lt__(self, other):
        return self.F_cost < other.F_cost or (self.F_cost == other.F_cost and self.H_cost < other.H_cost)

    def dist_to(self, other):
        return math.sqrt((other.X - self.X)**2 + (other.Y - self.Y)**2) * 10

    def update_F_cost(self):
        self.F_cost = self.H_cost + self.G_cost

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def __str__(self):
        return f"({self.X},{self.Y}): G={self.G_cost} H={self.H_cost} F={self.F_cost}"

def A_STAR(start_X, start_Y, end_X, end_Y, _map, _entity_optional_target = None):
    if not (0 <= start_X < _map.nb_CellX and 0 <= start_Y < _map.nb_CellY and 
            0 <= end_X < _map.nb_CellX and 0 <= end_Y < _map.nb_CellY):
        return None # Invalid start or end

    start_node = Node(start_X, start_Y)
    
    target_node = Node(end_X, end_Y)

    start_node.H_cost = start_node.dist_to(target_node)
    start_node.update_F_cost()

    searching = []
    heapq.heappush(searching, (start_node.F_cost, start_node))

    discoverd = {}
    searched = set()

    
    collided_with_entity = False # these 3 variables are used in case we have an entity as target

    current_region = _map.entity_matrix.get((target_node.Y//_map.region_division, target_node.X//_map.region_division), None)

    if (current_region != None):
        current_entities = current_region.get((target_node.Y, target_node.X), None)
        if(current_entities):
            for current_entity in current_entities:
                _entity_optional_target = current_entity

    while searching:
        _, best_node = heapq.heappop(searching)
        
        # these conditions are have only sense when the target is an entity 
        # not a normal position path finding, but it doesnt affect 
        # the algo in the case of normal pathfinding



        ##found path !!###
        if best_node == target_node or collided_with_entity:
            # Reconstruct path
            path = []
            while best_node:
                path.append((best_node.X, best_node.Y))
                best_node = best_node.previus
            path.reverse()
            return path
        ## end ##
        
        searched.add((best_node.X, best_node.Y))

        for offsetY in [-1, 0, 1]:
            for offsetX in [-1, 0, 1]: # neighbors are the cells around
                neighbor_X = best_node.X + offsetX
                neighbor_Y = best_node.Y + offsetY

                if neighbor_X < 0 or neighbor_Y < 0 or neighbor_X >= _map.nb_CellX or neighbor_Y >= _map.nb_CellY: # not in bound
                    continue

                cell_walkable = True 

                #check if the current cellX and cellY contains entities 
                region = _map.entity_matrix.get((neighbor_Y//_map.region_division, neighbor_X//_map.region_division), None)

                if (region != None):
                    entities = region.get((neighbor_Y, neighbor_X), None)
                    if(entities): # entities exists so the cell is occupied
            
                        for entity in entities:
                            if (entity == _entity_optional_target):
                                cell_walkable = True 
                                collided_with_entity = True 
                                break

                            if isinstance(entity, Building): # some building can be walkable
                                if not(entity.walkable):    # if it is not , False and break
                                    cell_walkable = False
                                    break

                            elif isinstance(entity, Resources):
                                cell_walkable = False
                                break

                if not(cell_walkable):
                    continue

                neighbor_node = discoverd.get((neighbor_Y, neighbor_X),None) 

                if neighbor_node is None: # we didnt discover this cell in the grid, so we create the node 
                    neighbor_node = Node(neighbor_X, neighbor_Y)
                    neighbor_node.G_cost = neighbor_node.dist_to(start_node) 
                    neighbor_node.H_cost = neighbor_node.dist_to(target_node)
                    neighbor_node.update_F_cost()
                    neighbor_node.previus = best_node

                    discoverd[(neighbor_Y, neighbor_X)] = neighbor_node # now it is discoverd and we need to explore it, push to the heap
                    heapq.heappush(searching, (neighbor_node.F_cost, neighbor_node)) # we push with respect to the F_cost, priority to the lowest F cost
                else:
                    current_G_cost = best_node.G_cost + best_node.dist_to(neighbor_node) 
                    if current_G_cost < neighbor_node.G_cost: # if it smaller, we found a path connected to this node, better than a previous one
                        neighbor_node.G_cost = current_G_cost # update its G cost
                        neighbor_node.update_F_cost()
                        neighbor_node.previus = best_node # connect the path

    return None  # No path found
