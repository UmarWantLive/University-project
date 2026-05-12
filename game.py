import pygame
import particles

from paddle import Paddle
from ball import Ball
from particles import Particle

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
        self.particles = []
        self.can_spawn_particles = True
        self.paused = False

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

        # столкновение с левой ракеткой
        if self.ball.rect.colliderect(self.left_paddle.rect):

            self.ball.speed_x *= -1

            # убираем залипание
            self.ball.rect.left = self.left_paddle.rect.right

            if self.can_spawn_particles:
                self.spawn_particles()
                self.can_spawn_particles = False

        # столкновение с правой ракеткой
        if self.ball.rect.colliderect(self.right_paddle.rect):

            self.ball.speed_x *= -1

            # убираем залипание
            self.ball.rect.right = self.right_paddle.rect.left

            if self.can_spawn_particles:
                self.spawn_particles()
                self.can_spawn_particles = False

    def spawn_particles(self):

        for _ in range(20):

            self.particles.append(
                Particle(
                    self.ball.rect.centerx,
                    self.ball.rect.centery
                )
            )
    def finish_match(self, winner):

        self.finished = True
        self.winner = winner

        records = load_records()

        records["matches_played"] += 1

        if winner == "Left Player":
            records["left_player_wins"] += 1

        else:
            records["right_player_wins"] += 1


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
            self.finish_match("Left Player")

        if self.right_score >= WIN_SCORE:
            self.finish_match("Right Player")

        save_records(records)
    
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
        if self.paused:
            return
        self.ball.move()
        # разрешаем снова спавн, когда мяч в центре
        if abs(self.ball.rect.centerx - WIDTH // 2) < 50:
            self.can_spawn_particles = True

        if self.mode == "AI":
            self.update_ai()

        self.collisions()
        self.scoring()

        for particle in self.particles:
            particle.update()

        self.particles = [
                p for p in self.particles
                if p.life > 0
            ]



    def draw(self):

        self.screen.fill(BLACK)

        self.draw_middle_line()

        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)

        self.ball.draw(self.screen)

        for particle in self.particles:
            particle.draw(self.screen)

        self.draw_scores()

        # PAUSE OVERLAY
        if self.paused:

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))

            self.screen.blit(overlay, (0, 0))

            pause_font = pygame.font.SysFont("Arial", 90)

            pause_text = pause_font.render(
                "PAUSED",
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                pause_text,
                (
                    WIDTH // 2 - pause_text.get_width() // 2,
                    HEIGHT // 2 - pause_text.get_height() // 2
                )
            )

        pygame.display.flip()