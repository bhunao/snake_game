# pygame
# window size = 900x600
# snake size = 20x20
# food size = 20x20
# snake speed = 1
# snake direction = right
# snake length = 3

# create a window
import random

import pygame
from objs import Food, Snake


def main():
        # maingame loop
    pygame.init()
    # create screen
    screen = pygame.display.set_mode((900, 600))
    # set title of the window
    pygame.display.set_caption("Snake Game")
    # set background color
    GRAY = (100, 100, 100)
    screen.fill(GRAY)

    # snake
    # snake blocks are 20x20 pixels
    snake = [
        Snake(300, 240, 20, 20),
        Snake(280, 240, 20, 20),
        Snake(260, 240, 20, 20)
    ]

    food = Food(random.randint(0, 520), random.randint(0, 460), 20, 20)

    while True:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # check if the event is a keypress
                elif event.type == pygame.KEYDOWN:
                    # if the key is escape, quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    # if the key is left
                    elif event.key == pygame.K_LEFT:
                        snake[0].direction = "left"
                    # if the key is right
                    elif event.key == pygame.K_RIGHT:
                        snake[0].direction = "right"
                    # if the key is up
                    elif event.key == pygame.K_UP:
                        snake[0].direction = "up"
                    # if the key is down
                    elif event.key == pygame.K_DOWN:
                        snake[0].direction = "down"
        # update snake
        for block in snake:
            block.update()
        # check if snake eats food
        if snake[0] == food:
            # spawn food
            food.left = random.randint(0, 520)
            food.top = random.randint(0, 460)
            # add a new snake block
            snake.append(Snake(0, 0, 20, 20))
        # draw snake
        for block in snake:
            block.update()
            block.draw(screen)
        # draw food
        food.draw()
        # update the screen
        pygame.display.update()
        # run at 60 frames per second
        pygame.time.delay(60)
        # check if snake dies
        if snake[0].colliderect():
            # game over
            snake[0].die()
        # check if snake eats the edge of the screen
