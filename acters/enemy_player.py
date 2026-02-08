import pygame
from acters.character_state import CharacterState
from engine.configuration import Configuration
from utils.sprite_loader import load_sprite_sheet

class EnemyPlayer:
    def __init__(self, x, y, width, height, player_controls, ws_client = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.player_controls = player_controls
        self.ws_client = ws_client

        self.hitbox_width = width
        self.hitbox_height = height
        
        self.frame_offset_x = 100 
        self.frame_offset_y = 57  
        
        self.collision_rect = pygame.Rect(self.x + self.frame_offset_x, self.y + self.frame_offset_y, self.hitbox_width, self.hitbox_height)
        
        self.jump_velocity = -9.8  # Negative for upward movement, adjust as needed
        self.can_jump = True  # Tracks if the player is able to jump
        
        self.y_vel = 0
        self.on_ground = False
        self.speed = 5
        self.direction = "right"
        self._state = CharacterState.IDLE
        
        self.init_frames()
        
        
        self.frame_index = 0
        self.state_counter = 0
        self.animation_speed = 0.02
        self.last_update_time = pygame.time.get_ticks()
        self.current_frame = self.movement_frames[0]
        
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

    def draw(self):
        if self.direction == 'left':
            flipped_image = pygame.transform.flip(self.current_frame, True, False)
            self.screen.blit(flipped_image, (self.x, self.y))
        else:
            self.screen.blit(self.current_frame, (self.x, self.y))
            
        if Configuration()._instance.debug_mode:
            pygame.draw.rect(self.screen, (255, 0, 0), self.collision_rect, 1)
