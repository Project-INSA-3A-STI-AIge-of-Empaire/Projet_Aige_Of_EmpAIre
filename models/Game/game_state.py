import pygame
import random 
import webbrowser
#from Game.savegame import *
from ImageProcessingDisplay import UserInterface, StartMenu, PauseMenu, Camera, TerminalCamera 
from GameField.map import *
from GLOBAL_VAR import *
from Entity import *
from yattag import Doc
import tkinter as tk
from tkinter import filedialog, messagebox
import pickle

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
        self.selected_players = 2
        self.camera = Camera()
        self.terminal_camera = TerminalCamera()
        self.map = Map(MAP_CELLX,MAP_CELLY)
        self.display_mode = ISO2D # Mode d'affichage par défaut
        self.savegamefile = None
        # Pour gérer le délai de basculement d'affichage
        self.last_switch_time = 0
        self.switch_cooldown = ONE_SEC*(0.2)  # Délai de 200ms (0,2 secondes)
        self.full_screen = True
        self.mouse_held = False


    def start_game(self):
        """Méthode pour démarrer la génération de la carte après que l'utilisateur ait validé ses choix."""
        self.map.generate_map(self.selected_mode, self.selected_players)

    def set_map_type(self, map_type):
        self.selected_map_type = map_type

    def set_difficulty_mode(self, mode):
        self.selected_mode = mode

    def set_display_mode(self, mode):
        self.display_mode = mode

    def set_players(self, players):
        self.selected_players = players
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
            #self.screen.set_alpha(None)
        else:
            self.full_screen = False
            gameloop.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            #self.screen.set_alpha(None)
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
                gameloop.screen.set_alpha(None)
            elif self.display_mode == TERMINAL:
                self.display_mode = ISO2D
                gameloop.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                gameloop.screen.set_alpha(None)
            self.last_switch_time = current_time


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

    def generate_html_file(self):

        team_dict = {}
        for player in self.map.players_dict.values():
            team = player.team
            if team not in team_dict:
                team_dict[team] = {}

            for repr_key in player.entities_dict:
                if repr_key not in team_dict[team]:
                    team_dict[team][repr_key] = ""
                for ent in player.entities_dict[repr_key].values():
                    match ent:
                        case Unit():
                            team_dict[team][repr_key] += ent.get_unit_html()
                        case Building():
                            team_dict[team][repr_key] += ent.get_building_html()
                for repr_key in player.resources: 
                    if repr_key not in team_dict[team]:
                        team_dict[team][repr_key] = ""
                    total_value = 0
                    for repr_value in player.resources.values():
                        if isinstance(repr_value, int):  
                            total_value += repr_value
                        else:
                            team_dict[team][repr_key] += str(repr_value) 
                    team_dict[team][repr_key] += str(total_value)
            
                # Creation of the HTML file the  yattag library
            doc, tag, text = Doc().tagtext()

            doc.asis('<!DOCTYPE html>')
            with tag('html', lang='en'):
                with tag('head'):
                    with tag('script'):
                        text('''
            function toggleTeam(teamId) {
                var teamDiv = document.getElementById("team-" + teamId);
                if (teamDiv.style.display === "none") {
                    teamDiv.style.display = "block";
                } else {
                    teamDiv.style.display = "none";
                }
            }
                        ''')
                    with tag('title'):
                        text('Age of Empires - Overview')
                with tag('body'):
                    with tag('h1'):
                        text('Age of Empires - Overview')
                    for team in team_dict.keys():
                        with tag('button', onclick=f"toggleTeam({team})"):
                            text(f"Show Team {team}")
                    for team, entities in team_dict.items():
                        with tag('div', id=f"team-{team}", style="display:none;"):
                            with tag('h2'):
                                text(f"Team {team}")
                            for entity_type, html_content in entities.items():
                                with tag('h3'):
                                    text(entity_type)  # Titre du type d'entité (Unit, Building, Resource)
                                with tag('ul'):
                                    if html_content.strip():  # Si le contenu n'est pas vide
                                        with tag('li'):
                                            doc.asis(html_content)
                                    else:
                                        with tag('li'):
                                            text(f"No {entity_type}s available")

            # Sauvegarder le fichier HTML généré
            print("HTML content to write:", doc.getvalue())
            with open('overview.html', 'w') as f:
                f.write(doc.getvalue())
            webbrowser.open_new_tab('overview.html')   



        def select_save_file(self):
            # Initialise la fenêtre Tkinter
            root = tk.Tk()
            root.withdraw()  # Masquer la fenêtre principale

            # Ouvrir la boîte de dialogue pour sélectionner un fichier
            file_path = filedialog.askopenfilename(
                title="Sélectionner un fichier de sauvegarde",
                filetypes=[("Fichiers de sauvegarde", "*.save"), ("Tous les fichiers", "*.*")]
            )

            if file_path:
                # Affiche le chemin du fichier sélectionné
                print(f"Fichier sélectionné : {file_path}")
                messagebox.showinfo("Fichier sélectionné", f"Vous avez sélectionné : {file_path}")
            else:
                # Affiche un message si aucun fichier n'a été sélectionné
                print("Aucun fichier sélectionné.")
                messagebox.showwarning("Aucun fichier", "Vous n'avez pas sélectionné de fichier.")

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
