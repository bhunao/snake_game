from calendar import c
import math
import pygame
import os
import random
import sys


# constants
# 900x600 screen
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
# 20x20 snake block
SNAKE_BLOCK_SIZE = 20
# 20x20 food block
FOOD_BLOCK_SIZE = 20
# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
# snake starting position and direction
#start position is in the middle of the screen
STAR_POSITION = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]

# snake starts moving to the right
direction = "right"

# start pygame
pygame.init()

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# score class
class Score:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.text = self.font.render(str(score), True, WHITE)
        self.rect = self.text.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.text, self.rect)
    
    def update(self, score):
        self.score = score
        self.text = self.font.render(str(score), True, BLUE)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)
        self.draw()

class Food:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.food_block = pygame.Rect(x, y, width, height)
    
    def update(self):
        self.draw()
    
    def draw(self):
        pygame.draw.rect(screen, RED, self.food_block)
    
    def spawn(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(0, SCREEN_HEIGHT - self.height)
        self.food_block = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw()


# Snake class x, y, width, height
class Snake:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "right"
        self.score = Score(SCREEN_WIDTH - 100, 50, 0)
        self.font = pygame.font.SysFont("comicsansms", 10)
        self.body = []
        self.body.append(pygame.Rect(self.x, self.y, self.width, self.height))
        self.body.append(pygame.Rect(self.x - SNAKE_BLOCK_SIZE,
                         self.y, self.width, self.height))
        self.body.append(pygame.Rect(
            self.x - SNAKE_BLOCK_SIZE*2, self.y, self.width, self.height))

    def update(self, direction: str=None):
        if direction:
            self.direction = direction
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.body.insert(0, pygame.Rect(
            self.x, self.y, self.width, self.height))
        self.body.pop()
        self.score.update(len(self.body))
        self.draw()
        self.move()

    def grow(self):
        self.body.append(pygame.Rect(0, 0, self.width, self.height))

    def move(self):
        if self.direction == "right":
            self.velocity_x = SNAKE_BLOCK_SIZE
            self.velocity_y = 0
        elif self.direction == "left":
            self.velocity_x = -SNAKE_BLOCK_SIZE
            self.velocity_y = 0
        elif self.direction == "up":
            self.velocity_x = 0
            self.velocity_y = -SNAKE_BLOCK_SIZE
        elif self.direction == "down":
            self.velocity_x = 0
            self.velocity_y = SNAKE_BLOCK_SIZE

    def draw_line(self, other: pygame.rect):
        dist = int(math.hypot(self.x - other.x, self.y - other.y))
        self.text = self.font.render(str(dist), True, BLACK)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.text, self.rect)
        pygame.draw.line(screen, WHITE, (self.x, self.y), (other.x, other.y))

    def draw(self):
        for block in self.body:
            pygame.draw.rect(screen, GREEN, block)

    def check_collision(self, other: pygame.Rect):
        for block in self.body:
            if block.colliderect(other.food_block):
                return True
        return False

    def brain(self, other: pygame.rect):
        if self.x < other.x:
            self.direction = "right"
        elif self.x > other.x:
            self.direction = "left"
        elif self.y < other.y:
            self.direction = "down"
        elif self.y > other.y:
            self.direction = "up"


# main function game loop

# function that returns a new snake at a random position
def get_random_snake() -> Snake:
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    return Snake(x, y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE)

def main():
    direction = "right"
    snakes = [
        Snake(STAR_POSITION[0], STAR_POSITION[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE),
    ]
    snakes.extend([get_random_snake() for i in range(5)])

    food = Food(0, 0, FOOD_BLOCK_SIZE, FOOD_BLOCK_SIZE)
    food.spawn()



    # main game loop
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
                        direction = "left"
                    # if the key is right
                    elif event.key == pygame.K_RIGHT:
                        direction = "right"
                    # if the key is up
                    elif event.key == pygame.K_UP:
                        direction = "up"
                    # if the key is down
                    elif event.key == pygame.K_DOWN:
                        direction = "down"

        screen.fill(GRAY)


        if not snakes:
           print("Game over")

        # update 
        for snake in snakes:
            snake.update()
            snake.brain(food.food_block)
            snake.draw_line(food.food_block)
        food.update()

        # check if snake eats food
        if snake.check_collision(food):
            snake.grow()
            food.spawn()

        # update screen
        pygame.display.update()
        # set game speed
        pygame.time.delay(100)


# run the main function
if __name__ == "__main__":
    main()
