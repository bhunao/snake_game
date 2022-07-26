from random import randint

import pygame
from pygame._sprite import Group
from pygame.sprite import Sprite

pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)


class Tower(Sprite):
    def __init__(self, x, y, t="02"):
        super().__init__()
        self.image = pygame.image.load(f"tower/PNG/Towers (grey)/tower_{t:0>2}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


g = Group()


def convert(x, y):
    return 150 + x * 40 - y * 40, 150 + x * 20 + y * 20


t1 = Tower(*convert(0, 0))
t2 = Tower(*convert(1, 0))
t3 = Tower(*convert(2, 0))

g.add(t1, t2, t3)


unordered = []
for col in range(20):
    for row in range(15):
        x = col * 78
        y = row * 20
        if row % 2 == 0:
            x += 40
        i = str(randint(0, 54))
        pos = convert(row, col)
        t = Tower(*pos)
        unordered.append(t)
        # g.add(t)

sorted_ = sorted(unordered, key=lambda x: x.rect.y)
# g.add(sorted_)


# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    g.update()
    g.draw(screen)
    pygame.display.flip()
    pygame.time.delay(100)

