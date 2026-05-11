from config import *

class AIPlayer:
    def __init__(self, paddle):
        self.paddle = paddle

    def update(self, ball):
        if ball.rect.centery < self.paddle.rect.centery:
            self.paddle.move_up()

        if ball.rect.centery > self.paddle.rect.centery:
            self.paddle.move_down()