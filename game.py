import pygame

from paddle import Paddle
from ball import Ball
from ai import AIPlayer

from config import *
from storage import *

class Game:
    def __init__(self, screen):
        self.screen = screen

        settings = load_settings()

        self.left_paddle = Paddle(
            40,
            HEIGHT // 2,
            settings["paddle_speed"]
        )

        self.right_paddle = Paddle(
            WIDTH - 60,
            HEIGHT // 2,
            settings["paddle_speed"]
        )

        self.ball = Ball(settings["ball_speed"])

        self.ai = AIPlayer(self.right_paddle)

        self.left_score = 0
        self.right_score = 0

        self.font = pygame.font.SysFont("Arial", 40)

        self.pause = False

        self.records = load_records()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.left_paddle.move_up()

        if keys[pygame.K_s]:
            self.left_paddle.move_down()

    def collisions(self):
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.speed_x *= -1.1

        if self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.speed_x *= -1.1

    def scoring(self):
        if self.ball.rect.left <= 0:
            self.right_score += 1
            self.ball.reset()

        if self.ball.rect.right >= WIDTH:
            self.left_score += 1
            self.ball.reset()

        if self.left_score > self.records["best_score"]:
            self.records["best_score"] = self.left_score
            save_records(self.records)

    def draw_middle_line(self):
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(
                self.screen,
                WHITE,
                (WIDTH // 2 - 5, y, 10, 20)
            )

    def draw_scores(self):
        left = self.font.render(
            str(self.left_score),
            True,
            WHITE
        )

        right = self.font.render(
            str(self.right_score),
            True,
            WHITE
        )

        self.screen.blit(left, (400, 50))
        self.screen.blit(right, (560, 50))

    def update(self):
        if not self.pause:
            self.ball.move()
            self.ai.update(self.ball)

            self.collisions()
            self.scoring()

    def draw(self):
        self.screen.fill(BLACK)

        self.draw_middle_line()

        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)

        self.ball.draw(self.screen)

        self.draw_scores()

        pygame.display.flip()