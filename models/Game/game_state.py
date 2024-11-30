import pygame
import random
from GLOBAL_VAR import *
from entities.unit import Villager
from entities.resource import Wood, Gold, Food
from entities.building import TownCentre
class GameState:
    def __init__(self, tmap):
        self.is_paused = False
        self.speed = 1
        self.tile_size = 10
        self.grid = [['.' for _ in range(120)] for _ in range(120)]
        self.selected_map_type = "Carte Normal"
        self.selected_mode = "Lean"
        self.camera_x = 0
        self.camera_y = 0
        self.display_mode = "Terminal"  # Mode d'affichage par défaut
        # Pour gérer le délai de basculement d'affichage
        self.last_switch_time = 0
        self.switch_cooldown = 200  # Délai de 200ms (0,2 secondes)
                # Cooldown pour activer/désactiver la pause
        self.last_pause_time = 0
        self.pause_cooldown = 200  # Délai de 0.2 secondes pour la pause
        self.last_zoom_time = 0
        self.zoom_cooldown = 100  # Délai de 0.2 secondes pour le zoom
        self.tmap = tmap

    def start_game(self):
        """Méthode pour démarrer la génération de la carte après que l'utilisateur ait validé ses choix."""
        self.generate_map()

    def set_map_type(self, map_type):
        self.selected_map_type = map_type
        # La carte ne doit pas être régénérée immédiatement ici
        # Si vous souhaitez régénérer la carte immédiatement après chaque changement, décommentez la ligne suivante :
        # self.generate_map()

    def set_difficulty_mode(self, mode):
        self.selected_mode = mode

    def set_display_mode(self, mode):
        self.display_mode = mode

    def generate_map(self):
        match self.selected_map_type:
            case "Carte Normal":
                map_type = NORMAL_MAP
            case "Carte Centrée":
                map_type = CENTERED_MAP
        match self.selected_mode:
            case "Lean":
                self.tmap.generate_map(num_players=2)
            case "Mean":
                self.tmap.generate_map(num_players=2)
            case "Marines":
                self.tmap.generate_map(num_players=2)


    def place_resources_and_buildings(self):
        if self.selected_mode in ["Lean", "Mean"]:
            self.place_town_centre(1)
            self.place_villagers(3)
            if self.selected_mode == "Mean":
                self.place_military_buildings()
        elif self.selected_mode == "Marines":
            self.place_town_centre(3)
            self.place_villagers(15)
            self.place_military_buildings()

    def place_town_centre(self, count):
        for _ in range(count):
            x, y = self.random_empty_position()
            self.grid[y][x] = TownCentre()  # Place une instance de TownCentre

    def place_villagers(self, count):
        for _ in range(count):
            x, y = self.random_empty_position()
            self.grid[y][x] = Villager()  # Place une instance de Villager

    def place_military_buildings(self):
        """Place les bâtiments militaires (Barracks, Stable, Archery Range)."""
        buildings = ['B', 'S', 'A']  # 'B' pour Barracks, 'S' pour Stable, 'A' pour Archery Range
        for building in buildings:
            x, y = self.random_empty_position()
            self.grid[y][x] = building

    def random_empty_position(self):
        """Retourne une position vide aléatoire sur la carte."""
        while True:
            x = random.randint(0, 119)
            y = random.randint(0, 119)
            if self.grid[y][x] == '.':
                return x, y

    def generate_generous_map(self):
        # Placer des arbres sur la première ligne
        
        grid = [["." for _ in range(120)] for _ in range(120)]
        # Placer 300 arbres (bois)
        for _ in range(300):
            x, y = random.randint(0, 119), random.randint(0, 119)
            grid[y][x] = Wood()  # Place une instance de Wood
    
        # Placer 150 gisements d'or
        for _ in range(150):
            x, y = random.randint(0, 119), random.randint(0, 119)
            # S'assurer qu'on ne remplace pas un arbre déjà placé
            while grid[y][x] != ".":
                x, y = random.randint(0, 119), random.randint(0, 119)
            grid[y][x] = Gold()  # Place une instance de Gold
    
        return grid

    def generate_centered_map(self):
        grid = [["." for _ in range(120)] for _ in range(120)]
        for _ in range(50):
            x, y = 60 + random.randint(-10, 10), 60 + random.randint(-10, 10)
            grid[y][x] = Wood()
        for _ in range(200):
            x, y = 60 + random.randint(-10, 10), 60 + random.randint(-10, 10)
            grid[y][x] = Gold()  # Place une instance de Gold
        return grid

    def toggle_pause(self):
        """Activer/désactiver la pause avec un délai pour éviter le spam."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pause_time >= self.pause_cooldown:
            self.is_paused = not self.is_paused
            self.last_pause_time = current_time

    def set_speed(self, new_speed):
        if new_speed > 0:
            self.speed = new_speed

    def update(self):
        if not self.is_paused:
            pass

    def move_camera(self, dx, dy, screen):
        """Déplacer la caméra avec gestion des limites pour éviter les espaces vides."""
        screen_width, screen_height = screen.get_size()

        # Taille visible en tuiles
        visible_width = screen_width // self.tile_size
        visible_height = screen_height // self.tile_size


        # Limites maximales pour la caméra
        max_x = max(0, len(self.grid[0])- visible_width)  # Largeur de la carte - portion visible
        max_y = max(0, len(self.grid) - visible_height)  # Hauteur de la carte - portion visible

        # Mise à jour des coordonnées de la caméra avec restrictions
        self.camera_x = max(0, min(self.camera_x + dx, max_x))
        self.camera_y = max(0, min(self.camera_y + dy, max_y))

    def zoom_in(self):
        """Augmente la taille des tuiles pour zoomer."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_zoom_time >= self.zoom_cooldown:
            if self.tile_size < 40:  # Taille maximale pour le zoom
                self.tile_size += 2
            self.last_zoom_time = current_time

    def zoom_out(self):
        """Diminue la taille des tuiles pour dézoomer."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_zoom_time >= self.zoom_cooldown:
            if self.tile_size > 6:  # Taille minimale pour éviter des tuiles trop petites
                self.tile_size -= 2
            self.last_zoom_time = current_time

    def draw_pause_text(self, screen):
        """Affiche le texte 'Jeu en pause' au centre de l'écran."""
        font = pygame.font.SysFont('Arial', 48)
        text = font.render("Jeu en pause", True, (255, 0, 0))  # Rouge pour le texte
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

    def draw(self, screen):
        """Dessiner l'écran en fonction du mode d'affichage."""
        if self.display_mode == "Terminal":
            self.draw_terminal_view(screen)
        else:
            self.draw_2_5d_view(screen)

        # Afficher la minimap
        self.draw_minimap(screen)

        # Afficher le texte si le jeu est en pause
        if self.is_paused:
            self.draw_pause_text(screen)

    def draw_terminal_view(self, screen):
        """Affichage en mode Terminal (textuel)."""
        font = pygame.font.SysFont('Courier', int(self.tile_size*1.6))
        screen.fill((0, 0, 0))  # Noir en arrière-plan

        # Calcul des dimensions visibles exactes
        visible_width = screen.get_width() // font.size(" ")[0]  # Largeur visible en caractères
        visible_height = screen.get_height() // font.size(" ")[1]  # Hauteur visible en caractères

        # Affichage de chaque ligne visible
        for y in range(visible_height):
            row = ''
            for x in range(visible_width):
                grid_x = int(x + self.camera_x)
                grid_y = int(y + self.camera_y)

                if 0 <= grid_x < len(self.grid[0]) and 0 <= grid_y < len(self.grid):
                    row += self.grid[grid_y][grid_x].representation if self.grid[grid_y][grid_x] != '.' else ' '
                else:
                    row += ' '  # Hors des limites de la carte

            # Dessiner la ligne sur l'écran
            text = font.render(row, True, (255, 255, 255))
            screen.blit(text, (0, y * font.size(" ")[1]))


    def draw_2_5d_view(self, screen):
        """Affichage en mode 2.5D (graphique)."""
        visible_width = screen.get_width() // self.tile_size
        visible_height = screen.get_height() // self.tile_size

        # Calcul des décalages pour centrer la carte
        offset_x = self.camera_x
        offset_y = self.camera_y

        for y in range(visible_height):
            for x in range(visible_width):
                grid_x = x + offset_x
                grid_y = y + offset_y

                if 0 <= grid_x < len(self.grid[0]) and 0 <= grid_y < len(self.grid):
                    # Calcul des coordonnées isométriques
                    iso_x = (grid_x - grid_y) * self.tile_size // 2
                    iso_y = (grid_x + grid_y) * self.tile_size // 4

                    # Affichage des éléments non vides (arbres, bâtiments, etc.)
                    if self.grid[grid_y][grid_x] != '.':
                        if self.grid[grid_y][grid_x] == 'W':  # Wood (Arbre)
                            color = (34, 139, 34)  # Couleur vert pour l'arbre
                        elif self.grid[grid_y][grid_x] == 'G':  # Gold (Or)
                            color = (255, 215, 0)  # Couleur or
                        elif self.grid[grid_y][grid_x] == 'C':  # Town Centre
                            color = (0, 0, 255)  # Bleu pour le centre-ville
                        elif self.grid[grid_y][grid_x] == 'V':  # Villager
                            color = (255, 255, 255)  # Blanc pour le villageois
                        else:
                            color = (255, 0, 0)  # Rouge pour autres éléments comme les bâtiments militaires
                        
                        # Dessiner un polygone pour chaque élément (exemple pour les arbres et ressources)
                        pygame.draw.rect(screen, color, pygame.Rect(iso_x + screen.get_width() // 2, iso_y, self.tile_size, self.tile_size))

    def draw_minimap(self, screen):
        minimap_size = (200, 200)  # Dimensions de la minimap
        minimap_surface = pygame.Surface(minimap_size)
        minimap_surface.fill((50, 50, 50))  # Couleur de fond de la minimap

        # Taille de la carte
        map_width, map_height = len(self.grid[0]), len(self.grid)
        scale_x = minimap_size[0] / map_width
        scale_y = minimap_size[1] / map_height

        # Dessiner les ressources
        for y in range(map_height):
            for x in range(map_width):
                if self.grid[y][x] != '.':
                    color = (34, 139, 34) if isinstance(self.grid[y][x], Wood) else (255, 215, 0)
                    pygame.draw.rect(
                        minimap_surface,
                        color,
                        pygame.Rect(x * scale_x, y * scale_y, scale_x, scale_y)
                    )

        # Calculer les dimensions visibles
        screen_width, screen_height = screen.get_size()
        visible_tiles_x = screen_width / self.tile_size
        visible_tiles_y = screen_height / self.tile_size

        # Limiter la caméra aux bords de la carte
        self.camera_x = max(0, min(self.camera_x, map_width - visible_tiles_x))
        self.camera_y = max(0, min(self.camera_y, map_height - visible_tiles_y))

        # Position et taille du rectangle
        rect_x = self.camera_x * scale_x
        rect_y = self.camera_y * scale_y
        rect_width = min(visible_tiles_x * scale_x, minimap_size[0] - rect_x)
        rect_height = min(visible_tiles_y * scale_y, minimap_size[1] - rect_y)

        # Dessiner le rectangle jaune
        pygame.draw.rect(
            minimap_surface,
            (255, 255, 0),
            pygame.Rect(rect_x, rect_y, rect_width, rect_height),
            2
        )

        # Position de la minimap sur l'écran
        minimap_position = (screen.get_width() - minimap_size[0] - 10, screen.get_height() - minimap_size[1] - 10)
        screen.blit(minimap_surface, minimap_position)

        # Débogage
        # print(f"Camera pos: ({self.camera_x}, {self.camera_y}), scale: ({scale_x}, {scale_y})")
        # print(f"Rectangle pos: ({rect_x}, {rect_y}), size: ({rect_width}, {rect_height})")

    def toggle_display_mode(self):
        """Bascule entre les modes d'affichage Terminal et 2.5D."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time >= self.switch_cooldown:
            self.display_mode = "2.5D" if self.display_mode == "Terminal" else "Terminal"
            self.last_switch_time = current_time
