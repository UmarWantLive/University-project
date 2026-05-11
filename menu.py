import pygame
from config import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)

    def draw(self):
        self.screen.fill(BLACK)

        title = self.font.render("PONG COURSEWORK", True, WHITE)

        start = self.font.render(
            "ENTER - START",
            True,
            WHITE
        )

        quit_text = self.font.render(
            "ESC - EXIT",
            True,
            WHITE
        )

        self.screen.blit(title, (300, 200))
        self.screen.blit(start, (350, 350))
        self.screen.blit(quit_text, (350, 450))

        pygame.display.flip()