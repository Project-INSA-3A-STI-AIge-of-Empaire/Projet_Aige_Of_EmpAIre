from Entity.entity import *
from .player import *
# from GameField.map import Map
# from .player import DecisionNode
# from .decision_tree import tree  # Import the decision tree to use its structure.

class AIProfile:
    def __init__(self, strategy, aggressiveness=1.0, defense=1.0):
        """
        Initialize the AI profile with a specific strategy.
        :param strategy: Strategy type ('aggressive', 'defensive', 'balanced')
        :param aggressiveness: Aggressiveness level
        :param defense: Defense level
        """
        self.strategy = strategy
        self.aggressiveness = aggressiveness
        self.defense = defense

    def compare_ratios(self, actual_ratios, target_ratios, context):
        differences = {}
        for key, target in target_ratios.items():
            actual = actual_ratios.get(key, 0)
            diff = abs(target - actual)
            differences[key] = diff
        sorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)
        for building_repr in sorted_differences:
            existing_ids = set(context['player'].get_entities_by_class(['A','B','C','K','T', 'F', 'S', 'H']))
            print(f"Old list of building : {existing_ids}")
            result = context['player'].build_entity(context['player'].get_entities_by_class('v'), building_repr[0])
            print(f"Résultat de build_entity : {result}")
            new_ids = set(context['player'].get_entities_by_class(['A','B','C','K','T', 'F', 'S', 'H']))
            print(f"New list of buildings {new_ids}")
            new_building_ids = new_ids - existing_ids
            if result != 0:
                new_building_id = new_building_ids.pop()
                building = context['player'].linked_map.get_entity_by_id(new_building_id)
                if building.state == BUILDING_ACTIVE:
                    return
            # elif result == 0:
            #         print("test compare ratios ==0")
            #         for villager in context['units']['villager']:
            #             if villager.state == UNIT_IDLE:
            #                 villager.collect_entity(context['resource_id'])  # Start collecting resources
            #             elif villager.is_full():
            #                 villager.drop_to_entity(context['drop_off_id'])
            #         return "Gathered resources"
                


    def decide_action(self,tree, context):
        """
        Decide the action to perform based on strategy and decision tree.
        :param context: Dictionary containing the current game state.
        :return: The chosen action as a string.
        """
        # Get the actions from the decision tree
        if context['player'].is_busy:
            print("Player is busy. Waiting for the current action to complete.")
            return
        actions = tree.decide(context)
        print(f"The action is : {actions}")
        print(f"The strategy is : {self.strategy}")

        # Call the appropriate strategy
        if self.strategy == "aggressive":
            return self._aggressive_strategy(actions, context)
        elif self.strategy == "defensive":
            return self._defensive_strategy(actions, context)
        elif self.strategy == "balanced":
            return self._balanced_strategy(actions, context)

    def _aggressive_strategy(self, actions, context):
        """
        Implement the aggressive strategy by prioritizing attacks and military training.
        """
        target_ratios = {
            'T': 0.1,
            'H': 0.15,   
            'C': 0.1,   
            'F': 0.1,    
            'B': 0.2,    
            'S': 0.15,  
            'A': 0.15,   
            'K': 0.05
        }
        player = context['player']
        map = context['map']

        try:
            for action in actions:
                if action == "Attack the enemy!":
                    return attack(context)

                if action == "Train military units!":
                    # Train military units in training buildings
                    training_buildings = context['buildings']['training']
                    for building in training_buildings:
                        (context[player].linked_map.get_entity_by_id(building)).train_unit(context[player], 'h')  # Train HorseMan
                    return "Trained military units"
                
                if action == "Building structure!":
                    print("bonjour")
                    self.compare_ratios(context['buildings']['ratio'], target_ratios, context)
                    return "Structure are built!"

            # Default to gathering resources if no attack actions are possible
            return "Gather resources for further attacks"
        finally:
            context['player'].is_busy = False

    def _defensive_strategy(self, actions, context):
        """
        Implement the defensive strategy by focusing on repairs and defenses.
        """
        player = context['player']
        map = context['map']
        target_ratios = {
            'T': 0.1,
            'H': 0.15,   
            'C': 0.1,   
            'F': 0.1,    
            'B': 0.05,    
            'S': 0.15,  
            'A': 0.15,   
            'K': 0.2
        }

        try:
            for action in actions:
                if action == "Defend the village!":
                    # Defend the village by attacking enemies
                    military_units = player.get_entities_by_class(['h', 'a', 's'])
                    for unit_id in military_units:
                        unit = map.get_entity_by_id(unit_id)
                        unit.attack_entity(context['enemy_id'])  # Attack the enemy
                    return "Executed defense strategy"

                if action == "Repair critical buildings!":
                    # Repair damaged buildings
                    buildings_to_repair = [
                        building for building in map.entity_matrix.values()
                        if isinstance(building, Building) and building.hp < building.max_hp
                    ]
                    for building in buildings_to_repair:
                        building.repair()  # Assuming a repair method exists in Building class
                    return "Repaired critical buildings"
                
                if action == "Building structure!":
                    print("hello")
                    self.compare_ratios(context['buildings']['ratio'], target_ratios, context)
                    return "Structure are built!"

            # for villager in context['units']['villager']:
            #     if not villager.is_full() and is_unit_idle(villager):
            #         villager.collect_entity(context['resource_id'])
            #     else:
            #         drop_resources(context)
            # return "Gathering resources!"
        finally:
            context['player'].is_busy = False

    def _balanced_strategy(self, actions, context):
        """
        Implement the balanced strategy by combining gathering, training, and attacks.
        """
        player = context['player']
        map = context['map']
        target_ratios = {
            'T': 0.15,
            'H': 0.2,   
            'C': 0.1,   
            'F': 0.15,    
            'B': 0.1,    
            'S': 0.1,  
            'A': 0.1,   
            'K': 0.1
        }

        try:
            for action in actions:
                if action == "Gathering resources!":
                    # Gather resources with villager
                    for villager in context['units']['villager']:
                        villager.collect_entity(context['resource_id'])  # Start collecting resources
                    return "Gathered resources"

                elif action == "Dropping off resources!":
                    # Drop resources in storage buildings
                    villagers = player.get_entities_by_class(['v'])
                    for villager_id in villagers:
                        villager = player.linked_map.get_entity_by_id(villager_id)
                        villager.drop_to_entity(context['drop_off_id'])  # Drop off resources
                    return "Dropped off resources"

                elif action == "Train military units!":
                    # Train military units in training buildings
                    training_buildings = context['buildings']['training']
                    if training_buildings == None:
                        action = "Building structure!"
                    for building in training_buildings:
                        building['instance'].train_unit(player, context['current_time'], 'v')  # Train Villager
                    return "Trained military units"

                elif action == "Attack the enemy!":
                    # Attack the enemy
                    military_units = player.get_entities_by_class(['h', 'a', 's'])
                    for unit_id in military_units:
                        unit = map.get_entity_by_id(unit_id)
                        unit.attack_entity(context['enemy_id'])  # Attack the enemy
                    return "Executed attack strategy"
                
                elif action == "Building structure!":
                    self.compare_ratios(context['buildings']['ratio'], target_ratios, context)
                    return "Structure are built!"
        finally:
            context['player'].is_busy = False
        # Default to gathering resources if no actions are possible
        return "Gathered resources for balanced strategy"

