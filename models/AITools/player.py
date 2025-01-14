from GLOBAL_VAR import *
from GLOBAL_IMPORT import *
CLASS_MAPPING = {
    'A': ArcheryRange,
    'B': Barracks,
    'C': Camp,
    'K': Keep,
    'T': TownCenter,
    'F': Farm,
    'G': Gold,
    'W': Tree,
    'S': Stable,
    'H': House,
    'h': HorseMan,
    'a': Archer,
    's': SwordMan,
    'v': Villager,
    'c': CavalryArcher,
    'm':SpearMan,
    'x':AxeMan,
    'p': Projectile,
    'pa': Arrow,
    'ps':Spear,
    'fpa':FireArrow,
    'fps':FireSpear,
    'V': PVector2
}
class Player:
    
    def __init__(self, cell_Y, cell_X, team):
        self.team = team
        self.cell_Y = cell_Y
        self.cell_X = cell_X
        self.storages_id = set() # resource storages
        self.houses_id = set() # towncenters and storages
        self.current_population = 0
        
        self.entities_dict = {}
        self.linked_map = None
        

        
    def add_entity(self, entity):

        entity_dict = self.entities_dict.get(entity.representation, None)

        if entity_dict == None:
            self.entities_dict[entity.representation] = {}
            entity_dict = self.entities_dict.get(entity.representation, None)
        
        entity_dict[entity.id] = entity

        is_habitat = False
        is_storage = False

        if entity.representation in ['C', 'T']:
            is_storage = True
        if entity.representation in ['T', 'H']:
            is_habitat = True
        if is_storage:
            self.storages_id.add(entity.id)
        if is_habitat:
            self.houses_id.add(entity.id)

    def remove_entity(self, entity):
        print(entity)
        entity_dict = self.entities_dict.get(entity.representation, None)
        if entity_dict:
            entity_dict.pop(entity.id, None)
            
            if not entity_dict: # if empty remove 
                self.entities_dict.pop(entity.representation, None)
            is_habitat = False
            is_storage = False
            print(f"storages:{self.storages_id}")
            print(f"houses:{self.houses_id}")

            if isinstance(entity, Unit):
                if self.current_population <= self.get_current_population_capacity():
                    self.remove_population()
                self.current_population -= 1
            if entity.representation in ['C', 'T']:
                is_storage = True
            if entity.representation in ['T', 'H']:
                is_habitat = True
            if is_storage:
                #if entity.id in self.storages_id:
                self.storages_id.remove(entity.id)
            if is_habitat:
                #if entity.id in self.houses_id in self.houses_id:
                entity_population = entity.habitat.current_population
                self.houses_id.remove(entity.id)
                for _ in range(entity_population):
                    self.add_population()

                
            return 1
        return 0

    def get_entities_by_class(self, representations): # list of representations for exemple : ['a', 'h', 'v']

        id_list = []
        
        for representation in representations:
            entity_dict = self.entities_dict.get(representation, None)

            if entity_dict:

                for entity_id in entity_dict:
                    id_list.append(entity_id)
            print(f"ID List so far: {id_list}")
        
        return id_list

    def build_entity(self, villager_id_list, representation = "", entity_id = None):
        if entity_id == None:
            if (representation in ["T","H"]) and self.get_current_population_capacity() >= MAX_UNIT_POPULATION:
                return BUILDING_POPULATION_MAX_LIMIT
            
            BuildingClass = CLASS_MAPPING.get(representation, None)
            Instance = BuildingClass(None, None, None, self.team)
            
            if isinstance(Instance, Building) and Instance.affordable_by(self.get_current_resources()):
                self.remove_resources(Instance.cost)
                Instance.state = BUILDING_INPROGRESS
                self.linked_map.add_entity_to_closest(Instance, self.cell_Y, self.cell_X, random_padding = 0x1)

                for villager_id in villager_id_list:
                    villager = self.linked_map.get_entity_by_id(villager_id)

                    if villager != None:
                        villager.build_entity(Instance.id)
            
                return 1
            return 0
        else:
            for villager_id in villager_id_list:
                    villager = self.linked_map.get_entity_by_id(villager_id)

                    if villager != None:
                        villager.build_entity(entity_id)
            return 1



    def distribute_evenly(self, resource_type, amount):
        
        actual_ids = set()

        for storage_id in self.storages_id:
            current_storage = self.linked_map.get_entity_by_id(storage_id) 
            if current_storage.state == BUILDING_ACTIVE:
                actual_ids.add(storage_id)

        num_storages = len(actual_ids)
        if num_storages == 0:
            return amount  # No storages to distribute to

        per_storage = amount // num_storages
        leftover = amount % num_storages

        for storage_id in actual_ids:
            current_storage = self.linked_map.get_entity_by_id(storage_id)
            
            current_storage.storage.add_resource(resource_type, per_storage + (1 if leftover > 0 else 0))
            if leftover > 0:
                leftover -= 1

        return 0  # No leftover since there's no capacity limit

    def remove_from_largest(self, resource_type, amount):
        actual_ids = set()

        for storage_id in self.storages_id:
            current_storage = self.linked_map.get_entity_by_id(storage_id) 
            if current_storage.state == BUILDING_ACTIVE:
                actual_ids.add(storage_id)

        needed = amount
        while needed > 0:
            # Find the storage with the most of the resource
            largest_storage_id = max(actual_ids, key=lambda s_id: self.linked_map.get_entity_by_id(s_id).storage.resources.get(resource_type, 0), default=None)
            largest_storage = self.linked_map.get_entity_by_id(largest_storage_id)
            if not largest_storage or largest_storage.storage.resources.get(resource_type, 0) == 0:
                break  # No more resources available

            removed = largest_storage.storage.remove_resource(resource_type, needed)
            needed -= removed

        return amount - needed  # Amount successfully removed

    def add_resources(self, resources):

        for resource, amount in resources.items():
            self.distribute_evenly(resource, amount)

    
    def remove_resources(self, resources):
        for resource, amount in resources.items():
            self.remove_from_largest(resource, amount)

    def get_current_resources(self):

        resources = {"gold":0,"wood":0,"food":0}
        actual_ids = set()

        for storage_id in self.storages_id:
            current_storage = self.linked_map.get_entity_by_id(storage_id) 
            if current_storage.state == BUILDING_ACTIVE:
                actual_ids.add(storage_id)
                
        for storage_id in actual_ids:
            current_storage = self.linked_map.get_entity_by_id(storage_id)

            if current_storage:
                for resource, amount in current_storage.storage.resources.items():
                    resources[resource] += amount
        return resources
    """
    def remove_storage(self, toremove_storage_id):
        toremove_storage = self.linked_map.get_entity_by_id(toremove_storage_id)
        resources = toremove_storage.storage.resources 

        self.storages_id.remove(toremove_storage_id)

        return resources
    """

    def get_current_population_capacity(self):
        current_capacity = 0
        actual_ids = set()

        for house_id in self.houses_id:
            current_habitat = self.linked_map.get_entity_by_id(house_id) 
            if current_habitat.state == BUILDING_ACTIVE:
                actual_ids.add(house_id)

        for habitat_id in actual_ids:

            current_habitat = self.linked_map.get_entity_by_id(habitat_id)

            if current_habitat:
                current_capacity += current_habitat.habitat.capacity
        
        return current_capacity
    


    def add_population(self):
        actual_ids = set()

        for house_id in self.houses_id:
            current_habitat = self.linked_map.get_entity_by_id(house_id) 
            if current_habitat.state == BUILDING_ACTIVE:
                actual_ids.add(house_id)

        for habitat_id in actual_ids:

            current_habitat = self.linked_map.get_entity_by_id(habitat_id)

            if current_habitat:
                if current_habitat.habitat.add_population():
                    return True
        return False
    
    def remove_population(self):
        actual_ids = set()
        print("removing")
        for house_id in self.houses_id:
            current_habitat = self.linked_map.get_entity_by_id(house_id) 
            if current_habitat.state == BUILDING_ACTIVE:
                actual_ids.add(house_id)

        for habitat_id in actual_ids:

            current_habitat = self.linked_map.get_entity_by_id(habitat_id)

            if current_habitat:
                if current_habitat.habitat.remove_population():
                    return True
        return False
    


        