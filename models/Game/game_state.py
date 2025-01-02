import pygame
import random 
import webbrowser
#from Game.savegame import *
from ImageProcessingDisplay import UserInterface, StartMenu, PauseMenu, Camera, TerminalCamera 
from GameField.map import *
from GLOBAL_VAR import *

class GameState:
    def __init__(self, screen):
        #self.save_manager = Savegame(self)
        self.states = START
        self.screen = screen
        self.startmenu = StartMenu(screen)
        self.pausemenu = PauseMenu(screen)
        self.ui = UserInterface(screen)
        self.speed = 1
        self.selected_map_type = MAP_NORMAL
        self.selected_mode = LEAN
        self.camera = Camera()
        self.terminal_camera = TerminalCamera()
        self.map = Map(MAP_CELLX,MAP_CELLY)
        self.display_mode = ISO2D # Mode d'affichage par défaut
        # Pour gérer le délai de basculement d'affichage
        self.last_switch_time = 0
        self.switch_cooldown = ONE_SEC*(0.2)  # Délai de 200ms (0,2 secondes)
        self.full_screen = True
        self.mouse_held = False


    def start_game(self):
        """Méthode pour démarrer la génération de la carte après que l'utilisateur ait validé ses choix."""
        self.map.generate_map()

    def set_map_type(self, map_type):
        self.selected_map_type = map_type

    def set_difficulty_mode(self, mode):
        self.selected_mode = mode

    def set_display_mode(self, mode):
        self.display_mode = mode

    def toggle_pause(self):
        """Activer/désactiver la pause avec un délai pour éviter le spam."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time >= self.switch_cooldown:
            if self.states == PAUSE:
                self.states = PLAY
            elif self.states == PLAY:
                self.states = PAUSE
            self.last_switch_time = current_time

    def toggle_fullscreen(self, gameloop):
        if not(self.full_screen):
            self.full_screen = True
            gameloop.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        else:
            self.full_screen = False
            gameloop.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    def set_speed(self, new_speed):
        if new_speed > 0:
            self.speed = new_speed
    
    def toggle_display_mode(self, gameloop):
        """Bascule entre les modes d'affichage Terminal et 2.5D."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time >= self.switch_cooldown:
            if self.display_mode == ISO2D:
                self.display_mode = TERMINAL
                gameloop.screen = pygame.display.set_mode((20, 20), pygame.HWSURFACE | pygame.DOUBLEBUF )
            elif self.display_mode == TERMINAL:
                self.display_mode = ISO2D
                gameloop.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

            self.last_switch_time = current_time

    def update(self):
        if (self.states != PAUSE):
            pass

    def generate_html_file(self):
        with open("Game/generate.html", "r") as template_file:
            html_content = template_file.read()
    
       
        # buildings_positions = [(1, 2), (3, 4)]
        # building_list_html = ""
        # for i, position in enumerate(buildings_positions, start=1):  # Utiliser enumerate pour avoir un index
        #     building_list_html += f"""<li class="building">Building {i} : {position}</li>"""

        dict_archeryrange1 = {}
        dict_archeryrange2 = {}
        dict_barracks1 = {}
        dict_barracks2 = {}
        dict_camp1 = {}
        dict_camp2 = {}
        dict_farm1 = {}
        dict_farm2 = {}
        dict_house1 = {}
        dict_house2 = {}
        dict_keep1 = {}
        dict_keep2 = {}
        dict_stable1 = {}
        dict_stable2 = {}
        dict_towncenter1 = {}
        dict_towncenter2 = {}
        dict_unit1 = {}
        dict_unit2 = {}
        for current_region in self.map.entity_matrix.values():
            for entity_set in current_region.values():
                for entity in entity_set:
                        match type(entity):
                            case ArcheryRange if entity.team == 1 :
                                if entity.position not in dict_archeryrange1.values():
                                    dict_archeryrange1[len(dict_archeryrange1)] = entity.position
                            case ArcheryRange if entity.team == 2 :
                                if entity.position not in dict_archeryrange2.values():
                                    dict_archeryrange2[len(dict_archeryrange2)] = entity.position
                            case Barracks if entity.team == 1 :
                                if entity.position not in dict_barracks1.values():
                                    dict_barracks1[len(dict_barracks1)] = entity.position
                            case Barracks if entity.team == 2 : 
                                if entity.poition not in dict_barracks2.values():
                                    dict_barracks2[len(dict_barracks2)] = entity.position
                            case Camp if entity.team == 1 :
                                if entity.position not in dict_camp1.values():
                                    dict_camp1[len(dict_camp1)] = entity.position
                            case Camp if entity.team == 2 :
                                if entity.position not in dict_camp2.values():
                                    dict_camp2[len(dict_camp2)] = entity.position
                            case Farm if entity.team == 1 :
                                if entity.position not in dict_farm1.values():
                                    dict_farm1[len(dict_farm1)] = entity.position
                            case Farm if entity.team == 2 :
                                if entity.position not in dict_farm2.values():
                                    dict_farm2[len(dict_farm2)] = entity.position
                            case House if entity.team == 1 :
                                if entity.position not in dict_house1.values():
                                    dict_house1[len(dict_house1)] = entity.position
                            case House if entity.team == 2 :
                                if entity.position not in dict_house2.values():
                                    dict_house2[len(dict_house2)] = entity.position
                            case Keep if entity.team == 1 :
                                if entity.position not in dict_keep1.values():
                                    dict_keep1[len(dict_keep1)] = entity.position
                            case Keep if entity.team == 2 :
                                if entity.position not in dict_keep2.values():
                                    dict_keep2[len(dict_keep2)] = entity.position
                            case Stable if entity.team == 1 :
                                if entity.position not in dict_stable1.values():
                                    dict_stable1[len(dict_stable1)] = entity.position
                            case Stable if entity.team == 2 :
                                if entity.position not in dict_stable2.values():
                                    dict_stable2[len(dict_stable2)] = entity.position
                            case TownCenter if entity.team == 1 :
                                if entity.position not in dict_towncenter1.values():
                                    dict_towncenter1[len(dict_towncenter1)] = entity.position
                            case TownCenter if entity.team == 2 :
                                if entity.position not in dict_camp2.values():
                                    dict_towncenter2[len(dict_towncenter2)] = entity.position
                            case Unit if entity.team == 1 :
                                if entity.position not in dict_unit1.values():
                                    dict_unit1[len(dict_unit1)] = entity.position
                            case Unit if entity.team == 2 :
                                if entity.position not in dict_unit2.values():
                                    dict_unit2[len(dict_unit2)] = entity.position
        
        # Génération des listes HTML par type de bâtiment pour l'équipe 1
        archeryrange1_list_html = ""
        for i, position in dict_archeryrange1.items():
            archeryrange1_list_html += f'<li class="building">ArcheryRange {i} : {position}</li>'

        barracks1_list_html = ""
        for i, position in dict_barracks1.items():
            barracks1_list_html += f'<li class="building">Barracks {i} : {position}</li>'

        camp1_list_html = ""
        for i, position in dict_camp1.items():
            camp1_list_html += f'<li class="building">Camp {i} : {position}</li>'

        farm1_list_html = ""
        for i, position in dict_farm1.items():
            farm1_list_html += f'<li class="building">Farm {i} : {position}</li>'

        house1_list_html = ""
        for i, position in dict_house1.items():
            house1_list_html += f'<li class="building">House {i} : {position}</li>'

        keep1_list_html = ""
        for i, position in dict_keep1.items():
            keep1_list_html += f'<li class="building">Keep {i} : {position}</li>'

        stable1_list_html = ""
        for i, position in dict_stable1.items():
            stable1_list_html += f'<li class="building">Stable {i} : {position}</li>'

        towncenter1_list_html = ""
        for i, position in dict_towncenter1.items():
            towncenter1_list_html += f'<li class="building">TownCenter {i} : {position}</li>'

        # Génération des listes HTML par type de bâtiment pour l'équipe 2
        archeryrange2_list_html = ""
        for i, position in dict_archeryrange2.items():
            archeryrange2_list_html += f'<li class="building">ArcheryRange {i} : {position}</li>'

        barracks2_list_html = ""
        for i, position in dict_barracks2.items():
            barracks2_list_html += f'<li class="building">Barracks {i} : {position}</li>'

        camp2_list_html = ""
        for i, position in dict_camp2.items():
            camp2_list_html += f'<li class="building">Camp {i} : {position}</li>'

        farm2_list_html = ""
        for i, position in dict_farm2.items():
            farm2_list_html += f'<li class="building">Farm {i} : {position}</li>'

        house2_list_html = ""
        for i, position in dict_house2.items():
            house2_list_html += f'<li class="building">House {i} : {position}</li>'

        keep2_list_html = ""
        for i, position in dict_keep2.items():
            keep2_list_html += f'<li class="building">Keep {i} : {position}</li>'

        stable2_list_html = ""
        for i, position in dict_stable2.items():
            stable2_list_html += f'<li class="building">Stable {i} : {position}</li>'

        towncenter2_list_html = ""
        for i, position in dict_towncenter2.items():
            towncenter2_list_html += f'<li class="building">TownCenter {i} : {position}</li>'

        unit1_list_html = ""
        for i, e in dict_unit1.items():
            unit1_list_html +=f'<li class="unit">Unit {i} : {e}</li>'

        unit2_list_html = ""
        for i, e in dict_unit2.items():
            unit2_list_html +=f'<li class="unit">Unit {i} : {e}</li>'
        
        html_content = html_content.replace("{{ARCHERYRANGE1}}", archeryrange1_list_html)
        html_content = html_content.replace("{{ARCHERYRANGE2}}", archeryrange2_list_html)

        html_content = html_content.replace("{{BARRACKS1}}", barracks1_list_html)
        html_content = html_content.replace("{{BARRACKS2}}", barracks2_list_html)

        html_content = html_content.replace("{{CAMP1}}", camp1_list_html)
        html_content = html_content.replace("{{CAMP2}}", camp2_list_html)

        html_content = html_content.replace("{{FARM1}}", farm1_list_html)
        html_content = html_content.replace("{{FARM2}}", farm2_list_html)

        html_content = html_content.replace("{{HOUSE1}}", house1_list_html)
        html_content = html_content.replace("{{HOUSE2}}", house2_list_html)

        html_content = html_content.replace("{{KEEP1}}", keep1_list_html)
        html_content = html_content.replace("{{KEEP2}}", keep2_list_html)

        html_content = html_content.replace("{{STABLE1}}", stable1_list_html)
        html_content = html_content.replace("{{STABLE2}}", stable2_list_html)

        html_content = html_content.replace("{{TOWNCENTER1}}", towncenter1_list_html)
        html_content = html_content.replace("{{TOWNCENTER2}}", towncenter2_list_html)

        html_content = html_content.replace("{{UNITS1}}", unit1_list_html)
        html_content = html_content.replace("{{UNITS2}}", unit2_list_html)

        # Write the modified HTML content to a new file
        with open("overview.html", "w") as output_file:
            output_file.write(html_content)
        webbrowser.open_new_tab('overview.html')


    def toggle_resources(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time >= self.switch_cooldown:
            self.ui.toggle_resources()
            self.last_switch_time = current_time

    def toggle_units(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time >= self.switch_cooldown:
            self.ui.toggle_units()
            self.last_switch_time = current_time
    def toggle_builds(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time >= self.switch_cooldown:
            self.ui.toggle_builds()
            self.last_switch_time = current_time
    
    def toggle_all(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time >= self.switch_cooldown:
            self.ui.toggle_all()
            self.last_switch_time = current_time

    # def draw_pause_text(self, screen):
    #     """Affiche le texte 'Jeu en pause' au centre de l'écran."""
    #     font = pygame.font.SysFont('Arial', 48)
    #     text = font.render("Jeu en pause", True, (255, 0, 0))  # Rouge pour le texte
    #     text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    #     screen.blit(text, text_rect)

    

    # def draw_minimap(self, screen):
    #     minimap_size = (200, 200)  # Dimensions de la minimap
    #     minimap_surface = pygame.Surface(minimap_size)
    #     minimap_surface.fill((50, 50, 50))  # Couleur de fond de la minimap

    #     # Taille de la carte
    #     map_width, map_height = len(self.grid[0]), len(self.grid)
    #     scale_x = minimap_size[0] / map_width
    #     scale_y = minimap_size[1] / map_height

    #     # Dessiner les ressources
    #     for y in range(map_height):
    #         for x in range(map_width):
    #             if self.grid[y][x] != '.':
    #                 color = (34, 139, 34) if isinstance(self.grid[y][x], Wood) else (255, 215, 0)
    #                 pygame.draw.rect(
    #                     minimap_surface,
    #                     color,
    #                     pygame.Rect(x * scale_x, y * scale_y, scale_x, scale_y)
    #                 )

    #     # Calculer les dimensions visibles
    #     screen_width, screen_height = screen.get_size()
    #     visible_tiles_x = screen_width / self.tile_size
    #     visible_tiles_y = screen_height / self.tile_size

    #     # Limiter la caméra aux bords de la carte
    #     self.camera_x = max(0, min(self.camera_x, map_width - visible_tiles_x))
    #     self.camera_y = max(0, min(self.camera_y, map_height - visible_tiles_y))

    #     # Position et taille du rectangle
    #     rect_x = self.camera_x * scale_x
    #     rect_y = self.camera_y * scale_y
    #     rect_width = min(visible_tiles_x * scale_x, minimap_size[0] - rect_x)
    #     rect_height = min(visible_tiles_y * scale_y, minimap_size[1] - rect_y)

    #     # Dessiner le rectangle jaune
    #     pygame.draw.rect(
    #         minimap_surface,
    #         (255, 255, 0),
    #         pygame.Rect(rect_x, rect_y, rect_width, rect_height),
    #         2
    #     )

    #     # Position de la minimap sur l'écran
    #     minimap_position = (screen.get_width() - minimap_size[0] - 10, screen.get_height() - minimap_size[1] - 10)
    #     screen.blit(minimap_surface, minimap_position)
