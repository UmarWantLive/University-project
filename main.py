import pygame
import sys

from config import *
from menu import Menu
from game import Game

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pong Coursework")

clock = pygame.time.Clock()

menu = Menu(screen)

game = Game(screen)

in_menu = True

while True:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if in_menu:

                if event.key == pygame.K_RETURN:
                    in_menu = False

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            else:

                if event.key == pygame.K_ESCAPE:
                    game.pause = not game.pause

    if in_menu:
        menu.draw()

    else:
        game.handle_input()
        game.update()
        game.draw()