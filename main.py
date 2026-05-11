import pygame
import sys

from config import *
from menu import Menu
from game import Game
from statistics_screen import StatisticsScreen
from history_screen import HistoryScreen
from game_over import GameOverScreen


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Coursework")

clock = pygame.time.Clock()

menu = Menu(screen)
stats_screen = StatisticsScreen(screen)
history_screen = HistoryScreen(screen)
game_over_screen = GameOverScreen(screen)

state = "MENU"

game = None

while True:

    clock.tick(FPS)

    for event in pygame.event.get():

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

                    elif option == "EXIT":
                        pygame.quit()
                        sys.exit()

            elif state == "STATISTICS":
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"

            elif state == "HISTORY":
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"

            elif state == "GAME_OVER":
                if event.key == pygame.K_RETURN:
                    state = "MENU"

    if state == "MENU":
        menu.draw()

    elif state == "STATISTICS":
        stats_screen.draw()

    elif state == "HISTORY":
        history_screen.draw()

    elif state == "GAME":

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