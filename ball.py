import pygame
import random

from config import *



class Ball:
    def __init__(self):
        self.trail = []
        self.base_speed = 7
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

        self.trail.append(
            (self.rect.centerx, self.rect.centery)
        )

        if len(self.trail) > 8:
            self.trail.pop(0)        

    def reset(self):

        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        self.speed_x = random.choice(
            [-self.base_speed, self.base_speed]
        )

        self.speed_y = random.choice(
            [-self.base_speed, self.base_speed]
        )

    def draw(self, screen):

        # красивый trail
        for index, pos in enumerate(self.trail):

            alpha = index / len(self.trail)

            size = int(8 * alpha)

            color = (
                int(100 * alpha),
                int(180 * alpha),
                int(255 * alpha)
            )

            pygame.draw.circle(
                screen,
                color,
                pos,
                max(size, 1)
            )

        # основной мяч
        pygame.draw.ellipse(screen, WHITE, self.rect)