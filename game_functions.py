import random
from config import *
from models.snake import Snake


def get_random_snake(screen) -> Snake:
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    return Snake(screen, x, y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE)

def check_wall_collision(snake: Snake):
    if snake.x < 0 or snake.x > SCREEN_HEIGHT:
        return True
    if snake.y < 0 or snake.y > SCREEN_WIDTH:
        print(snake.x, snake.y, SCREEN_HEIGHT, SCREEN_WIDTH)
        return True
    return False