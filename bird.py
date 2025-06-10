import pygame
from settings import *

class Bird:
    MAX_TILT_UP = -15
    MAX_TILT_DOWN = 15
    TILT_SPEED = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.movement = 0
        self.tilt = 0
        self.tick_count = 0
        self.images = [
            pygame.image.load('bird1.png').convert_alpha(),
            pygame.image.load('bird2.png').convert_alpha(),
            pygame.image.load('bird3.png').convert_alpha(),
            pygame.image.load('bird4.png').convert_alpha(),
            pygame.image.load('bird5.png').convert_alpha(),
            pygame.image.load('bird6.png').convert_alpha(),
            pygame.image.load('bird7.png').convert_alpha(),
            pygame.image.load('bird8.png').convert_alpha()
        ]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=(x, y))

    def flap(self):
        self.movement = -7.5
        self.tilt = self.MAX_TILT_UP
        self.tick_count = 0  # Reset tick_count on flap

    def update(self, gravity):
        self.tick_count += 1
        self.movement += gravity
        self.rect.centery += self.movement

        # Handle animation
        self.image_index = (self.tick_count // self.ANIMATION_TIME) % len(self.images)
        self.image = self.images[self.image_index]

        # Adjust tilt
        if self.movement < 0 or self.rect.centery < self.y + 50:
            if self.tilt < self.MAX_TILT_UP:
                self.tilt = self.MAX_TILT_UP
        else:
            if self.tilt < self.MAX_TILT_DOWN:
                self.tilt += self.TILT_SPEED
                self.tilt = min(self.tilt, self.MAX_TILT_DOWN)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)
