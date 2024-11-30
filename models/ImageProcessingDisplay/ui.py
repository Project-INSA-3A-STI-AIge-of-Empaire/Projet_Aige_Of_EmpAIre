import pygame

class UserInterface:
    def __init__(self, screen):
        self.screen = screen
        self.map_options = ["Carte Normal", "Carte Centrée"]
        self.selected_map_index = 0
        
        self.game_mode_options = ["Lean", "Mean", "Marines"]
        self.selected_mode_index = 0
        
        self.display_mode = ["Menu","Terminal","2.5D","Pause"]
        self.selected_display_index = 0
        self.buttons = {
            "left_map": pygame.Rect(0, 0, 50, 50),  # Left button for map
            "right_map": pygame.Rect(0, 0, 50, 50),  # Right button for map
            "left_mode": pygame.Rect(0, 0, 50, 50),  # Left button for game mode
            "right_mode": pygame.Rect(0, 0, 50, 50),  # Right button for game mode
            "Terminal": pygame.Rect(0, 0, 115, 50),  # Terminal view button
            "2.5D": pygame.Rect(0, 0, 115, 50),  # 2.5D view button
            "Lancer la Partie": pygame.Rect(0, 0, 300, 50)  # Start game button
        }

    def draw(self):
        """Draw buttons and selected options on the screen."""
        self.screen.fill((255, 255, 255))  # Fill the screen with white
        screen_width, screen_height = self.screen.get_size()

        # Calculate positions based on screen size
        center_x = screen_width // 2
        center_y = screen_height // 2

        self.buttons["left_map"].topleft = (center_x - 215, center_y - 100)
        self.buttons["right_map"].topleft = (center_x + 165, center_y - 100)
        self.buttons["left_mode"].topleft = (center_x - 215, center_y - 40)
        self.buttons["right_mode"].topleft = (center_x + 165, center_y - 40)
        self.buttons["Terminal"].topleft = (center_x - 120, center_y + 20)
        self.buttons["2.5D"].topleft = (center_x + 5, center_y + 20)
        self.buttons["Lancer la Partie"].topleft = (center_x - 150, center_y + 80)

        # Draw map selection
        self._draw_button("left_map", "<")  # Left button for map
        map_label = f"Map: {self.map_options[self.selected_map_index]}"
        self._draw_text(map_label, (center_x, center_y - 85), centered=True)
        self._draw_button("right_map", ">")  # Right button for map

        # Draw game mode selection
        self._draw_button("left_mode", "<")  # Left button for game mode
        mode_label = f"Mode de jeu: {self.game_mode_options[self.selected_mode_index]}"
        self._draw_text(mode_label, (center_x, center_y - 25), centered=True)
        self._draw_button("right_mode", ">")  # Right button for game mode

        # Draw display mode buttons
        self._draw_button("Terminal", "Terminal", self.display_mode[self.selected_display_index] == "Terminal")
        self._draw_button("2.5D", "2.5D", self.display_mode[self.selected_display_index] == "2.5D")

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
        if self.buttons["left_map"].collidepoint(pos):
            self.selected_map_index = (self.selected_map_index - 1) % len(self.map_options)
        elif self.buttons["right_map"].collidepoint(pos):
            self.selected_map_index = (self.selected_map_index + 1) % len(self.map_options)
        elif self.buttons["left_mode"].collidepoint(pos):
            self.selected_mode_index = (self.selected_mode_index - 1) % len(self.game_mode_options)
        elif self.buttons["right_mode"].collidepoint(pos):
            self.selected_mode_index = (self.selected_mode_index + 1) % len(self.game_mode_options)
        elif self.buttons["Terminal"].collidepoint(pos):
            self.selected_display_index = 1
        elif self.buttons["2.5D"].collidepoint(pos):
            self.selected_display_index = 2
        elif self.buttons["Lancer la Partie"].collidepoint(pos):
            if self.selected_display_index == 0:
                return True  # Indicate that the game can start

        return False  # Indicate that the game cannot start
