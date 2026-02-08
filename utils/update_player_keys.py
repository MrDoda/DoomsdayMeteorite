

import pygame

from engine.configuration import Configuration


def update_player_keys(event, player_1_state):
    state_updates = {}
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            state_updates[str(pygame.K_SPACE)]= True
        if event.key == pygame.K_a:
            state_updates[str(pygame.K_a)]= True
        if event.key == pygame.K_d:
            state_updates[str(pygame.K_d)]= True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            state_updates[str(pygame.K_SPACE)]= False
        if event.key == pygame.K_a:
            state_updates[str(pygame.K_a)]= False
        if event.key == pygame.K_d:
            state_updates[str(pygame.K_d)]= False
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            state_updates["1"]= True

        if event.button == 3:
            state_updates["3"]= True
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            state_updates["1"]= False

        if event.button == 3:
            state_updates["3"]= False
    
    if state_updates:
            player_1_state.set_multiple(state_updates)