from Entity.entity import Entity
from Entity.building import Building
from GameField.map import Map

class DecisionNode:
    def __init__(self, question, yes_action=None, no_action=None, priority=0):
        self.question = question
        self.yes_action = yes_action
        self.no_action = no_action
        self.priority = priority

    def decide(self, context):
        actions = []

        if self.question(context):
            if isinstance(self.yes_action, DecisionNode):
                actions.extend(self.yes_action.decide(context))
            elif callable(self.yes_action):
                actions.append((self.yes_action, self.priority))
        else:
            if isinstance(self.no_action, DecisionNode):
                actions.extend(self.no_action.decide(context))
            elif callable(self.no_action):
                actions.append((self.no_action, self.priority))

        actions.sort(key=lambda x: x[1], reverse=True)
        return [action[0]() for action in actions]

# Exemple de questions et actions
def is_under_attack(context):
    return any(entity.hp < entity.max_hp for entity in context['map'].entity_matrix.values())

def resources_low(context):
    player = context['player']
    return player.resources['gold'] < 100 or player.resources['food'] < 100

def train_unit():
    return "Train a new unit."

def build_structure():
    return "Build a new structure."

def defend():
    return "Defend the base."

tree = DecisionNode(
    is_under_attack,
    yes_action=DecisionNode(
        resources_low,
        yes_action=build_structure,
        no_action=train_unit,
        priority=5
    ),
    no_action=defend,
    priority=10
)
