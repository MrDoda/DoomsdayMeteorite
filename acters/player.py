import pygame
import math
from acters.character_state import CharacterState
from engine.configuration import Configuration
from engine.physics_affected_object import PhysicsAffectedObject
from engine.player_controls_state import PlayerControlsState
from engine.player_controls_state import GameObjects

from utils.sprite_loader import load_sprite_sheet

class Player(PhysicsAffectedObject):
    def __init__(self, x, y, width, height, player_controls: PlayerControlsState):
        self.x = x
        self.y = y
        self.health = 3
        self.width = width
        self.height = height
        self.player_controls = player_controls

        self.score = 0
        self.is_shield = False
        
        self.hitbox_width = width
        self.hitbox_height = height
        
        self.frame_offset_x = 100 
        self.frame_offset_y = 57  
        self.type = "player"
        
        self.collision_rect = pygame.Rect(self.x + self.frame_offset_x, self.y + self.frame_offset_y, self.hitbox_width, self.hitbox_height)
        
        self.jump_velocity = -9.8
        self.can_jump = True
        
        self.y_vel = 0
        self.on_ground = False
        self.speed = 5
        self.direction = "right"
        self._state = CharacterState.IDLE
        
        self.hurt = 40
        
        self.init_frames()
        
        
        self.frame_index = 0
        self.state_counter = 0
        self.animation_speed = 0.02
        self.last_update_time = pygame.time.get_ticks()
        self.current_frame = self.movement_frames[0]
        
        self.image_heart = pygame.transform.scale(pygame.image.load("assets/heart/heart.png"), (50, 50))
        
        heart_tint_color = (224, 58, 7)
        self.image_heart.fill(heart_tint_color + (0,), None, pygame.BLEND_RGB_ADD)
        
        self.screen = pygame.display.get_surface()
        
        
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state != self._state:
            self._state = new_state
            self.frame_index = 0

    def init_frames(self):
        movement_frames = load_sprite_sheet('assets/golem/golem_walk.png', 8, 5, 256, 256)
        self.idle_frames = load_sprite_sheet('assets/golem/golem_idle.png', 8, 7, 256, 256)
        self.jump_frames = load_sprite_sheet('assets/golem/golem_jump.png', 8, 5, 256, 256)
    
        
        self.jump_frames_end = self.jump_frames[-4:]
        self.start_movement_frames = movement_frames[:4]
        self.movement_frames = movement_frames[4:]
        
    def update_collision_rect(self):
        self.collision_rect.x = self.x + self.frame_offset_x
        self.collision_rect.y = self.y + self.frame_offset_y
    
    def update(self):
        keys = self.player_controls.get()
        self.update_collision_rect()
        self.handle_state_transition(keys)
        self.animate_based_on_state()
        self.draw()
        
    def increase_score(sef):
        sef.score += 1
        
    def dmg(self):
        if GameObjects().is_colorful_mode:
            return
        
        if GameObjects().is_super_mario_mode:
            return
        
        if (self.is_shield):
            self.is_shield -= 1
            return
        
        if (self.hurt > 40):
            self.health -= 1
            self.hurt = 0
        
        if (self.health < 0):
            GameObjects().game_over = True
        
    def jump(self):
        if self.on_ground and self.can_jump:
            self.y_vel = self.jump_velocity
            self.on_ground = False
            self.can_jump = False

        
    def handle_state_transition(self, keys):
        moving = keys[str(pygame.K_a)] or keys[str(pygame.K_d)]
        
        if pygame.mouse.get_pos()[0] < self.collision_rect.centerx:
            self.direction = 'left'
        else:
            self.direction = 'right'

        if keys[str(pygame.K_a)]:
            self.x -= self.speed
            moving = True
            
        if keys[str(pygame.K_d)]:
            self.x += self.speed
            moving = True
            
        if keys[str(pygame.K_SPACE)] and self.can_jump:
                self.state = CharacterState.JUMPING
                self.jump()
        
        if self.state == CharacterState.JUMPING and not self.on_ground:
            
            return
        elif self.state == CharacterState.JUMPING and self.on_ground:
            self.state = CharacterState.JUMPING_END
            self.state_counter = 1
            
            return
            
        if self.state == CharacterState.JUMPING_END: 
            self.state_counter += 1
            if self.state_counter >= 4:
                self.state = CharacterState.IDLE
                self.state_counter = 0
                self.can_jump = True
            else:
                return
                
        if moving:
            if self.state == CharacterState.IDLE or self.state == CharacterState.START_MOVING:
                self.state = CharacterState.START_MOVING
                self.state_counter += 1  
                if self.state_counter >= 5:
                    self.state = CharacterState.MOVING
                    self.state_counter = 0 
            else:
                self.state = CharacterState.MOVING
        else:
            self.state = CharacterState.IDLE

            
    def animate_based_on_state(self):
        now = pygame.time.get_ticks()
        if now - self.last_update_time > 1000 * self.animation_speed:
            self.last_update_time = now

            if self.state == CharacterState.IDLE:
                self.last_update_time = now
                self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
                self.current_frame = self.idle_frames[self.frame_index]
                pass
            elif self.state == CharacterState.START_MOVING:
                self.frame_index = (self.frame_index + 1) % len(self.start_movement_frames)
                self.current_frame = self.start_movement_frames[self.frame_index]
                pass
            elif self.state == CharacterState.MOVING:
                self.frame_index = (self.frame_index + 1) % len(self.movement_frames)
                self.current_frame = self.movement_frames[self.frame_index]
                pass
            elif self.state == CharacterState.JUMPING:
                self.frame_index = (self.frame_index + 1) % len(self.jump_frames)
                self.current_frame = self.jump_frames[self.frame_index]
            elif self.state == CharacterState.JUMPING_END:
                self.current_frame = self.jump_frames_end[self.frame_index]

    def pulsating_value(self, initial_value, max_increase, speed):
        ticks = pygame.time.get_ticks()
        pulse = initial_value + (max_increase * 0.5) * (1 + math.sin(ticks * 0.001 * speed))
        return pulse

    def ate_a_cake(self):
        self.health += 1
        
    def shield(self):
        self.is_shield = 4

    def draw(self):
        if (self.hurt <= 40):
            self.current_frame = self.current_frame.copy()
            self.hurt +=1
            self.blue_tint_color = (255, 0, 0)
            self.current_frame.fill(self.blue_tint_color + (0,), None, pygame.BLEND_RGB_ADD)
            
        
        frame = self.current_frame
        if self.direction == 'left':
            frame = pygame.transform.flip(self.current_frame, True, False)
            
        if (GameObjects().is_super_mario_mode):
            current_ticks = pygame.time.get_ticks()
            tint_color = (
                (current_ticks // 5) % 255,  # Red component changing over time
                (current_ticks // 10) % 255,  # Green component changing over time
                (current_ticks // 15) % 255,  # Blue component changing over time
            )
            frame = frame.copy()
            frame.fill(tint_color + (0,), None, pygame.BLEND_RGB_ADD)
            
        
        self.screen.blit(frame, (self.x, self.y))
        
            
        for i in range(self.health+1):
            pulse = self.pulsating_value(1, 4, 8)
            
            heart_rect = (50 + pulse, 50 +pulse)
            heart_x = 20 + i * (50+pulse -10)
            heart_y = (50 + pulse - 15)
            
            heart_x -= pulse
            heart_y -= pulse
            
            self.screen.blit(pygame.transform.scale(self.image_heart, heart_rect), (heart_x, heart_y) )
            
            if self.is_shield:
                pygame.draw.circle(self.screen, (37, 240, 209), self.collision_rect.center, (self.collision_rect.width * 1.2 + pulse), 3)
            
        if Configuration()._instance.debug_mode:
            pygame.draw.rect(self.screen, (255, 0, 0), self.collision_rect, 1)
