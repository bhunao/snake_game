import pygame
from config import *


class Score:
    def __init__(self, scree, x, y, score, color=BLACK):
        self.x = x
        self.y = y
        self.score = score
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.color = color
        self.screen = scree
        self.text = self.font.render(str(score), True, self.color)
        self.rect = self.text.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        self.screen.blit(self.text, self.rect)
    
    def update(self, score):
        self.score = score
        self.text = self.font.render(str(score), True, self.color)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)
        self.draw()
