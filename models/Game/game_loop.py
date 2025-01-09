import pygame

from ImageProcessingDisplay import UserInterface
from GLOBAL_VAR import *
from Game.game_state import * 


class GameLoop:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.screen.set_alpha(None)
        self.screen_width, self.screen_height = self.screen.get_width(), self.screen.get_height()
        pygame.display.set_caption("Age Of Empaire II")

        pygame.mouse.set_visible(False)

        self.font = pygame.font.Font(None, 24)

        self.clock = pygame.time.Clock()

        self.state = GameState(self.screen)


    
    def handle_start_events(self, event):
        if pygame.key.get_pressed()[pygame.K_F12]:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN and self.state.startmenu.handle_click(event.pos):
            self.state.set_map_type(self.state.startmenu.map_options[self.state.startmenu.selected_map_index])
            self.state.set_difficulty_mode(self.state.startmenu.selected_mode_index)
            self.state.set_display_mode(self.state.startmenu.display_mode)
            self.state.set_players(self.state.startmenu.selected_player_count_index)
            self.state.start_game()
            self.state.states = PLAY

    def handle_pause_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.state.pausemenu.handle_click(event.pos, self.state)

    def handle_play_events(self, event, mouse_x, mouse_y):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = self.state.camera.convert_from_isometric_2d(mouse_x, mouse_y)
            if event.button == LEFT_CLICK:
                entity_id = self.state.map.mouse_get_entity(self.state.camera, mouse_x, mouse_y)
                
                self.state.mouse_held = True
            elif event.button == RIGHT_CLICK:
                Y, X = math.floor(y / TILE_SIZE_2D), math.floor(x / TILE_SIZE_2D)
                house = ArcheryRange(Y, X, None, 2)
                self.state.map.add_entity(house)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.state.mouse_held = False

    def handle_keyboard_inputs(self, move_flags, current_time):
        keys = pygame.key.get_pressed()
        scale = 2 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 1

        # Zoom de la caméra
        if keys[pygame.K_KP_PLUS] or keys[pygame.K_k]:
            self.state.camera.adjust_zoom(current_time, 0.1, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif keys[pygame.K_KP_MINUS] or keys[pygame.K_j]:
            self.state.camera.adjust_zoom(current_time, -0.1, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Basculer le mode d'affichage
        if keys[pygame.K_F10]:
            self.state.toggle_display_mode(self)

        # Sauvegarder et charger
        if keys[pygame.K_F11]:
            pass
        if keys[pygame.K_F12]:
            pass

        # Générer fichier HTML
        if keys[pygame.K_TAB]:
            self.state.generate_html_file()
            self.state.toggle_pause()

        # Pause
        if keys[pygame.K_p]:
            self.state.toggle_pause()

        # Mouvement de la caméra
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_flags |= 0b0010
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            move_flags |= 0b0001
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_flags |= 0b0100
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            move_flags |= 0b1000

        if keys[pygame.K_f]:
            self.state.toggle_fullscreen(self)

        # Overlays
        if keys[pygame.K_F1]:
            self.state.toggle_resources()
        if keys[pygame.K_F2]:
            self.state.toggle_units()
        if keys[pygame.K_F3]:
            self.state.toggle_builds()
        if keys[pygame.K_F4]:
            self.state.toggle_all()

        self.state.camera.move_flags = move_flags
        self.state.terminal_camera.move_flags = move_flags
        self.state.terminal_camera.move(current_time)
        self.state.camera.move(current_time, 5 * scale)

    def update_game_state(self, current_time):
        if not (self.state.states == PAUSE):
            self.state.map.update_all_events(current_time, self.state.camera, self.screen)

    def render_display(self, current_time, mouse_x, mouse_y):
        if self.state.states == START:
            self.state.startmenu.draw()
        elif self.state.states == PAUSE:
            self.state.pausemenu.draw()
        elif self.state.states == PLAY:
            self.screen.fill((0, 0, 0))
            if self.state.display_mode == ISO2D:
                self.state.map.display(current_time, self.state.screen, self.state.camera, self.screen_width, self.screen_height)
                fps = int(self.clock.get_fps())
                fps_text = self.font.render(f"FPS: {fps}", True, (255, 255, 255))
                self.screen.blit(fps_text, (10, 10))
                self.state.ui.draw_resources(self.state.map.players_dict)
            elif self.state.display_mode == TERMINAL:
                self.state.map.terminal_display(current_time, self.state.terminal_camera)
        self.screen.blit(CURSOR_IMG, (mouse_x, mouse_y))
        pygame.display.flip()


    def run(self):
        running = True
        while running:
            self.screen_width, self.screen_height = self.screen.get_width(), self.screen.get_height()
            move_flags = 0
            mouse_x, mouse_y = pygame.mouse.get_pos()
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.state.states == START:
                    self.handle_start_events(event)
                elif self.state.states == PAUSE:
                    self.handle_pause_events(event)
                elif self.state.states == PLAY:
                    self.handle_play_events(event, mouse_x, mouse_y)

            if self.state.mouse_held:
                self.state.map.minimap.update_camera(self.state.camera, mouse_x, mouse_y)

            if not (self.state.states == START):
                self.handle_keyboard_inputs(move_flags, current_time)

            self.update_game_state(current_time)
            self.render_display(current_time, mouse_x, mouse_y)
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = GameLoop()
    game.run()
