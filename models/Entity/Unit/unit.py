from Entity.entity import *
from AITools.a_star import *
from math import floor, sqrt
import random

class Unit(Entity):

    def __init__(self, cell_Y, cell_X, position, team, representation, hp, cost, training_time, speed, attack, attack_speed = 1, _range=1):
        super().__init__(cell_Y, cell_X, position, team, representation)
        self.hp = hp
        self.max_hp = hp
        self.training_time=training_time
        self.cost=cost


        self.last = pygame.time.get_ticks()
        self.attack = attack
        self.attack_speed = attack_speed
        self.range= _range
        self.last_time_attacked = pygame.time.get_ticks()
        self.will_attack = False
        self.attack_frame = 0
        self.entity_target_id= None
        
        self.check_range_with_target = False
        self.first_time_pass = True
        self.locked_with_target = False
        self.speed=speed
        self.last_time_moved = pygame.time.get_ticks()
        self.move_per_sec = TILE_SIZE_2D # 1 tile per speed of each unit ( tile size in the 2d mechanics plane)
        
        self.move_position = PVector2(0, 0)
        self.path_to_position = None
        self.current_to_position = None

        self.direction = 0
        self.target_direction = None
        self.last_time_update_direction = pygame.time.get_ticks()

        #self.last_time_collided = pygame.time.get_ticks()
        self.walkable = True
        self.state = UNIT_IDLE
        self.attack_delta_time = None

        self.linked_group = None # we need it if leader
        self.role_in_group = None # specify the role in the group
        self.group_node = None # if follower we node the node to move to it
        self.leader_reached_position = True

        #animation attributes
        self.image = None
        self.animation_frame = 0
        self.animation_direction = 0 # direction index for display
        self.last_animation_time = pygame.time.get_ticks()
        self.animation_speed = []  # Animation frame interval in milliseconds for each unit_state
        self.linked_map = None
        self.HitboxClass = Circle

        self._entity_optional_target_id = None
        
    def adapte_attack_delta_time(self):
        if self.attack_speed > 1:
            self.attack_delta_time = (self.attack_speed) * ONE_SEC
        else:
            self.attack_delta_time = self.attack_speed * ONE_SEC
            self.animation_speed[2] = self.animation_speed[2]/self.attack_speed*1.5

    def set_direction_index(self):
        self.animation_direction = MAP_ANGLE_INDEX(self.direction, UNIT_ANGLE_MAPPING) # map the animation index for the direction with repect to the sprites sheet

    def affordable_by(self, player):
        for resource, amount in player.resources.items():
            if amount < self.cost.get(resource, None):
                return False
        
        return True 

    def update_path_nodes(self, entity):
        if self.path_to_position:
            
            for Y_to_maybe_remove in range(entity.cell_Y, entity.cell_Y - entity.sq_size, -1):
                for X_to_maybe_remove in range(entity.cell_X, entity.cell_X - entity.sq_size, -1):
                    
                    self.path_to_position.pop((Y_to_maybe_remove, X_to_maybe_remove), None)
                    
            

            if self.path_to_position:
                current_node, _ = next(iter(self.path_to_position.items()))
                
                found_around = True
                next_entity = None

                region = self.linked_map.entity_matrix.get((current_node[0]//self.linked_map.region_division, current_node[1]//self.linked_map.region_division), None)
                if region:

                    current_set = region.get((current_node[0], current_node[1]), None)
                    if current_set:
                        for entity in current_set:

                            if entity.id != self._entity_optional_target_id:

                                if not(entity.walkable):
                                    found_around = False
                                    next_entity = entity
                                    break
                
                if found_around:
                    around_path = A_STAR(self.cell_X, self.cell_Y, current_node[1], current_node[0], self.linked_map, self, pass_flags = 1)

                    if around_path:
                        current_node, _ = next(iter(around_path.items()))
                        around_path.pop(current_node)
                        self.path_to_position = around_path | self.path_to_position
                else:
                    self.update_path_nodes(next_entity)

            else:
                self.move_position.x = self.position.x
                self.move_position.y = self.position.y

                #self.current_to_position = None




            
    def len_current_animation_frames(self):
        return len(self.image.get(self.state,None).get(0, None)) #the length changes with respect to the state but the zoom and direction does not change the animation frame count
 
    def update_animation_frame(self, current_time):
        global ONE_SEC
        if current_time - self.last_animation_time > ONE_SEC/self.animation_speed[self.state]:
            self.last_animation_time = current_time

            self.animation_frame = (self.animation_frame + 1)%(self.len_current_animation_frames()) #the length changes with respect to the state but the zoom and direction does not change the animation frame count

    def changed_cell_position(self):
        topleft = PVector2(self.cell_X*self.linked_map.tile_size_2d, self.cell_Y*self.linked_map.tile_size_2d)
        bottomright = PVector2((self.cell_X + 1)*self.linked_map.tile_size_2d, (self.cell_Y + 1)*self.linked_map.tile_size_2d)

        return not(self.position < bottomright and self.position > topleft)

    def track_cell_position(self):
        if (self.changed_cell_position()):
            
            live_cell_X = int(floor(self.position.x/self.linked_map.tile_size_2d))
            live_cell_Y = int(floor(self.position.y/self.linked_map.tile_size_2d))
            cell_free = True 

            live_region = self.linked_map.entity_matrix.get((live_cell_Y//self.linked_map.region_division, live_cell_X//self.linked_map.region_division))
            if (live_region):

                live_entity_set = live_region.get((live_cell_Y, live_cell_X))
                if(live_entity_set):

                    for live_entity in live_entity_set:
                        if not(live_entity.walkable):
                            cell_free = False
            if cell_free:
                uself = self.linked_map.remove_entity(self) # remove from the current cell
                self.cell_X, self.cell_Y = live_cell_X, live_cell_Y # update the cell
                self.change_cell_on_map()

    def change_cell_on_map(self): # to change the cell position on the map 
        region = self.linked_map.entity_matrix.get((self.cell_Y//self.linked_map.region_division, self.cell_X//self.linked_map.region_division))

        if (region):
            current_set = region.get((self.cell_Y, self.cell_X))

            if(current_set):
                current_set.add(self)
            else:
                current_set = set()
                current_set.add(self)
                region[(self.cell_Y, self.cell_X)] = current_set
        else:
            region = {}
            current_set = set()
            current_set.add(self)
            region[(self.cell_Y, self.cell_X)] = current_set

            self.linked_map.entity_matrix[(self.cell_Y//self.linked_map.region_division, self.cell_X//self.linked_map.region_division)] = region    

        self.linked_map.entity_id_dict[self.id] = self



    def move_to_position(self,current_time, camera, screen):
        if (current_time - self.last_time_moved > ONE_SEC/(self.move_per_sec*self.speed)):

            self.last_time_moved = current_time
            collided, avoidance_force = self.avoid_others()

            # Apply avoidance force if collision is detected
            if collided:
                self.position += avoidance_force

             
            
            if self.path_to_position != None and self.current_to_position == self.move_position:

                to_target_directly = False

                if self.path_to_position == {}:
                    to_target_directly = True
                elif len(self.path_to_position) == 1:
                    # if we entered the last last cell we dont go to the center of the cell, straight to the position
                    
                    last_node, _ = next(iter(self.path_to_position.items())) 
                    to_target_directly = (self.cell_X == last_node[1] and self.cell_Y == last_node[0])

                if to_target_directly:
                    self.target_direction = self.position.alpha_angle(self.move_position)
                    
                    amount_x = math.cos(self.target_direction)*(TILE_SIZE_2D/self.move_per_sec)
                    amount_y = math.sin(self.target_direction)*(TILE_SIZE_2D/self.move_per_sec)
                    self.position.x += amount_x
                    self.position.y += amount_y    

                    if self.position == self.move_position:
                        self.path_to_position = None
                else:
                    
                    dbg_kl = list(self.path_to_position.keys())
                    # for debugging purposes
                    for i in range(len(dbg_kl) - 1):
                        
                        (Y1, X1) = dbg_kl[i]
                        (Y2, X2) = dbg_kl[i + 1]
                        
                        
                        iso_x1, iso_y1 = camera.convert_to_isometric_2d(X1 * TILE_SIZE_2D + TILE_SIZE_2D/2, Y1 * TILE_SIZE_2D + TILE_SIZE_2D/2)
                        iso_x2, iso_y2 = camera.convert_to_isometric_2d(X2 * TILE_SIZE_2D + TILE_SIZE_2D/2, Y2 * TILE_SIZE_2D + TILE_SIZE_2D/2)
                        
                        # Draw a line between these two points
                        pygame.draw.line(screen, (255, 0, 0), (iso_x1, iso_y1), (iso_x2, iso_y2), 2)
                    


                    current_node, _ = next(iter(self.path_to_position.items()))

                    current_path_node_position = PVector2(current_node[1] * TILE_SIZE_2D + TILE_SIZE_2D/2, current_node[0] * TILE_SIZE_2D + TILE_SIZE_2D/2)
                    self.target_direction = self.position.alpha_angle(current_path_node_position)
                    

                    amount_x = math.cos(self.target_direction)*(TILE_SIZE_2D/self.move_per_sec)
                    amount_y = math.sin(self.target_direction)*(TILE_SIZE_2D/self.move_per_sec)
                    
                    self.position.x += amount_x
                    self.position.y += amount_y 
                
                    if self.position == current_path_node_position:
                        self.path_to_position.pop(current_node)
            else:
                self.check_and_set_path()

            self.track_cell_position()

    def check_and_set_path(self):
        self.path_to_position = A_STAR(self.cell_X, self.cell_Y, math.floor(self.move_position.x/TILE_SIZE_2D), math.floor(self.move_position.y/TILE_SIZE_2D), self.linked_map,self)
                
        if self.path_to_position != None:
            self.current_to_position = PVector2(self.move_position.x, self.move_position.y)
            current_node, _ = next(iter(self.path_to_position.items()))
            self.path_to_position.pop(current_node)
        else : 
            self.change_state(UNIT_IDLE)

    def try_to_move(self, current_time,camera, screen):
        if (self.state != UNIT_DYING):
            if self.state == UNIT_WALKING:
                if self.position == self.move_position:
                    if self.leader_reached_position:
                        if not(self.state == UNIT_IDLE):
                            self.change_state(UNIT_IDLE)
                else:
                    if not(self.state == UNIT_WALKING):
                        self.change_state(UNIT_WALKING)
                    self.move_to_position(current_time, camera, screen )
    
    def avoid_others(self):
        collided = False
        avoidance_force = PVector2(0, 0)  # We will store the avoidance force here

        # Check surrounding cells for nearby units
        for offsetY in [-1, 0, 1]:
            for offsetX in [-1, 0, 1]:

                currentY = self.cell_Y + offsetY
                currentX = self.cell_X + offsetX

                
                current_region = self.linked_map.entity_matrix.get((currentY//self.linked_map.region_division, currentX//self.linked_map.region_division))

                if current_region:
                    current_set = current_region.get((currentY, currentX))

                    if current_set:
                        for entity in current_set:

                            if entity.id != self.id  and entity.id != self._entity_optional_target_id:
                                distance = self.position.abs_distance(entity.position)
                
                                if isinstance(entity, Unit):
                                    # If the distance between units is smaller than a threshold, avoid collision
                                    if distance < COLLISION_THRESHOLD:
                                        # Calculate the direction to push the unit away from the other
                                        diff = self.position - entity.position
                                        diff.normalize()  # Normalize to get direction
                                        diff *= 1/distance  # Stronger force the closer the units are
                                        avoidance_force += diff
                                        collided = True
                                elif not(entity.walkable):
                                    
                                    if self.collide_with_entity(entity):

                                        self.update_path_nodes(entity)

                                        diff = self.position - entity.position
                                        diff.normalize()  # Normalize to get direction
                                        diff *= TILE_SIZE_2D/distance  
                                        avoidance_force += diff
                                        collided = True


                                    

        return collided, avoidance_force

    def move_to(self, position):
        if (position.x>=0 and position.y>=0 and position.x<=self.linked_map.tile_size_2d*self.linked_map.nb_CellX and position.y<=self.linked_map.tile_size_2d*self.linked_map.nb_CellY):
            if not(self.state == UNIT_WALKING):
                self.change_state(UNIT_WALKING)
            self.move_position.x = position.x
            self.move_position.y = position.y
        else:
            if not(self.state == UNIT_IDLE):
                self.change_state(UNIT_IDLE)
        
    def change_state(self, new_state):
        self.state = new_state

        if new_state != UNIT_ATTACKING and new_state != UNIT_DYING:
            self.animation_frame = random.randint(0, self.len_current_animation_frames() - 1)
        else:
            self.animation_frame = 0 # we put the animationframe index to 0 for attack and dying or task
        
        if new_state == UNIT_IDLE:
            self.path_to_position = None
            self._entity_optional_target_id = None
        if self.will_attack:
            self.will_attack = False
        # to avoid index out of bound in the animationframes list, 
        # for exmample for Archer 
        # idle has 60 frames, move has 30
        # the unit moves on the 58th frame
        # the state changes, now it is moving, but the frame index is 58
        # and move has max 30, 58 > 30 ==> unsupported type (Nonetype)

          

    def attack_entity(self, entity_id):
            
        self.entity_target_id = entity_id
        if self.entity_target_id == None:
            if not(self.state == UNIT_IDLE):
                self.change_state(UNIT_IDLE)
        #self.last_time_attacked = pygame.time.get_ticks()
        self.check_range_with_target = False
        self.locked_with_target = False

    def display(self, current_time, screen, camera, g_width, g_height):
        
        iso_x, iso_y = camera.convert_to_isometric_2d(self.position.x, self.position.y)
        
        px, py = camera.convert_to_isometric_2d(self.cell_X*TILE_SIZE_2D + TILE_SIZE_2D/2, self.cell_Y*TILE_SIZE_2D + TILE_SIZE_2D/2)
        if (camera.check_in_point_of_view(iso_x, iso_y, g_width, g_height)):
            
            #camera.draw_box(screen, self)
            self.set_direction_index()
            display_image(META_SPRITES_CACHE_HANDLE(camera.zoom, list_keys = [self.representation, self.state, self.animation_direction, self.animation_frame], camera = camera), iso_x, iso_y, screen, 0x04, 1)
            #if not(self.is_dead()):
            #    draw_percentage_bar(screen, camera, iso_x, iso_y, self.hp, self.max_hp, self.sq_size, self.team)
            draw_point(screen, (0, 0, 0), px, py, radius=5)
            draw_isometric_circle(camera, screen, self.position.x, self.position.y, self.box_size, RED_COLOR)

     

    def check_collision_around(self): # this function is only made to se if we need to recalculate the path for the unit
        collided = False

        for offsetY in [-1, 0, 1]:
            for offsetX in [-1, 0, 1]:

                currentY = self.cell_Y + offsetY
                currentX = self.cell_X + offsetX

                if not(self.cell_X != currentX and self.cell_Y != currentY):
                    current_region = self.linked_map.entity_matrix.get((currentY//self.linked_map.region_division, currentX//self.linked_map.region_division))

                    if (current_region):
                        current_set = current_region.get((currentY, currentX))

                        if (current_set):
                            for entity in current_set:
                                if entity.id != self._entity_optional_target_id:
                                    if not(entity.walkable):
                                        if (self.collide_with_entity(entity)):
                                            collided = True # all we need is to get one collision with a non walkable entity
                                            break 
                                    
                if (collided):
                    break
            if (collided):
                break
        
        return collided 

    def is_dead(self):
        return self.hp <= 0
    
    def will_vanish(self):
        return self.is_dead() and self.animation_frame == self.len_current_animation_frames() - 1
    
    def update(self, current_time, camera, screen):
        self.update_animation_frame(current_time)
        self.try_to_attack(current_time, camera, screen)
        self.try_to_move(current_time, camera, screen)
        self.update_direction(current_time)

    def update_direction(self, current_time):

        if self.target_direction != None:

            if current_time - self.last_time_update_direction > ONE_SEC/120:
                self.last_time_update_direction = current_time

                # Get the delta angle
                delta_angle = (self.target_direction - self.direction) % (2 * math.pi)
                if delta_angle > math.pi:
                    delta_angle -= 2 * math.pi

                # Determine rotation speed
                rotation_speed = math.radians(7)  # Speed in radians per update
                if abs(delta_angle) < rotation_speed:
                    self.direction = self.target_direction  # Snap to target if close
                    self.target_direction = None
                else:
                    self.direction += max(-rotation_speed, min(rotation_speed, delta_angle))

                self.direction %= (2 * math.pi)  # Normalize within [0, 2π]
    
    def get_unit_html(self):
        return f'<li class="unit">{self.dict_repr.get(self.representation)} : {self.position}</li>'
        
