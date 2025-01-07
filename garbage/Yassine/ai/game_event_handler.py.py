from GameField.map import Map
from ai_profiles import AIProfile
from Entity.entity import Entity
from Player.player import Player

class GameEventHandler:
    def __init__(self, map, players):
        self.map = map
        self.players = players
        self.ai_profiles = {
            player_id: AIProfile(strategy="balanced") for player_id in players
        }

    def process_ai_decisions(self):
        """
        Process AI decisions for all players.
        """
        for player_id, player in self.players.items():
            ai_profile = self.ai_profiles.get(player_id)
            if ai_profile:
                context = {'player': player, 'map': self.map}
                action = ai_profile.decide_action(context)
                print(f"Player {player_id} decided to: {action}")

    def run_event_cycle(self):
        """
        Run the event cycle to handle AI decisions and player events.
        """
        print("Processing AI decisions...")
        self.process_ai_decisions()
