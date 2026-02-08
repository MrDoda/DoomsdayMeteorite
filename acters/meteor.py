import random
import pygame
from acters.meteor_sprite import MeteorSprite
from engine.configuration import Configuration
from engine.game_objects import GameObjects
from engine.physics_affected_object import PhysicsAffectedObject
from utils.sprite_loader import load_sprite_sheet
import asyncio


class Meteor(PhysicsAffectedObject):
    def __init__(self):
        self.x = 20
        self.y = 0
        self.width = 100
        self.height = 50
        
        self.frame_offset_y = 0
        self.frame_offset_x = 0
        
        self.type = "meteor"
        self.move_count = 0
        
        self.y_vel = 4
        self.on_ground = False
        
        self.collision_rect = pygame.Rect(self.x, self.y, 45, 80)
        self.meteor_frames = MeteorSprite().meteor_frames
        
        self.frame_index = 0
        self.animation_speed = 0.04
        self.last_update_time = pygame.time.get_ticks()
        self.current_frame = self.meteor_frames[0]
        
        self.random_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        self.screen = pygame.display.get_surface()
        
        
    def move(self):
        self.move_count += 1
        self.y = 0
        self.x = random.randint(1, self.screen.get_width())
        self.random_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update_time > 1000 * self.animation_speed:
            self.last_update_time = now
            self.frame_index = (self.frame_index + 1) % len(self.meteor_frames)
            self.current_frame = self.meteor_frames[self.frame_index]
        
    def update(self):
        if self.move_count == 2:
            GameObjects().remove_object(self)
        else:            
            self.animation()
            self.draw()
        
        
    def draw(self):
        self.update_collision_rect()
        meteor_frame = pygame.transform.rotate(pygame.transform.scale(self.current_frame, (self.width, self.height)), 90)
        if (GameObjects().is_colorful_mode):
            meteor_frame.fill(self.random_rgb + (0,), None, pygame.BLEND_RGB_ADD)
        self.screen.blit(meteor_frame, (self.x, self.y))
        
        if Configuration()._instance.debug_mode:
            pygame.draw.rect(self.screen, (255, 0, 0), self.collision_rect, 1)
        
    def update_collision_rect(self):
        self.collision_rect = pygame.Rect(self.x, self.y, 45, 80)