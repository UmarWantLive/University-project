import pygame
import sys

from achievements_screen import AchievementsScreen
from config import *
from menu import Menu
from game import Game
from statistics_screen import StatisticsScreen
from history_screen import HistoryScreen
from game_over import GameOverScreen

# запуск pygame и всех его модулей
pygame.init()

# создание игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Coursework")

# объект для ограничения FPS
# чтобы игра работала одинаково быстро
clock = pygame.time.Clock()

menu = Menu(screen)
stats_screen = StatisticsScreen(screen)
history_screen = HistoryScreen(screen)
achievements_screen = AchievementsScreen(screen)
game_over_screen = GameOverScreen(screen)

state = "MENU"

game = None

# бесконечный игровой цикл
# работает пока пользователь не закроет игру
while True:
# ограничение кадров в секунду
    clock.tick(FPS)

# обработка всех действий пользователя
# клавиши, закрытие окна и т.д.
    for event in pygame.event.get():
# закрытие игры через крестик окна
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if state == "MENU":

                if event.key == pygame.K_UP:
                    menu.move_up()

                if event.key == pygame.K_DOWN:
                    menu.move_down()

                if event.key == pygame.K_RETURN:

                    option = menu.options[menu.selected]

                    if option == "START VS AI":
                        game = Game(screen, "AI")
                        state = "GAME"

                    elif option == "START PVP":
                        game = Game(screen, "PVP")
                        state = "GAME"

                    elif option == "STATISTICS":
                        state = "STATISTICS"

                    elif option == "MATCH HISTORY":
                        state = "HISTORY"

                    elif option == "ACHIEVEMENTS":
                        state = "ACHIEVEMENTS"

                    elif option == "EXIT":
                        pygame.quit()
                        sys.exit()

            elif state == "STATISTICS":
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"

            elif state == "HISTORY":
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"
            elif state == "ACHIEVEMENTS":

                if event.key == pygame.K_ESCAPE:
                    state = "MENU"
            if event.key == pygame.K_ESCAPE and game:
                game.paused = not game.paused    
            elif state == "GAME_OVER":
                if event.key == pygame.K_RETURN:
                    state = "MENU"

    if state == "MENU":
        menu.draw()

    elif state == "STATISTICS":
        stats_screen.draw()

    elif state == "HISTORY":
        history_screen.draw()
    elif state == "ACHIEVEMENTS":
        achievements_screen.draw()

    elif state == "GAME":

        if not game.paused:
# обработка управления игроками
            game.handle_input()
            game.update()
        
        game.draw()

        if game.finished:
            state = "GAME_OVER"

    elif state == "GAME_OVER":
        game_over_screen.draw(
            game.winner,
            game.left_score,
            game.right_score
        )