from typing import List, Union

import pygame
from acters.cake_is_a_lie import Cake
from acters.meteor import Meteor
from acters.super_meteor import SuperMeteor
from engine.game_objects import GameObjects
from engine.physics_affected_object import PhysicsAffectedObject


class PhysicsEngine:
    
    def __init__(self, gravity=0.5):
        self.gravity = gravity

    def apply_physics(self):
        for obj in GameObjects().get_objects():
            if not obj.on_ground:
                obj.y_vel += self.gravity
                obj.y += obj.y_vel
                
            self.check_collisions(obj)
            if (obj.type == "meteor"):
                self.check_player_struct(obj)
                
            if (obj.type == "cake"):
                self.check_player_eat_cake(obj)
            

    def check_collisions(self, obj:PhysicsAffectedObject):
        for platform in GameObjects().get_platforms():
            if obj.collision_rect.colliderect(platform.rect):
                if (obj.on_ground):
                    continue
                if obj.y_vel > 0 and obj.collision_rect.bottom > platform.rect.top:
                    obj.y = platform.rect.top - (obj.collision_rect.height + obj.frame_offset_y)
                    obj.y_vel = 0
                    obj.on_ground = True
                    
                    if (obj.type == "meteor"):
                        obj.move()
                        meteor = Meteor()
                        meteor.move()
                        GameObjects().add_obj(meteor)
                        GameObjects().player1.increase_score()
                        
                    break
        
        else:
            obj.on_ground = False
            
    def check_player_eat_cake(self, cake:Cake):
        if cake.collision_rect.colliderect(GameObjects().player1.collision_rect):
            cake.apply_effect()
            GameObjects().remove_object(cake)

    def check_player_struct(self, obj:PhysicsAffectedObject):
        if obj.collision_rect.colliderect(GameObjects().player1.collision_rect):
            if (GameObjects().is_super_mario_mode):
                GameObjects().remove_object(obj) 
                obj.move()  
                GameObjects().hidden_balance += 1
                pygame.time.set_timer(pygame.USEREVENT + 3, 6000)
                if (len(GameObjects().get_objects()) < 6):
                    meteor = Meteor()
                    meteor.move()
                    GameObjects().add_obj(meteor)
                
            GameObjects().player1.dmg()
        
        if GameObjects().player2 and obj.collision_rect.colliderect(GameObjects().player2.collision_rect):
            GameObjects().player2.dmg()