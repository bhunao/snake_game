import pygame


class Snake:
    def __init__(self, x, y) -> None:
        self.x = x
        self.x = y
        self.body = pygame.Rect(x, y, 10, 10)
