import pygame
from pygame.locals import *
import time
import random

SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load(
            "resources/apple.jpg").convert()  # loading apple
        self.parent_screen = parent_screen
        self.x = SIZE * 3  # size of apple
        self.y = SIZE * 3

    def draw(self):

        # draws apple on surface at location
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 13) * SIZE
        self.y = random.randint(0, 11) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length

        # loading "snake" from resources
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block_x = [SIZE] * length
        self.block_y = [SIZE] * length  # locations of block
        self.direction = "down"

    def draw(self):
        self.parent_screen.fill((40, 200, 0))

        for i in range(self.length):

            # draws object on surface at location
            self.parent_screen.blit(
                self.block, (self.block_x[i], self.block_y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]

        if self.direction == "up":
            self.block_y[0] -= SIZE
        if self.direction == "down":
            self.block_y[0] += SIZE
        if self.direction == "left":
            self.block_x[0] -= SIZE
        if self.direction == "right":
            self.block_x[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()

        # setting the display(background) and its size
        self.surface = pygame.display.set_mode((600, 520))

        self.snake = Snake(self.surface, 5)  # create instance of snake
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:  # there is a collison
                return True

        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                raise "Game Over"

    def show_game_over(self):
        self.surface.fill((40, 200, 0))
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(
            f"score:  {self.snake.length} ", True, (255, 255, 255))
        self.surface.blit(line1, (300, 260))

        line2 = font.render(
            "Play again, press Enter!", True, (255, 255, 255))
        self.surface.blit(line2, (300, 230))

        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f"score:  {self.snake.length} ", True, (255, 255, 255))
        self.surface.blit(score, (400, 2))

    def run(self):

        running = True
        pause = False
        while running:
            for event in pygame.event.get():  # get all the user interactions
                if event.type == KEYDOWN:

                    if event.key == K_RETURN:   # play game again
                        pause = False

                    # user using keys to move block

                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:  # selecting exit button
                    running = False
            try:
                if not pause:

                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)

    def reset(self):
        self.snake = Snake(self.surface, 5)  # create instance of snake
        self.apple = Apple(self.surface)


if __name__ == '__main__':
    game = Game()
    game.run()
