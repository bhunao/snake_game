import random, pygame
from config import *


class Food:
    def __init__(self, screen, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.block = pygame.Rect(x, y, width, height)
    
    def update(self):
        self.draw()
    
    def draw(self):
        pygame.draw.rect(self.screen, RED, self.block)
    
    def spawn(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(0, SCREEN_HEIGHT - self.height)
        self.block = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw()
        print("food spawned", self.x, self.y)

