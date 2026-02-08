import pygame
from acters.meteor import Meteor
from engine.configuration import Configuration


class SuperMeteor(Meteor):
    def __init__(self):
        super().__init__()
        self.blue_tint_color = (0, 0, 255)
        
    def draw(self):
        self.update_collision_rect()
        img = pygame.transform.rotate(pygame.transform.scale(self.current_frame, (self.width, self.height)), 90)
        img.fill(self.blue_tint_color + (0,), None, pygame.BLEND_RGB_ADD)
        self.screen.blit(img, (self.x, self.y))
        
        if Configuration()._instance.debug_mode:
            pygame.draw.rect(self.screen, (255, 0, 0), self.collision_rect, 1)