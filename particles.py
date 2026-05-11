import pygame
import random

class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.size = random.randint(2, 6)

        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)

        self.life = 30

    def update(self):

        self.x += self.speed_x
        self.y += self.speed_y

        self.life -= 1

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (self.x, self.y, self.size, self.size)
        )