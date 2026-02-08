import math
import pygame


class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load("assets/platform/hell_platform.png")
        self.image_width = 256
        self.image = pygame.transform.scale(self.image, (self.image_width, 45))
        self.screen = pygame.display.get_surface()

    def draw(self, screen):
        pygame.draw.rect(screen, (224, 96, 7), self.rect)
        for i in range(math.floor(self.screen.get_width() / self.image_width)):
            screen.blit(self.image, (i * self.image_width, self.y))