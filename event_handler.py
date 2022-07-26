import pygame
from pygame.math import Vector2

from custom_events import ANIMATION_ON_GROW, PLAYER_DEATH, RESTART_GAME
from objects import Snake, Effect, Text, Food


def grow_animation(object_, effect_object, effects):
    pos = Vector2(object_.pos * object_.full_block)
    pos.x += object_.full_block // 2
    pos.y += object_.full_block // 2
    effects.append(effect_object(pos))
    effects.append(effect_object(pos, size=3))
    effects.append(effect_object(pos, size=5))


def event_handler(snake, food, effects, texts):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event == ANIMATION_ON_GROW:
            grow_animation(snake, Effect, effects)
        elif event == PLAYER_DEATH:
            game_over = Text((400, 300), "Game Over")
            texts.append(game_over)
            press_spc = Text((400, 400), "Press Space to restart")
            texts.append(press_spc)
        elif event == RESTART_GAME:
            snake.respawn()
            effects.clear()
            texts.clear()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.speed = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                snake.speed = Vector2(-1, 0)
            if event.key == pygame.K_UP:
                snake.speed = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                snake.speed = Vector2(0, 1)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_SPACE:
                pygame.event.post(RESTART_GAME)
                print(f"space pressed: {event.key}")
            if event.key == pygame.K_q:
                grow_animation(snake, Effect, effects)
