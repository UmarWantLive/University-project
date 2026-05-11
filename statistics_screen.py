import pygame

from config import *
from storage import load_records


class StatisticsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 38)
        self.title_font = pygame.font.SysFont("Arial", 60)

    def draw(self):
        self.screen.fill(BLACK)

        records = load_records()

        title = self.title_font.render(
            "STATISTICS",
            True,
            WHITE
        )

        self.screen.blit(title, (330, 70))

        stats = [
            f"Best Score: {records['best_score']}",
            f"Matches Played: {records['matches_played']}",
            f"Left Player Wins: {records['left_player_wins']}",
            f"Right Player Wins: {records['right_player_wins']}",
            f"Total Goals: {records['total_goals']}"
        ]

        for index, line in enumerate(stats):
            text = self.font.render(line, True, WHITE)
            self.screen.blit(text, (250, 220 + index * 70))

        back = self.font.render(
            "Press ESC to return",
            True,
            GREEN
        )

        self.screen.blit(back, (300, 620))

        pygame.display.flip()