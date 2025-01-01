from GLOBAL_VAR import *
from idgen import *
from AITools.player import *
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

    

    def __str__(self):
        return f"ent<{self.representation},Y:{self.cell_Y},X:{self.cell_X},sz:{self.sq_size}>"
    
    def update(self, current_time):
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
                
                ClassLoad = SAVE_MAPPING.get(attr_value.get("representation", None), None)
                if (ClassLoad): # has a load method in the method specified in it
                    
                    current_attr_value = ClassLoad.load(attr_value)
                else:
                    current_attr_value = attr_value
            else:
                current_attr_value = attr_value
        
            setattr(instance, attr_name, current_attr_value)

        return instance
