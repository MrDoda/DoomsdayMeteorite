import pygame

def load_sprite_sheet(sheet_path, cols, rows, frame_width, frame_height):
    """Load and slice a sprite sheet into individual frames."""
    sprite_sheet = pygame.image.load(sheet_path).convert_alpha()
    frames = []
    for row in range(rows):
        for col in range(cols):
            frame_rect = (col * frame_width, row * frame_height, frame_width, frame_height)
            frame = sprite_sheet.subsurface(frame_rect)
            frames.append(frame)
    return frames
