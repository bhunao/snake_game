import math
import random
import pygame


from config import *
from models.score import Score

# Snake class x, y, width, height
class Snake:
    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "right"
        self.screen = screen
        self.score = Score(screen, SCREEN_WIDTH - 100, 50, 0)
        self.font = pygame.font.SysFont("comicsansms", 10)
        self.body = []
        self.body.append(pygame.Rect(self.x, self.y, self.width, self.height))
        self.body.append(pygame.Rect(self.x - SNAKE_BLOCK_SIZE,
                         self.y, self.width, self.height))
        self.body.append(pygame.Rect(
            self.x - SNAKE_BLOCK_SIZE*2, self.y, self.width, self.height))
        self.block = self.body[0]

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.body.insert(0, pygame.Rect(self.x - SNAKE_BLOCK_SIZE, self.y, self.width, self.height))
        self.body.pop()
        self.score.update(len(self.body))
        self.draw()
        self.move()

    def grow(self):
        self.body.append(pygame.Rect(0, 0, self.width, self.height))

    def move(self):
        vlcity = 1
        if self.direction == "right":
            self.velocity_x = vlcity
            self.velocity_y = 0
        elif self.direction == "left":
            self.velocity_x = -vlcity
            self.velocity_y = 0
        elif self.direction == "up":
            self.velocity_x = 0
            self.velocity_y = -vlcity
        elif self.direction == "down":
            self.velocity_x = 0
            self.velocity_y = vlcity

    def draw_line(self, other: pygame.rect):
        dist = int(math.hypot(self.x - other.x, self.y - other.y))
        text = f'{dist}/{self.score.score}'
        self.text = self.font.render(text, True, BLACK)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)
        self.screen.blit(self.text, self.rect)
        dist = int(math.hypot(self.x - other.x, self.y - other.y)) / 250
        color = WHITE if dist < 1 else BLUE
        pygame.draw.line(self.screen, color, (self.x, self.y), (other.x, other.y))

    def draw(self):
        for block in self.body:
            pygame.draw.rect(self.screen, GREEN, block)

    def check_collision(self, other: pygame.Rect):
        for block in self.body:
            if (block.x == other.x and block.y == other.y):
                #print(f" colision at {block.x}, {block.y} - {other.x}, {other.y}")
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

