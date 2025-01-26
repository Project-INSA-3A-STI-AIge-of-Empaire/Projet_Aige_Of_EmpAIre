from GLOBAL_VAR import *
from GLOBAL_IMPORT import *
from .game_event_handler import *
from .ai_profiles import*
from random import randint,seed
import time
from .commons_actions import perform_attack

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

class DecisionNode:
    def __init__(self, question, yes_action=None, no_action=None, priority=0):
        self.question = question
        self.yes_action = yes_action
        self.no_action = no_action
        self.priority = priority

    def decide(self, context):
        actions = []
        print(f"Question result: {self.question(context)}")
        if self.question(context):
            print(f"Taking YES branch: {self.yes_action}")
            if isinstance(self.yes_action, DecisionNode):
                actions.extend(self.yes_action.decide(context))
            else:
                if callable(self.yes_action):
                    result = self.yes_action(context)
                    actions.append((result, self.priority))
                    print(f"Yes action called: {actions}")
        else:
            print(f"Taking NO branch: {self.no_action}")
            if isinstance(self.no_action, DecisionNode):
                actions.extend(self.no_action.decide(context))
            else:
                if callable(self.no_action):
                    print(f"No action called: {actions}")
                    result = self.no_action(context)
                    actions.append((result, self.priority))

        actions.sort(key=lambda x: x[1], reverse=True)

        print(f"The decide method return : {actions}")
        return [action if isinstance(action, str) else action[0] for action in actions]

# ---- Questions ----
def is_under_attack(context):
    return context['under_attack']

def resources_critical(context):
    resources = context['player'].get_current_resources()
    return resources['gold'] < 50 or resources['food'] < 50 or resources['wood'] < 50

def buildings_insufficient(context):
    return not context['buildings'].get('storage', False)

def has_enough_military(context):
    return context['military_units'] >= 10

def is_unit_idle(unit):
    return unit.state == UNIT_IDLE

def closest_town_center(context):
    player = context['player']
    town_center = player.entity_closest_to('T', player.cell_Y, player.cell_X)
    if town_center:
        context['closest_town_center'] = town_center
    return town_center is not None

def is_villager_full(unit):
    return unit['type'] == 'villager' and unit['instance'].is_full()

# ---- Actions ----
def defend(context):
    for unit in context['units']:
        if unit['type'] == 'military':
            unit['instance'].attack_entity(context['enemy_id'])
    return "Defend the village!"

def gather_resources(context):
    for villager in context['units']['villager']:
        if not villager.is_full() and is_unit_idle(villager):
            villager.collect_entity(context['resource_id'])
        else:
            drop_resources(context)
    return "Gathering resources!"

def train_military(context):
    for building in context['buildings']['training']:
        building['instance'].train_unit(context['player'], 'v')
    return "Train military units!"

def attack(context):
    return perform_attack(context)

def drop_resources(context):
    for unit in context['units']['villager']:
        if unit.is_full() and not is_under_attack(context):
            unit.drop_to_entity(context['drop_off_id'])
    return "Dropping off resources!"

def find_closest_resources(context):
    print("find ressources de jules")
    resources_to_find='W'
    if min(context['resources']["gold"], context['resources']["wood"])==context['resources']["gold"]:
        resources_to_find='G'
    town_center = context['player'].linked_map.get_entity_by_id(context['closest_town_center'])
    if town_center:
        closest_resource = context['player'].entity_closest_to(resources_to_find, town_center.cell_Y, town_center.cell_X)  # Example for gold
        context['resource_id'] = closest_resource if closest_resource else None
    return "Found closest resources!"

def build_structure(context):
    # villager_ids = [unit.id for unit in context['units'].get('villager', []) if is_unit_idle(unit)]
    # if villager_ids:
    #     context['player'].build_entity(villager_ids, 'B',)  # Example for Town Center
    return "Building structure!"
        

def enemy_visible(context):
    return context['enemy_visible']

# ---- Arbre de décision ----
tree = DecisionNode(
    is_under_attack,
    yes_action=DecisionNode(
        enemy_visible,
        yes_action=attack,
        no_action=defend,
        priority=10
    ),
    no_action=DecisionNode(
        resources_critical,
        yes_action=DecisionNode(
            buildings_insufficient,
            yes_action=drop_resources,
            no_action=gather_resources,
            priority=8
        ),
        no_action=DecisionNode(
            has_enough_military,
            yes_action=train_military,
            no_action=DecisionNode(
                closest_town_center,
                yes_action=DecisionNode(
                    find_closest_resources,
                    yes_action=build_structure,
                    no_action=DecisionNode(
                        is_villager_full,
                        yes_action=drop_resources,
                        no_action=gather_resources,
                        priority=7
                    ),
                    priority=7
                ),
                no_action=gather_resources,
                priority=7
            ),
            priority=7
        ),
        priority=9
    ),
    priority=10
)

def choose_strategy(Player):
    Strategy_list=["agressive","defensive","balanced"]
    seed(time.perf_counter())
    n=randint(0,2)
    return Strategy_list[n]

class Player:
    
    def __init__(self, cell_Y, cell_X, team):
        self.team = team
        self.cell_Y = cell_Y
        self.cell_X = cell_X
        self.storages_id = set() # resource storages
        self.houses_id = set() # towncenters and storages

        self.current_population = 0
        self.homeless_units = 0

        self.entities_dict = {}
        self.linked_map = None

        self.decision_tree= tree
        self.ai_profile = AIProfile(strategy = choose_strategy(self))
        self.game_handler = GameEventHandler(self.linked_map,self,self.ai_profile)

        self.refl_acc = 0


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


            if isinstance(entity, Unit):
                if self.current_population <= self.get_current_population_capacity():
                    self.remove_population()
                else:
                    self.homeless_units -= 1
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

    def get_entities_by_class(self, representations, is_free = False): # list of representations for exemple : ['a', 'h', 'v']

        id_list = []
        
        for representation in representations:
            entity_dict = self.entities_dict.get(representation, None)

            if entity_dict:

                for entity_id in entity_dict:
                    entity = self.linked_map.get_entity_by_id(entity_id)
                    add = True

                    if is_free and not(entity.is_free()):
                        add = False
                    if add:
                        id_list.append(entity_id)

        return id_list

    def build_entity(self, villager_id_list, representation = "", entity_id = None):
        if villager_id_list:
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
        else:
            return 0



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

    def update_population(self,dt):
        pop = self.current_population
        cpop = self.get_current_population_capacity()
        if pop > cpop:
            self.homeless_units = pop - cpop

        elif pop < cpop and self.homeless_units > 0:
            range_val = self.homeless_units
            for _ in range(range_val):

                if not(self.add_population()):
                    break
                else:
                    self.homeless_units -= 1

        print(f"current population:{self.current_population}, current cap:{self.get_current_population_capacity()}")

    def entity_closest_to(self, ent_repr_list, cell_Y, cell_X): # we give the ent_repr for the entity we want and then we give a certain position and we will return the closest entity of the given type to the cell_X, cell_Y
        closest_id = None
        ent_ids = None

        for ent_repr in ent_repr_list:
            if ent_repr not in ["W", "G"]:
                print(f"Searching closest entity: {ent_repr} at coordinates ({cell_Y}, {cell_X})")
                ent_ids = self.get_entities_by_class(ent_repr)
            else:
                ent_ids = self.linked_map.resource_id_dict.get(ent_repr, None)
                
            if ent_ids:

                closest_dist = float('inf')

                for ent_id in ent_ids:

                    current_entity = self.linked_map.get_entity_by_id(ent_id)
                    if current_entity:

                        current_dist = math.dist([current_entity.cell_X, current_entity.cell_Y], [cell_X, cell_Y])

                        if current_dist < closest_dist:
                            closest_id = current_entity.id
                            closest_dist = current_dist 
            
        return closest_id
    
    def get_closest_ennemy(self):
        closest_id = None
        closest_distance = float('inf')
        for entity_id,entity in self.linked_map.entity_id_dict.items():
            if entity.team != self.team and isinstance(entity, Unit):
                current_distance = math.dist([entity.cell_X, entity.cell_Y],[self.cell_X,self.cell_Y])
                if current_distance < closest_distance:
                    closest_id = entity_id
                    closest_distance = current_distance
        closest_entity = self.linked_map.get_entity_by_id(closest_id)
        return closest_entity,closest_distance, closest_id
    
    def is_free(self):
        return 'is_free'

    def update(self, dt):
        self.update_population(dt)
        self.refl_acc+=dt
        if self.refl_acc>ONE_SEC/3:
            self.player_turn(dt)

    def player_turn(self,dt):
        print("Decision tree avant utilisation:", self.decision_tree)
        decision = self.game_handler.process_ai_decisions(self.decision_tree)
        print(f"Decision effectué : {decision}")
        self.refl_acc=0
    
        # # decision = self.ai_profile.decide_action(self.decision_tree, context)
        # return decision
    
    # def set_build(self, villager_id_list):
    #     i = 0
    #     while(i < 4):
    #         villager_id_list.append(self.villager_free[i])
    #         i += 1
    #     self.build_entity(villager_id_list, 'B')
    #     print(f"Before remove: villager_free = {self.villager_free}, attempting to remove {villager_id_list}")
    #     for villager_id in villager_id_list:
    #         if villager_id in self.villager_free:
    #             self.villager_free.remove(villager_id)
    #     self.villager_occupied.append(villager_id_list)


    # def set_resources(self, collector_id):
    #     drop_build_id = self.entity_closest_to('T', self.entities_dict['v'][collector_id].cell_Y, self.entities_dict['v'][collector_id].cell_X)
    #     object = self.linked_map.get_entity_by_id(drop_build_id)
    #     resource_id = self.entity_closet_to('G', object.cell_Y, object.cell_X)
    #     self.villager_free.remove(collector_id)
    #     self.set_collect(object,resource_id)
    #     self.villager_occupied.append(collector_id)

    # def set_collect(self, villager, entity_id):
    #     if not villager.is_full():
    #         villager.move_to(entity_id.position)
    #         villager.collect_entity(entity_id)


        