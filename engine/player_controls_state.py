import json
import pygame
from engine.game_objects import GameObjects

class PlayerControlsState:
    def __init__(self, ws_client=None, initial_state=None):
        self._state = initial_state if initial_state else {
            str(pygame.K_SPACE): False,
            str(pygame.K_a): False,
            str(pygame.K_d): False,
        }
        self.ws_client = ws_client

    def get(self):
        return self._state
    
    def set_multiple(self, updates):
        changes = {}
        for key, value in updates.items():
            if self._state.get(key, object()) != value:
                self._state[key] = value
                changes[key] = value
        
        if changes and self.ws_client:
            changes["x"] = GameObjects().player1.x
            changes["y"] = GameObjects().player1.y
            if (self.ws_client):
                self._trigger_update_multiple(changes)

    def _trigger_update_multiple(self, changes):
        self.ws_client.send(json.dumps(changes))