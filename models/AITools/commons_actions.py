from GLOBAL_VAR import *
from GLOBAL_IMPORT import *

def perform_attack(context):
    for unit in context['units']:
        if unit['type'] == 'military':
            unit['instance'].attack_entity(context['enemy_id'])
    return "Attacking the enemy!"