import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_SPEED
from random import randint

class Coin:
    def __init__(self):
        self.image = pygame.image.load("coin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.reset()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.reset()

    def reset(self):
        
        self.rect.x = SCREEN_WIDTH + randint(100, 500)  # Adjust range as needed
        self.rect.y = randint(
            50, SCREEN_HEIGHT - 50
        )
