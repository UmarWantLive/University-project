import pygame

from config import *


class Menu:
    def __init__(self, screen):
        self.screen = screen

        self.title_font = pygame.font.SysFont("Arial", 72)
        self.menu_font = pygame.font.SysFont("Arial", 40)

        self.options = [
            "START VS AI",
            "START PVP",
            "STATISTICS",
            "MATCH HISTORY",
            "EXIT"
        ]

        self.selected = 0

    def move_up(self):
        self.selected -= 1

        if self.selected < 0:
            self.selected = len(self.options) - 1

    def move_down(self):
        self.selected += 1

        if self.selected >= len(self.options):
            self.selected = 0

    def draw(self):
        self.screen.fill(BLACK)

        title = self.title_font.render(
            "PONG COURSEWORK",
            True,
            WHITE
        )

        self.screen.blit(title, (220, 100))

        for index, option in enumerate(self.options):

            color = WHITE

            if index == self.selected:
                color = GREEN

            text = self.menu_font.render(
                option,
                True,
                color
            )

            self.screen.blit(
                text,
                (350, 250 + index * 70)
            )

        pygame.display.flip()