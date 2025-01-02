from Entity.Building.building import *
from Entity.Unit.MeleeUnit.horseman import HorseMan
from Entity.Unit.MeleeUnit.villager import Villager
from Entity.Unit.MeleeUnit.swordman import SwordMan
from Entity.Unit.RangedUnit.archer import Archer
TRAINABLE_UNITS = {
    "h":HorseMan,
    "v":Villager,
    "a":Archer,
    "s":SwordMan
}

class TrainingBuilding(Building):

    def __init__(self, cell_Y, cell_X, position, team,representation, sq_size, hp, cost, build_time, trainable_units):
        super().__init__(cell_Y, cell_X, position, team,representation, sq_size, hp, cost, build_time)
        self.trainable_units = trainable_units

        self.time_left = None
        self.last_time_changed_delta = None 
        self.unit_being_trained = None


    def try_to_train(self, current_time):
        
        if self.time_left != None and self.unit_being_trained:# if not None
            
            if self.time_left > (0 + 1e-5):

                elapsed_time = max(3,current_time - self.last_time_changed_delta) # to ensure that timeleft is decresing
                
                self.time_left = self.time_left - elapsed_time
                self.last_time_changed_delta  = current_time

            else:
                
                if self.unit_being_trained:
                    
                    self.linked_map.add_entity_to_closest(self.unit_being_trained, self.cell_Y, self.cell_X)

                    self.unit_being_trained = None
                    self.time_left = None
                    self.last_time_changed_delta = None



    def train_unit(self, player, current_time, entity_repr):
        if self.unit_being_trained == None:
            if entity_repr in self.trainable_units:
                UnitClass = TRAINABLE_UNITS.get(entity_repr, None)
                unit = UnitClass(None, None, None, player.team)

                if unit.affordable_by(player):
                    
                    player.remove_resources(unit.cost)
                    
                    self.unit_being_trained = unit

                    self.time_left = self.unit_being_trained.training_time * ONE_SEC
                    self.last_time_changed_delta = current_time
            
    def display(self, current_time, screen, camera, g_width, g_height):
        super().display(current_time, screen, camera, g_width, g_height)
        if self.unit_being_trained:
            iso_x, iso_y = camera.convert_to_isometric_2d(self.position.x - self.linked_map.tile_size_2d/2, self.position.y - self.linked_map.tile_size_2d/2)
            draw_percentage_bar(screen, camera, iso_x, iso_y, self.unit_being_trained.training_time - self.time_left/ONE_SEC, self.unit_being_trained.training_time, self.sq_size)
            display_image(META_SPRITES_CACHE_HANDLE(camera.zoom, list_keys = [self.unit_being_trained.representation + "i"], camera = camera), iso_x, iso_y, screen, 0x04, 1)





