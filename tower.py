from random import randint

import pygame
from pygame._sprite import Group

from tower_objects import convert, Tower, Apple, SnakeGroup, Background

pygame.init()
size = width, height = 1400, 800
screen = pygame.display.set_mode(size)

g = Group()
apple = Apple()
g.add(apple)

bg = Background()

t1 = Tower(0, 0)
t2 = Tower(1, 0)
t3 = Tower(2, 0)

snake = SnakeGroup()
print(f"snake: {snake}")



unordered = []

sorted_ = sorted(unordered, key=lambda x: x.rect.y)
# g.add(sorted_)


# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_UP:
                snake.velocity = (0, -1)
            if event.key == pygame.K_DOWN:
                snake.velocity = (0, 1)
            if event.key == pygame.K_LEFT:
                snake.velocity = (-1, 0)
            if event.key == pygame.K_RIGHT:
                snake.velocity = (1, 0)





    screen.fill((0, 0, 0))
    bg.draw(screen)
    snake.update()
    snake.draw(screen)
    g.update()
    g.draw(screen)
    pygame.display.flip()
    pygame.time.delay(500)

    if snake.x == apple.x:
        if snake.y == apple.y:
            snake.grow()
            rx = randint(0, 8)
            ry = randint(0, 8)
            g.remove(apple)
            g.add(Apple(rx, ry))

