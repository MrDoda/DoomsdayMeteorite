import math
import random
import pygame
import sys
from acters.cake_is_a_lie import Cake
from acters.meteor import Meteor
from acters.player import Player
from acters.super_meteor import SuperMeteor
from engine.animated_background import AnimatedBackground
from engine.configuration import Configuration
from engine.game_menu import GameMenu
from engine.game_objects import GameObjects
from engine.player_controls_state import PlayerControlsState
from engine.physics_engine import PhysicsEngine
from engine.websocket_client import WebSocketSingleton
from layout.platform import Platform
from utils.draw_text import draw_text
from utils.update_player_keys import update_player_keys

class MainGameLoop:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen_width, self.screen_height = 1280, 720
        self.screen = pygame.display.set_mode(( 1280, 720))
        self.clock = pygame.time.Clock()
        self.game_objects = GameObjects()
        
        self.latency = 5

        self.ws_url = "ws://localhost:6789"

        self.ws_client = WebSocketSingleton(self.ws_url)

        self.player_1_state = PlayerControlsState(self.ws_client)
        self.player_2_state = PlayerControlsState()
        self.ws_client.set_player_2_control_state(self.player_2_state)


        self.player1 = Player(self.screen_width // 2, self.screen_height // 2, 50, 73, self.player_1_state)
        self.game_objects.add_obj(self.player1)
        self.game_objects.player1 = self.player1

        if (self.ws_client.ws_connected):
            self.player2 = Player(self.screen_width // 2.4, self.screen_height // 3, 50, 73, self.player_2_state)
            self.game_objects.add_obj(self.player2)
            self.game_objects.player2 = self.player2
            
        self.platform = Platform(0, self.screen_height - 20, self.screen_width, 20)
        self.game_objects.add_platform(self.platform)

        self.meteor = Meteor()
        self.game_objects.add_obj(self.meteor)

        self.physics_engine = PhysicsEngine()
        self.background = AnimatedBackground(self.screen)

        self.main_menu = GameMenu()

        self.last_action_time = pygame.time.get_ticks()
        
        Configuration()
        
        with open("record.txt", "r+") as file:
            current_record = file.readline().strip()
            file.seek(0)
            self.game_objects.current_record = current_record
        
        self.game_loop()


    def init_game(self):
        self.player_1_state = PlayerControlsState(self.ws_client)
        self.player_2_state = PlayerControlsState()
        self.ws_client.set_player_2_control_state(self.player_2_state)

        self.game_objects.clear()

        self.player1 = Player(self.screen_width // 2, self.screen_height // 2, 50, 73, self.player_1_state)
        self.game_objects.add_obj(self.player1)
        self.game_objects.player1 = self.player1

        if (self.ws_client.ws_connected):
            self.player2 = Player(self.screen_width // 2.4, self.screen_height // 3, 50, 73, self.player_2_state)
            self.game_objects.add_obj(self.player2)
            self.game_objects.player2 = self.player2
            # for multiplayer consistency
            random.seed("CAKE IS A LIE !")
            
            
        self.platform = Platform(0, self.screen_height - 20, self.screen_width, 20)
        self.game_objects.add_platform(self.platform)

        self.meteor = Meteor()
        self.game_objects.add_obj(self.meteor)
        
        self.cake = Cake()
        self.cake.move()
        self.game_objects.add_obj(self.cake)
        
        
        self.main_menu.is_menu_open = False
        self.main_menu.record_saved = False
        
        
        
    def increase_difficulty(self):
        current_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_action_time > 6000:
            self.last_action_time = current_time
            self.meteor = SuperMeteor()
            self.meteor.move()
            self.game_objects.add_obj(self.meteor)
            self.game_objects.add_obj(Cake())
        
    def game_loop(self):
        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.USEREVENT+1:
                    self.game_objects.is_colorful_mode = False
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                if event.type == pygame.USEREVENT+2:
                    self.game_objects.is_super_mario_mode = False
                    pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                if event.type == pygame.USEREVENT+3:
                    for i in range(math.floor(self.game_objects.hidden_balance / 3)):
                        meteor = SuperMeteor()
                        meteor.move()
                        self.game_objects.add_obj(meteor)
                    pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if (self.main_menu.is_menu_open and self.game_objects.game_over):
                            self.init_game()
                        if (not self.main_menu.is_game_initialized):
                            self.init_game()
                            self.main_menu.is_game_initialized = True
                        
                    if event.key == pygame.K_F1:
                        Configuration.toggle_debug_mode()
                update_player_keys(event, self.player_1_state)
            
            self.background.update()
            
            if (not self.ws_client.ws_connected):
                draw_text("Server Unavailable", self.screen_width - 150, 10, (255, 0, 0))
                
            draw_text(f"Survived meteorites: {self.player1.score}", 20, 20, (74, 224, 214))
            draw_text(f"Record: {self.game_objects.current_record}", 20, 100, (227, 121, 100), 30)
            
            if (self.main_menu.is_menu_open or self.game_objects.game_over):
                self.main_menu.draw()
                pygame.display.flip()
                self.clock.tick(40)
                continue
            
            self.increase_difficulty()   
                
            for object in self.game_objects.get_objects():
                object.update()
                
            for platform in self.game_objects.get_platforms():
                platform.draw(self.screen)
                
            self.physics_engine.apply_physics()
            
            pygame.display.flip()
            self.clock.tick(40)

        pygame.quit()
        sys.exit()

game = MainGameLoop()