import pygame
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