import pygame

from paddle import Paddle
from ball import Ball

from config import *
from storage import *


class Game:
    def __init__(self, screen, mode="AI"):
        self.screen = screen

        self.left_paddle = Paddle(40, HEIGHT // 2, 7)
        self.right_paddle = Paddle(WIDTH - 60, HEIGHT // 2, 7)

        self.ball = Ball()

        self.left_score = 0
        self.right_score = 0

        self.font = pygame.font.SysFont("Arial", 50)

        self.mode = mode

        self.finished = False
        self.winner = ""

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.left_paddle.move_up()

        if keys[pygame.K_s]:
            self.left_paddle.move_down()

        if self.mode == "PVP":
            if keys[pygame.K_UP]:
                self.right_paddle.move_up()

            if keys[pygame.K_DOWN]:
                self.right_paddle.move_down()

    def update_ai(self):
        if self.ball.rect.centery < self.right_paddle.rect.centery:
            self.right_paddle.move_up()

        if self.ball.rect.centery > self.right_paddle.rect.centery:
            self.right_paddle.move_down()

    def collisions(self):
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.speed_x *= -1

        if self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.speed_x *= -1

    def scoring(self):
        records = load_records()

        if self.ball.rect.left <= 0:
            self.right_score += 1
            records["total_goals"] += 1
            self.ball.reset()

        if self.ball.rect.right >= WIDTH:
            self.left_score += 1
            records["total_goals"] += 1
            self.ball.reset()

        if self.left_score > records["best_score"]:
            records["best_score"] = self.left_score

        if self.right_score > records["best_score"]:
            records["best_score"] = self.right_score

        if self.left_score >= WIN_SCORE:
        pygame.display.flip()