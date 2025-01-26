import pygame
from GLOBAL_VAR import *

class StartMenu:
    def __init__(self, screen):
        self.screen = screen

        # Map cell count
        self.map_cell_count = 256  # Default value
        self.editing_map_cell_count = False  # Track if the user is editing the cell count

        # Map type options
        self.map_options = ["Carte Normal", "Carte Centrée"]
        self.selected_map_index = MAP_NORMAL

        # Game mode options
        self.game_mode_options = ["Lean", "Mean", "Marines"]
        self.selected_mode_index = LEAN

        # Player count options
        self.selected_player_count = 2  # Default to 2 players
        self.editing_player_count = False  # Track if the player is editing the count

        self.display_mode = TERMINAL  # Default display mode

        # Buttons
        self.buttons = {
            "left_map": pygame.Rect(0, 0, 50, 50),
            "right_map": pygame.Rect(0, 0, 50, 50),
            "left_mode": pygame.Rect(0, 0, 50, 50),
            "right_mode": pygame.Rect(0, 0, 50, 50),
            "left_player_count": pygame.Rect(0, 0, 50, 50),
            "right_player_count": pygame.Rect(0, 0, 50, 50),
            "Terminal": pygame.Rect(0, 0, 115, 50),
            "2.5D": pygame.Rect(0, 0, 115, 50),
            "Lancer la Partie": pygame.Rect(0, 0, 300, 50),
            "left_map_cell": pygame.Rect(0, 0, 50, 50),
            "right_map_cell": pygame.Rect(0, 0, 50, 50)
        }

    def draw(self):
        """Draw buttons and selected options on the screen."""
        self.screen.fill((255, 255, 255))  # Fill the screen with white
        screen_width, screen_height = self.screen.get_size()
        self.screen.blit(adjust_sprite(START_IMG,screen_width, screen_height), (0, 0))
        # Calculate positions based on screen size
        center_x = screen_width // 2
        center_y = screen_height // 2

        self.buttons["left_map_cell"].topleft = (center_x - 215, center_y - 200)
        self.buttons["right_map_cell"].topleft = (center_x + 165, center_y - 200)
        self.buttons["left_map"].topleft = (center_x - 215, center_y - 140)
        self.buttons["right_map"].topleft = (center_x + 165, center_y - 140)
        self.buttons["left_mode"].topleft = (center_x - 215, center_y - 80)
        self.buttons["right_mode"].topleft = (center_x + 165, center_y - 80)
        self.buttons["left_player_count"].topleft = (center_x - 215, center_y - 20)
        self.buttons["right_player_count"].topleft = (center_x + 165, center_y - 20)
        self.buttons["Terminal"].topleft = (center_x - 120, center_y + 40)
        self.buttons["2.5D"].topleft = (center_x + 5, center_y + 40)
        self.buttons["Lancer la Partie"].topleft = (center_x - 150, center_y + 100)

        # Draw map cell count
        self._draw_button("left_map_cell", "<")
        if self.editing_map_cell_count:
            map_cell_label = "Cellules: _"
        else:
            map_cell_label = f"Cellules: {self.map_cell_count}"
        self._draw_text(map_cell_label, (center_x, center_y - 185), centered=True)
        self._draw_button("right_map_cell", ">")

        # Draw map selection
        self._draw_button("left_map", "<")
        map_label = f"Carte: {self.map_options[self.selected_map_index]}"
        self._draw_text(map_label, (center_x, center_y - 125), centered=True)
        self._draw_button("right_map", ">")

        # Draw game mode selection
        self._draw_button("left_mode", "<")
        mode_label = f"Mode: {self.game_mode_options[self.selected_mode_index]}"
        self._draw_text(mode_label, (center_x, center_y - 65), centered=True)
        self._draw_button("right_mode", ">")

        # Draw player count selection
        self._draw_button("left_player_count", "<")
        if self.editing_player_count:
            player_count_label = "Joueurs: _"
        else:
            player_count_label = f"Joueurs: {self.selected_player_count}"
        self._draw_text(player_count_label, (center_x, center_y - 5), centered=True)
        self._draw_button("right_player_count", ">")

        # Draw display mode buttons
        self._draw_button("Terminal", "Terminal", self.display_mode == TERMINAL)
        self._draw_button("2.5D", "2.5D", self.display_mode == ISO2D)

        # Draw launch game button
        self._draw_button("Lancer la Partie", "Lancer la Partie")

    def _draw_button(self, key, text, selected=False):
        """Draw a button with text."""
        rect = self.buttons[key]
        color = (0, 128, 0) if selected else (128, 128, 128)  # Green if selected, grey otherwise
        pygame.draw.rect(self.screen, color, rect)
        font = pygame.font.SysFont(None, 36)
        button_text = font.render(text, True, (255, 255, 255))
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)

    def _draw_text(self, text, pos, centered=False):
        """Draw text at a specific position."""
        font = pygame.font.SysFont(None, 36)
        rendered_text = font.render(text, True, (0, 0, 0))
        text_rect = rendered_text.get_rect(center=pos if centered else None)
        self.screen.blit(rendered_text, text_rect if centered else pos)

    def handle_click(self, pos):
        """Handle clicks on buttons."""
        if self.buttons["left_map_cell"].collidepoint(pos):
            self.map_cell_count = max(120, self.map_cell_count - 1)
        elif self.buttons["right_map_cell"].collidepoint(pos):
            self.map_cell_count = min(1024, self.map_cell_count + 1)
        elif self.buttons["left_map"].collidepoint(pos):
            self.selected_map_index = (self.selected_map_index - 1) % len(self.map_options)
        elif self.buttons["right_map"].collidepoint(pos):
            self.selected_map_index = (self.selected_map_index + 1) % len(self.map_options)
        elif self.buttons["left_mode"].collidepoint(pos):
            self.selected_mode_index = (self.selected_mode_index - 1) % len(self.game_mode_options)
        elif self.buttons["right_mode"].collidepoint(pos):
            self.selected_mode_index = (self.selected_mode_index + 1) % len(self.game_mode_options)
        elif self.buttons["left_player_count"].collidepoint(pos):
            self.selected_player_count = max(2, self.selected_player_count - 1)
        elif self.buttons["right_player_count"].collidepoint(pos):
            self.selected_player_count += 1
        elif self.buttons["Terminal"].collidepoint(pos):
            self.display_mode = TERMINAL
        elif self.buttons["2.5D"].collidepoint(pos):
            self.display_mode = ISO2D
        elif self.buttons["Lancer la Partie"].collidepoint(pos):
            return True  # Indicate that the game can start

        return False  # Indicate that the game cannot start

    def handle_keydown(self, event):
        """Handle keyboard input for editable fields."""
        if self.editing_map_cell_count:
            if event.key == pygame.K_RETURN:  # Confirm input
                self.editing_map_cell_count = False
                self.map_cell_count = min(1024, max(120, self.map_cell_count))
            elif event.key == pygame.K_BACKSPACE:  # Remove last digit
                self.map_cell_count = int(str(self.map_cell_count)[:-1] or "120")
            elif event.unicode.isdigit():  # Add new digit
                # On gère la saisie des chiffres correctement
                if self.map_cell_count == '':
                    self.map_cell_count = int(event.unicode)  # Si c'est vide, on met le premier chiffre
                else:
                    self.map_cell_count = self.map_cell_count * 10 + int(event.unicode)  # On ajoute le chiffre à la fin

        elif self.editing_player_count:
            if event.key == pygame.K_RETURN:  # Confirm input
                self.editing_player_count = False
                self.selected_player_count = min(20, max(2, self.selected_player_count))  # Limite entre 2 et 20
            elif event.key == pygame.K_BACKSPACE:  # Remove last digit
                self.selected_player_count = int(str(self.selected_player_count)[:-1] or "2")
            elif event.unicode.isdigit():  # Add new digit
                # Même logique pour le nombre de joueurs
                if self.selected_player_count == '':
                    self.selected_player_count = int(event.unicode)  # Si c'est vide, on met le premier chiffre
                else:
                    self.selected_player_count = self.selected_player_count * 10 + int(event.unicode)  # Ajouter le chiffre à la fin




    def start_editing_map_cell_count(self):
        """Enable editing map cell count."""
        self.editing_map_cell_count = True
        self.map_cell_count = 0  # Vider la valeur lorsque l'on commence à éditer

    def start_editing_player_count(self):
        """Enable editing player count."""
        self.editing_player_count = True
        self.selected_player_count = 0  # Vider la valeur lorsque l'on commence à éditer
