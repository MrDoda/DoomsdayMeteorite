from typing import List, Union

import pygame
from engine.physics_affected_object import PhysicsAffectedObject
from layout.platform import Platform


class GameObjects:
    _instance = None
    game_over = False
    player2 = None
    player1 = None
    platforms:List[Platform] = []
    objects:List[PhysicsAffectedObject] = []
    hidden_balance = 0
    is_colorful_mode = False
    is_super_mario_mode = False
    current_record = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameObjects, cls).__new__(cls)
        return cls._instance

    def add_platform(self, platform: Union[Platform, List[Platform]]):
        if isinstance(platform, list):
            self.platforms.extend(platform)
        else:
            self.platforms.append(platform)

    def add_obj(self, obj: Union[PhysicsAffectedObject, List[PhysicsAffectedObject]]):
        if isinstance(obj, list):
            self.objects.extend(obj)
        else:
            self.objects.append(obj)
            
    def remove_object(self, obj: Union[PhysicsAffectedObject, List[PhysicsAffectedObject]]):
        if isinstance(obj, list):
            for item in obj:
                if item in self.objects:
                    self.objects.remove(item)
        else:
            if obj in self.objects:
                self.objects.remove(obj)
            
    def get_platforms(self):
        return self.platforms

    def get_objects(self):
        return self.objects
    
    def colorful_mode(self):
        pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
        self.is_colorful_mode = True
        
    def speed_mode(self):
        self.player1.speed = 10
        
    def super_mario_mode(self):
        self.is_super_mario_mode = True
        pygame.time.set_timer(pygame.USEREVENT + 2, 5000)
    
        
        
    
    def clear(self):
        self.game_over = False
        self.player2 = None
        self.player1 = None
        self.platforms:List[Platform] = []
        self.objects:List[PhysicsAffectedObject] = []
