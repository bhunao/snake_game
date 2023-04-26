from random import randint

import pygame
from pygame.math import Vector2

from event_handler import event_handler
from objects import Snake, Food, ScoreBoard, Background

# Define Constants
WHITE = (255, 255, 255)
WIDTH, HEIGHT = (800, 600)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

snake = Snake()
food = Food()
score_board = ScoreBoard((0,0))
bg = Background((WIDTH, HEIGHT))
effects = []
texts = []

clock = pygame.time.Clock()
while True:
    # event handling
    score = len(snake.segments)
    screen.fill(WHITE)
    bg.draw(screen)
    event_handler(snake, food, effects, texts)

    snake.brain(food)
    snake.update()
    snake.draw(screen)

    food.draw(screen, border_radius=2, width=15)

    score_board.draw_score(screen, score)

    for effect in effects:
        effect.draw(screen)
        effect.update()

    for text in texts:
        text.draw(screen)

    # TODO: separete when player collides with food and when it is near the food
    if abs(food.pos.x - snake.pos.x) <= 1 and abs(food.pos.y - snake.pos.y) <= 1:
        snake.grow(food)
        food.pos = Vector2(
            randint(0, WIDTH // snake.full_block - 1),
            randint(0, HEIGHT // snake.full_block - 1)
        )

    pygame.display.update()
    clock.tick(60)
