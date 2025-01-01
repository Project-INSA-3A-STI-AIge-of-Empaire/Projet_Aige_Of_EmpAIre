from Entity.entity import * 
class Building(Entity):

    def __init__(self, cell_Y, cell_X, position, team,representation, sq_size, hp, cost, build_time, walkable = False):
        super().__init__(cell_Y, cell_X, position, team, representation, sq_size)
        self.hp = hp
        self.max_hp = hp
        self.cost = cost
        self.build_time = build_time
        self.walkable = walkable
        self.linked_map = None
        self.display_choice = 0
        self.last_animation_time = pygame.time.get_ticks()
        self.animation_frame = 0
        self.state = BUILDING_ACTIVE
        self.animation_speed = [1, 1, 20]

    def len_current_animation_frames(self):
        return len(self.image.get(self.state,None).get(self.display_choice, None)) #the length changes with respect to the state but the zoom and direction does not change the animation frame count

    def affordable_by(self, player):
        for resource, amount in player.resources.items():
            if amount < self.cost.get(resource, None):
                return False
        
        return True 
    
    def update_animation_frame(self, current_time):
        global ONE_SEC
        if current_time - self.last_animation_time > ONE_SEC/self.animation_speed[self.state]:

            
            self.last_animation_time = current_time

            self.animation_frame = (self.animation_frame + 1)%(self.len_current_animation_frames()) #the length changes with respect to the state but the zoom and direction does not change the animation frame count
            
            water_mark_list =WATER_MARK_SKIP.get(self.representation)
            if (water_mark_list):
                if (self.state, self.display_choice, self.animation_frame) in water_mark_list:
                    self.animation_frame = (self.animation_frame + 1)%(self.len_current_animation_frames()) #the length changes with respect to the state but the zoom and direction does not change the animation frame count

    def display(self, current_time, screen, camera, g_width, g_height):
        
        iso_x, iso_y = camera.convert_to_isometric_2d(self.position.x, self.position.y)
        
        px, py = camera.convert_to_isometric_2d(self.cell_X*TILE_SIZE_2D + TILE_SIZE_2D/2, self.cell_Y*TILE_SIZE_2D + TILE_SIZE_2D/2)
        if (camera.check_in_point_of_view(iso_x, iso_y, g_width, g_height)):
            
            camera.draw_box(screen, self)

            display_image(META_SPRITES_CACHE_HANDLE(camera.zoom, list_keys = [self.representation, self.state, self.display_choice, self.animation_frame], camera = camera), iso_x, iso_y, screen, 0x04, 1)
            if not(self.is_dead()):
                draw_percentage_bar(screen, camera, iso_x, iso_y, self.hp, self.max_hp, self.sq_size, self.team)
            draw_point(screen, (0, 0, 0), px, py, radius=5)
    """
    def display(self,current_time, screen, camera, g_width, g_height):

        iso_x, iso_y = camera.convert_to_isometric_2d(self.position.x, self.position.y)
        if (camera.check_in_point_of_view(iso_x, iso_y, g_width, g_height)):
            camera.draw_box(screen, self)
            display_image(META_SPRITES_CACHE_HANDLE(camera.zoom, list_keys = [self.representation], camera = camera),iso_x, iso_y, screen, 0x04, 3)
            draw_percentage_bar(screen, camera, iso_x, iso_y, self.hp, self.max_hp, self.sq_size, self.team)
    """

    def change_state(self, state):
        self.state = state
        self.animation_frame = 0

    def is_dead(self):
        return self.hp <= 0
    
    def will_vanish(self):
        return self.is_dead() and self.animation_frame == self.len_current_animation_frames() - 1

    def update(self, current_time):
        self.update_animation_frame(current_time)