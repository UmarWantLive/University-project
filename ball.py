import pygame
import random

from config import *


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(
            WIDTH // 2,
            HEIGHT // 2,
            BALL_SIZE,
            BALL_SIZE
        )

        self.speed_x = random.choice([-6, 6])
        self.speed_y = random.choice([-6, 6])

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.speed_y *= -1

        if self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        self.speed_x = random.choice([-6, 6])
        self.speed_y = random.choice([-6, 6])

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)