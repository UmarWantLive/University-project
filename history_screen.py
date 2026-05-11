import pygame

from config import *
from storage import load_history


class HistoryScreen:
    def __init__(self, screen):
        self.screen = screen

        self.title_font = pygame.font.SysFont("Arial", 60)
        self.font = pygame.font.SysFont("Arial", 30)

    def draw(self):
        self.screen.fill(BLACK)

        title = self.title_font.render(
            "MATCH HISTORY",
            True,
            WHITE
        )

        self.screen.blit(title, (270, 50))

        history = load_history()

        if len(history) == 0:
            text = self.font.render(
                "No matches played yet",
                True,
                RED
            )

            self.screen.blit(text, (350, 300))

        else:
            last_matches = history[-10:]

            for index, match in enumerate(reversed(last_matches)):
                line = (
                    f"Winner: {match['winner']} | "
                    f"Score: {match['score']} | "
                    f"Mode: {match['mode']}"
                )

                text = self.font.render(
                    line,
                    True,
                    WHITE
                )

                self.screen.blit(text, (120, 180 + index * 45))

        back = self.font.render(
            "Press ESC to return",
            True,
            GREEN
        )

        self.screen.blit(back, (320, 640))

        pygame.display.flip()