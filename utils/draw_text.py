import pygame


def draw_text(text, x, y, color, size = 24):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    screen = pygame.display.get_surface()
    screen.blit(text_surface, (x, y))
