import pygame
import json

from config import *


class AchievementsScreen:

    def __init__(self, screen):

        self.screen = screen

        self.font = pygame.font.SysFont("Arial", 40)

    def load_achievements(self):

        try:
            with open("achievements.json", "r") as f:
                return json.load(f)

        except:
            return {}

    def draw(self):

        self.screen.fill(BLACK)

        ach = self.load_achievements()

        title = self.font.render(
            "ACHIEVEMENTS",
            True,
            WHITE
        )

        self.screen.blit(title, (350, 50))

        y = 180

        for name, unlocked in ach.items():

            color = GREEN if unlocked else RED

            text = self.font.render(
                f"{name}: {'UNLOCKED' if unlocked else 'LOCKED'}",
                True,
                color
            )

            self.screen.blit(text, (200, y))

            y += 80

        pygame.display.flip()