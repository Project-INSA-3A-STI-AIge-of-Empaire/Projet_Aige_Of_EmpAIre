import pygame

from ImageProcessingDisplay import UserInterface
from GLOBAL_VAR import *
from Game.game_state import * 


class GameLoop:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption("Age Of Empaire II")

        pygame.mouse.set_visible(False)

        self.font = pygame.font.Font(None, 24)

        self.clock = pygame.time.Clock()

        
        self.state = GameState(self.screen)
        

    def run(self):
        
        archer = Archer(5, 5, PVector2(0, 0), 1) # debugging
        villager = HorseMan(7,7,PVector2(0, 0), 2)
        keep = Stable(9,3,PVector2(0, 0), 2)
        
        entity = None

        target_pos = PVector2(0,0)
        self.state.map.add_entity(archer)
        self.state.map.add_entity(villager)
        self.state.map.add_entity(keep)
        running = True
        while running:
            move_flags = 0

            mouse_x, mouse_y = pygame.mouse.get_pos()

            current_time = pygame.time.get_ticks()
            
            SCREEN_WIDTH, SCREEN_HEIGHT = self.state.screen.get_width(), self.state.screen.get_height()
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print(archer.save())
                if self.state.states == START:
                    if pygame.key.get_pressed()[pygame.K_F12]:
                        #load a savegame
                        #self.state.save_manager.load_game()
                        pass
                    if event.type == pygame.MOUSEBUTTONDOWN and self.state.startmenu.handle_click(event.pos):
                        # Mise à jour des paramètres du jeu en quittant le menu
                        self.state.set_map_type(self.state.startmenu.map_options[self.state.startmenu.selected_map_index])
                        self.state.set_difficulty_mode(self.state.startmenu.selected_mode_index)
                        self.state.set_display_mode(self.state.startmenu.display_mode)
                        self.state.start_game()
                        self.state.states = PLAY
                if self.state.states == PAUSE:
                     if event.type == pygame.MOUSEBUTTONDOWN:
                        self.state.pausemenu.handle_click(event.pos, self.state) 

                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == LEFT_CLICK:
                            self.state.mouse_held = True
                            
                            entity_id = self.state.map.mouse_get_entity(self.state.camera, mouse_x, mouse_y)

                        elif event.button == RIGHT_CLICK:
                            bx, by = self.state.camera.convert_from_isometric_2d(mouse_x, mouse_y)
                            villager.move_position.x = bx
                            villager.move_position.y = by


                        print(f"screen( width:{SCREEN_WIDTH}, {SCREEN_HEIGHT}), mouse( x:{mouse_x}, y:{mouse_y})")
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.state.mouse_held = False

            if (self.state.mouse_held):
                self.state.map.minimap.update_camera(self.state.camera, mouse_x, mouse_y)

            # Gestion des touches pressées pendant la partie
            keys = pygame.key.get_pressed()
            if not (self.state.states == START):
                # Zoom de la caméra
                if keys[pygame.K_KP_PLUS] or keys[pygame.K_k]:  # Touche + du pavé numérique
                    self.state.camera.adjust_zoom(pygame.time.get_ticks(), 0.1, SCREEN_WIDTH, SCREEN_HEIGHT)
                elif keys[pygame.K_KP_MINUS] or keys[pygame.K_j]:  # Touche - du pavé numérique
                    self.state.camera.adjust_zoom(pygame.time.get_ticks(), -0.1, SCREEN_WIDTH, SCREEN_HEIGHT)

                # Basculer le mode d'affichage
                if keys[pygame.K_F10]:
                    self.state.toggle_display_mode(self)
                #savegame
                if keys[pygame.K_F11]:
                    #self.state.save_manager.save_game()
                    pass
                #loadgame
                if keys[pygame.K_F12]:
                    #self.state.save_manager.load_game()
                    pass
                #génerer fichier html
                if keys[pygame.K_TAB]:
                    self.state.generate_html_file()
                    self.state.toggle_pause()

                # Pause
                if keys[pygame.K_p]:
                    self.state.toggle_pause()
                    
                # Mouvement de la caméra
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    scale = 2
                else:
                    scale = 1
                if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
                    move_flags |= 0b0010
                if keys[pygame.K_LEFT] or keys[pygame.K_q] :
                    move_flags |= 0b0001
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    move_flags |= 0b0100
                if keys[pygame.K_UP] or keys[pygame.K_z]:
                    move_flags |= 0b1000
                if keys[pygame.K_f]:
                    self.state.toggle_fullscreen(self)

                if keys:
                    self.state.camera.move_flags = move_flags
                    self.state.terminal_camera.move_flags = move_flags
                    self.state.terminal_camera.move(current_time)
                    self.state.camera.move(current_time, 5*scale)



                # Overlay ressource etc
                if keys[pygame.K_F1]:
                    self.state.toggle_resources()

                if keys[pygame.K_F2]:
                    self.state.toggle_units()

                if keys[pygame.K_F3]:
                    self.state.toggle_builds()

                if keys[pygame.K_F4]:
                    self.state.toggle_all()

                
            # Mettre à jour l'état du jeu
            if not (self.state.states == PAUSE):
                self.state.update()
                

            # Effacer l'écran avant de dessiner
            
            if self.state.states == START:
                self.state.startmenu.draw()
                
            elif self.state.states == PAUSE:
                self.state.pausemenu.draw()
            else:
                self.screen.fill((0, 0, 0))
                if (self.state.display_mode == ISO2D): # everything in the iso2d 
                    

                    self.state.map.display(current_time, self.state.screen, self.state.camera, SCREEN_WIDTH, SCREEN_HEIGHT)
                    
                    fps = int(self.clock.get_fps())
                    fps_text = self.font.render(f"FPS: {fps}", True, (255, 255, 255))
                    screen.blit(fps_text, (10, 10))
                    self.state.ui.draw_resources(self.state.map.entity_matrix)
                    
                    # Rafraîchissement de l'affichage
                   
                elif (self.state.display_mode == TERMINAL):
                    self.state.map.terminal_display(current_time, self.state.terminal_camera)
                    
                self.state.map.update_all_events(current_time)
                archer.try_to_attack(current_time, entity_id, self.state.camera)
                villager.try_to_move(current_time, self.state.camera)

                
            screen.blit(CURSOR_IMG,(mouse_x, mouse_y))
                
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()


if __name__ == "__main__":
    game = GameLoop()
    game.run()
