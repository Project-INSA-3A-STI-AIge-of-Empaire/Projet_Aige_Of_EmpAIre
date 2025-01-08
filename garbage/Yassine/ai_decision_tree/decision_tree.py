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
            else:
                if callable(self.yes_action):
                    actions.append((self.yes_action, self.priority))
        else:
            if isinstance(self.no_action, DecisionNode):
                actions.extend(self.no_action.decide(context))
            else:
                if callable(self.no_action):
                    actions.append((self.no_action, self.priority))

        actions.sort(key=lambda x: x[1], reverse=True)

        return [action[0]() for action in actions]
# ---- Questions ----
def is_under_attack(context):
    return context['under_attack']

def resources_critical(context):
    return context['resources']['gold'] < 50 or context['resources']['food'] < 50

def buildings_insufficient(context):
    return not context['buildings'].get('storage', False)

def has_enough_military(context):
    return context['military_units'] >= 10

def enemy_visible(context):
    return context['enemy_visible']

def is_storage_full(context):
    return context['resources']['gold'] >= 500 or context['resources']['food'] >= 500

def is_enemy_nearby(context):
    return context['enemy_distance'] < 10

def is_army_balanced(context):
    units = context['military_units_details']
    return units.get('archers', 0) > 2 and units.get('infantry', 0) > 2

def is_critical_building_damaged(context):
    return any(b['hp'] < b['max_hp'] * 0.5 for b in context['buildings']['critical'])

def is_ready_for_expansion(context):
    return context['resources']['gold'] > 300 and context['resources']['food'] > 300 and context['military_units'] >= 20

# ---- Actions ----
def defend():
    return "Defend the village!"

def gather_resources():
    return "Gather critical resources!"

def build_or_upgrade():
    return "Build or upgrade buildings!"

def train_military():
    return "Train military units!"

def attack():
    return "Attack the enemy!"

def repair_buildings():
    return "Repair critical buildings!"

def build_storage():
    return "Build a new storage facility!"

def attack_nearest_enemy():
    return "Attack the nearest enemy!"

def strengthen_army():
    return "Strengthen the army with diverse units!"

def repair_critical_buildings():
    return "Repair critical buildings!"

def expand_territory():
    return "Expand the territory!"
tree = DecisionNode(
    is_under_attack,
    yes_action=DecisionNode(
        is_enemy_nearby,
        yes_action=attack_nearest_enemy,
        no_action=defend,
        priority=10
    ),
    no_action=DecisionNode(
        resources_critical,
        yes_action=DecisionNode(
            is_storage_full,
            yes_action=build_storage,
            no_action=gather_resources,
            priority=9
        ),
        no_action=DecisionNode(
            buildings_insufficient,
            yes_action=build_or_upgrade,
            no_action=DecisionNode(
                is_ready_for_expansion,
                yes_action=expand_territory,
                no_action=DecisionNode(
                    is_critical_building_damaged,
                    yes_action=repair_critical_buildings,
                    no_action=DecisionNode(
                        is_army_balanced,
                        yes_action=train_military,
                        no_action=strengthen_army,
                        priority=7
                    ),
                    priority=8
                )
            ),
            priority=6
        )
    )
)
