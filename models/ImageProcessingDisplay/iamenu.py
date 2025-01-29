import pygame
from GLOBAL_VAR import *

class IAMenu:
    def __init__(self, screen, num_players):
        self.screen = screen
        self.num_players = num_players
        self.sliders = []
        self.confirm_button = pygame.Rect(0, 0, 200, 50)  # Position updated in draw()
        
        for i in range(num_players):
            aggressive_slider = pygame.Rect(100, 100 + i * 60, 300, 10)
            defensive_slider = pygame.Rect(100, 130 + i * 60, 300, 10)
            self.sliders.append({
                "aggressive": aggressive_slider,
                "defensive": defensive_slider,
                "aggressive_value": 1,
                "defensive_value": 1
            })
    
    def draw(self):
        self.screen.fill((255, 255, 255))
        screen_width, screen_height = self.screen.get_size()
        
        for i, slider_set in enumerate(self.sliders):
            self._draw_slider(slider_set["aggressive"], slider_set["aggressive_value"], f"Agressive {i+1}")
            self._draw_slider(slider_set["defensive"], slider_set["defensive_value"], f"Defense {i+1}")
        
        self.confirm_button.topleft = (screen_width // 2 - 100, screen_height - 80)
        pygame.draw.rect(self.screen, (0, 255, 0), self.confirm_button)
        self._draw_text("Confirmer", (self.confirm_button.centerx, self.confirm_button.centery), centered=True)
    
    def _draw_slider(self, slider_rect, value, label):
        pygame.draw.rect(self.screen, (200, 200, 200), slider_rect)
        thumb_x = slider_rect.x + int((value - 1) / 2 * slider_rect.width)
        pygame.draw.rect(self.screen, (0, 0, 255), (thumb_x, slider_rect.y - 5, 10, 20))
        self._draw_text(f"{label}: {value}", (slider_rect.x, slider_rect.y - 20))
    
    def _draw_text(self, text, pos, centered=False):
        font = pygame.font.Font(None, 28)
        rendered_text = font.render(text, True, (0, 0, 0))
        text_rect = rendered_text.get_rect(center=pos if centered else None)
        self.screen.blit(rendered_text, text_rect if centered else pos)
    
    def handle_click(self, pos):
        for slider_set in self.sliders:
            if slider_set["aggressive"].collidepoint(pos):
                slider_set["aggressive_value"] = min(3, max(1, slider_set["aggressive_value"] + 1))
            elif slider_set["defensive"].collidepoint(pos):
                slider_set["defensive_value"] = min(3, max(1, slider_set["defensive_value"] + 1))
        
        if self.confirm_button.collidepoint(pos):
            return self.get_ai_values()
        return None
    
    def get_ai_values(self):
        return [(s["aggressive_value"], s["defensive_value"]) for s in self.sliders]