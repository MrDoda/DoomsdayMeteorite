import pygame
import os

class AnimatedBackground:
    def __init__(self, screen, base_path='assets/background/ezgif-frame-', image_count=200):
        self.screen = screen
        self.images = []
        self.current_image_index = 0
        self.frame_counter = 0
        self.load_images(base_path, image_count)
        music_path = "assets/mp3/e1m1.mp3"
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    def load_images(self, base_path, image_count):
        for i in range(1, image_count + 1):
            image_path = f"{base_path}{str(i).zfill(3)}.jpg"
            if os.path.exists(image_path):
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, self.screen.get_size())
                self.images.append(image)
            else:
                print(f"Warning: Missing image at {image_path}")

    def update(self):
        if self.images:
            self.frame_counter += 1
            if self.frame_counter >= 2:
                self.frame_counter = 0
                self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.screen.blit(self.images[self.current_image_index], (0, 0))
