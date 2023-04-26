from random import randint

import pygame
from pygame._sprite import Group
from pygame.sprite import Sprite


def convert(x, y):
    return 150 + x * 40 - y * 40, 150 + x * 20 + y * 20


class Tower(Sprite):
    def __init__(self, x, y, t="02"):
        super().__init__()
        self.image = pygame.image.load(f"tower/PNG/Towers (grey)/tower_{t:0>2}.png")
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.velocity = (1,0)
        self.rect.x ,self.rect.y = convert(x, y)

    def update(self):
        x, y = convert(self.x, self.y)
        self.rect.x, self.rect.y = x, y
        # self.x += self.velocity[0]
        # self.y += self.velocity[1]


class Apple(Sprite):
    def __init__(self, x=5, y=5):
        super().__init__()
        self.image = pygame.image.load(f"tower/PNG/Towers (red)/tower_13.png")
        self.rect = self.image.get_rect()
        self.x, self.y = x,y
        self.rect.x ,self.rect.y = convert(self.x, self.y)


class SnakeGroup(Group):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x, self.y = x, y
        self.velocity = (1,0)
        self.start_snake()

    def start_snake(self):
        x = self.x
        self.add(Tower(x-2, 0))
        self.add(Tower(x-1, 0))
        self.add(Tower(0, 0))

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        new_tower = Tower(self.x, self.y)
        self.add(new_tower)
        self.remove(self.sprites()[0])

    def draw(self, screen):
        sort = sorted(self.sprites(), key=lambda x: x.rect.y)
        for tower in sort:
            screen.blit(tower.image, tower.rect)

    def grow(self):
        self.add(Tower(self.x, self.y))


class Ground(Sprite):
    def __init__(self, pos):
        super().__init__()
        n = randint(0, 1)
        self.image = pygame.image.load(f"tower/PNG/Landscape/landscape_{n:0>2}.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Background(Group):
    def __init__(self):
        super().__init__()
        self.start()

    def start(self):
        # 150 + x * 40 - y * 40, 150 + x * 20 + y * 20
        x_off = 67
        y_off = 34
        for x in range(0, 20):
            for y in range(0, 20):
                pos = 150 + x * x_off - y * x_off, -150 + x * y_off + y * y_off
                self.add(Ground(pos))

