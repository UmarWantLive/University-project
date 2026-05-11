import pygame

from config import *


class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen

        self.title_font = pygame.font.SysFont("Arial", 72)
        self.font = pygame.font.SysFont("Arial", 40)

    def draw(self, winner, left_score, right_score):
        self.screen.fill(BLACK)

        title = self.title_font.render(
            "GAME OVER",
            True,
            RED
        )

        self.screen.blit(title, (270, 120))

        winner_text = self.font.render(
            f"Winner: {winner}",
            True,
            WHITE
        )

        score_text = self.font.render(
            f"Final Score: {left_score} : {right_score}",
            True,
            WHITE
        )

        restart = self.font.render(
            "Press ENTER to return to menu",
            True,
            GREEN
        )

        self.screen.blit(winner_text, (360, 300))
        self.screen.blit(score_text, (320, 380))
        self.screen.blit(restart, (220, 520))

        pygame.display.flip()