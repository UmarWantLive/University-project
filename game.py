import pygame
import particles
import json

from paddle import Paddle
from ball import Ball
from particles import Particle

from config import *
from storage import *

# загрузка истории матчей из JSON файла
def load_history():

    try:
        with open("history.json", "r") as f:
            return json.load(f)

    except:
        return []


def save_history(data):

    with open("history.json", "w") as f:
# сохранение данных в JSON файл
        json.dump(data, f, indent=4)

def load_achievements():

    try:
        with open("achievements.json", "r") as f:
            return json.load(f)

    except:
        return {
            "first_win": False,
            "ten_matches": False,
            "hard_mode_win": False
        }

def save_achievements(data):

    with open("achievements.json", "w") as f:
        json.dump(data, f, indent=4)

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
# получение состояния клавиатуры
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

# проверка столкновения мяча и ракетки
    def collisions(self):

        # столкновение с левой ракеткой
        if self.ball.rect.colliderect(self.left_paddle.rect):
# изменение направления мяча
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
# завершение матча
# сохранение статистики и истории
    def finish_match(self, winner):
        ach = load_achievements()

        ach["first_win"] = True

        self.finished = True
        self.winner = winner

        records = load_records()
        history = load_history()
        records["matches_played"] += 1

        if records["matches_played"] >= 10:
            ach["ten_matches"] = True

        if self.ball.base_speed > 10:
            ach["hard_mode_win"] = True

        if winner == "Left Player":
            records["left_player_wins"] += 1

        else:
            records["right_player_wins"] += 1
        
        
        history.append({
            "winner": winner,
            "left_score": self.left_score,
            "right_score": self.right_score,
            "mode": self.mode
        })
        save_records(records)
        save_achievements(ach)
        records = load_records()
        save_history(history)

# система подсчёта очков
    def scoring(self):

        records = load_records()

        # гол правому игроку
        if self.ball.rect.left <= 0:

            self.right_score += 1
            records["total_goals"] += 1

            # увеличение сложности
            self.ball.base_speed += 0.5

            self.ball.reset()

        # гол левому игроку
        if self.ball.rect.right >= WIDTH:

            self.left_score += 1
            records["total_goals"] += 1

            # увеличение сложности
            self.ball.base_speed += 0.5

            self.ball.reset()

        # рекорд
        if self.left_score > records["best_score"]:
            records["best_score"] = self.left_score

        if self.right_score > records["best_score"]:
            records["best_score"] = self.right_score

        # победа
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
# рисование красивого фона
# градиент + сетка
    def draw_background(self):
        pygame.draw.circle(
            self.screen,
            (0, 150, 255),
            (WIDTH // 2, HEIGHT // 2),
            5
        )

        for y in range(HEIGHT):

            ratio = y / HEIGHT

            color = (
                0,
                int(50 * ratio),
                int(120 * ratio)
            )
            pygame.draw.line(
                self.screen,
                color,
                (0, y),
                (WIDTH, y)
            )

        for x in range(0, WIDTH, 40):
            pygame.draw.line(
                self.screen,
                (20, 20, 20),
                (x, 0),
                (x, HEIGHT)
            )
# главный рендер игры
# рисует все объекты
    def draw(self):
        self.draw_background()
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
# прозрачность pause overlay
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
