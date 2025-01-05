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

    def draw_resources(self, entity_matrix):
        player_1_data = {
            "F" : 0,
            "W" : 0,
            "G": 0,
            "v" : 0,
            "s" : 0,
            "h" : 0,
            "a" : 0,
            "T" : 0,
            "H" : 0,
            "C" : 0,
            "F" : 0,
            "B" : 0,
            "S" : 0,
            "A" : 0,
            "K" : 0,
            "ca": 0,
            "sm":0,
            "am":0
        }
        player_2_data = {
            "F" : 0,
            "W" : 0,
            "G": 0,
            "v" : 0,
            "s" : 0,
            "h" : 0,
            "a" : 0,
            "T" : 0,
            "H" : 0,
            "C" : 0,
            "F" : 0,
            "B" : 0,
            "S" : 0,
            "A" : 0,
            "K" : 0,
            "ca": 0,
            "sm":0,
            "am":0
        }
        for current_region in entity_matrix.values():
            for entity_set in current_region.values():
                for entity in entity_set:
                    if entity.team == 1:
                        player_1_data[entity.representation] += 1
                    elif entity.team == 2:
                        player_2_data[entity.representation] += 1


        # Position des joueurs
        player_1_pos = (10, 15)
        player_2_pos = (self.screen.get_width()//2, 15)

        # Y offsets distincts pour chaque joueur
        y_offset_player_1 = 0
        y_offset_player_2 = 0
        
        # Affichage des données des joueurs
        if self.display_resources:
            display_image(ICONS["Mi"], player_1_pos[0], player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Wi"], player_1_pos[0] + 100, player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            display_image(ICONS["Gi"], player_1_pos[0] + 200, player_1_pos[1]+y_offset_player_1, self.screen, 0x04)
            resources = f"     : {player_1_data['F']} |  : {player_1_data['W']} |   : {player_1_data['G']}"
            text = self.font.render(resources, True, WHITE_COLOR)
            self.screen.blit(text, (player_1_pos[0], player_1_pos[1] + y_offset_player_1))
            y_offset_player_1 += 20

        if self.display_units:
            units = f"Units - Villagers: {player_1_data['v']} | Swordsman: {player_1_data['s']} | Horseman: {player_1_data['h']} | Archer: {player_1_data['a']}"
            text = self.font.render(units, True, WHITE_COLOR)
            self.screen.blit(text, (player_1_pos[0], player_1_pos[1] + y_offset_player_1))
            y_offset_player_1 += 20

        if self.display_builds:
            builds = f"Builds - Town Centre : {player_1_data['T']} | House : {player_1_data['H']} | Camp : {player_1_data['C']} | Farm : {player_1_data['F']} | Barracks : {player_1_data['B']} | Stable : {player_1_data['S']} | Keep : {player_1_data['K']}"
            text = self.font.render(builds, True, WHITE_COLOR)
            self.screen.blit(text, (player_1_pos[0], player_1_pos[1] + y_offset_player_1))
            y_offset_player_1 += 20

        # Affichage des données pour Player 2
        if self.display_resources:
            resources = f"Player 2 - Food: {player_2_data['F']} | Wood: {player_2_data['W']} | Gold: {player_2_data['G']}"
            text = self.font.render(resources, True, WHITE_COLOR)
            self.screen.blit(text, (player_2_pos[0], player_2_pos[1] + y_offset_player_2))
            y_offset_player_2 += 20

        if self.display_units:
            units = f"Units - Villagers: {player_2_data['v']} | Swordsman: {player_2_data['s']} | Horseman: {player_2_data['h']} | Archer: {player_2_data['a']}"
            text = self.font.render(units, True, WHITE_COLOR)
            self.screen.blit(text, (player_2_pos[0], player_2_pos[1] + y_offset_player_2))
            y_offset_player_2 += 20

        if self.display_builds:
            builds = f"Builds - Town Centre : {player_2_data['T']} | House : {player_2_data['H']} | Camp : {player_2_data['C']} | Farm : {player_2_data['F']} | Barracks : {player_2_data['B']} | Stable : {player_2_data['S']} | Keep : {player_2_data['K']}"
            text = self.font.render(builds, True, WHITE_COLOR)
            self.screen.blit(text, (player_2_pos[0], player_2_pos[1] + y_offset_player_2))
            y_offset_player_2 += 20

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