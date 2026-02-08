import math
import random
import pygame
from acters.cake_sprite import CakeSprite
from acters.meteor import Meteor
from engine.configuration import Configuration
from engine.game_objects import GameObjects


class Cake(Meteor):
    cake_types = []
    current_type = None
    
    def __init__(self):
        super().__init__()
        
        self.type = "cake"
        
        self.base_width = 70
        self.base_height = 75
        
        self.width = self.base_width
        self.height = self.base_height
        
        self.cake_frames = CakeSprite().cake_frames
        cakes = ["cake_speed", "cake_barrier", "rainbow_cake", "cake_health", "chocolate_cake", "super_cake"]
        
        self.cake_types = list(zip(cakes, self.cake_frames))
        
        self.y = 0
        self.x = random.randint(1, self.screen.get_width())
        
        self.set_cake_type(random.randint(0,len(cakes) - 1))
            
        
    def sparkling_effect(self, base_color):
        intensity = 50
        chance_of_sparkle = 0.5
        sparkle_duration = 200
        cycle_duration = 1000
        
        current_ticks = pygame.time.get_ticks()
        phase = current_ticks % cycle_duration
        
        is_sparkling = phase < (chance_of_sparkle * cycle_duration)
        
        if is_sparkling and phase % sparkle_duration < sparkle_duration / 2:
            sparkle_color = tuple(min(255, channel + intensity) for channel in base_color)
        else:
            sparkle_color = base_color
        
        return sparkle_color
    
    def wobble_effect(self):
        intensity = 10
        speed = 1000

        current_ticks = pygame.time.get_ticks()
        wobble = intensity * math.sin(2 * math.pi * current_ticks / speed)

        self.width = self.base_width + wobble
        self.height = self.base_height + wobble 
        
        
    def set_cake_type(self, index):
        self.current_type = self.cake_types[index]
        self.current_frame = self.current_type[1]
        
    def animation(self):
        pass
    def apply_effect(self):
        if self.current_type[0] == "rainbow_cake":
            GameObjects().colorful_mode()
            pass
        
        if self.current_type[0] == "cake_speed":
            GameObjects().speed_mode()
            pass
            
        if self.current_type[0] == "cake_health":
            GameObjects().player1.ate_a_cake()
            pass
        
        if self.current_type[0] == "cake_barrier":
            GameObjects().player1.shield()
            pass
        
        if self.current_type[0] == "super_cake":
            GameObjects().super_mario_mode()
            pass
        
        if self.current_type[0] == "chocolate_cake":
            # no bonuses, just eat
            pass
        
        
    def draw(self):
        self.wobble_effect()
        self.update_collision_rect()
        tint_color = self.sparkling_effect((255, 0, 0))
        
        img = pygame.transform.scale(self.current_frame, (self.width, self.height))
        img.fill(tint_color + (0,), None, pygame.BLEND_RGB_ADD)
        self.screen.blit(img, (self.x, self.y))
        
        if Configuration()._instance.debug_mode:
            pygame.draw.rect(self.screen, (255, 0, 0), self.collision_rect, 1)