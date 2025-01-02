

class IdGenerator:

    def __init__(self, _id_ticket = 0):
        self.id_ticket = _id_ticket

    def give_ticket(self):
        old_ticket = self.id_ticket
        self.id_ticket += 1

        return old_ticket
    
ID_GENERATOR = IdGenerator() # this needs to be save and load to properly give the ids for entities

