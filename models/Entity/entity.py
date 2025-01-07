from GLOBAL_VAR import *
from idgen import *
from AITools.player import *
from shapely.geometry import Point, Polygon
import math
from shape import *

class Entity():
    def __init__(self, cell_Y, cell_X, position, team, representation, sq_size = 1,id = None):
        global ID_GENERATOR
        self.cell_Y = cell_Y
        self.cell_X = cell_X
        self.position = position
        self.team = team
        self.representation = representation
        if id:
            self.id = id
        else:
            self.id = ID_GENERATOR.give_ticket()
        self.sq_size = sq_size
        self.image = None
        self.dict_repr = {
            'wood':"Wood",
            'gold':"Gold",
            'food':"Food",
            'v':"Villager",
            's':"Swordsman",
            'h':"Horseman",
            'a':"Archer",
            'am':"AxeMan",
            'ca':"CavalryArcher",
            'sm':"SpearMan",
            'T':"TownCenter",
            'H':"House",
            'C':"Camp",
            'F':"Farm",
            'B':"Barracks",
            'S':"Stable",
            'A':"ArcheryRange",
            'K':"Keep"
            }

    

        self.box_size = None
        self.HitboxClass = None
        self.walkable = False
    def __str__(self):
        return f"ent<{self.id},{self.representation},Y:{self.cell_Y},X:{self.cell_X},sz:{self.sq_size}>"
    
    def collide_with_shape(self, shape):
        shape_self = self.HitboxClass(self.position.x, self.position.y, self.box_size)

        return shape_self.collide_with(shape)
    
    def collide_with_entity(self, entity):
        
        self_shape = self.HitboxClass(self.position.x, self.position.y, self.box_size)
        ent_shape = entity.HitboxClass(entity.position.x, entity.position.y, entity.box_size)
        
        Status = False
        
        """
        alpha = self.position.alpha_angle(entity.position)
        op_alpha = alpha + math.pi
        if isinstance(entity, Unit):
            if self_shape.collide_with(ent_shape):
                Status = True 
            if flags and Status:
                while self_shape.collide_with(ent_shape):
                    self.position.x += round(math.cos(op_alpha))
                    self.position.y += round(math.sin(op_alpha))
                    self_shape = self.ShapeClass(self.position.x, self.position.y, self.bs)
            if pygame.time.get_ticks() - self.last_time_computed > 1:
                self.last_time_computed = pygame.time.get_ticks()
                return Status
            return False
        else:
        """     
        if self_shape.collide_with(ent_shape):
            Status = True
        # i wrote it like this on purpose incase there is some future update
        return Status
    
    def update(self, current_time, camera = None, screen = None):
        return None
    def save(self):

        data_to_save = {}
        current_data_to_save = None

        for attr_name, attr_value in self.__dict__.items():

            if not(attr_name == "image"):
                
                if hasattr(attr_value, "save"):
                    current_data_to_save = attr_value.save()
                else:
                    current_data_to_save = attr_value

                data_to_save[attr_name] = current_data_to_save

        return data_to_save
    
    
    
    @classmethod
    def load(cls, data_to_load):
        global SAVE_MAPPING
        instance = cls.__new__(cls) # skip the __init__()
        current_attr_value = None
        for attr_name, attr_value in data_to_load.items():
            
            if (isinstance(attr_value, dict)): # has the attribute representation then we will see
                
                ClassLoad = CLASS_MAPPING.get(attr_value.get("representation", None), None)
                if (ClassLoad): # has a load method in the method specified in it
                    
                    current_attr_value = ClassLoad.load(attr_value)
                else:
                    current_attr_value = attr_value
            else:
                current_attr_value = attr_value
        
            setattr(instance, attr_name, current_attr_value)

        return instance
