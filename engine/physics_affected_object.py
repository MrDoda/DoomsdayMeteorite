from typing import Protocol
import pygame

class PhysicsAffectedObject(Protocol):
    x: float
    y: float
    frame_offset_x: float
    frame_offset_y: float
    y_vel: float
    on_ground: bool
    collision_rect: pygame.Rect
    type: str
    
    def update(self): ...
    def draw(self, screen): ...
    def update_collision_rect(self): ...
