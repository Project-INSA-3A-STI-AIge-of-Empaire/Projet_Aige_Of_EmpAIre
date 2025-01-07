class DecisionNode:
    def __init__(self, question, yes_action=None, no_action=None, priority=0):
        """
        Représente un nœud de décision dans l'arbre.
        :param question: Fonction booléenne qui évalue le contexte.
        :param yes_action: Action ou sous-arbre si la question est vraie.
        :param no_action: Action ou sous-arbre si la question est fausse.
        :param priority: Priorité de ce nœud dans la prise de décision.
        """
        self.question = question
        self.yes_action = yes_action
        self.no_action = no_action
        self.priority = priority

    def decide(self, context):
        """
        Parcourt l'arbre pour déterminer l'action à exécuter.
        Trie les actions selon leur priorité.
        :param context: Dictionnaire contenant les caractéristiques du jeu.
        :return: Liste des actions exécutées triées par priorité.
        """
        actions = []

        # Vérifie la question pour choisir la branche oui/non
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

        # Trie les actions par priorité (priorité élevée en premier)
        actions.sort(key=lambda x: x[1], reverse=True)

        # Exécute les actions
        results = []
        for action, _ in actions:
            if callable(action):  # Si c'est une fonction
                results.append(action())
            else:  # Si c'est déjà un résultat
                results.append(action)

        return results


# ---- Définir les questions ----
def is_under_attack(context):
    return context['under_attack']

def resources_critical(context):
    return context['gold'] < 50 or context['food'] < 50

def buildings_insufficient(context):
    return not context['buildings'].get('storage', False)

def has_enough_military(context):
    return context['military_units'] >= 10

def enemy_visible(context):
    return context['enemy_visible']


# ---- Définir les actions ----
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


# ---- Construire l'arbre de décision ----
tree = DecisionNode(
    is_under_attack,
    yes_action=DecisionNode(
        lambda context: True,  # Défendre a toujours la plus haute priorité en cas d'attaque
        yes_action=defend,
        no_action=None,
        priority=10
    ),
    no_action=DecisionNode(
        resources_critical,
        yes_action=DecisionNode(
            lambda context: True,
            yes_action=gather_resources,
            no_action=None,
            priority=9
        ),
        no_action=DecisionNode(
            buildings_insufficient,
            yes_action=DecisionNode(
                lambda context: True,
                yes_action=build_or_upgrade,
                no_action=None,
                priority=8
            ),
            no_action=DecisionNode(
                has_enough_military,
                yes_action=DecisionNode(
                    enemy_visible,
                    yes_action=DecisionNode(
                        lambda context: True,
                        yes_action=attack,
                        no_action=None,
                        priority=7
                    ),
                    no_action=DecisionNode(
                        lambda context: True,
                        yes_action=repair_buildings,
                        no_action=None,
                        priority=5
                    )
                ),
                no_action=DecisionNode(
                    lambda context: True,
                    yes_action=train_military,
                    no_action=None,
                    priority=6
                )
            )
        )
    )
)

# ---- Exemple de contextes ----
context_1 = {
    'under_attack': True,
    'gold': 100,
    'food': 150,
    'military_units': 10,
    'enemy_visible': False,
    'buildings': {'storage': True, 'barracks': True}
}

context_2 = {
    'under_attack': False,
    'gold': 30,
    'food': 60,
    'military_units': 5,
    'enemy_visible': True,
    'buildings': {'storage': False, 'barracks': True}
}

# ---- Tester l'arbre ----
actions_1 = tree.decide(context_1)
actions_2 = tree.decide(context_2)

print("Actions pour contexte 1 :", actions_1)
print("Actions pour contexte 2 :", actions_2)
