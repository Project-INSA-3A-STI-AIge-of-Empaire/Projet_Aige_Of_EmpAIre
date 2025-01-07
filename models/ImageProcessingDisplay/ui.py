import pygame
from GLOBAL_VAR import *
from ImageProcessingDisplay.imagemethods import *

class UserInterface:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.display_resources = False
        self.display_units = False
        self.display_builds = False

    def draw_resources(self, players_dict):
        player_1_data = {
            "F" : players_dict[1].resources["food"],
            "W" : players_dict[1].resources["wood"],
            "G": players_dict[1].resources["gold"],
            "v" : len(players_dict[1].entities_dict["v"]),
            "s" : len(players_dict[1].entities_dict["s"]),
            "h" : len(players_dict[1].entities_dict["h"]),
            "a" : len(players_dict[1].entities_dict["a"]),
            "T" : len(players_dict[1].entities_dict["T"]),
            "H" : len(players_dict[1].entities_dict["H"]),
            "C" : len(players_dict[1].entities_dict["C"]),
            "F" : len(players_dict[1].entities_dict["F"]),
            "B" : len(players_dict[1].entities_dict["B"]),
            "S" : len(players_dict[1].entities_dict["S"]),
            "A" : len(players_dict[1].entities_dict["A"]),
            "K" : len(players_dict[1].entities_dict["K"]),
            "ca": len(players_dict[1].entities_dict["ca"]),
            "sm":len(players_dict[1].entities_dict["sm"]),
            "am":len(players_dict[1].entities_dict["am"])
        }
        player_2_data = {
            "F" : players_dict[2].resources["food"],
            "W" : players_dict[2].resources["wood"],
            "G": players_dict[2].resources["gold"],
            "v" : len(players_dict[2].entities_dict["v"]),
            "s" : len(players_dict[2].entities_dict["s"]),
            "h" : len(players_dict[2].entities_dict["h"]),
            "a" : len(players_dict[2].entities_dict["a"]),
            "T" : len(players_dict[2].entities_dict["T"]),
            "H" : len(players_dict[2].entities_dict["H"]),
            "C" : len(players_dict[2].entities_dict["C"]),
            "F" : len(players_dict[2].entities_dict["F"]),
            "B" : len(players_dict[2].entities_dict["B"]),
            "S" : len(players_dict[2].entities_dict["S"]),
            "A" : len(players_dict[2].entities_dict["A"]),
            "K" : len(players_dict[2].entities_dict["K"]),
            "ca": len(players_dict[2].entities_dict["ca"]),
            "sm":len(players_dict[2].entities_dict["sm"]),
            "am":len(players_dict[2].entities_dict["am"])
        }
        
        for current_region in entity_matrix.values():
            for entity_set in current_region.values():
                for entity in entity_set:
                    if entity.team == 1:
                        player_1_data[entity.representation] += 1
                    elif entity.team == 2:
                        player_2_data[entity.representation] += 1


        # Position des joueurs
        player_1_pos = (20, 50)
        player_2_pos = (self.screen.get_width()//2, 50)

        # Y offsets distincts pour chaque joueur
        y_offset_player_1 = 0
        y_offset_player_2 = 0
        
        # Affichage des données des joueurs
        if self.display_resources:
            display_image(ICONS["Mi"], player_1_pos[0], player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Wi"], player_1_pos[0] + 105, player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Gi"], player_1_pos[0] + 210, player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            resources = f"    : {player_1_data['F']}           : {player_1_data['W']}           : {player_1_data['G']}"
            text = self.font.render(resources, True, WHITE_COLOR)
            self.screen.blit(text, (player_1_pos[0], player_1_pos[1]- 12 + y_offset_player_1))
            y_offset_player_1 += 50

        if self.display_units:
            display_image(ICONS["vi"], player_1_pos[0], player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["si"], player_1_pos[0] + 105, player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["hi"], player_1_pos[0] + 210, player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["ai"], player_1_pos[0] + 315, player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            units = f"    : {player_1_data['v']}           : {player_1_data['s']}           : {player_1_data['h']}           : {player_1_data['a']}"
            text = self.font.render(units, True, WHITE_COLOR)
            self.screen.blit(text, (player_1_pos[0], player_1_pos[1] -12 + y_offset_player_1))
            y_offset_player_1 += 50

        if self.display_builds:
            display_image(ICONS["Ti"], player_1_pos[0], player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Hi"], player_1_pos[0] + 105, player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Ci"], player_1_pos[0] + 210, player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Fi"], player_1_pos[0] + 315, player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Bi"], player_1_pos[0], player_1_pos[1]+ 50 +y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Si"], player_1_pos[0] + 105, player_1_pos[1]+ 50 +y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Ki"], player_1_pos[0] + 210, player_1_pos[1]+ 50 +y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Ai"], player_1_pos[0] + 315, player_1_pos[1]+ 50 +y_offset_player_1, self.screen, 0x04)
            builds = f"    : {player_1_data['T']}         : {player_1_data['H']}           : {player_1_data['C']}           : {player_1_data['F']}"
            builds2 = f"    : {player_1_data['B']}         : {player_1_data['S']}           : {player_1_data['K']}           : {player_1_data['A']}"
            text = self.font.render(builds, True, WHITE_COLOR)
            text2 = self.font.render(builds2, True, WHITE_COLOR)
            self.screen.blit(text, (player_1_pos[0], player_1_pos[1] - 12 + y_offset_player_1))
            self.screen.blit(text2, (player_1_pos[0], player_1_pos[1] - 12 + 50 + y_offset_player_1))
            y_offset_player_1 += 100

        # Affichage des données pour Player 2
        if self.display_resources:
            display_image(ICONS["Mi"], player_2_pos[0], player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["Wi"], player_2_pos[0] + 105, player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["Gi"], player_2_pos[0] + 210, player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            resources = f"    : {player_2_data['F']}           : {player_2_data['W']}           : {player_2_data['G']}"
            text = self.font.render(resources, True, WHITE_COLOR)
            self.screen.blit(text, (player_2_pos[0], player_2_pos[1]- 12 + y_offset_player_2))
            y_offset_player_2 += 50

        if self.display_units:
            display_image(ICONS["vi"], player_2_pos[0], player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["si"], player_2_pos[0] + 105, player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["hi"], player_2_pos[0] + 210, player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["ai"], player_2_pos[0] + 315, player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            units = f"    : {player_2_data['v']}           : {player_2_data['s']}           : {player_2_data['h']}           : {player_2_data['a']}"
            text = self.font.render(units, True, WHITE_COLOR)
            self.screen.blit(text, (player_2_pos[0], player_2_pos[1] -12 + y_offset_player_2))
            y_offset_player_2 += 50

        if self.display_builds:
            display_image(ICONS["Ti"], player_2_pos[0], player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["Hi"], player_2_pos[0] + 105, player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["Ci"], player_2_pos[0] + 210, player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["Fi"], player_2_pos[0] + 315, player_2_pos[1]+y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["Bi"], player_2_pos[0], player_2_pos[1]+ 50 +y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["Si"], player_2_pos[0] + 105, player_2_pos[1]+ 50 +y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["Ki"], player_2_pos[0] + 210, player_2_pos[1]+ 50 +y_offset_player_2, self.screen, 0x04)
            display_image(ICONS["Ai"], player_2_pos[0] + 315, player_2_pos[1]+ 50 +y_offset_player_2, self.screen, 0x04)
            builds = f"    : {player_2_data['T']}         : {player_2_data['H']}           : {player_2_data['C']}           : {player_2_data['F']}"
            builds2 = f"    : {player_2_data['B']}         : {player_2_data['S']}           : {player_2_data['K']}           : {player_2_data['A']}"
            text = self.font.render(builds, True, WHITE_COLOR)
            text2 = self.font.render(builds2, True, WHITE_COLOR)
            self.screen.blit(text, (player_2_pos[0], player_2_pos[1] - 12 + y_offset_player_2))
            self.screen.blit(text2, (player_2_pos[0], player_2_pos[1] - 12 + 50 + y_offset_player_2))
            y_offset_player_2 += 100

    def toggle_resources(self):
        self.display_resources = not self.display_resources

    def toggle_units(self):
        self.display_units = not self.display_units
    def toggle_builds(self):
        self.display_builds = not self.display_builds
    
    def toggle_all(self):
        self.display_resources = not self.display_resources
        self.display_units = not self.display_units
        self.display_builds = not self.display_builds