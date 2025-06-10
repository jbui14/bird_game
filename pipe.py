import pygame
from random import randint
from settings import SCREEN_WIDTH, PIPE_WIDTH, PIPE_SPEED

class Pipe:
    def __init__(self):
        self.spacing = 225  # Space between top and bottom pipes
        self.x = SCREEN_WIDTH + 100

        # Heights of the top and bottom pipes
        top_height = randint(50, 300)
        bottom_height = top_height + self.spacing

        self.top_pipe = pygame.image.load('toppipe.png').convert_alpha()
        self.bottom_pipe = pygame.image.load('botpipe.png').convert_alpha() 

        # Create rect objects for each pipe for positioning and collision
        self.top_rect = self.top_pipe.get_rect(topleft=(self.x, top_height - self.top_pipe.get_height()))
        self.bottom_rect = self.bottom_pipe.get_rect(topleft=(self.x, bottom_height))

        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        screen.blit(self.top_pipe, self.top_rect)
        screen.blit(self.bottom_pipe, self.bottom_rect)

    def collide(self, bird_rect):
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)
