import pygame

from engine.game_objects import GameObjects


class GameMenu:
    is_menu_open = True
    is_game_initialized = False
    record_saved = False
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
        text = "Press Space to start!"
        font_name = pygame.font.match_font('arial')
        font_size = 40
        font = pygame.font.Font(font_name, font_size)
        text_color = (255, 165, 0)
        self.press_space_to_start = font.render(text, True, text_color)
        self.text_rect = self.press_space_to_start.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2))
        
        text_over = "GAME OVER!"
        text_color_over = (255, 129, 0)
        self.game_over = font.render(text_over, True, text_color_over)
        self.text_rect_over = self.press_space_to_start.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2 - 100))
        
    
    def draw(self):
        if (GameObjects().game_over):
            
            self.is_menu_open = True
            self.screen.blit(self.game_over, self.text_rect_over)
            
        if self.is_menu_open:
            if int(GameObjects().current_record) < GameObjects().player1.score:
                GameObjects().current_record = GameObjects().player1.score
                with open("record.txt", "r+") as file:
                    file.write(str(GameObjects().player1.score))
                self.record_saved = True
            self.screen.blit(self.press_space_to_start, self.text_rect)