import pygame
from GLOBAL_VAR import *
from game_state import GameState
from ..ImageProcessingDisplay.ui import UserInterface
from ..GameField.map import Map

class GameLoop:
    def __init__(self, screen_width = SCREEN_WIDTH, screen_height = SCREEN_HEIGHT, fps = 800 ):
        tmap = Map(MAP_CELLX, MAP_CELLY)
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption("AOE2")
        loading = pygame.image.load("loading.png")
        self.clock = pygame.time.Clock()
        current_time = pygame.time.get_ticks()
        self.state = GameState()
        self.ui = UserInterface(self.screen)
        self.FPS = fps

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            SCREEN_WIDTH, SCREEN_HEIGHT = self.screen.get_width(), self.screen.get_height()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.display_mode == MODE_TERMINAL or self.display_mode == MODE_ISO_2D:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        self.display_mode = MODE_PAUSE
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.ui.handle_click(event.pos):
                        # Mise à jour des paramètres du jeu en quittant le menu
                        self.state.set_map_type(self.ui.map_options[self.ui.selected_map_index])
                        self.state.set_difficulty_mode(self.ui.selected_mode_index)
                        self.display_mode = self.ui.display_mode
                        self.state.start_game()

            # Gestion des touches pressées pendant la partie
            keys = pygame.key.get_pressed()
            if self.display_mode == MODE_TERMINAL or self.display_mode == MODE_ISO_2D :
                last_offset_x, last_offset_y = camera.view_port.position.x, camera.view_port.position.y
                # Zoom de la caméra
                if keys[pygame.K_p]:  # Touche + du pavé numérique
                    camera.adjust_zoom(1)
                elif keys[pygame.K_o]:  # Touche - du pavé numérique
                    camera.adjust_zoom(-1)

                # Basculer le mode d'affichage
                if keys[pygame.K_t]:
                    self.state.toggle_display_mode()
                # Pause
                if keys[pygame.K_p]:
                    self.state.toggle_pause()
                ## Mouvement de la caméra
                # Mouvement rapide
                if keys[pygame.K_LSHIFT]:
                    camera_dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] or keys[pygame.K_d] - keys[pygame.K_q]
                    camera_dy = keys[pygame.K_DOWN] - keys[pygame.K_UP] or keys[pygame.K_s] - keys[pygame.K_z]
                else:
                #mouvement lent
                    camera_dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] or keys[pygame.K_d] - keys[pygame.K_q]
                    camera_dy = keys[pygame.K_DOWN] - keys[pygame.K_UP] or keys[pygame.K_s] - keys[pygame.K_z]
                if camera_dx or camera_dy:
                    camera.view_port.position.x = last_offset_x + (camera_dx)
                    camera.view_port.position.y = last_offset_y + (camera_dy)

            # Mettre à jour l'état du jeu
            if not self.state.is_paused:
                self.state.update()

            # Effacer l'écran avant de dessiner
            self.screen.fill((0, 0, 0))
            if self.display_mode == 0:
                self.ui.draw()
            elif self.display_mode == 1:
                self.tmap.display_terminal(current_time, camera, SCREEN_WIDTH, SCREEN_HEIGHT)
            elif self.display_mode == 2:
                self.tmap.display(current_time, self.screen, camera, SCREEN_WIDTH, SCREEN_HEIGHT)



            fps = int(self.clock.get_fps())
            fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
            self.screen.blit(fps_text, (10, 10))

            self.screen.blit(CURSOR_IMG,(mouse_x, mouse_y))
            # Rafraîchissement de l'affichage
            pygame.display.flip()
            self.clock.tick(self.FPS)
            

        pygame.quit()


if __name__ == "__main__":
    game = GameLoop()
    game.run()
