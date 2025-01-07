class Player:
    
    def __init__(self, team, resources = {"gold":0,"wood":0,"food":0}):
        self.team = team
        self.resources = resources
        self.entities_matrix = {}
        self.linked_map = None

    def add_resources(self, resources):

        for resource, amount in resources.items():
            if resource in self.resources and isinstance(amount, (int, float)): # the isinstance is just to prevent undefined behavior ( if happend)
                self.resources[resource] += amount
    
    def remove_resources(self, resources):

        for resource, amount in resources.items():
            if resource in self.resources and isinstance(amount, (int, float )):
                self.resources[resource] = max(0, self.resources[resource] - amount) # in case something unusual happen so the currency doesnt drop to neg numbers, it is not going to happen but who knows
    
    def add_entity(self, entity):

        entity_dict = self.entities_matrix.get(entity.representation, None)

        if entity_dict == None:
            self.entities_matrix[entity.representation] = {}
            entity_dict = self.entities_matrix.get(entity.representation, None)
        
        entity_dict[entity.id] = entity

    def remove_entity(self, entity):

        entity_dict = self.entities_matrix.get(entity.representation, None)
        if entity_dict:
            entity_dict.pop(entity.id, None)

            if not entity_dict: # if empty remove 
                self.entities_matrix.pop(entity.representation, None)

            return 1
        return 0

    def get_entities_by_class(self, representations): # list of representations for exemple : ['a', 'h', 'v']

        id_list = []
        
        for representation in representations:
            entity_dict = self.entities_matrix.get(representation, None)

            if entity_dict:

                for entity_id in entity_dict:
                    id_list.append(entity_id)
        
        return id_list
    
