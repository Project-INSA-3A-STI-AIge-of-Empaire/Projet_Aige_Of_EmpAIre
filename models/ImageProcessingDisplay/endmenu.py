import pygame
from GLOBAL_VAR import *

class EndMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(MEDIEVALSHARP, 28)
        self.title_font = pygame.font.Font(MEDIEVALSHARP, 36)

        # Button dimensions
        self.button_width = 200
        self.button_height = 50

        # Button positions
        self.buttons = {}
        self._update_buttons()

    def _update_buttons(self):
        """Recalculate button positions based on screen size."""
        screen_width, screen_height = self.screen.get_size()
        center_x = screen_width // 2

        self.buttons = {
            'main_menu': pygame.Rect(center_x - self.button_width // 2, screen_height - 160, self.button_width, self.button_height),
            'quit': pygame.Rect(center_x - self.button_width // 2, screen_height - 90, self.button_width, self.button_height)
        }

    def draw(self, player_scores):
        """Draw the end menu with the leaderboard and buttons."""
        # Update button positions in case of screen resize
        self._update_buttons()

        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(220)  # Transparency level (0-255)
        overlay.fill((0, 0, 0))  # Black background
        self.screen.blit(overlay, (0, 0))

        # Draw end menu title
        title_text = self.title_font.render("End Menu", True, WHITE_COLOR)
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Draw leaderboard
        for i, (player, time) in enumerate(player_scores):
            score_text = self.font.render(f"{i + 1}. {player}: {time}", True, WHITE_COLOR)
            score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 150 + i * 40))
            self.screen.blit(score_text, score_rect)

        # Draw buttons
        for button_text, button_rect in self.buttons.items():
            pygame.draw.rect(self.screen, (50, 50, 50), button_rect)  # Button background
            text = self.font.render(button_text.replace('_', ' ').capitalize(), True, WHITE_COLOR)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def handle_click(self, pos, game_state):
        """Handle button clicks."""
        if self.buttons['main_menu'].collidepoint(pos):
            game_state.go_to_main_menu()
        elif self.buttons['quit'].collidepoint(pos):
            pygame.quit()
            exit()
